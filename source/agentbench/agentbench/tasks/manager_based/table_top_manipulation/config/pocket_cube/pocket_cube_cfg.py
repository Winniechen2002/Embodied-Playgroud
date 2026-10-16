"""Shared physical scene and observations for bimanual 2x2 cube tasks."""

from __future__ import annotations

import copy
from dataclasses import MISSING
from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.sim import schemas
from isaaclab.sim.spawners.from_files import spawn_from_usd
from isaaclab.sim.utils import bind_physics_material
from isaaclab.assets import (
    ArticulationCfg,
    AssetBaseCfg,
    RigidObjectCfg,
    RigidObjectCollectionCfg,
)
from isaaclab.envs import ManagerBasedEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.utils import configclass
from pxr import Gf, UsdPhysics

from ... import mdp
from . import pocket_cube_observations
from .pocket_cube_rules import CORNER_NAMES
from .pocket_cube_spawners import spawn_pocket_cube_root, spawn_switchable_cube_joints


TABLE_TOP_Z = 0.60
CUBE_WIDTH = 0.050
NOMINAL_CUBIE_GAP = 0.0008
CUBIE_SHRINK = 0.0004
NOMINAL_CUBIE_SIZE = (CUBE_WIDTH - NOMINAL_CUBIE_GAP) / 2.0
CUBIE_VISUAL_SIZE = NOMINAL_CUBIE_SIZE - CUBIE_SHRINK
# This is also the declared exterior used by the strict penetration audit.
# The scan-derived convex collision is rounded, but it receives no permission
# to bypass that full 24.2 mm audited envelope.
CUBIE_COLLISION_INSET = 0.0
CUBIE_COLLISION_SIZE = CUBIE_VISUAL_SIZE - CUBIE_COLLISION_INSET
CUBIE_CENTER_OFFSET = (NOMINAL_CUBIE_SIZE + NOMINAL_CUBIE_GAP) / 2.0
CUBIE_GAP = 2.0 * CUBIE_CENTER_OFFSET - CUBIE_VISUAL_SIZE
CUBE_SUPPORT_TOP_Z = TABLE_TOP_Z + 0.025
CUBE_SUPPORT_GAP = 0.0005
CUBE_REST_SIZE = (0.032, 0.032, 0.025)
CUBE_CENTER = (
    0.56,
    0.0,
    CUBE_SUPPORT_TOP_Z + CUBE_WIDTH / 2.0 + CUBE_SUPPORT_GAP,
)
TABLE_MATERIAL = sim_utils.RigidBodyMaterialCfg(
    static_friction=0.9,
    dynamic_friction=0.7,
    restitution=0.0,
)
REST_MATERIAL = sim_utils.RigidBodyMaterialCfg(
    # The visibly separate cube rest represents a rubber manipulation mat.
    # It remains an open, flat contact surface: no wall, pin, cage, or hidden
    # attachment constrains the cube, and a robot can still lift it vertically.
    static_friction=2.2,
    dynamic_friction=1.8,
    restitution=0.0,
)
CUBE_MATERIAL = sim_utils.RigidBodyMaterialCfg(
    static_friction=1.4,
    dynamic_friction=1.1,
    restitution=0.0,
)

# Keep the inertial distribution identical to pocket_cube.md.  The previous
# values happened to preserve the same 70 g total, but put ten times too much
# of it in the temporary carrier and too little in the eight visible corners.
# That made a selected layer and every lock handoff behave unlike the declared
# physical mechanism even though a scale would report the expected weight.
CUBIE_MASS = 0.0075
CORE_MASS = 0.008
CARRIER_MASS = 0.002
SCANNED_CUBIE_ASSET_DIR = (
    Path(__file__).resolve().parents[5]
    / "assets/assets/pocket_cube/scanned_gap_matched"
)
# Keep inertial properties controlled while changing only the collision shell.
# PhysX otherwise treats the scanned exterior as a homogeneous solid and
# introduces a 0.07--0.14 mm COM offset that the real internal mechanism does
# not justify.  This is the exact inertia of the previous 24.2 mm, 7.5 g box.
SCANNED_CUBIE_DIAGONAL_INERTIA = 7.320500117202755e-7


def _iter_mesh_prims(prim):
    for child in prim.GetAllChildren():
        if child.GetTypeName() == "Mesh":
            yield child
        yield from _iter_mesh_prims(child)


