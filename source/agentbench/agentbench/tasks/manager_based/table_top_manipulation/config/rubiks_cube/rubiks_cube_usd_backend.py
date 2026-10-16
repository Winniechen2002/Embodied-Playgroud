"""Atomic USD joint backend for the hybrid Rubik's Cube mechanism."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Protocol, Sequence

try:
    from .rubiks_cube_mechanism import ConstraintFrame
except ImportError:  # Loaded directly by dependency-light unit tests.
    from rubiks_cube_mechanism import ConstraintFrame


@dataclass(frozen=True)
class JointUpdate:
    path: str
    enabled: bool
    frame: ConstraintFrame | None = None


class JointEditor(Protocol):
    def apply_transaction(self, updates: Sequence[JointUpdate]) -> None: ...


def _require_authoring_result(result, label: str) -> None:
    if not result:
        raise RuntimeError(f"USD authoring failed for {label}")


def _multiply_quaternions(left, right):
    lw, lx, ly, lz = left
    rw, rx, ry, rz = right
    return (
        lw * rw - lx * rx - ly * ry - lz * rz,
        lw * rx + lx * rw + ly * rz - lz * ry,
        lw * ry - lx * rz + ly * rw + lz * rx,
        lw * rz + lx * ry - ly * rx + lz * rw,
    )


def _relative_constraint_frame(reference: ConstraintFrame, target: ConstraintFrame) -> ConstraintFrame:
    inverse = (
        reference.quaternion[0],
        -reference.quaternion[1],
        -reference.quaternion[2],
        -reference.quaternion[3],
    )
    delta = tuple(target.position[index] - reference.position[index] for index in range(3))
    rotated = _multiply_quaternions(
        _multiply_quaternions(inverse, (0.0, *delta)),
        reference.quaternion,
    )
    return ConstraintFrame(
        tuple(rotated[1:]),
        _multiply_quaternions(inverse, target.quaternion),
    )


class _PxrAttachmentDeclarationApi:
    def get_rigid_body(self, stage, path):
        from pxr import UsdPhysics

        prim = stage.GetPrimAtPath(path)
        if not prim or not UsdPhysics.RigidBodyAPI.Get(stage, path):
            return None
        return prim

    def world_pose(self, prim):
        from pxr import Usd, UsdGeom

        matrix = UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
        translation = matrix.ExtractTranslation()
        quaternion = matrix.ExtractRotationQuat()
        imaginary = quaternion.GetImaginary()
        return ConstraintFrame(
            tuple(float(translation[index]) for index in range(3)),
            (float(quaternion.GetReal()), *(float(imaginary[index]) for index in range(3))),
        )

    def define_fixed_joint(self, stage, path, hand_path, core_path, frame):
        from pxr import Gf, Sdf, UsdPhysics

        hand_target = Sdf.Path(hand_path)
        core_target = Sdf.Path(core_path)
        local_position_0 = Gf.Vec3f(*frame.position)
        w, x, y, z = frame.quaternion
        local_rotation_0 = Gf.Quatf(w, Gf.Vec3f(x, y, z))
        local_position_1 = Gf.Vec3f(0.0, 0.0, 0.0)
        local_rotation_1 = Gf.Quatf(1.0, Gf.Vec3f(0.0, 0.0, 0.0))
        joint = UsdPhysics.FixedJoint.Define(stage, path)
        if not joint:
            raise RuntimeError(f"failed to define grasp attachment joint: {path}")
        _require_authoring_result(
            joint.CreateBody0Rel().SetTargets((hand_target,)), "body0 targets"
        )
        _require_authoring_result(
            joint.CreateBody1Rel().SetTargets((core_target,)), "body1 targets"
        )
        _require_authoring_result(
            joint.CreateLocalPos0Attr().Set(local_position_0), "local position 0"
        )
        _require_authoring_result(
            joint.CreateLocalRot0Attr().Set(local_rotation_0), "local rotation 0"
        )
        _require_authoring_result(
            joint.CreateLocalPos1Attr().Set(local_position_1), "local position 1"
        )
        _require_authoring_result(
            joint.CreateLocalRot1Attr().Set(local_rotation_1), "local rotation 1"
        )
        _require_authoring_result(
            joint.CreateJointEnabledAttr().Set(False), "enabled state"
        )
        _require_authoring_result(
            joint.CreateExcludeFromArticulationAttr().Set(True),
            "articulation exclusion",
        )


def declare_hand_core_attachment(stage, resolved_cube_path: str, *, hand_body_name='panda_hand', api=None) -> ConstraintFrame:
    """Declare one disabled measured hand/core fixed joint before simulation."""

    root = str(resolved_cube_path).rstrip("/")
    if not root or "/" not in root:
        raise ValueError("resolved cube prim path is invalid")
    if not isinstance(hand_body_name, str) or not hand_body_name or '/' in hand_body_name:
        raise ValueError('hand_body_name must be one USD body name')
    parent = root.rsplit("/", 1)[0]
    hand_path = f"{parent}/Robot/{hand_body_name}"
    core_path = f"{root}/Mechanism/core"
    joint_path = f"{root}/Joints/robot_hand_core_attachment"
    declaration = _PxrAttachmentDeclarationApi() if api is None else api
    hand = declaration.get_rigid_body(stage, hand_path)
    core = declaration.get_rigid_body(stage, core_path)
    missing = [path for path, prim in ((hand_path, hand), (core_path, core)) if prim is None]
    if missing:
        raise RuntimeError(f"missing rigid-body target for grasp attachment: {missing}")
    hand_pose = declaration.world_pose(hand)
    core_pose = declaration.world_pose(core)
    frame = _relative_constraint_frame(hand_pose, core_pose)
    declaration.define_fixed_joint(stage, joint_path, hand_path, core_path, frame)
    return frame


def spawn_rubiks_cube_with_hand_attachment(
    prim_path, cfg, translation=None, orientation=None, **kwargs
):
    """Spawn the cube USD and immediately declare its disabled hand joint."""

    from isaaclab.sim.spawners.from_files.from_files import spawn_from_usd

    prim = spawn_from_usd(
        prim_path,
        cfg,
        translation=translation,
        orientation=orientation,
        **kwargs,
    )
    hand_body_name = getattr(cfg, 'attachment_hand_body_name', 'panda_hand')
    if hand_body_name == 'panda_hand':
        declare_hand_core_attachment(prim.GetStage(), str(prim.GetPath()))
    else:
        declare_hand_core_attachment(prim.GetStage(), str(prim.GetPath()), hand_body_name=hand_body_name)
    return prim


class PxrJointEditor:
    """Apply a group of USD joint changes under one ``Sdf.ChangeBlock``."""

    def __init__(self, stage):
        self.stage = stage

    def apply_transaction(self, updates: Sequence[JointUpdate]) -> None:
        from pxr import Gf, Sdf, UsdPhysics

        resolved = []
        for update in updates:
            joint = UsdPhysics.Joint.Get(self.stage, update.path)
            if not joint:
                raise RuntimeError(f"missing cube joint prim: {update.path}")
            if type(update.enabled) is not bool:
                raise TypeError("joint enabled state must be bool")
            if update.frame is not None:
                values = (*update.frame.position, *update.frame.quaternion)
                if len(update.frame.position) != 3 or len(update.frame.quaternion) != 4:
                    raise ValueError("joint frame must contain a 3-vector and quaternion")
                if any(isinstance(value, bool) or not math.isfinite(float(value)) for value in values):
                    raise ValueError("joint frame values must be finite")
                position_value = Gf.Vec3f(*update.frame.position)
                w, x, y, z = update.frame.quaternion
                rotation_value = Gf.Quatf(w, Gf.Vec3f(x, y, z))
            else:
                position_value = None
                rotation_value = None
            resolved.append((update, joint, position_value, rotation_value))
        with Sdf.ChangeBlock():
            for update, joint, position_value, rotation_value in resolved:
                if update.frame is not None:
                    _require_authoring_result(
                        joint.CreateLocalPos0Attr().Set(position_value),
                        f"{update.path} local position",
                    )
                    _require_authoring_result(
                        joint.CreateLocalRot0Attr().Set(rotation_value),
                        f"{update.path} local rotation",
                    )
                _require_authoring_result(
                    joint.CreateJointEnabledAttr().Set(update.enabled),
                    f"{update.path} enabled state",
                )


def read_cube_joint_snapshot(stage, root_path: str, *, hand_body_name='panda_hand') -> dict:
    """Read the authored joint graph, not UsdConstraintBackend's Python caches.

    This is bounded to joints below the declared cube root. It does not claim
    to inspect arbitrary external scene constraints or query PhysX's internal
    constraint solver. Later native samples must establish physical effects.
    """
    from pxr import Usd, UsdPhysics

    root = str(root_path).rstrip('/')
    prim = stage.GetPrimAtPath(root)
    if not prim:
        raise ValueError('Cube root is missing')
    from .rubiks_cube_constraint_audit import joint_graph, validate_joints
    body_paths = {name: root+'/Cubies/'+name for name in (
        b for values in joint_graph().values() for b in values[:2] if b.startswith('cubie_'))}
    body_paths.update({name: root+'/Mechanism/'+name
                      for name in ('world_anchor', 'core', 'carrier_x', 'carrier_y', 'carrier_z')})
    if not isinstance(hand_body_name,str) or not hand_body_name or '/' in hand_body_name:
        raise ValueError('Invalid declared hand body')
    # The audit graph uses one canonical hand role. Its actual native body is
    # frozen by the embodiment and verified here, never selected by a client.
    body_paths['panda_hand'] = root.rsplit('/', 1)[0]+'/Robot/'+hand_body_name
    path_names = {path: name for name, path in body_paths.items()}
    def body(relation):
        targets = relation.GetTargets()
        if len(targets) != 1 or str(targets[0]) not in path_names:
            raise ValueError('Joint targets an undeclared rigid body')
        return path_names[str(targets[0])]
    def quat(value):
        return [float(value.GetReal()), *map(float, value.GetImaginary())]
    def limit(value):
        if math.isnan(float(value)):
            raise ValueError('Invalid joint limit')
        return ('inf' if value > 0 else '-inf') if math.isinf(float(value)) else float(value)
    result = {}
    for child in Usd.PrimRange(prim):
        if not child.IsA(UsdPhysics.Joint):
            continue
        name = child.GetName()
        if str(child.GetPath()) != root+'/Joints/'+name or name in result:
            raise ValueError('Joint outside declared cube joint scope')
        joint = UsdPhysics.Joint(child)
        revolute = UsdPhysics.RevoluteJoint(child) if child.IsA(UsdPhysics.RevoluteJoint) else None
        result[name] = dict(enabled=joint.GetJointEnabledAttr().Get(),
            body0=body(joint.GetBody0Rel()), body1=body(joint.GetBody1Rel()),
            position0=list(map(float,joint.GetLocalPos0Attr().Get())),
            position1=list(map(float,joint.GetLocalPos1Attr().Get())),
            quaternion0=quat(joint.GetLocalRot0Attr().Get()), quaternion1=quat(joint.GetLocalRot1Attr().Get()),
            type=child.GetTypeName(), axis=str(revolute.GetAxisAttr().Get()) if revolute else None,
            lower_limit=limit(revolute.GetLowerLimitAttr().Get()) if revolute else None,
            upper_limit=limit(revolute.GetUpperLimitAttr().Get()) if revolute else None,
            drive_schemas=sorted(str(s) for s in child.GetAppliedSchemas() if 'DriveAPI' in str(s)),
            collision_enabled=joint.GetCollisionEnabledAttr().Get(),
            exclude_from_articulation=joint.GetExcludeFromArticulationAttr().Get())
    validate_joints(result)
    return result


class UsdConstraintBackend:
    """Translate mechanism transitions into one atomic USD edit transaction."""

    def __init__(self, root_path: str, cubie_ids: Sequence[str], editor: JointEditor):
        self.root_path = root_path.rstrip("/")
        self.cubie_ids = tuple(cubie_ids)
        if len(self.cubie_ids) != 26 or len(set(self.cubie_ids)) != 26:
            raise ValueError("USD cube backend requires 26 unique cubie ids")
        self.editor = editor
        self.active_attachments: set[tuple[str, str]] = set()
        self.world_anchor_enabled = True
        self.transport_locks_enabled = False
        self.world_anchor_released_during_transport = False
        self.hand_attachment_enabled = False

    def _anchor_path(self, cubie_id: str) -> str:
        return f"{self.root_path}/Joints/core_anchor_{cubie_id}"

    def _attachment_path(self, axis: str, cubie_id: str) -> str:
        return f"{self.root_path}/Joints/carrier_attachment_{axis}_{cubie_id}"

    def _hinge_path(self, axis: str) -> str:
        return f"{self.root_path}/Joints/carrier_hinge_{axis}"

    def _transport_lock_path(self, axis: str) -> str:
        return f"{self.root_path}/Joints/carrier_transport_lock_{axis}"

    def _world_anchor_path(self) -> str:
        return f"{self.root_path}/Joints/world_core_anchor"

    def _hand_attachment_path(self) -> str:
        return f"{self.root_path}/Joints/robot_hand_core_attachment"

    def activate_layer(self, axis: str, cubie_frames: dict[str, ConstraintFrame]) -> None:
        normalized_axis = axis.lower()
        if normalized_axis not in {"x", "y", "z"}:
            raise ValueError(f"unsupported carrier axis: {axis!r}")
        if self.active_attachments:
            raise RuntimeError("cannot activate a layer while attachments are already enabled")
        if self.hand_attachment_enabled:
            raise RuntimeError("cannot activate a layer while the robot hand attachment is enabled")
        if self.transport_locks_enabled or not self.world_anchor_enabled:
            raise RuntimeError("cannot activate a layer during whole-cube transport")
        active = tuple(sorted(cubie_frames))
        if len(active) != 9 or not set(active) <= set(self.cubie_ids):
            raise ValueError("an active face must contain exactly nine known cubies")
        updates = []
        for cubie_id in active:
            updates.append(JointUpdate(self._anchor_path(cubie_id), enabled=False))
        for cubie_id in active:
            updates.append(
                JointUpdate(
                    self._attachment_path(normalized_axis, cubie_id),
                    enabled=True,
                    frame=cubie_frames[cubie_id],
                )
            )
        self.editor.apply_transaction(updates)
        self.active_attachments = {(normalized_axis, cubie_id) for cubie_id in active}

    def anchor_all(self, cubie_frames: dict[str, ConstraintFrame]) -> None:
        if set(cubie_frames) != set(self.cubie_ids):
            raise ValueError("anchoring requires frames for all 26 cubies")
        updates = [
            JointUpdate(self._attachment_path(axis, cubie_id), enabled=False)
            for axis, cubie_id in sorted(self.active_attachments)
        ]
        updates.extend(
            JointUpdate(self._anchor_path(cubie_id), enabled=True, frame=cubie_frames[cubie_id])
            for cubie_id in sorted(self.cubie_ids)
        )
        self.editor.apply_transaction(updates)
        self.active_attachments.clear()

    def prepare_transport(self, carrier_frames: dict[str, ConstraintFrame]) -> None:
        """Atomically replace the three carrier hinges with transport locks."""

        if set(carrier_frames) != {"x", "y", "z"}:
            raise ValueError("transport preparation requires x, y, and z carrier frames")
        if self.active_attachments:
            raise RuntimeError("cannot prepare transport while a layer is active")
        if self.transport_locks_enabled:
            raise RuntimeError("transport is already prepared")
        if not self.world_anchor_enabled:
            raise RuntimeError("cannot prepare transport while the world anchor is released")
        updates = [JointUpdate(self._hinge_path(axis), enabled=False) for axis in "xyz"]
        updates.extend(
            JointUpdate(
                self._transport_lock_path(axis),
                enabled=True,
                frame=carrier_frames[axis],
            )
            for axis in "xyz"
        )
        self.editor.apply_transaction(updates)
        self.transport_locks_enabled = True
        self.world_anchor_released_during_transport = False

    def release_world_anchor(self) -> None:
        """Release the dynamic core only after transport has been prepared."""

        if not self.transport_locks_enabled:
            raise RuntimeError("transport must be prepared before releasing the world anchor")
        if not self.world_anchor_enabled:
            raise RuntimeError("world anchor is already released")
        self.editor.apply_transaction((JointUpdate(self._world_anchor_path(), enabled=False),))
        self.world_anchor_enabled = False
        self.world_anchor_released_during_transport = True

    def acquire_hand_attachment(self, hand_core_frame: ConstraintFrame) -> None:
        """Atomically exchange measured world support for the hand attachment."""

        if not self.transport_locks_enabled:
            raise RuntimeError("transport must be prepared before grasp attachment")
        if not self.world_anchor_enabled:
            raise RuntimeError("world anchor must be enabled before grasp attachment")
        if self.hand_attachment_enabled:
            raise RuntimeError("hand attachment is already enabled")
        self.editor.apply_transaction(
            (
                JointUpdate(self._hand_attachment_path(), enabled=True, frame=hand_core_frame),
                JointUpdate(self._world_anchor_path(), enabled=False),
            )
        )
        self.hand_attachment_enabled = True
        self.world_anchor_enabled = False
        self.world_anchor_released_during_transport = True

    def capture_support_and_detach(self, core_frame: ConstraintFrame) -> None:
        """Atomically replace the hand attachment by measured world support."""

        if not self.transport_locks_enabled:
            raise RuntimeError("cannot capture support outside whole-cube transport")
        if self.world_anchor_enabled:
            raise RuntimeError("world anchor is already enabled")
        if not self.hand_attachment_enabled:
            raise RuntimeError("valid hand attachment is required before support capture")
        self.editor.apply_transaction(
            (
                JointUpdate(self._world_anchor_path(), enabled=True, frame=core_frame),
                JointUpdate(self._hand_attachment_path(), enabled=False),
            )
        )
        self.world_anchor_enabled = True
        self.hand_attachment_enabled = False

    def reanchor_world(self, core_frame: ConstraintFrame) -> None:
        """Freeze the core at its measured settled pose without writing body state."""

        if not self.transport_locks_enabled:
            raise RuntimeError("cannot reanchor outside whole-cube transport")
        if self.world_anchor_enabled:
            raise RuntimeError("world anchor is already enabled")
        self.editor.apply_transaction(
            (JointUpdate(self._world_anchor_path(), enabled=True, frame=core_frame),)
        )
        self.world_anchor_enabled = True

    def finish_transport(self) -> None:
        """Atomically restore unlimited hinges after the core is reanchored."""

        if not self.transport_locks_enabled:
            raise RuntimeError("transport is not prepared")
        if not self.world_anchor_enabled:
            raise RuntimeError("world anchor must be enabled before finishing transport")
        if self.hand_attachment_enabled:
            raise RuntimeError("hand attachment must be disabled before finishing transport")
        if not self.world_anchor_released_during_transport:
            raise RuntimeError("world anchor has not been released and reanchored")
        updates = [
            JointUpdate(self._transport_lock_path(axis), enabled=False) for axis in "xyz"
        ]
        updates.extend(JointUpdate(self._hinge_path(axis), enabled=True) for axis in "xyz")
        self.editor.apply_transaction(updates)
        self.transport_locks_enabled = False
        self.world_anchor_released_during_transport = False

    def reset(
        self,
        cubie_frames: dict[str, ConstraintFrame],
        world_core_frame: ConstraintFrame,
    ) -> None:
        if set(cubie_frames) != set(self.cubie_ids):
            raise ValueError("reset requires frames for all 26 cubies")
        updates = [
            JointUpdate(self._attachment_path(axis, cubie_id), enabled=False)
            for axis in ("x", "y", "z")
            for cubie_id in sorted(self.cubie_ids)
        ]
        updates.extend(
            JointUpdate(self._anchor_path(cubie_id), enabled=True, frame=cubie_frames[cubie_id])
            for cubie_id in sorted(self.cubie_ids)
        )
        updates.extend(
            JointUpdate(self._transport_lock_path(axis), enabled=False) for axis in "xyz"
        )
        updates.extend(JointUpdate(self._hinge_path(axis), enabled=True) for axis in "xyz")
        updates.append(
            JointUpdate(
                self._world_anchor_path(),
                enabled=True,
                frame=world_core_frame,
            )
        )
        updates.append(JointUpdate(self._hand_attachment_path(), enabled=False))
        self.editor.apply_transaction(updates)
        self.active_attachments.clear()
        self.transport_locks_enabled = False
        self.world_anchor_enabled = True
        self.world_anchor_released_during_transport = False
        self.hand_attachment_enabled = False
