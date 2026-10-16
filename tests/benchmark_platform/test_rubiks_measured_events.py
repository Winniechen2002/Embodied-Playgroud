"""Synthetic 120 Hz measurements exercise scoring logic, not native task success."""
import math

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from test_rubiks_state import module


class Trace:
    def __init__(self, scramble=()):
        self.rules = module('rubiks_cube_rules')
        self.native = module('rubiks_cube_native_observation')
        self.state = self.rules.CubeState.solved().apply_sequence(scramble)
        self.names = tuple(sorted(self.state.pieces))+('world_anchor','core','carrier_x','carrier_y','carrier_z')
        self.step = 0
        self.core_position = np.array([.7,0,.6355])
        self.core_rotation = np.eye(3)
        self.poses = self._poses()
        self.hand = np.array([1.,0,0,0])

    def _poses(self, face=None, angle=0.):
        result = np.zeros((31,7)); result[:,:3] = self.core_position; result[:,6] = 1.
        result[27:,3:] = Rotation.from_matrix(self.core_rotation).as_quat()
        moving = self.state.active_cubie_ids(face) if face else ()
        axis = np.array(self.rules.FACE_NORMALS[face])*self.rules.FACE_AXIS_SIGN[face][1] if face else np.array([0,0,1])
        turn = Rotation.from_rotvec(axis*angle).as_matrix()
        for i,name in enumerate(self.names[:26]):
            piece = self.state.pieces[name]
            rotation = turn if name in moving else np.eye(3)
            result[i,:3] += self.core_rotation @ rotation @ (np.array(piece.position)*.024)
            result[i,3:] = Rotation.from_matrix(self.core_rotation @ rotation @ np.array(piece.orientation)).as_quat()
        if face:
            idx = self.names.index('carrier_'+self.rules.FACE_AXIS_SIGN[face][0].lower())
            result[idx,3:] = Rotation.from_matrix(self.core_rotation @ turn).as_quat()
        return result

    def sample(self):
        return self.native.NativeCubeSample(self.step,self.step/120,self.names,self.poses,np.zeros((31,6)))

    def tick(self, tracker, forces=(2.,2.)):
        self.step += 1
        return tracker.observe(self.sample(),hand_quaternion_wxyz=self.hand,finger_contact_forces_n=forces)

    def turn(self, tracker, move, *, wrist=True, forces=(2.,2.), settle_steps=64):
        face = move[0]
        axis = 'XYZ'.index(self.rules.FACE_AXIS_SIGN[face][0])
        delta = (-1 if len(move)==1 else 1)*self.rules.FACE_AXIS_SIGN[face][1]*math.pi/2
        for angle in np.linspace(0.,delta,91)[1:]:
            self.poses = self._poses(face,angle)
            if wrist:
                vector = np.zeros(3); vector[axis] = angle
                q = Rotation.from_matrix(self.core_rotation @ Rotation.from_rotvec(vector).as_matrix()).as_quat()
                self.hand = q[[3,0,1,2]]
            self.tick(tracker,forces)
        for _ in range(settle_steps):
            self.tick(tracker,forces)
        self.state = self.state.apply_move(move)


def tracker_for(trace):
    return module('rubiks_cube_measured_events').MeasuredTurns(trace.sample(),hand_quaternion_wxyz=trace.hand)


def test_center_normal_equivalence_does_not_hide_tilted_sticker():
    observer = module('rubiks_cube_observer')
    trace = Trace()
    center = next(name for name,p in trace.state.pieces.items() if p.position==(0,0,1))
    i = trace.names.index(center)
    trace.poses[i,3:] = Rotation.from_euler('z',.31).as_quat()
    measured,_ = observer.classify_native_snapshot(trace.names,trace.poses,ignore_center_twist=True)
    assert measured.facelet_string()==trace.state.facelet_string()
    assert observer.classify_native_snapshot(trace.names,trace.poses)[0] is None
    trace.poses[i,3:] = Rotation.from_euler('x',.31).as_quat()
    assert observer.classify_native_snapshot(trace.names,trace.poses,ignore_center_twist=True)[0] is None


def test_center_equivalence_preserves_edge_flip_legality():
    observer = module('rubiks_cube_observer'); trace = Trace()
    edge = next(name for name,p in trace.state.pieces.items() if p.position==(1,0,1))
    trace.poses[trace.names.index(edge),3:] = Rotation.from_rotvec(np.array([1.,0,1])*math.pi/math.sqrt(2)).as_quat()
    measured,report = observer.classify_native_snapshot(trace.names,trace.poses,ignore_center_twist=True)
    assert measured is None and not report['legal']


@pytest.mark.parametrize('face',list('URFDLB'))
@pytest.mark.parametrize('suffix',['',"'",'2'])
def test_all_eighteen_notations_are_reconstructed_from_physical_quarters(face,suffix):
    trace = Trace(); tracker = tracker_for(trace)
    moves = [face,face] if suffix=='2' else [face+suffix]
    for move in moves:
        trace.turn(tracker,move)
    assert [e['move'] for e in tracker.events]==moves
    assert all(e['metrics']['success_tolerance_met'] for e in tracker.events)
    assert tracker.measured_state.facelet_string()==trace.state.facelet_string()


