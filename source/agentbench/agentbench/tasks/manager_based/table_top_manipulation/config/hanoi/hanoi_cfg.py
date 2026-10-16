"""Tower-of-Hanoi scene with handled rings and a Franka Panda gripper on a tabletop."""

import copy
from dataclasses import MISSING
from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg, AssetBaseCfg, RigidObjectCfg
from isaaclab.envs import ManagerBasedEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.sim import schemas
from isaaclab.sim.spawners.from_files import spawn_from_usd
from isaaclab.sim.utils import bind_physics_material
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
from isaaclab_assets.robots.franka import FRANKA_PANDA_HIGH_PD_CFG

from ... import mdp


TABLE_TOP_Z = 0.60
BOARD_HEIGHT = 0.025
RING_HEIGHT = 0.035
RING_Z_GAP = 0.0
BOARD_SIZE = (0.58, 0.88, BOARD_HEIGHT)
BOARD_CENTER = (0.71, 0.0, TABLE_TOP_Z + BOARD_HEIGHT * 0.5)
PEG_X = 0.67
PEG_YS = (-0.32, 0.0, 0.32)
PEG_HEIGHT = 0.20
PEG_RADIUS = 0.016
RING_MASS = 0.03
RING_CENTER_X = PEG_X
RING_CENTER_Y = PEG_YS[0]
RING_BASE_Z = TABLE_TOP_Z + BOARD_HEIGHT + RING_HEIGHT * 0.5
RING_FILTER_PRIMS = [
    "{ENV_REGEX_NS}/RingXLarge",
    "{ENV_REGEX_NS}/RingLarge",
    "{ENV_REGEX_NS}/RingMedium",
    "{ENV_REGEX_NS}/RingSmall",
    "{ENV_REGEX_NS}/RingXSmall",
]
VISION_CAMERA_WIDTH = 640
VISION_CAMERA_HEIGHT = 480
VISION_CAMERA_EYE = (1.9, -2.4, 1.55)
VISION_CAMERA_TARGET = (0.28, -0.28, 0.78)
# Keep the Franka on the tabletop in front of the board. The base should not
# overlap the Hanoi board or any peg, otherwise contact diagnostics start dirty.
ROBOT_BASE_X = 0.36
ROBOT_BASE_Y = 0.00
ROBOT_BASE_Z = TABLE_TOP_Z
RING_ASSET_DIR = Path(__file__).resolve().parents[5] / "assets" / "assets" / "hanoi_rings"
RING_PHYSICS_MATERIAL = sim_utils.RigidBodyMaterialCfg(
    static_friction=1.6,
    dynamic_friction=1.2,
    restitution=0.0,
    friction_combine_mode="average",
    restitution_combine_mode="min",
)
PEG_PHYSICS_MATERIAL = sim_utils.RigidBodyMaterialCfg(
    static_friction=0.005,
    dynamic_friction=0.002,
    restitution=0.0,
    friction_combine_mode="average",
    restitution_combine_mode="min",
)
SURFACE_PHYSICS_MATERIAL = sim_utils.RigidBodyMaterialCfg(
    static_friction=0.8,
    dynamic_friction=0.6,
    restitution=0.0,
    friction_combine_mode="average",
    restitution_combine_mode="min",
)


def _iter_mesh_prims(prim):
    for child in prim.GetAllChildren():
        if child.GetTypeName() == "Mesh":
            yield child
        yield from _iter_mesh_prims(child)


def _spawn_ring_with_rigid(prim_path, cfg, *args, **kwargs):
    spawn_cfg = copy.copy(cfg)
    spawn_cfg.rigid_props = None
    spawn_cfg.collision_props = None
    spawn_cfg.mass_props = None
    prim = spawn_from_usd(prim_path, spawn_cfg, *args, **kwargs)
    prim_path_resolved = prim.GetPath().pathString
    if cfg.rigid_props is not None:
        schemas.define_rigid_body_properties(prim_path_resolved, cfg.rigid_props)
    if cfg.mass_props is not None:
        schemas.define_mass_properties(prim_path_resolved, cfg.mass_props)
    if cfg.collision_props is not None:
        stage = prim.GetStage()
        mesh_props = sim_utils.ConvexHullPropertiesCfg(hull_vertex_limit=16)
        for child in _iter_mesh_prims(prim):
            child_path = child.GetPath().pathString
            schemas.define_collision_properties(child_path, cfg.collision_props, stage=stage)
            schemas.define_mesh_collision_properties(child_path, mesh_props, stage=stage)
        material_path = f"{prim_path_resolved}/PhysicsMaterial"
        RING_PHYSICS_MATERIAL.func(material_path, RING_PHYSICS_MATERIAL)
        bind_physics_material(prim_path_resolved, material_path, stage=stage)
    return prim