def _spawn_scanned_cubie(prim_path, cfg, *args, **kwargs):
    """Spawn a scan mesh with the task's controlled rigid-body properties."""

    source_cfg = copy.copy(cfg)
    source_cfg.rigid_props = None
    source_cfg.collision_props = None
    source_cfg.mass_props = None
    prim = spawn_from_usd(prim_path, source_cfg, *args, **kwargs)
    resolved_path = prim.GetPath().pathString
    stage = prim.GetStage()
    schemas.define_rigid_body_properties(
        resolved_path, cfg.rigid_props, stage=stage
    )
    schemas.define_mass_properties(resolved_path, cfg.mass_props, stage=stage)

    mass_api = UsdPhysics.MassAPI.Apply(prim)
    mass_api.CreateCenterOfMassAttr().Set(Gf.Vec3f(0.0, 0.0, 0.0))
    mass_api.CreateDiagonalInertiaAttr().Set(
        Gf.Vec3f(*((SCANNED_CUBIE_DIAGONAL_INERTIA,) * 3))
    )
    mass_api.CreatePrincipalAxesAttr().Set(Gf.Quatf(1.0))

    # A 64-vertex cook retained too many tiny scan facets and produced contact
    # normal jitter.  Sixteen vertices preserve the rounded-corner silhouette
    # while outperforming the previous box in the controlled PhysX A/B.
    mesh_props = sim_utils.ConvexHullPropertiesCfg(hull_vertex_limit=16)
    for mesh in _iter_mesh_prims(prim):
        mesh_path = mesh.GetPath().pathString
        schemas.define_collision_properties(
            mesh_path, cfg.collision_props, stage=stage
        )
        schemas.define_mesh_collision_properties(
            mesh_path, mesh_props, stage=stage
        )

    material_path = f"{resolved_path}/PhysicsMaterial"
    CUBE_MATERIAL.func(material_path, CUBE_MATERIAL)
    bind_physics_material(resolved_path, material_path, stage=stage)
    return prim


def _cubie_cfg(corner_name: str) -> RigidObjectCfg:
    local = (
        CUBIE_CENTER_OFFSET if "R" in corner_name else -CUBIE_CENTER_OFFSET,
        CUBIE_CENTER_OFFSET if "F" in corner_name else -CUBIE_CENTER_OFFSET,
        CUBIE_CENTER_OFFSET if "U" in corner_name else -CUBIE_CENTER_OFFSET,
    )
    return RigidObjectCfg(
        prim_path=f"{{ENV_REGEX_NS}}/PocketCube/Cubies/Cubie_{corner_name.lower()}",
        spawn=sim_utils.UsdFileCfg(
            func=_spawn_scanned_cubie,
            usd_path=str(
                SCANNED_CUBIE_ASSET_DIR / f"cubie_{corner_name.lower()}.usd"
            ),
            # The full-resolution scan remains in the USD, while the existing
            # pose-synchronized render shell avoids stale nested RTX transforms
            # under Fabric. Physics uses the scan-derived convex hull.
            visible=False,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
                retain_accelerations=True,
                linear_damping=0.06,
                angular_damping=0.06,
                max_linear_velocity=2.0,
                max_angular_velocity=20.0,
                max_depenetration_velocity=0.2,
                solver_position_iteration_count=32,
                # Match the robot articulation's contact solve quality.  The
                # previous four velocity iterations allowed a fast detent
                # release to exceed the 0.25 mm visible-shell tolerance even
                # though the contact offsets were already conservative.
                solver_velocity_iteration_count=8,
            ),
            collision_props=sim_utils.CollisionPropertiesCfg(
                contact_offset=0.00025, rest_offset=0.0
            ),
            mass_props=sim_utils.MassPropertiesCfg(mass=CUBIE_MASS),
            activate_contact_sensors=True,
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=tuple(CUBE_CENTER[index] + local[index] for index in range(3)),
            rot=(1.0, 0.0, 0.0, 0.0),
        ),
    )


def _strict_collision_props() -> sim_utils.CollisionPropertiesCfg:
    """Create non-penetrating contact settings for cube-adjacent geometry."""
    return sim_utils.CollisionPropertiesCfg(contact_offset=0.0008, rest_offset=0.0)


