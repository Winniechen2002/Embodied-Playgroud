"""Tower-of-Hanoi environment with a Franka FR3 arm and a right Sharpa Hand."""

import copy

from isaaclab.envs import ManagerBasedEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.utils import configclass

from agentbench.robot_agents.franka_sharpa_right import (
    FR3_SHARPA_RIGHT_CFG,
    FR3_SHARPA_RIGHT_FINGERTIP_BODY_NAMES,
    FR3_SHARPA_RIGHT_PALM_BODY_NAME,
)

from ... import mdp
from ..hanoi.hanoi_cfg import (
    HanoiEventsCfg,
    HanoiObservationsCfg,
    HanoiVisionObservationsCfg,
    HanoiSceneCfg,
    RING_FILTER_PRIMS,
    ROBOT_BASE_X,
    ROBOT_BASE_Y,
    ROBOT_BASE_Z,
)


SHARPA_FINGER_JOINT_NAMES = [
    "right_index_MCP_FE",
    "right_index_MCP_AA",
    "right_index_PIP",
    "right_index_DIP",
    "right_middle_MCP_FE",
    "right_middle_MCP_AA",
    "right_middle_PIP",
    "right_middle_DIP",
    "right_ring_MCP_FE",
    "right_ring_MCP_AA",
    "right_ring_PIP",
    "right_ring_DIP",
    "right_pinky_CMC",
    "right_pinky_MCP_FE",
    "right_pinky_MCP_AA",
    "right_pinky_PIP",
    "right_pinky_DIP",
    "right_thumb_CMC_FE",
    "right_thumb_CMC_AA",
    "right_thumb_MCP_FE",
    "right_thumb_MCP_AA",
    "right_thumb_IP",
]


@configclass
class SharpaHanoiSceneCfg(HanoiSceneCfg):
    """The unchanged Hanoi scene with Sharpa fingertip contact sensors."""

    # These Panda-gripper sensors are inherited from HanoiSceneCfg and do not
    # exist on the Sharpa robot.
    left_finger_ring_contact = None
    right_finger_ring_contact = None

    for fingertip_name in FR3_SHARPA_RIGHT_FINGERTIP_BODY_NAMES:
        locals()[f"{fingertip_name}_ring_contact"] = ContactSensorCfg(
            prim_path=f"{{ENV_REGEX_NS}}/Robot/sharpa_hand/{fingertip_name}",
            update_period=0.0,
            history_length=3,
            debug_vis=False,
            track_contact_points=False,
            track_friction_forces=False,
            filter_prim_paths_expr=RING_FILTER_PRIMS,
        )

    del fingertip_name


@configclass
class SharpaHanoiActionsCfg:
    """Joint-position control for the Franka arm and all Sharpa fingers."""

    arm_action = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["panda_joint(1|2|3|4|5|6|7)"],
        scale=0.5,
        use_default_offset=True,
    )
    hand_action = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=SHARPA_FINGER_JOINT_NAMES,
        scale=0.1,
        use_default_offset=True,
        preserve_order=True,
    )


@configclass
class SharpaHanoiObservationsCfg(HanoiObservationsCfg):
    """Hanoi state observations using the Sharpa palm as the end effector."""

    @configclass
    class StateCfg(HanoiObservationsCfg.StateCfg):
        ee_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={"asset_cfg": SceneEntityCfg("robot", body_names=[FR3_SHARPA_RIGHT_PALM_BODY_NAME])},
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class SharpaHanoiEventsCfg(HanoiEventsCfg):
    """Fixed Hanoi resets plus high-friction Sharpa fingertips."""

    fingertip_physics_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg(
                "robot", body_names=FR3_SHARPA_RIGHT_FINGERTIP_BODY_NAMES
            ),
            "static_friction_range": [16.0, 16.0],
            "dynamic_friction_range": [12.0, 12.0],
            "restitution_range": [0.0, 0.0],
            "num_buckets": 1,
            "make_consistent": True,
        },
    )