def test_cancelling_moves_require_two_measured_events():
    idle = Trace(); no_motion = tracker_for(idle)
    for _ in range(64): idle.tick(no_motion)
    assert no_motion.events==[]
    active = Trace(); moves = tracker_for(active)
    active.turn(moves,'U'); active.turn(moves,"U'")
    assert [e['move'] for e in moves.events]==['U',"U'"]
    assert moves.measured_state.facelet_string()==no_motion.measured_state.facelet_string()


def test_rigid_whole_cube_motion_is_not_a_layer_event():
    trace = Trace(); tracker = tracker_for(trace)
    for angle in np.linspace(0,math.pi/2,80):
        trace.core_rotation = Rotation.from_euler('x',angle).as_matrix()
        trace.core_position = np.array([.7,.1*math.sin(angle),.6355+.06*math.sin(angle)])
        trace.poses = trace._poses(); trace.tick(tracker)
    assert tracker.events==[]


def test_release_after_measured_quarter_does_not_dilute_rotation_contact_history():
    trace=Trace(); tracker=tracker_for(trace)
    trace.turn(tracker,'U',settle_steps=0)
    carrier=trace.names.index('carrier_x')
    # A passive empty carrier delays the 31-body rest window after the
    # completed layer motion. The hand can already have released the cube.
    for i in range(100):
        trace.poses[carrier,3:] = Rotation.from_euler('x',.03*(-1)**i).as_quat()
        trace.tick(tracker,(0.,0.))
    trace.poses[carrier,3:] = [0.,0.,0.,1.]
    for _ in range(64): trace.tick(tracker,(0.,0.))
    assert [event['move'] for event in tracker.events]==['U']


@pytest.mark.parametrize('defect',['gap','duplicate','no_contact','no_wrist','jump'])
def test_incomplete_or_nonphysical_turn_evidence_is_rejected(defect):
    trace = Trace(); tracker = tracker_for(trace)
    with pytest.raises(ValueError):
        if defect=='gap':
            trace.step += 1; trace.tick(tracker)
        elif defect=='duplicate':
            trace.tick(tracker); tracker.observe(trace.sample(),hand_quaternion_wxyz=trace.hand,finger_contact_forces_n=(2.,2.))
        elif defect=='jump':
            trace.state = trace.state.apply_move('U'); trace.poses = trace._poses()
            for _ in range(65): trace.tick(tracker)
        else:
            trace.turn(tracker,'U',wrist=defect!='no_wrist',forces=(0.,0.) if defect=='no_contact' else (2.,2.))
    assert tracker.events==[]


@pytest.mark.parametrize('pending_contact', [True, False])
def test_subthreshold_layer_median_waits_without_discarding_motion_evidence(pending_contact):
    # Native run 012: maximum cubie angle 1.024 degrees, layer median .694.
    # One cubie crossing the onset threshold cannot classify an entire layer.
    trace = Trace(); tracker = tracker_for(trace)
    trace.turn(tracker, 'U')
    trace.hand = np.array([1., 0, 0, 0]); trace.tick(tracker)
    trace.poses = trace._poses('U', math.radians(.69))
    piece = next(n for n in trace.state.active_cubie_ids('U')
                 if len(trace.state.pieces[n].stickers) > 1)
    i = trace.names.index(piece)
    trace.poses[i, 3:] = (Rotation.from_euler('z', .334, degrees=True)
                         * Rotation.from_quat(trace.poses[i, 3:])).as_quat()
    trace.hand = Rotation.from_euler('z', 20, degrees=True).as_quat()[[3, 0, 1, 2]]
    for _ in range(200):
        trace.tick(tracker, (2., 2.) if pending_contact else (0., 0.))
    assert [event['move'] for event in tracker.events] == ['U']

    def finish_turn():
        for angle in range(2, 91):
            trace.poses = trace._poses('U', math.radians(angle))
            wrist = 20 + 70 * (angle - 1) / 89
            trace.hand = Rotation.from_euler('z', wrist, degrees=True).as_quat()[[3, 0, 1, 2]]
            trace.tick(tracker)
        for _ in range(64):
            trace.tick(tracker)

    if pending_contact:
        finish_turn()
        assert [event['move'] for event in tracker.events] == ['U', "U'"]
        # Evidence ends at the first 87-degree layer sample, where this
        # deliberately nonuniform wrist path has reached 87.640449 degrees.
        assert tracker.events[-1]['metrics']['wrist_axis_delta_rad'] == pytest.approx(math.radians(87.6404494382))
    else:
        with pytest.raises(ValueError, match='contact_maintenance_below_threshold'):
            finish_turn()
        assert [event['move'] for event in tracker.events] == ['U']


def test_unclassified_motion_outside_layer_tolerance_is_still_rejected():
    trace = Trace(); tracker = tracker_for(trace)
    piece = next(n for n, p in trace.state.pieces.items() if len(p.stickers) > 1)
    trace.poses[trace.names.index(piece), 3:] = Rotation.from_euler('z', 3.01, degrees=True).as_quat()
    with pytest.raises(ValueError, match='does not identify one face layer'):
        trace.tick(tracker)
    assert tracker.events == []
