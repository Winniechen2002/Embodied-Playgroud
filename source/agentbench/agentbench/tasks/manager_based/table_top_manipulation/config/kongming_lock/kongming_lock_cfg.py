"""Isaac Lab configuration for two Franka Pandas and a six-piece burr lock."""

from __future__ import annotations

import copy
from pathlib import Path
from dataclasses import MISSING

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg, AssetBaseCfg, RigidObjectCfg
from isaaclab.envs import ManagerBasedEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.utils import configclass
from isaaclab_assets.robots.franka import FRANKA_PANDA_HIGH_PD_CFG
from pxr import UsdGeom

from ... import mdp
from ..tabletop_background_cfg import background_asset_cfg
from ..tabletop_background import initialize_root_pose
from .shapes import CANONICAL_SPEC, PIECE_NAMES, TABLE_TOP_Z
from .lock_mdp import privileged_lock_state
from .evaluation import ROBOT_CONTACT_BODIES
from .gripper_action import ContinuousGripperPositionActionCfg


ROOT = Path(__file__).resolve().parents[5]
ASSET_DIR = ROOT / "assets" / "assets" / "kongming_lock"
TABLE_CENTER = (0.70, 0.0, 0.35)
TABLE_SIZE = (1.65, 1.55, 0.50)
CONTACT_FILTER_PATHS = ([f"{{ENV_REGEX_NS}}/KongmingLock/{name}" for name in PIECE_NAMES]
    + ["{ENV_REGEX_NS}/Table"]
    + [f"{{ENV_REGEX_NS}}/{side}Panda/{body}" for side in ('Left','Right') for body in ROBOT_CONTACT_BODIES])


def spawn_kongming_lock_root(
    prim_path: str,
    cfg: sim_utils.SpawnerCfg,
    translation=None,
    orientation=None,
    **kwargs,
):
    """Create the non-physical Xform parent used by the six rigid pieces."""

    del cfg, kwargs
    stage = sim_utils.get_current_stage()
    root_expression, leaf_name = prim_path.rsplit("/", 1)
    env_roots = sim_utils.find_matching_prim_paths(root_expression)
    if not env_roots:
        raise RuntimeError(f"No environments match Kongming-lock root path: {prim_path}")
    source_prim = None
    for env_root in env_roots:
        root = UsdGeom.Xform.Define(stage, f"{env_root}/{leaf_name}").GetPrim()
        # Isaac Lab's XformPrimView requires this canonical operation stack,
        # including for identity parents that carry no physical body.
        standardize = getattr(sim_utils, "standardize_xform_ops", initialize_root_pose)
        standardize(root, translation=translation, orientation=orientation)
        source_prim = source_prim or root
    assert source_prim is not None
    return source_prim


def _piece_cfg(name: str) -> RigidObjectCfg:
    piece = CANONICAL_SPEC.piece(name)
    return RigidObjectCfg(
        prim_path=f"{{ENV_REGEX_NS}}/KongmingLock/{name}",
        spawn=sim_utils.UsdFileCfg(
            usd_path=str(ASSET_DIR / f"{name}.usda"),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
                linear_damping=0.04,
                angular_damping=0.04,
                max_depenetration_velocity=2.0,
                solver_position_iteration_count=64,
                solver_velocity_iteration_count=8,
            ),
            collision_props=sim_utils.CollisionPropertiesCfg(
                contact_offset=0.0002,
                rest_offset=0.0,
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=piece.assembly_position,
            rot=piece.assembly_quat_wxyz,
        ),
    )


def _panda_cfg(side: str) -> ArticulationCfg:
    cfg = copy.deepcopy(FRANKA_PANDA_HIGH_PD_CFG).replace(
        prim_path=f"{{ENV_REGEX_NS}}/{side.title()}Panda"
    )
    cfg.spawn.rigid_props.disable_gravity = True
    cfg.spawn.activate_contact_sensors = True
    cfg.spawn.articulation_props.fix_root_link = True
    cfg.spawn.articulation_props.solver_position_iteration_count = 64
    cfg.spawn.articulation_props.solver_velocity_iteration_count = 8
    cfg.actuators["panda_hand"].effort_limit_sim = 140.0
    cfg.actuators["panda_hand"].stiffness = 1800.0
    cfg.actuators["panda_hand"].damping = 120.0
    # Both bases approach from the open table edge; the right arm holds the
    # vertical core from -X while the left uses the exposed outer bar ends.
    cfg.init_state.pos = (0.42, -0.34 if side == "left" else 0.34, TABLE_TOP_Z)
    cfg.init_state.rot = (1.0, 0.0, 0.0, 0.0)
    cfg.init_state.joint_pos = {
        "panda_joint1": 0.78 if side == "left" else -0.78,
        "panda_joint2": -0.78,
        "panda_joint3": 0.0,
        "panda_joint4": -2.35,
        "panda_joint5": 0.0,
        # Franka joint 6 has a one-sided lower limit in Isaac Sim 4.5; use the
        # same valid elbow posture for both bases and mirror only the yaw joints.
        "panda_joint6": 1.57,
        "panda_joint7": 0.78 if side == "left" else -0.78,
        "panda_finger_joint.*": 0.04,
    }
    cfg.spawn.semantic_tags = [("class", f"{side}_franka")]
    return cfg