def _internal_body_cfg(prim_path: str, mass: float) -> RigidObjectCfg:
    return RigidObjectCfg(
        prim_path=prim_path,
        spawn=sim_utils.SphereCfg(
            # Collision is disabled, so this radius is purely the inertial
            # scaffold for the maximal-coordinate lock mechanism.  A 4 mm
            # sphere gave Core/Carrier inertias roughly two orders of
            # magnitude below the eight cubies constrained 12.7 mm away and
            # visibly exploded at idle.  Match the 25 mm cube half-width so
            # the constrained aggregate has a physically scaled inertia.
            radius=CUBE_WIDTH / 2.0,
            visible=False,
            collision_props=sim_utils.CollisionPropertiesCfg(collision_enabled=False),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
                retain_accelerations=True,
                linear_damping=0.08,
                angular_damping=0.08,
                max_linear_velocity=2.0,
                max_angular_velocity=20.0,
                max_depenetration_velocity=0.2,
                solver_position_iteration_count=32,
                solver_velocity_iteration_count=4,
            ),
            mass_props=sim_utils.MassPropertiesCfg(mass=mass),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=CUBE_CENTER, rot=(1.0, 0.0, 0.0, 0.0)
        ),
    )


POCKET_CUBE_CORE_CFG = _internal_body_cfg(
    "{ENV_REGEX_NS}/PocketCube/Core", CORE_MASS
)
POCKET_CUBE_CARRIER_CFG = _internal_body_cfg(
    "{ENV_REGEX_NS}/PocketCube/Carrier", CARRIER_MASS
)


def _fixed_reset(asset_name: str) -> EventTerm:
    return EventTerm(
        func=mdp.reset_root_state_uniform,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg(asset_name),
            "pose_range": {axis: (0.0, 0.0) for axis in ("x", "y", "z", "roll", "pitch", "yaw")},
            "velocity_range": {axis: (0.0, 0.0) for axis in ("x", "y", "z", "roll", "pitch", "yaw")},
        },
    )


def reset_pocket_cubies(env, env_ids, asset_cfg: SceneEntityCfg) -> None:
    """Restore every independent corner body to its configured solved pose."""

    cubies = env.scene[asset_cfg.name]
    state = cubies.data.default_object_state[env_ids].clone()
    state[..., :3] += env.scene.env_origins[env_ids, None, :]
    cubies.write_object_state_to_sim(state, env_ids=env_ids)


@configclass
class PocketCubeSceneCfg(InteractiveSceneCfg):
    left_robot: ArticulationCfg = MISSING
    right_robot: ArticulationCfg = MISSING
    pocket_cube_root: AssetBaseCfg = AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/PocketCube",
        spawn=sim_utils.SpawnerCfg(func=spawn_pocket_cube_root, visible=False),
    )
    pocket_cube: RigidObjectCfg = POCKET_CUBE_CORE_CFG
    pocket_cube_carrier: RigidObjectCfg = POCKET_CUBE_CARRIER_CFG
    pocket_cube_cubies_root: AssetBaseCfg = AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/PocketCube/Cubies",
        spawn=sim_utils.SpawnerCfg(func=spawn_pocket_cube_root, visible=False),
    )
    pocket_cubies: RigidObjectCollectionCfg = RigidObjectCollectionCfg(
        rigid_objects={name.lower(): _cubie_cfg(name) for name in CORNER_NAMES}
    )
    pocket_cube_joints: AssetBaseCfg = AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/PocketCube/Joints",
        spawn=sim_utils.SpawnerCfg(
            func=spawn_switchable_cube_joints,
            visible=False,
        ),
    )
    table: RigidObjectCfg = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Table",
        spawn=sim_utils.CuboidCfg(
            size=(1.05, 1.10, 0.50),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            physics_material=TABLE_MATERIAL,
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(0.32, 0.34, 0.36), roughness=0.62
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.45, 0.0, TABLE_TOP_Z - 0.25), rot=(1.0, 0.0, 0.0, 0.0)
        ),
    )

    cube_rest: RigidObjectCfg = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/CubeRest",
        spawn=sim_utils.CuboidCfg(
            # A visible open pedestal, narrower than the cube footprint so the
            # lower layer remains reachable by ordinary parallel grippers.  It
            # has no stem, side wall, pin, cage, or attachment: the cube remains
            # a free body and can slide, tip, or be picked up.
            size=CUBE_REST_SIZE,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
            collision_props=_strict_collision_props(),
            physics_material=REST_MATERIAL,
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(0.10, 0.11, 0.12), roughness=0.75
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(
                CUBE_CENTER[0],
                CUBE_CENTER[1],
                TABLE_TOP_Z + 0.0125,
            ),
            rot=(1.0, 0.0, 0.0, 0.0),
        ),
    )

    sky_light = AssetBaseCfg(
        prim_path="/World/skyLight",
        spawn=sim_utils.DomeLightCfg(intensity=900.0, color=(0.88, 0.91, 1.0)),
    )


