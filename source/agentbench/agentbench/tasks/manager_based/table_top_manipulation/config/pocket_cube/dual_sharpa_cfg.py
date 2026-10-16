"""Two standalone Sharpa Wave hands manipulating a physical 2x2 cube."""

import copy
import math

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
from ..sharpa_hanoi.sharpa_hanoi_cfg import SHARPA_FINGER_JOINT_NAMES
from .pocket_cube_cfg import (
    CUBE_CENTER,
    PocketCubeEnvCfgBase,
    PocketCubeEventsCfg,
    PocketCubeObservationsCfg,
    PocketCubeSceneCfg,
)


FLOATING_TRANSLATION_JOINT_NAMES = ("right_x_joint", "right_y_joint", "right_z_joint")
FLOATING_ROTATION_JOINT_NAMES = ("right_roll_joint", "right_pitch_joint", "right_yaw_joint")


@configclass
class DualSharpaPocketCubeActionsCfg:
    left_translation = mdp.RelativeJointPositionActionCfg(
        asset_name="left_robot",
        joint_names=list(FLOATING_TRANSLATION_JOINT_NAMES),
        scale=0.02,
        preserve_order=True,
    )
    left_rotation = mdp.RelativeJointPositionActionCfg(
        asset_name="left_robot",
        joint_names=list(FLOATING_ROTATION_JOINT_NAMES),
        scale=0.08,
        preserve_order=True,
    )
    left_hand = mdp.RelativeJointPositionActionCfg(
        asset_name="left_robot",
        joint_names=SHARPA_FINGER_JOINT_NAMES,
        scale=0.08,
        preserve_order=True,
    )
    right_translation = mdp.RelativeJointPositionActionCfg(
        asset_name="right_robot",
        joint_names=list(FLOATING_TRANSLATION_JOINT_NAMES),
        scale=0.02,
        preserve_order=True,
    )
    right_rotation = mdp.RelativeJointPositionActionCfg(
        asset_name="right_robot",
        joint_names=list(FLOATING_ROTATION_JOINT_NAMES),
        scale=0.08,
        preserve_order=True,
    )
    right_hand = mdp.RelativeJointPositionActionCfg(
        asset_name="right_robot",
        joint_names=SHARPA_FINGER_JOINT_NAMES,
        scale=0.08,
        preserve_order=True,
    )


@configclass
class DualSharpaPocketCubeObservationsCfg(PocketCubeObservationsCfg):
    @configclass
    class StateCfg(PocketCubeObservationsCfg.StateCfg):
        left_palm_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={
                "asset_cfg": SceneEntityCfg(
                    "left_robot", body_names=[FLOATING_SHARPA_RIGHT_PALM_BODY_NAME]
                )
            },
        )
        right_palm_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={
                "asset_cfg": SceneEntityCfg(
                    "right_robot", body_names=[FLOATING_SHARPA_RIGHT_PALM_BODY_NAME]
                )
            },
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class DualSharpaPocketCubeEventsCfg(PocketCubeEventsCfg):
    left_fingertip_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg(
                "left_robot", body_names=FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES
            ),
            "static_friction_range": (3.0, 3.0),
            "dynamic_friction_range": (2.5, 2.5),
            "restitution_range": (0.0, 0.0),
            "num_buckets": 1,
            "make_consistent": True,
        },
    )
    right_fingertip_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg(
                "right_robot", body_names=FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES
            ),
            "static_friction_range": (3.0, 3.0),
            "dynamic_friction_range": (2.5, 2.5),
            "restitution_range": (0.0, 0.0),
            "num_buckets": 1,
            "make_consistent": True,
        },
    )


@configclass
class DualSharpaPocketCubeSceneCfg(PocketCubeSceneCfg):
    """Sharpa scene with one contact filter per physical corner body."""

    for side in ("left", "right"):
        for fingertip_name in FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES:
            locals()[f"{side}_{fingertip_name}_face_contacts"] = ContactSensorCfg(
                prim_path=f"{{ENV_REGEX_NS}}/{side.title()}Sharpa/{fingertip_name}",
                update_period=0.0,
                history_length=1,
                debug_vis=False,
                track_contact_points=True,
                # Match the current task-wide contact capacity. A compliant
                # fingertip may touch several neighboring scan hulls and can
                # exceed PhysX's four-entry default manifold buffer.
                max_contact_data_count_per_prim=64,
                track_friction_forces=False,
                filter_prim_paths_expr=[
                    f"{{ENV_REGEX_NS}}/PocketCube/Cubies/Cubie_{corner}"
                    for corner in ("urf", "ufl", "ulb", "ubr", "dfr", "dlf", "dbl", "drb")
                ],
            )

    del side, fingertip_name


def _sharpa_hand_cfg(side: str):
    cfg = copy.deepcopy(FLOATING_SHARPA_RIGHT_CFG)
    cfg.prim_path = f"{{ENV_REGEX_NS}}/{side.title()}Sharpa"
    cfg.spawn.activate_contact_sensors = True
    cfg.spawn.rigid_props.disable_gravity = True
    cfg.spawn.articulation_props.fix_root_link = True
    cfg.spawn.articulation_props.enabled_self_collisions = False
    cfg.init_state.pos = (
        CUBE_CENTER[0],
        -0.25 if side == "left" else 0.25,
        # Both stations use the official right-hand asset and face the cube
        # with opposite +/-90-degree rolls. Its asymmetric thumb therefore
        # extends downward on the left and upward on the right. Side-specific
        # mount heights place both complete collision envelopes at the same
        # safe 15 mm clearance above the 0.60 m table.
        CUBE_CENTER[2] + (0.095 if side == "left" else 0.005),
    )
    cfg.init_state.rot = (1.0, 0.0, 0.0, 0.0)
    cfg.init_state.joint_pos.pop("right_(x|y|z)_joint", None)
    cfg.init_state.joint_pos.pop("right_(roll|pitch|yaw)_joint", None)
    cfg.init_state.joint_pos.update(
        {
            "right_x_joint": 0.0,
            "right_y_joint": 0.0,
            "right_z_joint": 0.0,
            # Both assets are the official right hand.  Opposing roll poses
            # make their finger directions face the cube from either side.
            "right_roll_joint": -math.pi / 2 if side == "left" else math.pi / 2,
            "right_pitch_joint": 0.0,
            "right_yaw_joint": 0.0,
        }
    )
    cfg.spawn.semantic_tags = [("class", f"{side}_sharpa_hand")]
    return cfg


@configclass
class DualSharpaPocketCubeEnvCfg(PocketCubeEnvCfgBase):
    scene: DualSharpaPocketCubeSceneCfg = DualSharpaPocketCubeSceneCfg(
        num_envs=64, env_spacing=2.2, replicate_physics=False
    )
    observations: DualSharpaPocketCubeObservationsCfg = DualSharpaPocketCubeObservationsCfg()
    actions: DualSharpaPocketCubeActionsCfg = DualSharpaPocketCubeActionsCfg()
    events: DualSharpaPocketCubeEventsCfg = DualSharpaPocketCubeEventsCfg()

    def __post_init__(self):
        super().__post_init__()
        self.scene.left_robot = _sharpa_hand_cfg("left")
        self.scene.right_robot = _sharpa_hand_cfg("right")
        self.sim.physx.gpu_max_rigid_patch_count = 2**21


@configclass
class DualSharpaPocketCubeEnvCfg_PLAY(DualSharpaPocketCubeEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.2
