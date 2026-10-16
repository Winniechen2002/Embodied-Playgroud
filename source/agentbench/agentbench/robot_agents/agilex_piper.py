"""AgileX Piper follower-arm configuration for the Songling ALOHA task."""

from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg


ROBOT_URDF_DIR = Path(__file__).resolve().parents[1] / "robot_urdfs"
AGILEX_PIPER_ARM_JOINT_NAMES = tuple(f"joint{index}" for index in range(1, 7))
AGILEX_PIPER_GRIPPER_JOINT_NAMES = ("gripper_joint1", "gripper_joint2")
AGILEX_PIPER_GRIPPER_BODY_NAMES = ("gripper_link1", "gripper_link2")
AGILEX_PIPER_EE_BODY_NAME = "gripper_base"


AGILEX_PIPER_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=str(
            ROBOT_URDF_DIR
            / "agilex_piper"
            / "urdf"
            / "piper_with_gripper_description.urdf"
        ),
        fix_base=True,
        merge_fixed_joints=False,
        make_instanceable=False,
        activate_contact_sensors=True,
        self_collision=False,
        convert_mimic_joints_to_normal_joints=False,
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            drive_type="force",
            target_type="position",
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(
                stiffness=0.0,
                damping=0.0,
            ),
        ),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=True,
            max_linear_velocity=20.0,
            max_angular_velocity=30.0,
            max_depenetration_velocity=2.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=32,
            solver_velocity_iteration_count=4,
            sleep_threshold=0.005,
            stabilization_threshold=0.0005,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.0),
        rot=(1.0, 0.0, 0.0, 0.0),
        joint_pos={
            "joint1": 0.0,
            "joint2": 2.52,
            "joint3": -1.87,
            "joint4": 0.0,
            "joint5": 0.0,
            "joint6": 0.0,
            "gripper_joint1": 0.04,
            "gripper_joint2": -0.04,
        },
    ),
    actuators={
        "piper_arm": ImplicitActuatorCfg(
            joint_names_expr=list(AGILEX_PIPER_ARM_JOINT_NAMES),
            effort_limit_sim=100.0,
            velocity_limit_sim=5.0,
            stiffness=120.0,
            damping=12.0,
            friction=0.02,
        ),
        "piper_gripper": ImplicitActuatorCfg(
            joint_names_expr=list(AGILEX_PIPER_GRIPPER_JOINT_NAMES),
            effort_limit_sim=10.0,
            velocity_limit_sim=1.0,
            stiffness=500.0,
            damping=25.0,
            friction=0.05,
        ),
    },
    soft_joint_pos_limit_factor=0.98,
)
