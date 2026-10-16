"""Read-only pose and collision predicates, independent of Isaac Lab."""
from __future__ import annotations
import numpy as np

ROBOT_CONTACT_BODIES = tuple(f'panda_link{i}' for i in range(8)) + ('panda_hand','panda_leftfinger','panda_rightfinger')
FORBIDDEN_CONTACT_LABELS = ('table',) + tuple(side+'.'+body for side in ('left','right') for body in ROBOT_CONTACT_BODIES)


def quaternion_matrix(q):
    q = np.asarray(q, dtype=float)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])


def matrix_quaternion(matrix):
    """WXYZ quaternion, including rotations whose trace is near minus one."""
    r=np.asarray(matrix,dtype=float)
    k=np.array([[r[0,0]-r[1,1]-r[2,2],r[0,1]+r[1,0],r[0,2]+r[2,0],r[2,1]-r[1,2]],
                [r[0,1]+r[1,0],r[1,1]-r[0,0]-r[2,2],r[1,2]+r[2,1],r[0,2]-r[2,0]],
                [r[0,2]+r[2,0],r[1,2]+r[2,1],r[2,2]-r[0,0]-r[1,1],r[1,0]-r[0,1]],
                [r[2,1]-r[1,2],r[0,2]-r[2,0],r[1,0]-r[0,1],np.trace(r)]])/3
    _,v=np.linalg.eigh(k);q=v[:, -1][[3,0,1,2]]
    return q if q[0]>=0 else -q


def interpolate_rotation(start,end,fraction):
    a,b=matrix_quaternion(start),matrix_quaternion(end)
    dot=float(np.dot(a,b))
    if dot<0:b=-b;dot=-dot
    t=float(np.clip(fraction,0.,1.))
    if dot>.9995:return quaternion_matrix((1-t)*a+t*b)
    angle=np.arccos(np.clip(dot,-1.,1.))
    return quaternion_matrix((np.sin((1-t)*angle)*a+np.sin(t*angle)*b)/np.sin(angle))


def reset_hold_metrics(initial, history, displacement_limit_m, window_steps=30):
    """Separate bounded gravity seating from continuing motion after reset."""
    peak={n:0. for n in initial}
    quiet=len(history)>=window_steps
    for i,sample in enumerate(history):
        if set(sample)!=set(initial):return dict(settled=False,peak_displacement_m=peak)
        for name,p in sample.items():
            displacement=float(np.linalg.norm(np.asarray(p['position'])-initial[name]['position']))
            speed=float(np.linalg.norm(p['linear_velocity']))
            spin=float(np.linalg.norm(p['angular_velocity']))
            q=np.asarray(p['quaternion']);q0=np.asarray(initial[name]['quaternion'])
            angle=2*np.arccos(np.clip(abs(np.dot(q,q0)/(np.linalg.norm(q)*np.linalg.norm(q0))),0,1))
            if not np.isfinite([displacement,speed,spin,angle]).all():quiet=False
            peak[name]=max(peak[name],displacement)
            quiet=quiet and displacement<=displacement_limit_m and angle<.03
            if i>=len(history)-window_steps:quiet=quiet and speed<.01 and spin<.1
    return dict(settled=bool(quiet),peak_displacement_m=peak,
                displacement_limit_m=displacement_limit_m,stable_window_steps=window_steps)


def cube_pair_clearance(centers_a, rotation_a, centers_b, rotation_b, half_extent):
    """Signed SAT gap: conservative positive clearance, negative penetration."""
    return box_pair_clearance(centers_a,rotation_a,np.full((len(centers_a),3),half_extent),
                              centers_b,rotation_b,np.full((len(centers_b),3),half_extent))


def box_pair_clearance(centers_a, rotation_a, half_a, centers_b, rotation_b, half_b):
    """Signed SAT gap of two rigid compounds with unequal rectangular boxes."""
    axes = list(rotation_a.T) + list(rotation_b.T)
    axes += [np.cross(a, b) for a in rotation_a.T for b in rotation_b.T]
    axes = np.asarray([a / np.linalg.norm(a) for a in axes if np.linalg.norm(a) > 1e-7])
    radius_a=np.asarray(half_a)@np.abs(axes@rotation_a).T
    radius_b=np.asarray(half_b)@np.abs(axes@rotation_b).T
    radius=radius_a[:,None,:]+radius_b[None,:,:]
    distances = np.abs((centers_a[:, None, :] - centers_b[None, :, :]) @ axes.T)
    overlaps = radius - distances
    return float(-overlaps.min(axis=-1).max())


