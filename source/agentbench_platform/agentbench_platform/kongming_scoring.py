"""Trusted physical Kongming evaluator, independent of controllers and Isaac.

See ``KongmingScorer`` for the private raw-input contract. Only the trusted
backend may supply these inputs; none of this module is a public tool.
"""
from __future__ import annotations

from copy import deepcopy
from itertools import combinations, permutations, product

import numpy as np
from scipy.optimize import least_squares, minimize
from scipy.spatial.transform import Rotation


POSITION_TOLERANCE = .0075
ANGLE_TOLERANCE = .08
PENETRATION_LIMIT = .002
SUPPORT_TOLERANCE = .002


def _array(value, shape):
    a = np.array(value, dtype=float, copy=True)
    if a.shape != shape or not np.isfinite(a).all():
        raise ValueError('invalid physical array')
    return a


def _rotation(q):
    q = _array(q, (4,))
    if abs(np.linalg.norm(q)-1) > .001:
        raise ValueError('invalid physical quaternion')
    return Rotation.from_quat(q[[1, 2, 3, 0]]).as_matrix()


def _axis_rotations():
    for order in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            r = np.eye(3)[:, order] * signs
            if np.linalg.det(r) > 0:
                yield r


def _box_key(centers, half):
    return sorted(map(tuple, np.round(np.column_stack((centers, half)), 9)))


def _clearance(a, b):
    ca, ra, ha = a
    cb, rb, hb = b
    axes = list(ra.T) + list(rb.T)
    axes += [np.cross(x, y) for x in ra.T for y in rb.T]
    axes = np.array([x/np.linalg.norm(x) for x in axes if np.linalg.norm(x) > 1e-7])
    radius = (ha @ np.abs(axes @ ra).T)[:, None] + (hb @ np.abs(axes @ rb).T)[None, :]
    distances = np.abs((ca[:, None]-cb[None, :]) @ axes.T)
    return float(np.min(np.max(distances-radius, axis=-1)))


def _angles(rotations):
    return Rotation.from_matrix(rotations).magnitude()