@configclass
class PocketCubeObservationsCfg:
    @configclass
    class StateCfg(ObsGroup):
        actions = ObsTerm(func=mdp.last_action)
        left_joint_pos = ObsTerm(
            func=mdp.joint_pos_rel, params={"asset_cfg": SceneEntityCfg("left_robot")}
        )
        left_joint_vel = ObsTerm(
            func=mdp.joint_vel_rel, params={"asset_cfg": SceneEntityCfg("left_robot")}
        )
        right_joint_pos = ObsTerm(
            func=mdp.joint_pos_rel, params={"asset_cfg": SceneEntityCfg("right_robot")}
        )
        right_joint_vel = ObsTerm(
            func=mdp.joint_vel_rel, params={"asset_cfg": SceneEntityCfg("right_robot")}
        )
        cube_root_pos = ObsTerm(
            func=mdp.root_pos_w, params={"asset_cfg": SceneEntityCfg("pocket_cube")}
        )
        cube_root_quat = ObsTerm(
            func=mdp.root_quat_w, params={"asset_cfg": SceneEntityCfg("pocket_cube")}
        )
        cube_detents = ObsTerm(
            func=pocket_cube_observations.cube_detent_state,
        )
        cubie_state = ObsTerm(func=pocket_cube_observations.cube_cubie_state)
        target_state = ObsTerm(func=pocket_cube_observations.cube_target_state)
        interlock = ObsTerm(func=pocket_cube_observations.cube_interlock_state)
        success = ObsTerm(func=pocket_cube_observations.cube_success)

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class PocketCubeEventsCfg:
    reset_left_robot = EventTerm(
        func=mdp.reset_joints_to_init,
        mode="reset",
        params={"asset_cfg": SceneEntityCfg("left_robot")},
    )
    reset_right_robot = EventTerm(
        func=mdp.reset_joints_to_init,
        mode="reset",
        params={"asset_cfg": SceneEntityCfg("right_robot")},
    )
    reset_cube_root = _fixed_reset("pocket_cube")
    reset_cube_carrier = _fixed_reset("pocket_cube_carrier")
    reset_cube_cubies = EventTerm(
        func=reset_pocket_cubies,
        mode="reset",
        params={"asset_cfg": SceneEntityCfg("pocket_cubies")},
    )


@configclass
class PocketCubeEnvCfgBase(ManagerBasedEnvCfg):
    # The default benchmark asks for L, while callers may supply any valid
    # sequence over U/D/F/B/R/L without changing the mechanism topology.
    target_moves: tuple[tuple[str, int], ...] = (("L", 1),)
    # A one-move benchmark can select its physical carrier at reset. This
    # avoids a loaded fixed-joint topology switch at first contact and must be
    # identical for every robot variant of the task.
    preconfigure_single_target_face: bool = True
    # Wrong-order contacts remain ordinary contacts but cannot unlock a layer.
    # This makes the declared exact move sequence part of the physical
    # interlock instead of allowing an incidental maximum torque projection to
    # seize the shared carrier ahead of the requested face.
    enforce_target_face_order: bool = True
    viewer: ViewerCfg = ViewerCfg(
        eye=(1.35, -1.45, 1.18),
        lookat=(0.52, 0.0, 0.69),
        origin_type="env",
    )
    scene: PocketCubeSceneCfg = PocketCubeSceneCfg(
        num_envs=256, env_spacing=2.2, replicate_physics=False
    )
    observations: PocketCubeObservationsCfg = PocketCubeObservationsCfg()
    actions = MISSING
    events: PocketCubeEventsCfg = PocketCubeEventsCfg()

    def __post_init__(self):
        self.scene.pocket_cube.spawn.semantic_tags = [("class", "pocket_cube")]
        for cubie_cfg in self.scene.pocket_cubies.rigid_objects.values():
            cubie_cfg.spawn.semantic_tags = [("class", "pocket_cube")]
        self.scene.table.spawn.semantic_tags = [("class", "table")]
        self.scene.cube_rest.spawn.semantic_tags = [("class", "cube_rest")]
        # The small corner bodies and live joint switching use a 240 Hz
        # physics loop while retaining a 60 Hz control period.
        self.decimation = 4
        self.sim.dt = 1 / 240
        self.sim.render_interval = self.decimation
        self.sim.physx.enable_ccd = True
        # Integrate the bounded local detent and its Newton-paired reaction on
        # every solver iteration.
        self.sim.physx.enable_external_forces_every_iteration = True
        self.sim.physx.bounce_threshold_velocity = 0.01
        self.sim.physx.friction_correlation_distance = 0.004
        self.sim.physx.gpu_max_rigid_patch_count = 2**19