def _ring_cfg(name: str, z_index: int) -> RigidObjectCfg:
    return RigidObjectCfg(
        prim_path=f"{{ENV_REGEX_NS}}/{name}",
        spawn=sim_utils.UsdFileCfg(
            func=_spawn_ring_with_rigid,
            usd_path=str(RING_ASSET_DIR / f"{name}.usda"),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                rigid_body_enabled=True,
                solver_position_iteration_count=16,
                solver_velocity_iteration_count=1,
                max_linear_velocity=1000.0,
                max_angular_velocity=1000.0,
                max_depenetration_velocity=5.0,
                disable_gravity=False,
            ),
            collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.001, rest_offset=0.0),
            mass_props=sim_utils.MassPropertiesCfg(mass=RING_MASS),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(RING_CENTER_X, RING_CENTER_Y, RING_BASE_Z + z_index * (RING_HEIGHT + RING_Z_GAP)),
            rot=(1.0, 0.0, 0.0, 0.0),
        ),
    )


def _peg_cfg(name: str, y: float) -> AssetBaseCfg:
    return AssetBaseCfg(
        prim_path=f"{{ENV_REGEX_NS}}/{name}",
        spawn=sim_utils.CylinderCfg(
            radius=PEG_RADIUS,
            height=PEG_HEIGHT,
            collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.001, rest_offset=0.0),
            physics_material=PEG_PHYSICS_MATERIAL,
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.16, 0.12, 0.08), roughness=0.4),
        ),
        init_state=AssetBaseCfg.InitialStateCfg(
            pos=(PEG_X, y, TABLE_TOP_Z + BOARD_HEIGHT + PEG_HEIGHT * 0.5),
            rot=(1.0, 0.0, 0.0, 0.0),
        ),
    )


def _fixed_root_reset(asset_name: str) -> EventTerm:
    return EventTerm(
        func=mdp.reset_root_state_uniform,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg(asset_name),
            "pose_range": {
                "x": (0.0, 0.0),
                "y": (0.0, 0.0),
                "z": (0.0, 0.0),
                "roll": (0.0, 0.0),
                "pitch": (0.0, 0.0),
                "yaw": (0.0, 0.0),
            },
            "velocity_range": {
                "x": (0.0, 0.0),
                "y": (0.0, 0.0),
                "z": (0.0, 0.0),
                "roll": (0.0, 0.0),
                "pitch": (0.0, 0.0),
                "yaw": (0.0, 0.0),
            },
        },
    )


@configclass
class HanoiSceneCfg(InteractiveSceneCfg):
    """Scene with a Franka Panda, table, pegs, and five movable handled Hanoi rings."""

    robot: ArticulationCfg = MISSING

    table: RigidObjectCfg = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Table",
        spawn=sim_utils.CuboidCfg(
            size=(1.0, 1.5, 0.5),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            physics_material=SURFACE_PHYSICS_MATERIAL,
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.48, 0.46, 0.43), roughness=0.55),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=(0.5, 0.0, 0.35), rot=(1.0, 0.0, 0.0, 0.0)),
    )

    hanoi_base: RigidObjectCfg = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/HanoiBase",
        spawn=sim_utils.CuboidCfg(
            size=BOARD_SIZE,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            physics_material=SURFACE_PHYSICS_MATERIAL,
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.38, 0.25, 0.14), roughness=0.45),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=BOARD_CENTER, rot=(1.0, 0.0, 0.0, 0.0)),
    )

    peg_left: AssetBaseCfg = _peg_cfg("PegLeft", PEG_YS[0])
    peg_middle: AssetBaseCfg = _peg_cfg("PegMiddle", PEG_YS[1])
    peg_right: AssetBaseCfg = _peg_cfg("PegRight", PEG_YS[2])

    ring_xlarge: RigidObjectCfg = _ring_cfg("RingXLarge", z_index=0)
    ring_large: RigidObjectCfg = _ring_cfg("RingLarge", z_index=1)
    ring_medium: RigidObjectCfg = _ring_cfg("RingMedium", z_index=2)
    ring_small: RigidObjectCfg = _ring_cfg("RingSmall", z_index=3)
    ring_xsmall: RigidObjectCfg = _ring_cfg("RingXSmall", z_index=4)

    left_finger_ring_contact: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/Robot/panda_leftfinger",
        update_period=0.0,
        history_length=3,
        debug_vis=False,
        track_contact_points=False,
        track_friction_forces=False,
        filter_prim_paths_expr=RING_FILTER_PRIMS,
    )
    right_finger_ring_contact: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/Robot/panda_rightfinger",
        update_period=0.0,
        history_length=3,
        debug_vis=False,
        track_contact_points=False,
        track_friction_forces=False,
        filter_prim_paths_expr=RING_FILTER_PRIMS,
    )

    plane = AssetBaseCfg(
        prim_path="/World/GroundPlane",
        init_state=AssetBaseCfg.InitialStateCfg(),
        spawn=sim_utils.GroundPlaneCfg(color=(0.52, 0.56, 0.58)),
        collision_group=-1,
    )

    sky_light = AssetBaseCfg(
        prim_path="/World/skyLight",
        spawn=sim_utils.DomeLightCfg(
            intensity=900.0,
            texture_file=f"{ISAAC_NUCLEUS_DIR}/Materials/Textures/Skies/PolyHaven/kloofendal_43d_clear_puresky_4k.hdr",
        ),
    )


