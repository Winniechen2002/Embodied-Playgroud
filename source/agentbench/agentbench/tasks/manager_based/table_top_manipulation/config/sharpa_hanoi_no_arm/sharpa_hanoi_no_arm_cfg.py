"""Tower of Hanoi with a freely movable right Sharpa Wave hand and no arm."""

import copy
import math

from isaaclab.envs import ManagerBasedEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.utils import configclass

from agentbench.robot_agents.franka_sharpa_right import (
    FLOATING_SHARPA_RIGHT_CFG,
    FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES,
    FLOATING_SHARPA_RIGHT_PALM_BODY_NAME,
)

from ... import mdp
from ..hanoi.hanoi_cfg import (
    BOARD_CENTER,
    BOARD_HEIGHT,
    BOARD_SIZE,
    HanoiEventsCfg,
    HanoiObservationsCfg,
    HanoiVisionObservationsCfg,
    HanoiSceneCfg,
    PEG_HEIGHT,
    PEG_RADIUS,
    PEG_X,
    PEG_YS,
    RING_FILTER_PRIMS,
    RING_HEIGHT,
    RING_MASS,
    RING_Z_GAP,
    TABLE_TOP_Z,
)
from ..sharpa_hanoi.sharpa_hanoi_cfg import SHARPA_FINGER_JOINT_NAMES


FLOATING_TRANSLATION_JOINT_NAMES = [
    "right_x_joint",
    "right_y_joint",
    "right_z_joint",
]
FLOATING_ROTATION_JOINT_NAMES = [
    "right_roll_joint",
    "right_pitch_joint",
    "right_yaw_joint",
]

SCENE_SCALE = 0.5
TABLE_CENTER_X = 0.5
SCALED_BOARD_CENTER_X = TABLE_CENTER_X + (BOARD_CENTER[0] - TABLE_CENTER_X) * SCENE_SCALE
SCALED_BOARD_HEIGHT = BOARD_HEIGHT * SCENE_SCALE
SCALED_BOARD_TOP_Z = TABLE_TOP_Z + SCALED_BOARD_HEIGHT
SCALED_PEG_X = TABLE_CENTER_X + (PEG_X - TABLE_CENTER_X) * SCENE_SCALE
SCALED_PEG_YS = tuple(y * SCENE_SCALE for y in PEG_YS)
SCALED_RING_HEIGHT = RING_HEIGHT * SCENE_SCALE
SCALED_RING_Z_GAP = RING_Z_GAP * SCENE_SCALE
SCALED_RING_BASE_Z = SCALED_BOARD_TOP_Z + SCALED_RING_HEIGHT * 0.5
_BASE_HANOI_SCENE = HanoiSceneCfg(
    num_envs=1, env_spacing=2.5, replicate_physics=False
)


def _scaled_table_cfg():
    cfg = copy.deepcopy(_BASE_HANOI_SCENE.table)
    cfg.spawn.size = tuple(size * SCENE_SCALE for size in cfg.spawn.size)
    # Keep the tabletop at its original world height while reducing its size.
    cfg.init_state.pos = (
        TABLE_CENTER_X,
        0.0,
        TABLE_TOP_Z - cfg.spawn.size[2] * 0.5,
    )
    return cfg


def _scaled_board_cfg():
    cfg = copy.deepcopy(_BASE_HANOI_SCENE.hanoi_base)
    cfg.spawn.size = tuple(size * SCENE_SCALE for size in BOARD_SIZE)
    cfg.init_state.pos = (
        SCALED_BOARD_CENTER_X,
        BOARD_CENTER[1] * SCENE_SCALE,
        TABLE_TOP_Z + SCALED_BOARD_HEIGHT * 0.5,
    )
    return cfg


def _scaled_peg_cfg(attribute_name: str, y: float):
    cfg = copy.deepcopy(getattr(_BASE_HANOI_SCENE, attribute_name))
    cfg.spawn.radius = PEG_RADIUS * SCENE_SCALE
    cfg.spawn.height = PEG_HEIGHT * SCENE_SCALE
    cfg.init_state.pos = (
        SCALED_PEG_X,
        y,
        SCALED_BOARD_TOP_Z + cfg.spawn.height * 0.5,
    )
    return cfg


def _scaled_ring_cfg(attribute_name: str, z_index: int):
    cfg = copy.deepcopy(getattr(_BASE_HANOI_SCENE, attribute_name))
    cfg.spawn.scale = (SCENE_SCALE, SCENE_SCALE, SCENE_SCALE)
    # Preserve density when every linear dimension is halved.
    cfg.spawn.mass_props.mass = RING_MASS * SCENE_SCALE**3
    cfg.init_state.pos = (
        SCALED_PEG_X,
        SCALED_PEG_YS[0],
        SCALED_RING_BASE_Z + z_index * (SCALED_RING_HEIGHT + SCALED_RING_Z_GAP),
    )
    return cfg


@configclass
class SharpaHanoiNoArmSceneCfg(HanoiSceneCfg):
    """Half-scale Hanoi scene with a full-size standalone Sharpa hand."""

    table = _scaled_table_cfg()
    hanoi_base = _scaled_board_cfg()
    peg_left = _scaled_peg_cfg("peg_left", SCALED_PEG_YS[0])
    peg_middle = _scaled_peg_cfg("peg_middle", SCALED_PEG_YS[1])
    peg_right = _scaled_peg_cfg("peg_right", SCALED_PEG_YS[2])
    ring_xlarge = _scaled_ring_cfg("ring_xlarge", 0)
    ring_large = _scaled_ring_cfg("ring_large", 1)
    ring_medium = _scaled_ring_cfg("ring_medium", 2)
    ring_small = _scaled_ring_cfg("ring_small", 3)
    ring_xsmall = _scaled_ring_cfg("ring_xsmall", 4)

    left_finger_ring_contact = None
    right_finger_ring_contact = None

    for fingertip_name in FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES:
        locals()[f"{fingertip_name}_ring_contact"] = ContactSensorCfg(
            prim_path=f"{{ENV_REGEX_NS}}/Robot/{fingertip_name}",
            update_period=0.0,
            history_length=3,
            debug_vis=False,
            track_contact_points=False,
            track_friction_forces=False,
            filter_prim_paths_expr=RING_FILTER_PRIMS,
        )

    del fingertip_name


