"""USD spawner for the pocket cube's switchable carrier constraints."""

from __future__ import annotations

from pxr import Gf, Sdf, Usd, UsdGeom, UsdPhysics

import isaaclab.sim as sim_utils

from .pocket_cube_rules import CORNER_NAMES


IDENTITY_Q = Gf.Quatf(1.0, Gf.Vec3f(0.0))


def _corner_local_position(name: str, offset: float) -> Gf.Vec3f:
    """Return a corner center using +X=R, +Y=F, +Z=U."""

    return Gf.Vec3f(
        offset if "R" in name else -offset,
        offset if "F" in name else -offset,
        offset if "U" in name else -offset,
    )


def _set_fixed_frame(joint: UsdPhysics.FixedJoint, position: Gf.Vec3f) -> None:
    joint.CreateLocalPos0Attr(position)
    joint.CreateLocalRot0Attr(IDENTITY_Q)
    joint.CreateLocalPos1Attr(Gf.Vec3f(0.0))
    joint.CreateLocalRot1Attr(IDENTITY_Q)


def _fixed_joint(
    stage: Usd.Stage,
    path: str,
    body0: str,
    body1: str,
    position: Gf.Vec3f,
    enabled: bool,
) -> UsdPhysics.FixedJoint:
    joint = UsdPhysics.FixedJoint.Define(stage, path)
    joint.CreateBody0Rel().SetTargets([Sdf.Path(body0)])
    joint.CreateBody1Rel().SetTargets([Sdf.Path(body1)])
    _set_fixed_frame(joint, position)
    joint.CreateJointEnabledAttr(enabled)
    joint.CreateCollisionEnabledAttr(False)
    joint.CreateExcludeFromArticulationAttr(True)
    return joint


def spawn_pocket_cube_root(
    prim_path: str,
    cfg: sim_utils.SpawnerCfg,
    translation=None,
    orientation=None,
    **kwargs,
) -> Usd.Prim:
    """Create the shared Xform parent required by the nested rigid bodies."""

    del cfg, translation, orientation, kwargs
    stage = sim_utils.get_current_stage()
    root_expression, leaf_name = prim_path.rsplit("/", 1)
    env_roots = sim_utils.find_matching_prim_paths(root_expression)
    if not env_roots:
        raise RuntimeError(f"No environments match pocket-cube root path: {prim_path}")
    source_prim = None
    for env_root in env_roots:
        root = UsdGeom.Xform.Define(stage, f"{env_root}/{leaf_name}").GetPrim()
        sim_utils.standardize_xform_ops(root)
        source_prim = source_prim or root
    assert source_prim is not None
    return source_prim


def spawn_switchable_cube_joints(
    prim_path: str,
    cfg: sim_utils.SpawnerCfg,
    translation=None,
    orientation=None,
    **kwargs,
) -> Usd.Prim:
    """Create core/carrier locks, eight lock pairs, and three inactive hinges.

    The mechanism is deliberately maximal-coordinate.  No rigid-body parent
    hierarchy is used as a physical connection, and no articulation root is
    authored: exactly one of the X/Y/Z carrier hinges is enabled for a turn.
    """

    del translation, orientation, kwargs
    stage = sim_utils.get_current_stage()
    root_expression, leaf_name = prim_path.rsplit("/", 1)
    cube_roots = sim_utils.find_matching_prim_paths(root_expression)
    if not cube_roots:
        raise RuntimeError(f"No environments match joint path: {prim_path}")

    # The centers and joint frames remain at the original 12.7 mm offset even
    # when the visible/collision corner bodies are made slightly smaller.
    offset = float(getattr(cfg, "cubie_offset", 0.0127))
    source_prim = None
    for cube_root in cube_roots:
        joints_path = f"{cube_root}/{leaf_name}"
        joints = UsdGeom.Xform.Define(stage, joints_path).GetPrim()
        sim_utils.standardize_xform_ops(joints)
        source_prim = source_prim or joints

        core = f"{cube_root}/Core"
        carrier = f"{cube_root}/Carrier"
        core_locks = f"{joints_path}/CoreLocks"
        carrier_locks = f"{joints_path}/CarrierLocks"
        stage.DefinePrim(core_locks, "Scope")
        stage.DefinePrim(carrier_locks, "Scope")

        for name in CORNER_NAMES:
            cubie = f"{cube_root}/Cubies/Cubie_{name.lower()}"
            local_position = _corner_local_position(name, offset)
            _fixed_joint(
                stage,
                f"{core_locks}/{name.lower()}",
                core,
                cubie,
                local_position,
                True,
            )
            _fixed_joint(
                stage,
                f"{carrier_locks}/{name.lower()}",
                carrier,
                cubie,
                local_position,
                False,
            )

        _fixed_joint(
            stage,
            f"{joints_path}/CoreCarrierLock",
            core,
            carrier,
            Gf.Vec3f(0.0),
            True,
        )

        for axis in ("X", "Y", "Z"):
            hinge = UsdPhysics.RevoluteJoint.Define(stage, f"{joints_path}/Hinge{axis}")
            hinge.CreateBody0Rel().SetTargets([Sdf.Path(core)])
            hinge.CreateBody1Rel().SetTargets([Sdf.Path(carrier)])
            hinge.CreateLocalPos0Attr(Gf.Vec3f(0.0))
            hinge.CreateLocalPos1Attr(Gf.Vec3f(0.0))
            hinge.CreateLocalRot0Attr(IDENTITY_Q)
            hinge.CreateLocalRot1Attr(IDENTITY_Q)
            hinge.CreateAxisAttr(axis)
            hinge.CreateLowerLimitAttr(-95.0)
            hinge.CreateUpperLimitAttr(95.0)
            hinge.CreateJointEnabledAttr(False)
            hinge.CreateCollisionEnabledAttr(False)
            hinge.CreateExcludeFromArticulationAttr(True)

    assert source_prim is not None
    return source_prim