def cube_pair_penetration(centers_a, rotation_a, centers_b, rotation_b, half_extent):
    """Maximum SAT overlap of two compounds of equally sized oriented cubes."""
    return max(0., -cube_pair_clearance(centers_a,rotation_a,centers_b,rotation_b,half_extent))


def lattice_motion_diagnostics(cubes, cell_size, grid_origin, floor_cell=-4):
    """Local one-cell translation blockers from measured, grid-aligned poses.

    Invalid alignment is reported as unknown, never as an unlocked part. This
    discrete diagnostic is not a substitute for the continuous collision audit.
    """
    occupied = {}
    aligned = {}
    for name, (centers, rotation) in cubes.items():
        coordinates = (centers - grid_origin) / cell_size
        rounded = np.rint(coordinates)
        residual = float(np.max(np.abs(coordinates-rounded))*cell_size)
        orientation_error = float(np.max(np.abs(np.abs(rotation)-np.rint(np.abs(rotation)))))
        aligned[name] = residual < .005 and orientation_error < .08
        occupied[name] = set(map(tuple, rounded.astype(int)))
    result = {}
    for name, cells in occupied.items():
        directions = {}
        if aligned[name] and all(aligned.values()):
            for axis in range(3):
                for sign in (-1, 1):
                    moved = {tuple(v+(sign if i==axis else 0) for i,v in enumerate(c)) for c in cells}
                    blockers = [other for other, shape in occupied.items() if other != name and moved & shape]
                    if min(c[2] for c in moved) < floor_cell:blockers.append('table')
                    directions['xyz'[axis]+('+' if sign>0 else '-')] = blockers
        result[name] = dict(grid_aligned=aligned[name], one_cell_blockers=directions,
                            movable_directions=[d for d,b in directions.items() if not b])
    return dict(source='measured_voxel_centers_quantized_to_spec_grid',
                translation_distance_m=cell_size, meaning='local translation only, not complete removal', pieces=result)


def goal_predicates(pieces, robots, max_penetration_m):
    """Instantaneous predicates; the environment adds the 30-frame window.

    No controller-supplied flags participate in success. All fields come from
    measured rigid bodies and the immutable target specification.
    """
    diagnostics = {}
    for name, p in pieces.items():
        position_error = float(np.linalg.norm(np.asarray(p['position']) - p['target']))
        q = np.asarray(p['quaternion'],dtype=float)
        target_q = np.asarray(p['target_quaternion'],dtype=float)
        dot = abs(float(np.dot(q/np.linalg.norm(q), target_q/np.linalg.norm(target_q))))
        angle_error = float(2 * np.arccos(np.clip(dot, 0, 1)))
        speed = float(np.linalg.norm(p['linear_velocity']))
        spin = float(np.linalg.norm(p['angular_velocity']))
        diagnostics[name] = dict(position_error_m=position_error, angle_error_rad=angle_error,
                                 speed_m_s=speed, spin_rad_s=spin,
                                 in_zone=position_error < .025 and angle_error < .25,
                                 stable=speed < .01 and spin < .10)
    opened = all(min(r['fingers']) >= .035 for r in robots.values())
    clear = all(np.linalg.norm(np.asarray(r['tcp']) - p['position']) >= .13
                for r in robots.values() for p in pieces.values())
    in_zones = len(pieces) == 6 and all(d['in_zone'] for d in diagnostics.values())
    stable = all(d['stable'] for d in diagnostics.values())
    penetration_ok = np.isfinite(max_penetration_m) and max_penetration_m <= .002
    return dict(instantaneous_goal=bool(in_zones and stable and opened and clear and penetration_ok),
                all_in_zones=in_zones, all_stable=stable, grippers_open=opened, arms_clear=clear,
                penetration_ok=bool(penetration_ok), pieces=diagnostics)