@configclass
class SharpaHanoiNoArmActionsCfg:
    """Relative 6-DoF palm motion followed by the 22 finger actions."""

    translation_action = mdp.RelativeJointPositionActionCfg(
        asset_name="robot",
        joint_names=FLOATING_TRANSLATION_JOINT_NAMES,
        scale=0.03,
        preserve_order=True,
    )
    rotation_action = mdp.RelativeJointPositionActionCfg(
        asset_name="robot",
        joint_names=FLOATING_ROTATION_JOINT_NAMES,
        scale=0.1,
        preserve_order=True,
    )
    hand_action = mdp.RelativeJointPositionActionCfg(
        asset_name="robot",
        joint_names=SHARPA_FINGER_JOINT_NAMES,
        scale=0.1,
        preserve_order=True,
    )


@configclass
class SharpaHanoiNoArmObservationsCfg(HanoiObservationsCfg):
    """Hanoi state observations using the floating Sharpa palm pose."""

    @configclass
    class StateCfg(HanoiObservationsCfg.StateCfg):
        ee_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={
                "asset_cfg": SceneEntityCfg(
                    "robot", body_names=[FLOATING_SHARPA_RIGHT_PALM_BODY_NAME]
                )
            },
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class SharpaHanoiNoArmEventsCfg(HanoiEventsCfg):
    """Fixed Hanoi resets plus high-friction Sharpa fingertips."""

    fingertip_physics_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg(
                "robot", body_names=FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES
            ),
            "static_friction_range": [16.0, 16.0],
            "dynamic_friction_range": [12.0, 12.0],
            "restitution_range": [0.0, 0.0],
            "num_buckets": 1,
            "make_consistent": True,
        },
    )


@configclass
class SharpaHanoiNoArmEnvCfg(ManagerBasedEnvCfg):
    """Hanoi with a collisionless virtual support carrying only a Sharpa hand."""

    viewer: ViewerCfg = ViewerCfg(
        eye=(1.45, -1.55, 1.30),
        lookat=(0.52, -0.10, 0.75),
        origin_type="env",
    )
    scene: SharpaHanoiNoArmSceneCfg = SharpaHanoiNoArmSceneCfg(
        num_envs=1024, env_spacing=2.5, replicate_physics=False
    )
    observations: SharpaHanoiNoArmObservationsCfg = SharpaHanoiNoArmObservationsCfg()
    actions: SharpaHanoiNoArmActionsCfg = SharpaHanoiNoArmActionsCfg()
    events: SharpaHanoiNoArmEventsCfg = SharpaHanoiNoArmEventsCfg()

    def __post_init__(self):
        robot_cfg = copy.deepcopy(FLOATING_SHARPA_RIGHT_CFG)
        robot_cfg.prim_path = "{ENV_REGEX_NS}/Robot"
        robot_cfg.spawn.rigid_props.disable_gravity = True
        robot_cfg.spawn.activate_contact_sensors = True
        # The base and five virtual intermediate links have no visible or
        # collision geometry. Fixing the root makes the 6-DoF chain an ideal
        # Cartesian pose stage for the standalone hand; it is not a rendered
        # or colliding robot arm.
        robot_cfg.spawn.articulation_props.fix_root_link = True
        robot_cfg.spawn.articulation_props.enabled_self_collisions = False
        robot_cfg.init_state.pos = (SCALED_PEG_X, SCALED_PEG_YS[0], 0.94)
        robot_cfg.init_state.rot = (1.0, 0.0, 0.0, 0.0)
        robot_cfg.init_state.joint_pos.pop("right_(x|y|z)_joint", None)
        robot_cfg.init_state.joint_pos.pop("right_(roll|pitch|yaw)_joint", None)
        robot_cfg.init_state.joint_pos.update(
            {
                "right_x_joint": 0.0,
                "right_y_joint": 0.0,
                "right_z_joint": 0.0,
                # The official mesh extends along local +Z. Turn it downward
                # so the fingers start above the source Hanoi tower.
                "right_roll_joint": math.pi - 1.0e-3,
                "right_pitch_joint": 0.0,
                "right_yaw_joint": 0.0,
            }
        )
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
class SharpaHanoiNoArmEnvCfg_PLAY(SharpaHanoiNoArmEnvCfg):
    """Single-environment variant for visualization and interactive control."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5


@configclass
class SharpaHanoiNoArmVisionEnvCfg(SharpaHanoiNoArmEnvCfg):
    """Floating Sharpa with only RGB and robot proprioception exposed."""

    scene: SharpaHanoiNoArmSceneCfg = SharpaHanoiNoArmSceneCfg(
        num_envs=1, env_spacing=2.5, replicate_physics=False
    )
    observations: HanoiVisionObservationsCfg = HanoiVisionObservationsCfg()


@configclass
class SharpaHanoiNoArmVisionEnvCfg_PLAY(SharpaHanoiNoArmVisionEnvCfg):
    """Single-environment floating-Sharpa vision configuration."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5