def _fixed_root_reset(asset_name: str) -> EventTerm:
    return EventTerm(
        func=mdp.reset_root_state_uniform,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg(asset_name),
            "pose_range": {key: (0.0, 0.0) for key in ("x", "y", "z", "roll", "pitch", "yaw")},
            "velocity_range": {key: (0.0, 0.0) for key in ("x", "y", "z", "roll", "pitch", "yaw")},
        },
    )


@configclass
class KongmingLockSceneCfg(InteractiveSceneCfg):
    """Table, two fixed Pandas, six free pieces, and bilateral sensors."""

    left_robot: ArticulationCfg = MISSING
    right_robot: ArticulationCfg = MISSING
    kongming_lock_root: AssetBaseCfg = AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/KongmingLock",
        spawn=sim_utils.SpawnerCfg(func=spawn_kongming_lock_root, visible=False),
    )
    background: AssetBaseCfg | None = background_asset_cfg("workshop", TABLE_CENTER, TABLE_SIZE)
    table: RigidObjectCfg = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Table",
        spawn=sim_utils.CuboidCfg(
            size=TABLE_SIZE,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
            collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.0002, rest_offset=0.0),
            # A wooden lock needs a high-friction tabletop so the vertical
            # bars can settle on their finite 2x2 end faces without a hidden
            # constraint or attachment.
            physics_material=sim_utils.RigidBodyMaterialCfg(static_friction=4.0, dynamic_friction=3.0),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.38, 0.36, 0.33), roughness=0.58),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=TABLE_CENTER, rot=(1.0, 0.0, 0.0, 0.0)),
    )
    plane = AssetBaseCfg(
        prim_path="/World/GroundPlane",
        init_state=AssetBaseCfg.InitialStateCfg(),
        spawn=sim_utils.GroundPlaneCfg(color=(0.52, 0.56, 0.58), visible=False),
        collision_group=-1,
    )
    sky_light = AssetBaseCfg(
        prim_path="/World/skyLight",
        spawn=sim_utils.DomeLightCfg(intensity=900.0, color=(1.0, 1.0, 1.0)),
    )

    piece_frame_x0: RigidObjectCfg = _piece_cfg("frame_x0")
    piece_frame_x1: RigidObjectCfg = _piece_cfg("frame_x1")
    piece_frame_y0: RigidObjectCfg = _piece_cfg("frame_y0")
    piece_frame_y1: RigidObjectCfg = _piece_cfg("frame_y1")
    piece_frame_z0: RigidObjectCfg = _piece_cfg("frame_z0")
    piece_key: RigidObjectCfg = _piece_cfg("key")

    left_finger_piece_contact: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/LeftPanda/panda_leftfinger",
        update_period=0.0,
        history_length=3,
        debug_vis=False,
        track_contact_points=True,
        max_contact_data_count_per_prim=64,
        filter_prim_paths_expr=CONTACT_FILTER_PATHS,
    )
    right_finger_piece_contact: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/RightPanda/panda_leftfinger",
        update_period=0.0,
        history_length=3,
        debug_vis=False,
        track_contact_points=True,
        max_contact_data_count_per_prim=64,
        filter_prim_paths_expr=CONTACT_FILTER_PATHS,
    )

    left_other_finger_piece_contact: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/LeftPanda/panda_rightfinger", update_period=0., history_length=3,
        filter_prim_paths_expr=CONTACT_FILTER_PATHS)
    right_other_finger_piece_contact: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/RightPanda/panda_rightfinger", update_period=0., history_length=3,
        filter_prim_paths_expr=CONTACT_FILTER_PATHS)

    left_arm_contacts: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/LeftPanda/panda_(link[1-7]|hand)", update_period=0.,history_length=3)
    right_arm_contacts: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/RightPanda/panda_(link[1-7]|hand)", update_period=0.,history_length=3)


@configclass
class KongmingLockActionsCfg:
    """Seven Panda joint positions and one binary gripper per arm."""

    left_arm = mdp.JointPositionActionCfg(
        asset_name="left_robot", joint_names=["panda_joint.*"], scale=0.5, use_default_offset=True
    )
    left_gripper = mdp.BinaryJointPositionActionCfg(
        asset_name="left_robot", joint_names=["panda_finger.*"],
        open_command_expr={"panda_finger_.*": 0.04}, close_command_expr={"panda_finger_.*": 0.0}
    )
    right_arm = mdp.JointPositionActionCfg(
        asset_name="right_robot", joint_names=["panda_joint.*"], scale=0.5, use_default_offset=True
    )
    right_gripper = mdp.BinaryJointPositionActionCfg(
        asset_name="right_robot", joint_names=["panda_finger.*"],
        open_command_expr={"panda_finger_.*": 0.04}, close_command_expr={"panda_finger_.*": 0.0}
    )