class KongmingScorer:
    """Own stable counters, geometry matching, and irrevocable hard failures.

    ``spec`` is a mapping with ``table_top_z`` and six ``pieces`` keyed by
    immutable body names. Each piece contains local ``centers``/``half_extents``
    (Nx3 collision cuboids), ``assembly_position``/``assembly_quaternion`` and
    ``target_position``/``target_quaternion`` (WXYZ). Family/route labels ignored.

    Snapshots have integer ``control_step`` and ``physics_step`` (four physics
    steps per control), ``pieces`` with position, quaternion, linear_velocity,
    angular_velocity, and ``robots`` keyed left/right. Robots contain two
    measured ``fingers``, ``tcp``, eight ``arm_forces_w`` (links 1..7 and hand),
    and two ``finger_contacts``. Each finger contains ``net_w``,
    ``allowed_piece_sum_w``, and 23 ``forbidden_forces_w`` (table, then eleven
    bodies of each robot: links 0..7, hand, and both fingers; the exact backend sensor
    ordering is irrelevant to the max-norm gate). Substep audits use the same
    physical schema, with fresh consecutive ``physics_step`` values.

    ``physical_success`` reports the stable final-state predicate. ``success``
    additionally requires complete 120 Hz audit coverage since control 1.
    Control 0 is a reset observation, never a stable-control or coverage sample.
    Missing, duplicate, or reordered substeps cannot complete coverage. Repeated
    control updates cannot advance counters. All geometric penetration/contact
    violations seen in either endpoint or substeps latch for the episode.
    """

    def __init__(self, mode, spec, *, case_spec=None, embodiment='franka-panda'):
        if mode not in ('assemble', 'disassemble'):
            raise ValueError('unsupported Kongming mode')
        self.mode = mode
        if embodiment not in ('franka-panda', 'dual-floating-sharpa'):
            raise ValueError('unsupported Kongming embodiment')
        self.embodiment = embodiment
        self.penetration_limit = PENETRATION_LIMIT
        self.case_spec = deepcopy(case_spec) if case_spec is not None else None
        self.table_z = float(spec['table_top_z'])
        if not np.isfinite(self.table_z) or len(spec['pieces']) != 6:
            raise ValueError('invalid six-piece specification')
        self.names = tuple(spec['pieces'])
        self.boxes, self.positions, self.rotations = {}, {}, {}
        prefix = 'assembly' if mode == 'assemble' else 'target'
        for name, p in spec['pieces'].items():
            centers = np.array(p['centers'], dtype=float, copy=True)
            if centers.ndim != 2 or centers.shape[1] != 3 or len(centers) == 0 or not np.isfinite(centers).all():
                raise ValueError('invalid collision centers')
            half = _array(p['half_extents'], centers.shape)
            if (half <= 0).any():
                raise ValueError('invalid collision dimensions')
            self.boxes[name] = centers, half
            if case_spec is not None:
                # scorer_spec binds target_position/target_quaternion to the
                # frozen case goal, including its XY/yaw transform.
                self.positions[name] = _array(p['target_position'], (3,))
                self.rotations[name] = _rotation(p['target_quaternion'])
            else:
                self.positions[name] = _array(p[prefix+'_position'], (3,))
                self.rotations[name] = _rotation(p[prefix+'_quaternion'])
        # Each S maps a measured body's local shape into a target body's local
        # shape. The full frozen box geometry, not a family name, decides this.
        self.equivalences = {}
        for a, b in product(self.names, repeat=2):
            ca, ha = self.boxes[a]
            cb, hb = self.boxes[b]
            self.equivalences[a, b] = tuple(s for s in _axis_rotations()
                if _box_key(ca @ s.T, ha @ np.abs(s).T) == _box_key(cb, hb))
        self.assignments = [p for p in permutations(self.names)
                            if all(self.equivalences[a, b] for a, b in zip(self.names, p))]
        self.last_control = 0
        self.stable_controls = 0
        self.observed_substeps = 0
        self.coverage_complete = True
        self.hard_failure = False
        self.failure_reasons = set()
        self._last = dict(instantaneous_goal=False, pose_goal_reached=False)

    def _physical(self, snapshot):
        if set(snapshot['pieces']) != set(self.names) or set(snapshot['robots']) != {'left', 'right'}:
            raise ValueError('incomplete physical bodies')
        positions, rotations, boxes, bounds = {}, {}, {}, {}
        stable = True
        for name, p in snapshot['pieces'].items():
            pos, rot = _array(p['position'], (3,)), _rotation(p['quaternion'])
            stable &= np.linalg.norm(_array(p['linear_velocity'], (3,))) < .01
            stable &= np.linalg.norm(_array(p['angular_velocity'], (3,))) < .10
            centers, half = self.boxes[name]
            world = centers @ rot.T + pos
            extent = half @ np.abs(rot).T
            bounds[name] = (np.min(world-extent, axis=0), np.max(world+extent, axis=0))
            positions[name], rotations[name], boxes[name] = pos, rot, (world, rot, half)
        gaps = {a+'/'+b: _clearance(boxes[a], boxes[b]) for a, b in combinations(self.names, 2)}
        penetration = max([0.] + [-v for v in gaps.values()] + [self.table_z-b[0][2] for b in bounds.values()])
        opened = clear = True
        forces = []
        for robot in snapshot['robots'].values():
            if self.embodiment == 'dual-floating-sharpa':
                measured = _array(robot['finger_positions'], (22,))
                defaults = _array(robot['finger_default_positions'], (22,))
                opened &= np.max(np.abs(measured-defaults)) <= .05
                tcp = _array(robot.get('tcp', robot.get('hand_position')), (3,))
            else:
                opened &= min(_array(robot['fingers'], (2,))) >= .035
                tcp = _array(robot['tcp'], (3,))
            clear &= all(np.linalg.norm(tcp-p) >= .13 for p in positions.values())
            if self.embodiment == 'dual-floating-sharpa':
                if len(robot.get('fingertip_contacts', ())) != 5:
                    raise ValueError('incomplete Sharpa fingertips')
                palm_contacts = robot.get('palm_contacts', ())
                if len(palm_contacts) != 1:
                    raise ValueError('incomplete Sharpa palm contact')
                for finger in tuple(robot['fingertip_contacts']) + tuple(palm_contacts):
                    net = _array(finger['net_w'], (3,))
                    allowed = _array(finger['forces_w'], (6, 3))
                    forbidden = _array(finger['forbidden_forces_w'], (7, 3))
                    if tuple(finger['piece_names']) != self.names:
                        raise ValueError('incorrect Sharpa piece force order')
                    forces.append(np.linalg.norm(net-allowed.sum(axis=0)))
                    forces.extend(np.linalg.norm(forbidden, axis=1))
                forces.extend(np.linalg.norm(_array(robot['body_forces_w'], (21, 3)), axis=1))
                continue
            forces.extend(np.linalg.norm(_array(robot['arm_forces_w'], (8, 3)), axis=1))
            if len(robot['finger_contacts']) != 2:
                raise ValueError('incomplete fingers')
            for finger in robot['finger_contacts']:
                net = _array(finger['net_w'], (3,))
                allowed = _array(finger['allowed_piece_sum_w'], (3,))
                forbidden = _array(finger['forbidden_forces_w'], (23, 3))
                forces.append(np.linalg.norm(net-allowed))
                forces.extend(np.linalg.norm(forbidden, axis=1))
        if penetration > self.penetration_limit + 1e-12:
            self.failure_reasons.add('penetration')
        if max(forces) >= .5:
            self.failure_reasons.add('forbidden_contact')
        self.hard_failure |= bool(self.failure_reasons)
        return positions, rotations, dict(all_stable=bool(stable), grippers_open=bool(opened),
            arms_clear=bool(clear), max_penetration_m=float(penetration), max_forbidden_contact_n=float(max(forces)),
            pair_clearances_m=gaps, bounds=bounds)

    def _fit(self, positions, rotations):
        measured_p = np.array([positions[n] for n in self.names])
        measured_r = np.array([rotations[n] for n in self.names])
        pos_tol = POSITION_TOLERANCE if self.mode == 'assemble' else .025
        angle_tol = ANGLE_TOLERANCE if self.mode == 'assemble' else .25
        if self.case_spec is not None:
            # Registered cases name the pieces and fixed goal poses. In a short
            # subtask, translating the remaining assembly is not an alternative
            # solution to keeping those pieces in their declared configuration.
            errors = {}
            for name in self.names:
                target_p, target_q = self.case_spec['goal_state'][name]
                position = float(np.linalg.norm(positions[name]-target_p))
                target_r = _rotation(target_q)
                options = [target_r @ symmetry for symmetry in self.equivalences[name, name]]
                angle = float(min(_angles(np.array([rotations[name] @ r.T for r in options]))))
                errors[name] = dict(position_m=position, angle_rad=angle)
            return all(e['position_m'] <= pos_tol+1e-12 and e['angle_rad'] <= angle_tol+1e-12
                for e in errors.values()), dict(case_goal_errors=errors)
        if self.case_spec is not None and self.embodiment == 'dual-floating-sharpa':
            # Public dual-hand cases bind every immutable piece identity.
            pe = np.array([np.linalg.norm(positions[n]-self.positions[n]) for n in self.names])
            ae = _angles(np.array([rotations[n] @ self.rotations[n].T for n in self.names]))
            score = float(max(pe.max()/pos_tol, ae.max()/angle_tol))
            return score <= 1, dict(normalized_max_residual=score,
                correspondence={n:n for n in self.names}, max_position_error_m=float(pe.max()),
                max_angle_error_rad=float(ae.max()))
        best = None
        if self.mode == 'assemble':
            # Rigid transforms preserve diameter. Reject distant intermediate
            # states before correspondence enumeration or numerical fitting.
            targets = np.array(list(self.positions.values()))
            target_diameter = np.max(np.linalg.norm(targets[:, None]-targets[None, :], axis=-1))
            measured_diameter = np.max(np.linalg.norm(measured_p[:, None]-measured_p[None, :], axis=-1))
            if measured_diameter > target_diameter + 2*pos_tol + 1e-12:
                return False, None
        # A unique solid key has few correspondences and provides finite global
        # hypotheses. Every accepted result is nevertheless one joint fit.
        anchor = min(range(6), key=lambda i: sum(bool(self.equivalences[self.names[i], b]) for b in self.names))
        for assignment in self.assignments:
            target_p = np.array([self.positions[n] for n in assignment])
            options = [[self.rotations[b] @ s for s in self.equivalences[a, b]]
                       for a, b in zip(self.names, assignment)]
            hypotheses = [np.eye(3)] if self.mode == 'disassemble' else [measured_r[anchor] @ r.T for r in options[anchor]]
            for initial_r in hypotheses:
                candidates = []
                for i, choices in enumerate(options):
                    errors = _angles(np.array([measured_r[i] @ (initial_r @ r).T for r in choices]))
                    pick = int(np.argmin(errors))
                    if errors[pick] > (2*angle_tol+1e-8 if self.mode == 'assemble' else angle_tol):
                        break
                    candidates.append(choices[pick])
                if len(candidates) != 6:
                    continue
                target_r = np.array(candidates)
                if self.mode == 'assemble':
                    initial_t = (measured_p-target_p @ initial_r.T).mean(axis=0)
                    # A conservative distance prefilter only; noisy anchor
                    # hypotheses cannot replace the refined rigid fit.
                    if np.max(np.linalg.norm(target_p @ initial_r.T+initial_t-measured_p, axis=1)) > .05:
                        continue
                    def residual(x):
                        r = Rotation.from_rotvec(x[:3]).as_matrix()
                        p = (target_p @ r.T+x[3:]-measured_p)/pos_tol
                        angles = Rotation.from_matrix(measured_r @ np.transpose(r @ target_r, (0, 2, 1))).as_rotvec()/angle_tol
                        return np.concatenate((p.ravel(), angles.ravel()))
                    initial = np.r_[Rotation.from_matrix(initial_r).as_rotvec(), initial_t]
                    fit = least_squares(residual, initial, max_nfev=60, ftol=1e-10, xtol=1e-10, gtol=1e-10).x
                    def errors(x):
                        values = residual(x).reshape(12, 3)
                        return np.linalg.norm(values, axis=1)
                    # Least squares need not find a feasible minimax solution.
                    if max(errors(fit)) > 1+1e-7:
                        fit_result = minimize(lambda x: x[6], np.r_[fit, max(errors(fit))], method='SLSQP',
                            constraints=[dict(type='ineq', fun=lambda x: x[6]-errors(x[:6]))],
                            options=dict(maxiter=100, ftol=1e-9))
                        fit = fit_result.x[:6]
                    err = errors(fit)
                else:
                    err = np.r_[np.linalg.norm(target_p-measured_p, axis=1)/pos_tol,
                        _angles(measured_r @ np.transpose(target_r, (0, 2, 1)))/angle_tol]
                score = float(max(err))
                if best is None or score < best['normalized_max_residual']:
                    best = dict(normalized_max_residual=score, correspondence=dict(zip(self.names, assignment)),
                        max_position_error_m=float(max(err[:6])*pos_tol), max_angle_error_rad=float(max(err[6:])*angle_tol))
                if (score <= 1+1e-7 if self.mode == 'assemble' else score < 1):
                    return True, best
        return False, best

    def audit_substep(self, snapshot):
        """Latch fresh hard evidence without fitting goals or counting controls."""
        try:
            _, _, physical = self._physical(snapshot)
            return dict(max_penetration_m=physical['max_penetration_m'],
                        max_forbidden_contact_n=physical['max_forbidden_contact_n'],hard_failure=self.hard_failure)
        except (KeyError, TypeError, ValueError):
            self.failure_reasons.add('invalid_substep'); self.hard_failure = True
            return dict(hard_failure=True)

    def update(self, snapshot, substep_audits=()):
        """Inspect one endpoint and optional four raw substeps, advancing once."""
        control = snapshot.get('control_step')
        physics = snapshot.get('physics_step')
        if type(control) is not int or control < 0 or type(physics) is not int or physics != control*4:
            raise ValueError('invalid control/physics step')
        samples = tuple(substep_audits)
        # Audit even repeated endpoints: they may contain newly exposed hard
        # violations, but replay can never fabricate stability or coverage.
        observed = []
        valid_samples = True
        for sample in samples:
            try:
                self._physical(sample)
                if sample.get('control_step') != control or type(sample.get('physics_step')) is not int:
                    raise ValueError('invalid substep identity')
                observed.append(sample['physics_step'])
            except (KeyError, TypeError, ValueError):
                valid_samples = False
                self.failure_reasons.add('invalid_substep')
                self.hard_failure = True
        try:
            positions, rotations, physical = self._physical(snapshot)
            pose_ok, fit = self._fit(positions, rotations)
            bounds = physical.pop('bounds')
            support = [self.table_z-SUPPORT_TOLERANCE <= b[0][2] <= self.table_z+SUPPORT_TOLERANCE for b in bounds.values()]
            support_ok = any(support) if self.mode == 'assemble' else all(support)
            if (self.mode == 'disassemble' and self.case_spec is not None
                    and self.case_spec['subtask'] != 'complete'):
                selected=set(self.case_spec['target_pieces'])
                supported={n for n,s in zip(bounds,support) if s}
                # Removed pieces must rest on the table. Retained pieces may
                # rest through the retained assembly's contact graph. A wholly
                # floating component still fails, as does a moved non-target.
                retained=set(self.names)-selected
                reachable=supported & retained
                for _ in retained:
                    for pair,gap in physical['pair_clearances_m'].items():
                        a,b=pair.split('/')
                        if a in retained and b in retained and gap <= .0075+1e-12:
                            if a in reachable:reachable.add(b)
                            if b in reachable:reachable.add(a)
                support_ok=selected <= supported and retained <= reachable
            region = all(b[0][0] >= .50 and b[1][0] <= .95 and b[0][1] >= -.22 and b[1][1] <= .22 for b in bounds.values()) if self.mode == 'assemble' else True
            if self.mode == 'assemble':
                gaps_ok = all(v <= .0075+1e-12 for v in physical['pair_clearances_m'].values())
            else:
                required = set(self.case_spec.get('target_pieces', ())) if self.case_spec else set(self.names)
                gaps_ok = all(
                    value > 0 for key, value in physical['pair_clearances_m'].items()
                    if key.split('/')[0] in required or key.split('/')[1] in required
                )
            goal = pose_ok and support_ok and region and gaps_ok and all(physical[k] for k in ('all_stable', 'grippers_open', 'arms_clear')) and not self.hard_failure
            self._last = dict(physical, instantaneous_goal=bool(goal), pose_goal_reached=bool(pose_ok),
                              support_ok=bool(support_ok), region_ok=bool(region), mating_or_separation_ok=bool(gaps_ok), fit=fit)
        except (KeyError, TypeError, ValueError):
            self._last = dict(instantaneous_goal=False, pose_goal_reached=False, invalid_physical_snapshot=True)
            self.failure_reasons.add('invalid_snapshot')
            self.hard_failure = True
        if control > self.last_control:
            consecutive = control == self.last_control+1
            complete = valid_samples and observed == list(range(physics-3, physics+1))
            self.coverage_complete &= consecutive and complete
            self.observed_substeps += len(set(observed) & set(range(physics-3, physics+1)))
            self.stable_controls = (self.stable_controls+1 if consecutive else 1) if self._last['instantaneous_goal'] else 0
            self.last_control = control
        elif control < self.last_control:
            self.coverage_complete = False
        # Every observed non-goal endpoint breaks the stable window, even
        # when replayed at the same control. Only fresh controls can rebuild it.
        if self.hard_failure or not self._last['instantaneous_goal']:
            self.stable_controls = 0
        return self.result()

    def result(self):
        physical_success = self._last['instantaneous_goal'] and self.stable_controls >= (60 if self.mode == 'assemble' else 30) and not self.hard_failure
        coverage = dict(expected_substeps=self.last_control*4, observed_substeps=self.observed_substeps,
                        complete=bool(self.last_control > 0 and self.coverage_complete))
        return deepcopy(dict(self._last, scoring_version='kongming-physical-v2', mode=self.mode,
            embodiment=self.embodiment,
            case_id=self.case_spec.get('case_id') if self.case_spec else None,
            subtask=self.case_spec.get('subtask', 'complete') if self.case_spec else 'complete',
            success=bool(physical_success and coverage['complete']), physical_success=bool(physical_success),
            stable_controls=self.stable_controls, hard_failure=bool(self.hard_failure),
            failure_reasons=sorted(self.failure_reasons), audit_coverage=coverage,
            collision_scope=('piece compound boxes vs pieces/table; five pads and all 21 collision-bearing non-pad links per hand'
                if self.embodiment == 'dual-floating-sharpa' else
                'piece compound boxes vs pieces/table; instrumented arm and finger contact forces')))
