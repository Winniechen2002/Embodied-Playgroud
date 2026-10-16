# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for a Franka Research 3 arm with a right Sharpa Wave hand.

The following configurations are available:

* :obj:`FR3_SHARPA_RIGHT_CFG`: Franka Research 3 with Sharpa Hand.
* :obj:`FLOATING_SHARPA_RIGHT_CFG`: Sharpa Hand with a collisionless 6-DoF virtual support.

"""

import math
from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators.actuator_cfg import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.controllers import DifferentialIKControllerCfg
from isaaclab.envs.mdp.actions.actions_cfg import (
    DifferentialInverseKinematicsActionCfg,
    JointPositionActionCfg,
    RelativeJointPositionActionCfg,
)
from isaaclab.utils import configclass

@configclass
class FR3SharpaRightRelJointPosActionCfg:
    action = RelativeJointPositionActionCfg(asset_name="robot", joint_names=[".*"], scale=0.1)


@configclass
class FR3SharpaRightIKPoseRelJointHybridActionsCfg:
    """Hybrid control: IK for arm, joint position for fingers."""

    arm_ik = DifferentialInverseKinematicsActionCfg(
        asset_name="robot",
        joint_names=["panda_joint(1|2|3|4|5|6|7)"],
        body_name="right_hand_C_MC",
        controller=DifferentialIKControllerCfg(
            command_type="pose",
            use_relative_mode=True,
            ik_method="dls",
        ),
        scale=0.01,
    )

    fingers_pos = JointPositionActionCfg(
        asset_name="robot",
        joint_names=[
            "right_index_(MCP_FE|MCP_AA|PIP|DIP)",
            "right_middle_(MCP_FE|MCP_AA|PIP|DIP)",
            "right_ring_(MCP_FE|MCP_AA|PIP|DIP)",
            "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)",
            "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)",
        ],
        use_default_offset=True,
        scale=0.1,
        preserve_order=True,
    )

@configclass 
class FloatingSharpaRightRelJointPosActionCfg:
    translation_action = RelativeJointPositionActionCfg(
        asset_name="robot",
        joint_names=["right_(x|y|z)_joint"],
        scale=0.03,
        preserve_order=True,
    )
    rotation_action = RelativeJointPositionActionCfg(
        asset_name="robot",
        joint_names=["right_(roll|pitch|yaw)_joint"],
        scale=0.1,
        preserve_order=True,
    )
    finger_action = RelativeJointPositionActionCfg(asset_name="robot", joint_names=[
        "right_index_(MCP_FE|MCP_AA|PIP|DIP)",
        "right_middle_(MCP_FE|MCP_AA|PIP|DIP)",
        "right_ring_(MCP_FE|MCP_AA|PIP|DIP)",
        "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)",
        "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)",
    ], scale=0.1, preserve_order=True)

##
# Configuration
##
ASSET_DIR = Path(__file__).parent.parent.resolve()  / "robot_usds"

FR3_SHARPA_RIGHT_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ASSET_DIR}/Sharpa_hand/FR3_Sharpa_right/FR3_Sharpa_right.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            retain_accelerations=True,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1000.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=32,
            solver_velocity_iteration_count=1,
            sleep_threshold=0.005,
            stabilization_threshold=0.0005,
        ),
        joint_drive_props=sim_utils.JointDrivePropertiesCfg(drive_type="force"),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.0),
        rot=(1.0, 0.0, 0.0, 0.0),
        joint_pos={
            "panda_joint1": 0.0,
            "panda_joint2": 0.0,
            "panda_joint3": 0.0,
            "panda_joint4": math.radians(-130.0),
            "panda_joint5": 0.0,
            "panda_joint6": math.radians(180.0),
            "panda_joint7": 0.0,
            "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 0.0,
            "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 0.0,
            "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 0.0,
            "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 0.0,
            "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 0.0,
        },
    ),
    actuators={
        "franka_sharpa_actuators": ImplicitActuatorCfg(
            joint_names_expr=[
                "panda_joint(1|2|3|4|5|6|7)",
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)",
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)",
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)",
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)",
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)",
                
            ],
            effort_limit_sim={
                "panda_joint(1|2|3|4|5|6|7)": 300.0,
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 10.0,
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 10.0,
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 10.0,
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 10.0,
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 10.0,
            },
            stiffness={
                "panda_joint(1|2|3|4|5|6|7)": 6000.0,
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 20.0,
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 20.0,
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 20.0,
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 20.0,
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 20.0,
            },
            damping={
                "panda_joint(1|2|3|4|5|6|7)": 600.0,
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 0.1,
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 0.1,
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 0.1,
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 0.1,
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 0.1,
            },
            friction={
                "panda_joint(1|2|3|4|5|6|7)": 1.0,
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 0.01,
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 0.01,
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 0.01,
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 0.01,
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 0.01,
            },
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)

FLOATING_SHARPA_RIGHT_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=(
            f"{ASSET_DIR}/Sharpa_hand/Floating_Sharpa_right/official_wave_01/"
            "right_sharpa_wave/right_sharpa_wave_with_float_base/"
            "right_sharpa_wave_with_float_base.usd"
        ),
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            retain_accelerations=True,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1000.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=64,
            solver_velocity_iteration_count=4,
            sleep_threshold=0.005,
            stabilization_threshold=0.0005,
        ),
        joint_drive_props=sim_utils.JointDrivePropertiesCfg(drive_type="force"),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.0),
        rot=(1.0, 0.0, 0.0, 0.0),
        joint_pos={
            "right_(x|y|z)_joint": 0.0,
            "right_(roll|pitch|yaw)_joint": 0.0,
            "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 0.0,
            "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 0.0,
            "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 0.0,
            "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 0.0,
            "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 0.0,
        },
    ),
    actuators={
        "floating_sharpa_right_actuators": ImplicitActuatorCfg(
            joint_names_expr=[
                "right_(x|y|z)_joint",
                "right_(roll|pitch|yaw)_joint",
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)",
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)",
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)",
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)",
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)",
            ],
            effort_limit_sim={
                "right_(x|y|z)_joint": 1.0e6,
                "right_(roll|pitch|yaw)_joint": 1.0e6,
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 50.0,
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 50.0,
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 50.0,
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 50.0,
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 50.0,
            },
            stiffness={
                "right_(x|y|z)_joint": 5000.0,
                "right_(roll|pitch|yaw)_joint": 500.0,
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 200.0,
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 200.0,
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 200.0,
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 200.0,
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 200.0,
            },
            damping={
                "right_(x|y|z)_joint": 500.0,
                "right_(roll|pitch|yaw)_joint": 50.0,
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 10.0,
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 10.0,
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 10.0,
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 10.0,
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 10.0,
            },
            friction={
                "right_(x|y|z)_joint": 0.0,
                "right_(roll|pitch|yaw)_joint": 0.0,
                "right_index_(MCP_FE|MCP_AA|PIP|DIP)": 0.01,
                "right_middle_(MCP_FE|MCP_AA|PIP|DIP)": 0.01,
                "right_ring_(MCP_FE|MCP_AA|PIP|DIP)": 0.01,
                "right_pinky_(CMC|MCP_FE|MCP_AA|PIP|DIP)": 0.01,
                "right_thumb_(CMC_FE|CMC_AA|MCP_FE|MCP_AA|IP)": 0.01,
            },
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)

# Robot-specific names from FR3_Sharpa_right.usd.
FR3_SHARPA_RIGHT_PALM_BODY_NAME = "right_hand_C_MC"
FR3_SHARPA_RIGHT_FINGERTIP_BODY_NAMES = [
    "right_thumb_elastomer",
    "right_index_elastomer",
    "right_middle_elastomer",
    "right_ring_elastomer",
    "right_pinky_elastomer",
]
FR3_SHARPA_RIGHT_HAND_TIPS_BODY_NAMES = [FR3_SHARPA_RIGHT_PALM_BODY_NAME] + FR3_SHARPA_RIGHT_FINGERTIP_BODY_NAMES
FR3_SHARPA_RIGHT_WRIST_JOINT_NAME = "panda_joint7"
FR3_SHARPA_RIGHT_ARM_JOINT_NAMES_EXPR = ["panda_joint(1|2|3|4|5|6|7)"]

FLOATING_SHARPA_RIGHT_PALM_BODY_NAME = "right_hand_C_MC"
FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES = [
    "right_thumb_elastomer",
    "right_index_elastomer",
    "right_middle_elastomer",
    "right_ring_elastomer",
    "right_pinky_elastomer",
]
FLOATING_SHARPA_RIGHT_HAND_TIPS_BODY_NAMES = [FLOATING_SHARPA_RIGHT_PALM_BODY_NAME] + FLOATING_SHARPA_RIGHT_FINGERTIP_BODY_NAMES
FLOATING_SHARPA_RIGHT_WRIST_JOINT_NAME = "right_yaw_joint"
FLOATING_SHARPA_RIGHT_ARM_JOINT_NAMES_EXPR = [
    "right_(x|y|z)_joint",
    "right_(roll|pitch|yaw)_joint",
]