@configclass
class KongmingLockObservationsCfg:
    @configclass
    class StateCfg(ObsGroup):
        left_joint_pos = ObsTerm(func=mdp.joint_pos_rel, params={"asset_cfg": SceneEntityCfg("left_robot")})
        left_joint_vel = ObsTerm(func=mdp.joint_vel_rel, params={"asset_cfg": SceneEntityCfg("left_robot")})
        right_joint_pos = ObsTerm(func=mdp.joint_pos_rel, params={"asset_cfg": SceneEntityCfg("right_robot")})
        right_joint_vel = ObsTerm(func=mdp.joint_vel_rel, params={"asset_cfg": SceneEntityCfg("right_robot")})
        privileged_state = ObsTerm(func=privileged_lock_state)

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class KongmingLockEventsCfg:
    reset_left_robot = _fixed_root_reset("left_robot")
    reset_right_robot = _fixed_root_reset("right_robot")
    reset_left_joints = EventTerm(func=mdp.reset_joints_by_offset, mode="reset", params={
        "asset_cfg": SceneEntityCfg("left_robot"), "position_range": (0.0, 0.0), "velocity_range": (0.0, 0.0)})
    reset_right_joints = EventTerm(func=mdp.reset_joints_by_offset, mode="reset", params={
        "asset_cfg": SceneEntityCfg("right_robot"), "position_range": (0.0, 0.0), "velocity_range": (0.0, 0.0)})
    reset_frame_x0 = _fixed_root_reset("piece_frame_x0")
    reset_frame_x1 = _fixed_root_reset("piece_frame_x1")
    reset_frame_y0 = _fixed_root_reset("piece_frame_y0")
    reset_frame_y1 = _fixed_root_reset("piece_frame_y1")
    reset_frame_z0 = _fixed_root_reset("piece_frame_z0")
    reset_key = _fixed_root_reset("piece_key")


@configclass
class KongmingLockEnvCfg(ManagerBasedEnvCfg):
    """Canonical fixed-state dual-Franka disassembly environment."""

    viewer: ViewerCfg = ViewerCfg(eye=(1.75, -2.05, 1.55), lookat=(0.68, 0.0, 0.72), origin_type="env")
    scene: KongmingLockSceneCfg = KongmingLockSceneCfg(num_envs=1, env_spacing=2.3, replicate_physics=False)
    observations: KongmingLockObservationsCfg = KongmingLockObservationsCfg()
    actions: KongmingLockActionsCfg = KongmingLockActionsCfg()
    events: KongmingLockEventsCfg = KongmingLockEventsCfg()

    def __post_init__(self):
        self.scene.left_robot = _panda_cfg("left")
        self.scene.right_robot = _panda_cfg("right")
        self.seed = 0
        self.decimation = 4
        self.sim.dt = 1 / 120
        self.sim.render_interval = self.decimation
        self.sim.physx.bounce_threshold_velocity = 0.01
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_max_rigid_patch_count = 2**20


@configclass
class KongmingLockEnvCfg_PLAY(KongmingLockEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.3


@configclass
class KongmingLockEnvCfg_ASSEMBLE(KongmingLockEnvCfg):
    """Six separate parked poses, without modifying the disassembly config."""

    def __post_init__(self):
        super().__post_init__()
        self.actions = copy.deepcopy(self.actions)
        for side in ('left', 'right'):
            setattr(self.actions, side + '_gripper', ContinuousGripperPositionActionCfg(
                asset_name=side + '_robot', joint_names=['panda_finger.*'],
                open_command_expr={'panda_finger_.*': .04},
                close_command_expr={'panda_finger_.*': 0.}))
        # Gentle support avoids core/table contact jitter (~10 N per pad).
        # The moving left hand retains the validated disassembly drive:
        # its end grasp must resist gravity torque on horizontal bars.
        # With the softer drive, native lower-Y lifting slipped by 26 degrees.
        hand = self.scene.right_robot.actuators['panda_hand']
        hand.stiffness = 400.0
        hand.damping = 80.0
        hand.effort_limit_sim = 40.0
        for piece in CANONICAL_SPEC.pieces:
            cfg = getattr(self.scene, 'piece_' + piece.name)
            cfg = copy.deepcopy(cfg)
            setattr(self.scene, 'piece_' + piece.name, cfg)
            cfg.init_state.pos = piece.target_position
            cfg.init_state.rot = piece.target_quat_wxyz


@configclass
class KongmingLockEnvCfg_ASSEMBLE_PLAY(KongmingLockEnvCfg_ASSEMBLE):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.3


__all__ = ["KongmingLockEnvCfg", "KongmingLockEnvCfg_PLAY", "KongmingLockEnvCfg_ASSEMBLE",
           "KongmingLockEnvCfg_ASSEMBLE_PLAY", "KongmingLockSceneCfg"]
