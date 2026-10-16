"""Dual Floating Sharpa configuration for the Kongming-lock task.

Both hands use the official right-hand asset.  The virtual six-DoF roots are
fixed to the world, so the public action is a pair of absolute native joint
targets rather than a hidden teleport or Cartesian shortcut.
"""

from __future__ import annotations

import copy

from isaaclab.envs import ManagerBasedEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.utils import configclass

from agentbench.robot_agents.franka_sharpa_right import (
    FLOATING_SHARPA_RIGHT_CFG,
    FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES,
    FLOATING_SHARPA_RIGHT_PALM_BODY_NAME,
)
from agentbench.sharpa_joint_names import SHARPA_FINGER_JOINT_NAMES, SHARPA_MOTION_JOINT_NAMES

from ... import mdp
from .sharpa_calibration import NON_PAD_BODIES, PRESET
from .kongming_lock_cfg import (
    KongmingLockSceneCfg,
    KongmingLockEventsCfg,
    CONTACT_FILTER_PATHS,
    _fixed_root_reset,
)


KONGMING_SHARPA_SENSOR_NAMES = tuple(
    f"{{side}}_{name}_kongming_contact" for name in FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES
)
KONGMING_SHARPA_ACTION_NAMES = tuple(SHARPA_MOTION_JOINT_NAMES) + tuple(SHARPA_FINGER_JOINT_NAMES)


def _sharpa_contact_filters(side: str):
    other = "right" if side == "left" else "left"
    return list(CONTACT_FILTER_PATHS[:6]) + [
        "{ENV_REGEX_NS}/Table",
        f"{{ENV_REGEX_NS}}/{other.title()}Sharpa/{FLOATING_SHARPA_RIGHT_PALM_BODY_NAME}",
        *[f"{{ENV_REGEX_NS}}/{other.title()}Sharpa/{name}"
          for name in FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES],
    ]


@configclass
class KongmingDualSharpaSceneCfg(KongmingLockSceneCfg):
    """Six pieces, tabletop and two independently controlled Sharpa hands."""

    # The inherited Panda-specific sensors are deliberately disabled.  Native
    # evidence is collected from the five elastomer bodies on each hand.
    left_finger_piece_contact = None
    right_finger_piece_contact = None
    left_other_finger_piece_contact = None
    right_other_finger_piece_contact = None
    left_arm_contacts = None
    right_arm_contacts = None

    for side in ("left", "right"):
        locals()[f"{side}_body_kongming_contact"] = ContactSensorCfg(
            prim_path=f"{{ENV_REGEX_NS}}/{side.title()}Sharpa/("+'|'.join(NON_PAD_BODIES)+')',
            update_period=0.0, history_length=3, debug_vis=False,
        )
        locals()[f"{side}_palm_kongming_contact"] = ContactSensorCfg(
            prim_path=f"{{ENV_REGEX_NS}}/{side.title()}Sharpa/{FLOATING_SHARPA_RIGHT_PALM_BODY_NAME}",
            update_period=0.0,
            history_length=3,
            debug_vis=False,
            track_contact_points=False,
            filter_prim_paths_expr=_sharpa_contact_filters(side),
        )
        for fingertip in FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES:
            locals()[f"{side}_{fingertip}_kongming_contact"] = ContactSensorCfg(
                prim_path=f"{{ENV_REGEX_NS}}/{side.title()}Sharpa/{fingertip}",
                update_period=0.0,
                history_length=3,
                debug_vis=False,
                track_contact_points=False,
                filter_prim_paths_expr=_sharpa_contact_filters(side),
            )
    del side, fingertip


@configclass
class KongmingDualSharpaActionsCfg:
    """Two 28-D blocks: six floating-base targets and 22 finger targets."""

    left_motion = mdp.JointPositionActionCfg(
        asset_name="left_robot", joint_names=list(SHARPA_MOTION_JOINT_NAMES),
        scale=1.0, use_default_offset=False, preserve_order=True,
    )
    left_fingers = mdp.JointPositionActionCfg(
        asset_name="left_robot", joint_names=list(SHARPA_FINGER_JOINT_NAMES),
        scale=1.0, use_default_offset=False, preserve_order=True,
    )
    right_motion = mdp.JointPositionActionCfg(
        asset_name="right_robot", joint_names=list(SHARPA_MOTION_JOINT_NAMES),
        scale=1.0, use_default_offset=False, preserve_order=True,
    )
    right_fingers = mdp.JointPositionActionCfg(
        asset_name="right_robot", joint_names=list(SHARPA_FINGER_JOINT_NAMES),
        scale=1.0, use_default_offset=False, preserve_order=True,
    )