@configclass
class HanoiActionsCfg:
    """Joint-space Franka arm control plus binary gripper control."""

    arm_action = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["panda_joint.*"],
        scale=0.5,
        use_default_offset=True,
    )
    gripper_action = mdp.BinaryJointPositionActionCfg(
        asset_name="robot",
        joint_names=["panda_finger.*"],
        open_command_expr={"panda_finger_.*": 0.04},
        close_command_expr={"panda_finger_.*": 0.0},
    )


@configclass
class HanoiObservationsCfg:
    """State observations for the robot and handled Hanoi rings."""

    @configclass
    class StateCfg(ObsGroup):
        actions = ObsTerm(func=mdp.last_action)
        joint_pos = ObsTerm(func=mdp.joint_pos_rel)
        joint_vel = ObsTerm(func=mdp.joint_vel_rel)
        ee_pose = ObsTerm(func=mdp.body_pose_w, params={"asset_cfg": SceneEntityCfg("robot", body_names=["panda_hand"])})
        ring_xlarge_pos = ObsTerm(func=mdp.root_pos_w, params={"asset_cfg": SceneEntityCfg("ring_xlarge")})
        ring_xlarge_quat = ObsTerm(func=mdp.root_quat_w, params={"asset_cfg": SceneEntityCfg("ring_xlarge")})
        ring_large_pos = ObsTerm(func=mdp.root_pos_w, params={"asset_cfg": SceneEntityCfg("ring_large")})
        ring_large_quat = ObsTerm(func=mdp.root_quat_w, params={"asset_cfg": SceneEntityCfg("ring_large")})
        ring_medium_pos = ObsTerm(func=mdp.root_pos_w, params={"asset_cfg": SceneEntityCfg("ring_medium")})
        ring_medium_quat = ObsTerm(func=mdp.root_quat_w, params={"asset_cfg": SceneEntityCfg("ring_medium")})
        ring_small_pos = ObsTerm(func=mdp.root_pos_w, params={"asset_cfg": SceneEntityCfg("ring_small")})
        ring_small_quat = ObsTerm(func=mdp.root_quat_w, params={"asset_cfg": SceneEntityCfg("ring_small")})
        ring_xsmall_pos = ObsTerm(func=mdp.root_pos_w, params={"asset_cfg": SceneEntityCfg("ring_xsmall")})
        ring_xsmall_quat = ObsTerm(func=mdp.root_quat_w, params={"asset_cfg": SceneEntityCfg("ring_xsmall")})

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class HanoiVisionObservationsCfg:
    """Robot-only observations; the environment adapter adds rendered RGB."""

    @configclass
    class PolicyCfg(ObsGroup):
        joint_pos = ObsTerm(func=mdp.joint_pos_rel)
        joint_vel = ObsTerm(func=mdp.joint_vel_rel)
        actions = ObsTerm(func=mdp.last_action)

        def __post_init__(self):
            self.enable_corruption = False
            # Image and proprioception have different ranks and must remain named.
            self.concatenate_terms = False

    policy: PolicyCfg = PolicyCfg()


