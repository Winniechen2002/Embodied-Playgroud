"""Trusted native joint authoring; no robot planning or body-state writes."""
from .rubiks_cube_constraint_audit import compare_joints
from .rubiks_cube_mechanism import ConstraintFrame
from .rubiks_cube_usd_backend import JointUpdate, PxrJointEditor, read_cube_joint_snapshot


class NativeFixture:
    """Apply guarded proposals and expose actual authored joint readback.

    The scorer observes/recomputes the resulting event through NativeBackend;
    this object cannot commit its own score or advance simulation. During reset
    settling it supplies readback only. Binding is performed once after the
    trusted runner has accepted a complete initialization window.
    """
    def __init__(self, env, *, editor=None, read_joints=None,hand_body_name='panda_hand'):
        self.env = env
        self.root = '/World/envs/env_0/RubiksCube'
        if editor is None or read_joints is None:
            from omni.usd import get_context
            stage = get_context().get_stage()
            editor = PxrJointEditor(stage)
            read_joints = lambda: read_cube_joint_snapshot(stage, self.root,hand_body_name=hand_body_name)
        self.editor, self.read_joints = editor, read_joints
        self.scorer = None
        self.state, self.epoch, self.operation = 'idle', 0, None

    def bind(self, scorer):
        if self.scorer is not None or scorer.fixture.epoch != 0 or scorer.fixture.state != 'idle':
            raise RuntimeError('Fixture may bind exactly once at accepted initialization')
        scorer.fixture.verify_current(self.read_joints())
        self.scorer = scorer

    def public_state(self):
        return dict(state=self.state, epoch=self.epoch)

    def evidence(self):
        return dict(version='hybrid_fixture_v1', **self.public_state(), joints=self.read_joints())

    def command(self, name, arguments):
        if self.scorer is None:
            raise RuntimeError('Fixture unavailable until initialization is accepted')
        audit = self.scorer.fixture
        if self.state != audit.state or self.epoch != audit.epoch:
            raise RuntimeError('Previous fixture transaction has not been independently audited')
        # Unexpected authored edits are fatal, not ordinary not-ready replies.
        current = self.read_joints()
        audit.verify_current(current)
        try:
            proposed = self.scorer.mechanism_plan(name, arguments)
        except ValueError as exc:
            return dict(accepted=False, **self.public_state(), private_reason=str(exc))
        _, next_state, next_operation = audit._transaction(name, arguments, self.scorer.last_row)
        updates = []
        for key, value in proposed.items():
            before = current[key]
            changed_frame = any(before[k] != value[k] for k in ('position0', 'quaternion0'))
            if before['enabled'] != value['enabled'] or changed_frame:
                frame = ConstraintFrame(tuple(value['position0']), tuple(value['quaternion0'])) if changed_frame else None
                updates.append(JointUpdate(self.root+'/Joints/'+key, enabled=value['enabled'], frame=frame))
        if updates:
            self.editor.apply_transaction(updates)
        compare_joints(proposed, self.read_joints())
        self.state, self.operation, self.epoch = next_state, next_operation, self.epoch+1
        return dict(accepted=True, **self.public_state(), authored_joint_count=len(updates))

    def apply_detent(self):
        # Transport replaces carrier hinges by measured fixed locks. Preserve
        # the legacy transport behavior: no carrier torque during that exchange.
        if self.operation == 'transport':
            self.env._zero_carrier_torques()
        else:
            self.env.apply_passive_detent()