@configclass
class KongmingDualSharpaObservationsCfg:
    @configclass
    class StateCfg(ObsGroup):
        left_joint_pos = ObsTerm(func=mdp.joint_pos_rel, params={"asset_cfg": SceneEntityCfg("left_robot")})
        left_joint_vel = ObsTerm(func=mdp.joint_vel_rel, params={"asset_cfg": SceneEntityCfg("left_robot")})
        right_joint_pos = ObsTerm(func=mdp.joint_pos_rel, params={"asset_cfg": SceneEntityCfg("right_robot")})
        right_joint_vel = ObsTerm(func=mdp.joint_vel_rel, params={"asset_cfg": SceneEntityCfg("right_robot")})
        left_palm_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={"asset_cfg": SceneEntityCfg("left_robot", body_names=[FLOATING_SHARPA_RIGHT_PALM_BODY_NAME])},
        )
        right_palm_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={"asset_cfg": SceneEntityCfg("right_robot", body_names=[FLOATING_SHARPA_RIGHT_PALM_BODY_NAME])},
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class KongmingDualSharpaEventsCfg(KongmingLockEventsCfg):
    """Fixed reset plus deterministic high-friction elastomer contacts."""

    reset_left_robot = _fixed_root_reset("left_robot")
    reset_right_robot = _fixed_root_reset("right_robot")
    reset_left_joints = EventTerm(func=mdp.reset_joints_by_offset, mode="reset", params={
        "asset_cfg": SceneEntityCfg("left_robot"), "position_range": (0.0, 0.0), "velocity_range": (0.0, 0.0)})
    reset_right_joints = EventTerm(func=mdp.reset_joints_by_offset, mode="reset", params={
        "asset_cfg": SceneEntityCfg("right_robot"), "position_range": (0.0, 0.0), "velocity_range": (0.0, 0.0)})

    left_fingertip_material = EventTerm(
        func=mdp.randomize_rigid_body_material, mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("left_robot", body_names=list(FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES)),
            "static_friction_range": (3.0, 3.0), "dynamic_friction_range": (2.5, 2.5),
            "restitution_range": (0.0, 0.0), "num_buckets": 1, "make_consistent": True,
        },
    )
    right_fingertip_material = EventTerm(
        func=mdp.randomize_rigid_body_material, mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("right_robot", body_names=list(FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES)),
            "static_friction_range": (3.0, 3.0), "dynamic_friction_range": (2.5, 2.5),
            "restitution_range": (0.0, 0.0), "num_buckets": 1, "make_consistent": True,
        },
    )


def _sharpa_cfg(side: str):
    cfg = copy.deepcopy(FLOATING_SHARPA_RIGHT_CFG)
    cfg.prim_path = f"{{ENV_REGEX_NS}}/{side.title()}Sharpa"
    cfg.spawn.activate_contact_sensors = True
    cfg.spawn.rigid_props.disable_gravity = True
    cfg.spawn.articulation_props.fix_root_link = True
    cfg.spawn.articulation_props.enabled_self_collisions = False
    # Side-separated nominal mount.  The native preflight verifies fingertip
    # clearance before a case is accepted; the virtual base remains fixed.
    mount = PRESET['mounts'][side]
    cfg.init_state.pos = tuple(mount['position'])
    cfg.init_state.rot = tuple(mount['quaternion'])
    cfg.init_state.joint_pos.pop("right_(x|y|z)_joint", None)
    cfg.init_state.joint_pos.pop("right_(roll|pitch|yaw)_joint", None)
    cfg.init_state.joint_pos.update({
        "right_x_joint": 0.0,
        "right_y_joint": 0.0,
        "right_z_joint": 0.0,
        "right_roll_joint": mount['root_angles'][0],
        "right_pitch_joint": mount['root_angles'][1],
        "right_yaw_joint": mount['root_angles'][2],
    })
    actuator = cfg.actuators["floating_sharpa_right_actuators"]
    for expression in actuator.stiffness:
        if any(f"right_{finger}_" in expression for finger in ("index", "middle", "ring", "pinky", "thumb")):
            actuator.stiffness[expression] = 400.0
    cfg.spawn.semantic_tags = [("class", f"{side}_floating_sharpa")]
    return cfg


@configclass
class KongmingDualSharpaEnvCfg(ManagerBasedEnvCfg):
    embodiment = "dual-floating-sharpa"
    viewer: ViewerCfg = ViewerCfg(eye=(1.75, -2.05, 1.55), lookat=(0.68, 0.0, 0.72), origin_type="env")
    scene: KongmingDualSharpaSceneCfg = KongmingDualSharpaSceneCfg(num_envs=1, env_spacing=2.3, replicate_physics=False)
    observations: KongmingDualSharpaObservationsCfg = KongmingDualSharpaObservationsCfg()
    actions: KongmingDualSharpaActionsCfg = KongmingDualSharpaActionsCfg()
    events: KongmingDualSharpaEventsCfg = KongmingDualSharpaEventsCfg()

    def __post_init__(self):
        self.scene.left_robot = _sharpa_cfg("left")
        self.scene.right_robot = _sharpa_cfg("right")
        self.scene.table.spawn.semantic_tags = [("class", "table")]
        self.seed = 0
        self.decimation = 4
        self.sim.dt = 1 / 120
        self.sim.render_interval = self.decimation
        self.sim.physx.solver_type = 0  # PGS; retain the piece asset's 64/8 iterations.
        self.sim.physx.bounce_threshold_velocity = 0.01
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_max_rigid_patch_count = 4 * 5 * 2**15


@configclass
class KongmingDualSharpaEnvCfg_PLAY(KongmingDualSharpaEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.3


@configclass
class KongmingDualSharpaEnvCfg_ASSEMBLE(KongmingDualSharpaEnvCfg):
    pass


@configclass
class KongmingDualSharpaEnvCfg_ASSEMBLE_PLAY(KongmingDualSharpaEnvCfg_PLAY):
    pass


__all__ = [
    "KongmingDualSharpaEnvCfg", "KongmingDualSharpaEnvCfg_PLAY",
    "KongmingDualSharpaEnvCfg_ASSEMBLE", "KongmingDualSharpaEnvCfg_ASSEMBLE_PLAY",
]