@configclass
class HanoiEventsCfg:
    """No reset randomization is required for the fixed tabletop Hanoi layout."""

    fingertip_physics_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names="panda_leftfinger|panda_rightfinger"),
            "static_friction_range": [16.0, 16.0],
            "dynamic_friction_range": [12.0, 12.0],
            "restitution_range": [0.0, 0.0],
            "num_buckets": 1,
            "make_consistent": True,
        },
    )
    reset_robot_joints = EventTerm(
        func=mdp.reset_joints_to_init,
        mode="reset",
        params={"asset_cfg": SceneEntityCfg("robot")},
    )
    reset_ring_xlarge = _fixed_root_reset("ring_xlarge")
    reset_ring_large = _fixed_root_reset("ring_large")
    reset_ring_medium = _fixed_root_reset("ring_medium")
    reset_ring_small = _fixed_root_reset("ring_small")
    reset_ring_xsmall = _fixed_root_reset("ring_xsmall")


@configclass
class HanoiEnvFrankaPandaCfg(ManagerBasedEnvCfg):
    """Tower-of-Hanoi tabletop environment with a Franka Panda gripper."""

    viewer: ViewerCfg = ViewerCfg(eye=(1.9, -2.4, 1.55), lookat=(0.28, -0.28, 0.78), origin_type="env")
    scene: HanoiSceneCfg = HanoiSceneCfg(num_envs=1024, env_spacing=2.5, replicate_physics=False)
    observations: HanoiObservationsCfg = HanoiObservationsCfg()
    actions: HanoiActionsCfg = HanoiActionsCfg()
    events: HanoiEventsCfg = HanoiEventsCfg()

    def __post_init__(self):
        robot_cfg = FRANKA_PANDA_HIGH_PD_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        robot_cfg.spawn.rigid_props.disable_gravity = True
        robot_cfg.spawn.activate_contact_sensors = True
        robot_cfg.spawn.articulation_props.fix_root_link = True
        robot_cfg.spawn.articulation_props.solver_position_iteration_count = 64
        robot_cfg.spawn.articulation_props.solver_velocity_iteration_count = 4
        robot_cfg.actuators["panda_hand"].effort_limit_sim = 140.0
        robot_cfg.actuators["panda_hand"].stiffness = 1800.0
        robot_cfg.actuators["panda_hand"].damping = 120.0
        robot_cfg.init_state.pos = (ROBOT_BASE_X, ROBOT_BASE_Y, ROBOT_BASE_Z)
        robot_cfg.init_state.rot = (1.0, 0.0, 0.0, 0.0)
        robot_cfg.init_state.joint_pos = {
            "panda_joint1": 0.78,
            "panda_joint2": -0.78,
            "panda_joint3": 0.0,
            "panda_joint4": -2.35,
            "panda_joint5": 0.0,
            "panda_joint6": 1.57,
            "panda_joint7": 0.78,
            "panda_finger_joint.*": 0.04,
        }
        self.scene.robot = robot_cfg
        self.scene.robot.spawn.semantic_tags = [("class", "robot")]
        self.scene.table.spawn.semantic_tags = [("class", "table")]
        self.scene.hanoi_base.spawn.semantic_tags = [("class", "hanoi_base")]

        self.decimation = 4
        self.sim.dt = 1 / 120
        self.sim.render_interval = self.decimation
        self.sim.physx.bounce_threshold_velocity = 0.01
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_max_rigid_patch_count = 4 * 5 * 2**15


@configclass
class HanoiEnvFrankaPandaCfg_PLAY(HanoiEnvFrankaPandaCfg):
    """Small-scene variant for visualization and interactive editing."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5


@configclass
class HanoiEnvFrankaPandaVisionCfg(HanoiEnvFrankaPandaCfg):
    """Vision-only agent interface with privileged object state removed."""

    scene: HanoiSceneCfg = HanoiSceneCfg(num_envs=1, env_spacing=2.5, replicate_physics=False)
    observations: HanoiVisionObservationsCfg = HanoiVisionObservationsCfg()


@configclass
class HanoiEnvFrankaPandaVisionCfg_PLAY(HanoiEnvFrankaPandaVisionCfg):
    """Single-environment vision configuration for interactive operation."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5