@configclass
class SharpaHanoiEnvCfg(ManagerBasedEnvCfg):
    """Tower-of-Hanoi environment with a Franka FR3 and right Sharpa Hand."""

    viewer: ViewerCfg = ViewerCfg(eye=(1.9, -2.4, 1.55), lookat=(0.28, -0.28, 0.78), origin_type="env")
    scene: SharpaHanoiSceneCfg = SharpaHanoiSceneCfg(num_envs=1024, env_spacing=2.5, replicate_physics=False)
    observations: SharpaHanoiObservationsCfg = SharpaHanoiObservationsCfg()
    actions: SharpaHanoiActionsCfg = SharpaHanoiActionsCfg()
    events: SharpaHanoiEventsCfg = SharpaHanoiEventsCfg()

    def __post_init__(self):
        robot_cfg = copy.deepcopy(FR3_SHARPA_RIGHT_CFG)
        robot_cfg.prim_path = "{ENV_REGEX_NS}/Robot"
        robot_cfg.spawn.rigid_props.disable_gravity = True
        robot_cfg.spawn.activate_contact_sensors = True
        robot_cfg.spawn.articulation_props.fix_root_link = True
        # The fixed Sharpa mount and FR3 link-7 collision meshes overlap in
        # the composed asset.  Whole-robot self-collision turns that overlap
        # into an explosive impulse on the first controlled physics step.
        # External hand/ring collisions remain enabled and are still physical.
        robot_cfg.spawn.articulation_props.enabled_self_collisions = False
        robot_cfg.spawn.articulation_props.solver_position_iteration_count = 64
        robot_cfg.spawn.articulation_props.solver_velocity_iteration_count = 4
        # The source Sharpa bundle uses 6000/600 for every FR3 joint, which is
        # numerically unstable at this environment's 120 Hz physics step and
        # can fold the arm into the Hanoi tower even for a small target change.
        # Match Isaac Lab's established gravity-free high-PD Franka gains.
        sharpa_actuator = robot_cfg.actuators["franka_sharpa_actuators"]
        arm_pattern = "panda_joint(1|2|3|4|5|6|7)"
        sharpa_actuator.stiffness.pop(arm_pattern, None)
        sharpa_actuator.damping.pop(arm_pattern, None)
        sharpa_actuator.effort_limit_sim.pop(arm_pattern, None)
        sharpa_actuator.stiffness.update(
            {"panda_joint[1-4]": 400.0, "panda_joint[5-7]": 400.0}
        )
        sharpa_actuator.damping.update(
            {"panda_joint[1-4]": 80.0, "panda_joint[5-7]": 80.0}
        )
        sharpa_actuator.effort_limit_sim.update(
            {"panda_joint[1-4]": 87.0, "panda_joint[5-7]": 12.0}
        )
        for joint_pattern in tuple(sharpa_actuator.stiffness):
            if "panda_joint" not in joint_pattern:
                sharpa_actuator.stiffness[joint_pattern] = 200.0
                sharpa_actuator.damping[joint_pattern] = 10.0
                sharpa_actuator.effort_limit_sim[joint_pattern] = 50.0
        robot_cfg.init_state.pos = (ROBOT_BASE_X, ROBOT_BASE_Y, ROBOT_BASE_Z)
        robot_cfg.init_state.rot = (1.0, 0.0, 0.0, 0.0)
        robot_cfg.init_state.joint_pos.update(
            {
                "panda_joint1": 0.78,
                "panda_joint2": -0.78,
                "panda_joint3": 0.0,
                "panda_joint4": -2.35,
                "panda_joint5": 0.0,
                "panda_joint6": 1.57,
                "panda_joint7": 0.78,
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
class SharpaHanoiEnvCfg_PLAY(SharpaHanoiEnvCfg):
    """Single-environment variant for visualization and interactive control."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5


@configclass
class SharpaHanoiVisionEnvCfg(SharpaHanoiEnvCfg):
    """Sharpa Hanoi with only RGB and robot proprioception exposed."""

    scene: SharpaHanoiSceneCfg = SharpaHanoiSceneCfg(
        num_envs=1, env_spacing=2.5, replicate_physics=False
    )
    observations: HanoiVisionObservationsCfg = HanoiVisionObservationsCfg()


@configclass
class SharpaHanoiVisionEnvCfg_PLAY(SharpaHanoiVisionEnvCfg):
    """Single-environment Sharpa vision configuration."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5
