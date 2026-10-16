# ManiSkill 几何任务

[Protocol](../evaluation_protocol.zh-CN.md) · [Index](index.zh-CN.md) · [JSON](tasks.json)

Embodied Playground 论文仅评测发射器 loaded 初态：完整 410 项为 410 组／1640 条件，EP-100 为 100 组／400 条件。本运行时清单另保留 ground，共 510 组／2040 条件。[EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.zh-CN.md)

下列每项每组四次，base seed 为 0。参数为维护者私有输入。目标字符串与字段名保留作者配置原文，不作为翻译后的协议正文。

<a id="maniskill_geometry-panda-P1"></a>
## `maniskill_geometry/panda/P1`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 8; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"bottom": 0.87, "half": [0.022, 0.022], "object": "round_peg", "support": "socket_board", "tolerance": 0.005, "type": "region", "xy": [0.04, 0.27]}, {"axis": [0, 0, 1], "object": "round_peg", "tolerance": 3, "type": "orientation", "world": [0, 0, 1]}, {"bottom": 0.87, "half": [0.022, 0.022], "object": "square_peg", "support": "socket_board", "tolerance": 0.005, "type": "region", "xy": [0.25, 0.27]}, {"axis": [0, 0, 1], "object": "square_peg", "tolerance": 3, "type": "orientation", "world": [0, 0, 1]}, {"bottom": 0.947, "half": [0.02, 0.055], "object": "long_peg", "tolerance": 0.006, "type": "region", "xy": [0.43, 0.302]}, {"axis": [0, 0, 1], "object": "long_peg", "tolerance": 3, "type": "orientation", "world": [0, -1, 0]}], "instruction": "Insert the round and square pegs into their matching top sockets and the long peg into the front-facing socket. Seat each fully without moving the board.", "milestones": [{"conditions": [{"bottom": 0.87, "half": [0.022, 0.022], "object": "round_peg", "support": "socket_board", "tolerance": 0.005, "type": "region", "xy": [0.04, 0.27]}, {"axis": [0, 0, 1], "object": "round_peg", "tolerance": 3, "type": "orientation", "world": [0, 0, 1]}, {"bottom": 0.87, "half": [0.022, 0.022], "object": "square_peg", "support": "socket_board", "tolerance": 0.005, "type": "region", "xy": [0.25, 0.27]}, {"axis": [0, 0, 1], "object": "square_peg", "tolerance": 3, "type": "orientation", "world": [0, 0, 1]}, {"bottom": 0.947, "half": [0.02, 0.055], "object": "long_peg", "tolerance": 0.006, "type": "region", "xy": [0.43, 0.302]}, {"axis": [0, 0, 1], "object": "long_peg", "tolerance": 3, "type": "orientation", "world": [0, -1, 0]}], "hold_steps": 2, "id": "complete", "requires": []}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      2.8973000049591064,
      1.7627999782562256,
      2.8973000049591064,
      -0.0697999969124794,
      2.8973000049591064,
      3.752500057220459,
      2.8973000049591064,
      1.0
    ],
    "low": [
      -2.8973000049591064,
      -1.7627999782562256,
      -2.8973000049591064,
      -3.0717999935150146,
      -2.8973000049591064,
      -0.017500000074505806,
      -2.8973000049591064,
      -1.0
    ],
    "names": [
      "arm.panda_joint1",
      "arm.panda_joint2",
      "arm.panda_joint3",
      "arm.panda_joint4",
      "arm.panda_joint5",
      "arm.panda_joint6",
      "arm.panda_joint7",
      "gripper[0]"
    ],
    "neutral_action": [
      0.0,
      0.39269909262657166,
      0.0,
      -1.9634953737258911,
      0.0,
      2.356194496154785,
      0.7853981852531433,
      1.0
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "gripper: PDJointPosMimicController; joint order=['panda_finger_joint1', 'panda_finger_joint2']; normalize_action=True; use_delta=False; native_low=[-0.009999999776482582]; native_high=[0.03999999910593033]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 8,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "bottom": 0.87,
        "half": [
          0.022,
          0.022
        ],
        "object": "round_peg",
        "support": "socket_board",
        "tolerance": 0.005,
        "type": "region",
        "xy": [
          0.04,
          0.27
        ]
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "round_peg",
        "tolerance": 3,
        "type": "orientation",
        "world": [
          0,
          0,
          1
        ]
      },
      {
        "bottom": 0.87,
        "half": [
          0.022,
          0.022
        ],
        "object": "square_peg",
        "support": "socket_board",
        "tolerance": 0.005,
        "type": "region",
        "xy": [
          0.25,
          0.27
        ]
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "square_peg",
        "tolerance": 3,
        "type": "orientation",
        "world": [
          0,
          0,
          1
        ]
      },
      {
        "bottom": 0.947,
        "half": [
          0.02,
          0.055
        ],
        "object": "long_peg",
        "tolerance": 0.006,
        "type": "region",
        "xy": [
          0.43,
          0.302
        ]
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "long_peg",
        "tolerance": 3,
        "type": "orientation",
        "world": [
          0,
          -1,
          0
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "bottom": 0.87,
            "half": [
              0.022,
              0.022
            ],
            "object": "round_peg",
            "support": "socket_board",
            "tolerance": 0.005,
            "type": "region",
            "xy": [
              0.04,
              0.27
            ]
          },
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "round_peg",
            "tolerance": 3,
            "type": "orientation",
            "world": [
              0,
              0,
              1
            ]
          },
          {
            "bottom": 0.87,
            "half": [
              0.022,
              0.022
            ],
            "object": "square_peg",
            "support": "socket_board",
            "tolerance": 0.005,
            "type": "region",
            "xy": [
              0.25,
              0.27
            ]
          },
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "square_peg",
            "tolerance": 3,
            "type": "orientation",
            "world": [
              0,
              0,
              1
            ]
          },
          {
            "bottom": 0.947,
            "half": [
              0.02,
              0.055
            ],
            "object": "long_peg",
            "tolerance": 0.006,
            "type": "region",
            "xy": [
              0.43,
              0.302
            ]
          },
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "long_peg",
            "tolerance": 3,
            "type": "orientation",
            "world": [
              0,
              -1,
              0
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "background_tape",
      "background_box"
    ],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "305f02fa87d51560bdaac0952ba647683a659c8428073e46273af54cab7978b6",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/panda/P1 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-panda-P1-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-everyday_robot_09-P2"></a>
## `maniskill_geometry/everyday_robot_09/P2`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 30; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"key": "lock/turn", "max": 1.59, "min": 1.52, "type": "joint"}, {"bottom": 0.845, "half": [0.06, 0.14], "object": "key", "support": "key_mat", "tolerance": 0.016, "type": "region", "xy": [0.42, -0.06]}], "instruction": "Insert the key blade into the cabinet lock, turn it clockwise by a quarter turn, then withdraw the key onto the small mat.", "milestones": [{"conditions": [{"high": [0.22, 0.29, 1.085], "low": [0.12, 0.08, 1.0], "object": "key", "type": "inside"}, {"object": "key", "support": "lock/rotor", "type": "contact"}], "hold_steps": 2, "id": "key_engaged", "requires": []}, {"conditions": [{"key": "lock/turn", "max": 1.59, "min": 1.52, "type": "joint"}], "hold_steps": 2, "id": "quarter_turn", "requires": ["key_engaged"]}, {"conditions": [{"key": "lock/turn", "max": 1.59, "min": 1.52, "type": "joint"}, {"bottom": 0.845, "half": [0.06, 0.14], "object": "key", "support": "key_mat", "tolerance": 0.016, "type": "region", "xy": [0.42, -0.06]}], "hold_steps": 2, "id": "complete", "requires": ["quarter_turn"]}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      6.28318977355957,
      6.28318977355957,
      3.1414999961853027,
      6.28318977355957,
      6.28318977355957,
      6.28318977355957,
      0.17453299462795258,
      0.4886919856071472,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.785398006439209,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      1.0471999645233154,
      1.2217299938201904,
      0.20943999290466309,
      0.6981319785118103,
      1.5707999467849731
    ],
    "low": [
      -6.28318977355957,
      -6.28318977355957,
      -3.1414999961853027,
      -6.28318977355957,
      -6.28318977355957,
      -6.28318977355957,
      -0.5235990285873413,
      -0.6981319785118103,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -1.0471999645233154,
      0.0,
      -0.20943999290466309,
      -0.6981319785118103,
      -0.26179900765419006
    ],
    "names": [
      "arm.shoulder_pan_joint",
      "arm.shoulder_lift_joint",
      "arm.elbow_joint",
      "arm.wrist_1_joint",
      "arm.wrist_2_joint",
      "arm.wrist_3_joint",
      "hand.hand_rh_WRJ2",
      "hand.hand_rh_WRJ1",
      "hand.hand_rh_FFJ4",
      "hand.hand_rh_FFJ3",
      "hand.hand_rh_FFJ2",
      "hand.hand_rh_FFJ1",
      "hand.hand_rh_MFJ4",
      "hand.hand_rh_MFJ3",
      "hand.hand_rh_MFJ2",
      "hand.hand_rh_MFJ1",
      "hand.hand_rh_RFJ4",
      "hand.hand_rh_RFJ3",
      "hand.hand_rh_RFJ2",
      "hand.hand_rh_RFJ1",
      "hand.hand_rh_LFJ5",
      "hand.hand_rh_LFJ4",
      "hand.hand_rh_LFJ3",
      "hand.hand_rh_LFJ2",
      "hand.hand_rh_LFJ1",
      "hand.hand_rh_THJ5",
      "hand.hand_rh_THJ4",
      "hand.hand_rh_THJ3",
      "hand.hand_rh_THJ2",
      "hand.hand_rh_THJ1"
    ],
    "neutral_action": [
      -2.430368185043335,
      -2.3849759101867676,
      2.2959721088409424,
      -1.376956820487976,
      -1.6293714046478271,
      -0.5064780116081238,
      0.0,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 30,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "key": "lock/turn",
        "max": 1.59,
        "min": 1.52,
        "type": "joint"
      },
      {
        "bottom": 0.845,
        "half": [
          0.06,
          0.14
        ],
        "object": "key",
        "support": "key_mat",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.42,
          -0.06
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "high": [
              0.22,
              0.29,
              1.085
            ],
            "low": [
              0.12,
              0.08,
              1.0
            ],
            "object": "key",
            "type": "inside"
          },
          {
            "object": "key",
            "support": "lock/rotor",
            "type": "contact"
          }
        ],
        "hold_steps": 2,
        "id": "key_engaged",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "lock/turn",
            "max": 1.59,
            "min": 1.52,
            "type": "joint"
          }
        ],
        "hold_steps": 2,
        "id": "quarter_turn",
        "requires": [
          "key_engaged"
        ]
      },
      {
        "conditions": [
          {
            "key": "lock/turn",
            "max": 1.59,
            "min": 1.52,
            "type": "joint"
          },
          {
            "bottom": 0.845,
            "half": [
              0.06,
              0.14
            ],
            "object": "key",
            "support": "key_mat",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.42,
              -0.06
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "quarter_turn"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "6df866c2905248312c8b842f80bb5c5a914d34e0219836494cf10561e71e4f83",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/everyday_robot_09/P2 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-everyday_robot_09-P2-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-panda-P3"></a>
## `maniskill_geometry/panda/P3`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 8; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"bottom": 0.852, "half": [0.04, 0.108], "object": "connector", "support": "port", "tolerance": 0.006, "type": "region", "xy": [0.17, 0.29]}, {"axis": [0, 1, 0], "object": "connector", "tolerance": 3, "type": "orientation", "world": [0, 1, 0]}], "instruction": "Align the connector rib with the recessed port, insert it fully, and release. Leave the two neighboring connectors untouched.", "milestones": [{"conditions": [{"bottom": 0.852, "half": [0.04, 0.108], "object": "connector", "support": "port", "tolerance": 0.006, "type": "region", "xy": [0.17, 0.29]}, {"axis": [0, 1, 0], "object": "connector", "tolerance": 3, "type": "orientation", "world": [0, 1, 0]}], "hold_steps": 2, "id": "complete", "requires": []}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      2.8973000049591064,
      1.7627999782562256,
      2.8973000049591064,
      -0.0697999969124794,
      2.8973000049591064,
      3.752500057220459,
      2.8973000049591064,
      1.0
    ],
    "low": [
      -2.8973000049591064,
      -1.7627999782562256,
      -2.8973000049591064,
      -3.0717999935150146,
      -2.8973000049591064,
      -0.017500000074505806,
      -2.8973000049591064,
      -1.0
    ],
    "names": [
      "arm.panda_joint1",
      "arm.panda_joint2",
      "arm.panda_joint3",
      "arm.panda_joint4",
      "arm.panda_joint5",
      "arm.panda_joint6",
      "arm.panda_joint7",
      "gripper[0]"
    ],
    "neutral_action": [
      0.0,
      0.39269909262657166,
      0.0,
      -1.9634953737258911,
      0.0,
      2.356194496154785,
      0.7853981852531433,
      1.0
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "gripper: PDJointPosMimicController; joint order=['panda_finger_joint1', 'panda_finger_joint2']; normalize_action=True; use_delta=False; native_low=[-0.009999999776482582]; native_high=[0.03999999910593033]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 8,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "bottom": 0.852,
        "half": [
          0.04,
          0.108
        ],
        "object": "connector",
        "support": "port",
        "tolerance": 0.006,
        "type": "region",
        "xy": [
          0.17,
          0.29
        ]
      },
      {
        "axis": [
          0,
          1,
          0
        ],
        "object": "connector",
        "tolerance": 3,
        "type": "orientation",
        "world": [
          0,
          1,
          0
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "max_force": 35,
        "name": "excessive_insertion_force",
        "object": "connector",
        "support": "port",
        "type": "force_limit"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "bottom": 0.852,
            "half": [
              0.04,
              0.108
            ],
            "object": "connector",
            "support": "port",
            "tolerance": 0.006,
            "type": "region",
            "xy": [
              0.17,
              0.29
            ]
          },
          {
            "axis": [
              0,
              1,
              0
            ],
            "object": "connector",
            "tolerance": 3,
            "type": "orientation",
            "world": [
              0,
              1,
              0
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "neighbor_-0.03",
      "neighbor_0.38"
    ],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "427fb71eb4a018ba70af327e72195bd54085f8f3da3f343eb51985aa3e225640",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/panda/P3 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-panda-P3-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-everyday_robot_03-P4"></a>
## `maniskill_geometry/everyday_robot_03/P4`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 23; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"bottom": 0.96, "half": [0.165, 0.123], "object": "lid", "support": "container", "tolerance": 0.005, "type": "region", "xy": [0.18, 0.26]}, {"axis": [1, 0, 0], "object": "lid", "tolerance": 3, "type": "orientation", "world": [1, 0, 0]}, {"gap": 0.004, "height": 0.96, "object": "lid", "points": [[-0.13, -0.1, -0.008], [-0.13, 0.1, -0.008], [0.12, -0.1, -0.008], [0.08, 0.1, -0.008]], "type": "rim_seated"}], "instruction": "Match the lid notch to the raised corner tab. Seat the lid evenly around the entire rim.", "milestones": [{"conditions": [{"bottom": 0.96, "half": [0.165, 0.123], "object": "lid", "support": "container", "tolerance": 0.005, "type": "region", "xy": [0.18, 0.26]}, {"axis": [1, 0, 0], "object": "lid", "tolerance": 3, "type": "orientation", "world": [1, 0, 0]}, {"gap": 0.004, "height": 0.96, "object": "lid", "points": [[-0.13, -0.1, -0.008], [-0.13, 0.1, -0.008], [0.12, -0.1, -0.008], [0.08, 0.1, -0.008]], "type": "rim_seated"}], "hold_steps": 2, "id": "complete", "requires": []}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      6.28318977355957,
      2.094399929046631,
      6.28318977355957,
      3.927000045776367,
      6.28318977355957,
      3.141590118408203,
      6.28318977355957,
      0.4699999988079071,
      1.6100000143051147,
      1.7089999914169312,
      1.6180000305175781,
      0.4699999988079071,
      1.6100000143051147,
      1.7089999914169312,
      1.6180000305175781,
      0.4699999988079071,
      1.6100000143051147,
      1.7089999914169312,
      1.6180000305175781,
      1.3960000276565552,
      1.1629999876022339,
      1.6440000534057617,
      1.718999981880188
    ],
    "low": [
      -6.28318977355957,
      -2.059000015258789,
      -6.28318977355957,
      -0.1919800043106079,
      -6.28318977355957,
      -1.6929700374603271,
      -6.28318977355957,
      -0.4699999988079071,
      -0.19599999487400055,
      -0.17399999499320984,
      -0.22699999809265137,
      -0.4699999988079071,
      -0.19599999487400055,
      -0.17399999499320984,
      -0.22699999809265137,
      -0.4699999988079071,
      -0.19599999487400055,
      -0.17399999499320984,
      -0.22699999809265137,
      0.2630000114440918,
      -0.10499999672174454,
      -0.1889999955892563,
      -0.16200000047683716
    ],
    "names": [
      "arm.joint1",
      "arm.joint2",
      "arm.joint3",
      "arm.joint4",
      "arm.joint5",
      "arm.joint6",
      "arm.joint7",
      "hand.hand_ffj0",
      "hand.hand_ffj1",
      "hand.hand_ffj2",
      "hand.hand_ffj3",
      "hand.hand_mfj0",
      "hand.hand_mfj1",
      "hand.hand_mfj2",
      "hand.hand_mfj3",
      "hand.hand_rfj0",
      "hand.hand_rfj1",
      "hand.hand_rfj2",
      "hand.hand_rfj3",
      "hand.hand_thj0",
      "hand.hand_thj1",
      "hand.hand_thj2",
      "hand.hand_thj3"
    ],
    "neutral_action": [
      4.560864448547363,
      0.5686802268028259,
      -2.295710563659668,
      1.0840566158294678,
      -5.91727876663208,
      1.8259373903274536,
      -3.810570240020752,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066,
      0.2630000114440918,
      0.07999999821186066,
      0.07999999821186066,
      0.07999999821186066
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -2.059000015258789, -6.28318977355957, -0.1919800043106079, -6.28318977355957, -1.6929700374603271, -6.28318977355957]; native_high=[6.28318977355957, 2.094399929046631, 6.28318977355957, 3.927000045776367, 6.28318977355957, 3.141590118408203, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -2.059000015258789, -6.28318977355957, -0.1919800043106079, -6.28318977355957, -1.6929700374603271, -6.28318977355957]; native_high=[6.28318977355957, 2.094399929046631, 6.28318977355957, 3.927000045776367, 6.28318977355957, 3.141590118408203, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -2.059000015258789, -6.28318977355957, -0.1919800043106079, -6.28318977355957, -1.6929700374603271, -6.28318977355957]; native_high=[6.28318977355957, 2.094399929046631, 6.28318977355957, 3.927000045776367, 6.28318977355957, 3.141590118408203, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -2.059000015258789, -6.28318977355957, -0.1919800043106079, -6.28318977355957, -1.6929700374603271, -6.28318977355957]; native_high=[6.28318977355957, 2.094399929046631, 6.28318977355957, 3.927000045776367, 6.28318977355957, 3.141590118408203, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -2.059000015258789, -6.28318977355957, -0.1919800043106079, -6.28318977355957, -1.6929700374603271, -6.28318977355957]; native_high=[6.28318977355957, 2.094399929046631, 6.28318977355957, 3.927000045776367, 6.28318977355957, 3.141590118408203, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -2.059000015258789, -6.28318977355957, -0.1919800043106079, -6.28318977355957, -1.6929700374603271, -6.28318977355957]; native_high=[6.28318977355957, 2.094399929046631, 6.28318977355957, 3.927000045776367, 6.28318977355957, 3.141590118408203, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -2.059000015258789, -6.28318977355957, -0.1919800043106079, -6.28318977355957, -1.6929700374603271, -6.28318977355957]; native_high=[6.28318977355957, 2.094399929046631, 6.28318977355957, 3.927000045776367, 6.28318977355957, 3.141590118408203, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_ffj0', 'hand_ffj1', 'hand_ffj2', 'hand_ffj3', 'hand_mfj0', 'hand_mfj1', 'hand_mfj2', 'hand_mfj3', 'hand_rfj0', 'hand_rfj1', 'hand_rfj2', 'hand_rfj3', 'hand_thj0', 'hand_thj1', 'hand_thj2', 'hand_thj3']; normalize_action=False; use_delta=False; native_low=[-0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, -0.4699999988079071, -0.19599999487400055, -0.17399999499320984, -0.22699999809265137, 0.2630000114440918, -0.10499999672174454, -0.1889999955892563, -0.16200000047683716]; native_high=[0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 0.4699999988079071, 1.6100000143051147, 1.7089999914169312, 1.6180000305175781, 1.3960000276565552, 1.1629999876022339, 1.6440000534057617, 1.718999981880188]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 23,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "bottom": 0.96,
        "half": [
          0.165,
          0.123
        ],
        "object": "lid",
        "support": "container",
        "tolerance": 0.005,
        "type": "region",
        "xy": [
          0.18,
          0.26
        ]
      },
      {
        "axis": [
          1,
          0,
          0
        ],
        "object": "lid",
        "tolerance": 3,
        "type": "orientation",
        "world": [
          1,
          0,
          0
        ]
      },
      {
        "gap": 0.004,
        "height": 0.96,
        "object": "lid",
        "points": [
          [
            -0.13,
            -0.1,
            -0.008
          ],
          [
            -0.13,
            0.1,
            -0.008
          ],
          [
            0.12,
            -0.1,
            -0.008
          ],
          [
            0.08,
            0.1,
            -0.008
          ]
        ],
        "type": "rim_seated"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "bottom": 0.96,
            "half": [
              0.165,
              0.123
            ],
            "object": "lid",
            "support": "container",
            "tolerance": 0.005,
            "type": "region",
            "xy": [
              0.18,
              0.26
            ]
          },
          {
            "axis": [
              1,
              0,
              0
            ],
            "object": "lid",
            "tolerance": 3,
            "type": "orientation",
            "world": [
              1,
              0,
              0
            ]
          },
          {
            "gap": 0.004,
            "height": 0.96,
            "object": "lid",
            "points": [
              [
                -0.13,
                -0.1,
                -0.008
              ],
              [
                -0.13,
                0.1,
                -0.008
              ],
              [
                0.12,
                -0.1,
                -0.008
              ],
              [
                0.08,
                0.1,
                -0.008
              ]
            ],
            "type": "rim_seated"
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "946ae696447d0931de8e22ab66db16496167d81d8e6097ca7371f12140a35ed3",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/everyday_robot_03/P4 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-everyday_robot_03-P4-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-panda-P5"></a>
## `maniskill_geometry/panda/P5`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 8; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"handle_center": [0.078, 0, 0.014], "hook": [0.25, 1.147], "object": "mug", "radius": 0.03, "type": "handle_on_hook"}, {"object": "mug", "support": "hook", "type": "contact"}, {"min": 0.95, "object": "mug", "type": "height"}], "instruction": "Guide the wall hook through the mug handle and release the mug into stable suspension. Do not disturb the adjacent mug.", "milestones": [{"conditions": [{"handle_center": [0.078, 0, 0.014], "hook": [0.25, 1.147], "object": "mug", "radius": 0.03, "type": "handle_on_hook"}, {"object": "mug", "support": "hook", "type": "contact"}, {"min": 0.95, "object": "mug", "type": "height"}], "hold_steps": 2, "id": "complete", "requires": []}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      2.8973000049591064,
      1.7627999782562256,
      2.8973000049591064,
      -0.0697999969124794,
      2.8973000049591064,
      3.752500057220459,
      2.8973000049591064,
      1.0
    ],
    "low": [
      -2.8973000049591064,
      -1.7627999782562256,
      -2.8973000049591064,
      -3.0717999935150146,
      -2.8973000049591064,
      -0.017500000074505806,
      -2.8973000049591064,
      -1.0
    ],
    "names": [
      "arm.panda_joint1",
      "arm.panda_joint2",
      "arm.panda_joint3",
      "arm.panda_joint4",
      "arm.panda_joint5",
      "arm.panda_joint6",
      "arm.panda_joint7",
      "gripper[0]"
    ],
    "neutral_action": [
      0.0,
      0.39269909262657166,
      0.0,
      -1.9634953737258911,
      0.0,
      2.356194496154785,
      0.7853981852531433,
      1.0
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "gripper: PDJointPosMimicController; joint order=['panda_finger_joint1', 'panda_finger_joint2']; normalize_action=True; use_delta=False; native_low=[-0.009999999776482582]; native_high=[0.03999999910593033]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 8,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "handle_center": [
          0.078,
          0,
          0.014
        ],
        "hook": [
          0.25,
          1.147
        ],
        "object": "mug",
        "radius": 0.03,
        "type": "handle_on_hook"
      },
      {
        "object": "mug",
        "support": "hook",
        "type": "contact"
      },
      {
        "min": 0.95,
        "object": "mug",
        "type": "height"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "handle_center": [
              0.078,
              0,
              0.014
            ],
            "hook": [
              0.25,
              1.147
            ],
            "object": "mug",
            "radius": 0.03,
            "type": "handle_on_hook"
          },
          {
            "object": "mug",
            "support": "hook",
            "type": "contact"
          },
          {
            "min": 0.95,
            "object": "mug",
            "type": "height"
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "adjacent_mug"
    ],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "9cb2f32773ba8a4436225d51e9ef5fe85b5f268d6f53bfec54cddceb38a584ab",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/panda/P5 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-panda-P5-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-everyday_robot_09-P6"></a>
## `maniskill_geometry/everyday_robot_09/P6`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 30; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"bottom": 0.845, "half": [0.3, 0.08], "object": "spatula", "support": "utensil_mat", "tolerance": 0.016, "type": "region", "xy": [0.2, -0.1]}, {"axis": [0, 0, 1], "object": "spatula", "tolerance": 8, "type": "orientation", "world": [1, 0, 0]}], "instruction": "Tilt and extract the long spatula through the holder opening, then lay it on the front mat. Keep the neighboring utensils upright and in place.", "milestones": [{"conditions": [{"min": 1.005, "object": "spatula", "type": "height"}, {"axis": [0, 0, 1], "object": "spatula", "tolerance": 40, "type": "orientation", "world": [0.7, 0, 0.714]}], "hold_steps": 2, "id": "tilted_clearance", "requires": []}, {"conditions": [{"bottom": 0.845, "half": [0.3, 0.08], "object": "spatula", "support": "utensil_mat", "tolerance": 0.016, "type": "region", "xy": [0.2, -0.1]}, {"axis": [0, 0, 1], "object": "spatula", "tolerance": 8, "type": "orientation", "world": [1, 0, 0]}], "hold_steps": 2, "id": "complete", "requires": ["tilted_clearance"]}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      6.28318977355957,
      6.28318977355957,
      3.1414999961853027,
      6.28318977355957,
      6.28318977355957,
      6.28318977355957,
      0.17453299462795258,
      0.4886919856071472,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.785398006439209,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      1.0471999645233154,
      1.2217299938201904,
      0.20943999290466309,
      0.6981319785118103,
      1.5707999467849731
    ],
    "low": [
      -6.28318977355957,
      -6.28318977355957,
      -3.1414999961853027,
      -6.28318977355957,
      -6.28318977355957,
      -6.28318977355957,
      -0.5235990285873413,
      -0.6981319785118103,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -1.0471999645233154,
      0.0,
      -0.20943999290466309,
      -0.6981319785118103,
      -0.26179900765419006
    ],
    "names": [
      "arm.shoulder_pan_joint",
      "arm.shoulder_lift_joint",
      "arm.elbow_joint",
      "arm.wrist_1_joint",
      "arm.wrist_2_joint",
      "arm.wrist_3_joint",
      "hand.hand_rh_WRJ2",
      "hand.hand_rh_WRJ1",
      "hand.hand_rh_FFJ4",
      "hand.hand_rh_FFJ3",
      "hand.hand_rh_FFJ2",
      "hand.hand_rh_FFJ1",
      "hand.hand_rh_MFJ4",
      "hand.hand_rh_MFJ3",
      "hand.hand_rh_MFJ2",
      "hand.hand_rh_MFJ1",
      "hand.hand_rh_RFJ4",
      "hand.hand_rh_RFJ3",
      "hand.hand_rh_RFJ2",
      "hand.hand_rh_RFJ1",
      "hand.hand_rh_LFJ5",
      "hand.hand_rh_LFJ4",
      "hand.hand_rh_LFJ3",
      "hand.hand_rh_LFJ2",
      "hand.hand_rh_LFJ1",
      "hand.hand_rh_THJ5",
      "hand.hand_rh_THJ4",
      "hand.hand_rh_THJ3",
      "hand.hand_rh_THJ2",
      "hand.hand_rh_THJ1"
    ],
    "neutral_action": [
      -2.430368185043335,
      -2.3849759101867676,
      2.2959721088409424,
      -1.376956820487976,
      -1.6293714046478271,
      -0.5064780116081238,
      0.0,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 30,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "bottom": 0.845,
        "half": [
          0.3,
          0.08
        ],
        "object": "spatula",
        "support": "utensil_mat",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.2,
          -0.1
        ]
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "spatula",
        "tolerance": 8,
        "type": "orientation",
        "world": [
          1,
          0,
          0
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "min": 1.005,
            "object": "spatula",
            "type": "height"
          },
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "spatula",
            "tolerance": 40,
            "type": "orientation",
            "world": [
              0.7,
              0,
              0.714
            ]
          }
        ],
        "hold_steps": 2,
        "id": "tilted_clearance",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.845,
            "half": [
              0.3,
              0.08
            ],
            "object": "spatula",
            "support": "utensil_mat",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.2,
              -0.1
            ]
          },
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "spatula",
            "tolerance": 8,
            "type": "orientation",
            "world": [
              1,
              0,
              0
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "tilted_clearance"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "other_utensil_0",
      "other_utensil_1"
    ],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "622b8b0fefe5640e87ace9f4d9a8fd59892481de3893fc7c7711c737ff66200a",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/everyday_robot_09/P6 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-everyday_robot_09-P6-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-panda-P7"></a>
## `maniskill_geometry/panda/P7`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 8; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"bottom": 0.86, "half": [0.015, 0.091], "object": "book", "support": "bookshelf", "tolerance": 0.005, "type": "region", "xy": [0.18, 0.3]}, {"axis": [0, 0, 1], "object": "book", "tolerance": 3, "type": "orientation", "world": [0, 0, 1]}], "instruction": "Stand the loose book upright and slide it into the narrow gap under the low shelf. Preserve both neighboring books.", "milestones": [{"conditions": [{"bottom": 0.86, "half": [0.015, 0.091], "object": "book", "support": "bookshelf", "tolerance": 0.005, "type": "region", "xy": [0.18, 0.3]}, {"axis": [0, 0, 1], "object": "book", "tolerance": 3, "type": "orientation", "world": [0, 0, 1]}], "hold_steps": 2, "id": "complete", "requires": []}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      2.8973000049591064,
      1.7627999782562256,
      2.8973000049591064,
      -0.0697999969124794,
      2.8973000049591064,
      3.752500057220459,
      2.8973000049591064,
      1.0
    ],
    "low": [
      -2.8973000049591064,
      -1.7627999782562256,
      -2.8973000049591064,
      -3.0717999935150146,
      -2.8973000049591064,
      -0.017500000074505806,
      -2.8973000049591064,
      -1.0
    ],
    "names": [
      "arm.panda_joint1",
      "arm.panda_joint2",
      "arm.panda_joint3",
      "arm.panda_joint4",
      "arm.panda_joint5",
      "arm.panda_joint6",
      "arm.panda_joint7",
      "gripper[0]"
    ],
    "neutral_action": [
      0.0,
      0.39269909262657166,
      0.0,
      -1.9634953737258911,
      0.0,
      2.356194496154785,
      0.7853981852531433,
      1.0
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "gripper: PDJointPosMimicController; joint order=['panda_finger_joint1', 'panda_finger_joint2']; normalize_action=True; use_delta=False; native_low=[-0.009999999776482582]; native_high=[0.03999999910593033]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 8,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "bottom": 0.86,
        "half": [
          0.015,
          0.091
        ],
        "object": "book",
        "support": "bookshelf",
        "tolerance": 0.005,
        "type": "region",
        "xy": [
          0.18,
          0.3
        ]
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "book",
        "tolerance": 3,
        "type": "orientation",
        "world": [
          0,
          0,
          1
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "bottom": 0.86,
            "half": [
              0.015,
              0.091
            ],
            "object": "book",
            "support": "bookshelf",
            "tolerance": 0.005,
            "type": "region",
            "xy": [
              0.18,
              0.3
            ]
          },
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "book",
            "tolerance": 3,
            "type": "orientation",
            "world": [
              0,
              0,
              1
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "left_book",
      "right_book"
    ],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "b54f04a082376a9947a9c15a25ff5fa151eb064e385c00cbe8a9566db83c2d78",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/panda/P7 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-panda-P7-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-everyday_robot_01-P8"></a>
## `maniskill_geometry/everyday_robot_01/P8`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 29; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"centers": [[0.083, 0.22, 1.151], [0.217, 0.22, 1.151]], "half": [0.026, 0.036, 0.018], "object": "portafilter", "points": [[-0.067, 0, 0.017], [0.067, 0, 0.017]], "type": "lugs_engaged"}, {"object": "portafilter", "support": "group_head", "type": "contact"}, {"axis": [1, 0, 0], "object": "portafilter", "tolerance": 8, "type": "orientation", "world": [1, 0, 0]}], "instruction": "Align the two portafilter ears with the group-head entry gaps, lift it into the head, then rotate the handle into the locking direction and release.", "milestones": [{"conditions": [{"high": [0.17, 0.24, 1.142], "low": [0.13, 0.2, 1.135], "object": "portafilter", "type": "center"}, {"axis": [1, 0, 0], "object": "portafilter", "tolerance": 12, "type": "orientation", "world": [0, 1, 0]}], "hold_steps": 2, "id": "ears_entered", "requires": []}, {"conditions": [{"centers": [[0.083, 0.22, 1.151], [0.217, 0.22, 1.151]], "half": [0.026, 0.036, 0.018], "object": "portafilter", "points": [[-0.067, 0, 0.017], [0.067, 0, 0.017]], "type": "lugs_engaged"}, {"object": "portafilter", "support": "group_head", "type": "contact"}, {"axis": [1, 0, 0], "object": "portafilter", "tolerance": 8, "type": "orientation", "world": [1, 0, 0]}], "hold_steps": 2, "id": "complete", "requires": ["ears_entered"]}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      2.8973000049591064,
      1.7627999782562256,
      2.8973000049591064,
      -0.0697999969124794,
      2.8973000049591064,
      3.752500057220459,
      2.8973000049591064,
      1.9198999404907227,
      0.3490999937057495,
      1.396299958229065,
      0.3490999937057495,
      1.745300054550171,
      1.5707999467849731,
      0.3490999937057495,
      1.745300054550171,
      1.396299958229065,
      1.5707999467849731,
      0.3490999937057495,
      1.745300054550171,
      1.396299958229065,
      1.5707999467849731,
      0.3490999937057495,
      1.745300054550171,
      1.396299958229065,
      0.26179999113082886,
      1.5707999467849731,
      0.3490999937057495,
      1.745300054550171,
      1.396299958229065
    ],
    "low": [
      -2.8973000049591064,
      -1.7627999782562256,
      -2.8973000049591064,
      -3.0717999935150146,
      -2.8973000049591064,
      -0.017500000074505806,
      -2.8973000049591064,
      -0.1745000034570694,
      -0.3490999937057495,
      -0.5235999822616577,
      -0.3490999937057495,
      0.0,
      -0.17453299462795258,
      -0.3490999937057495,
      0.0,
      0.0,
      -0.17453299462795258,
      -0.3490999937057495,
      0.0,
      0.0,
      -0.17453299462795258,
      -0.3490999937057495,
      0.0,
      0.0,
      0.0,
      -0.17453299462795258,
      -0.3490999937057495,
      0.0,
      0.0
    ],
    "names": [
      "arm.joint1",
      "arm.joint2",
      "arm.joint3",
      "arm.joint4",
      "arm.joint5",
      "arm.joint6",
      "arm.joint7",
      "hand.hand_right_thumb_CMC_FE",
      "hand.hand_right_thumb_CMC_AA",
      "hand.hand_right_thumb_MCP_FE",
      "hand.hand_right_thumb_MCP_AA",
      "hand.hand_right_thumb_IP",
      "hand.hand_right_index_MCP_FE",
      "hand.hand_right_index_MCP_AA",
      "hand.hand_right_index_PIP",
      "hand.hand_right_index_DIP",
      "hand.hand_right_middle_MCP_FE",
      "hand.hand_right_middle_MCP_AA",
      "hand.hand_right_middle_PIP",
      "hand.hand_right_middle_DIP",
      "hand.hand_right_ring_MCP_FE",
      "hand.hand_right_ring_MCP_AA",
      "hand.hand_right_ring_PIP",
      "hand.hand_right_ring_DIP",
      "hand.hand_right_pinky_CMC",
      "hand.hand_right_pinky_MCP_FE",
      "hand.hand_right_pinky_MCP_AA",
      "hand.hand_right_pinky_PIP",
      "hand.hand_right_pinky_DIP"
    ],
    "neutral_action": [
      1.3088804483413696,
      -0.7816517353057861,
      0.9281482696533203,
      -2.253324270248413,
      0.39186644554138184,
      1.2951308488845825,
      -0.06357824057340622,
      0.0,
      0.0,
      0.2199999988079071,
      0.0,
      0.0,
      0.2199999988079071,
      0.0,
      0.2199999988079071,
      0.2199999988079071,
      0.2199999988079071,
      0.0,
      0.2199999988079071,
      0.2199999988079071,
      0.2199999988079071,
      0.0,
      0.2199999988079071,
      0.2199999988079071,
      0.0,
      0.2199999988079071,
      0.0,
      0.2199999988079071,
      0.2199999988079071
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_right_thumb_CMC_FE', 'hand_right_thumb_CMC_AA', 'hand_right_thumb_MCP_FE', 'hand_right_thumb_MCP_AA', 'hand_right_thumb_IP', 'hand_right_index_MCP_FE', 'hand_right_index_MCP_AA', 'hand_right_index_PIP', 'hand_right_index_DIP', 'hand_right_middle_MCP_FE', 'hand_right_middle_MCP_AA', 'hand_right_middle_PIP', 'hand_right_middle_DIP', 'hand_right_ring_MCP_FE', 'hand_right_ring_MCP_AA', 'hand_right_ring_PIP', 'hand_right_ring_DIP', 'hand_right_pinky_CMC', 'hand_right_pinky_MCP_FE', 'hand_right_pinky_MCP_AA', 'hand_right_pinky_PIP', 'hand_right_pinky_DIP']; normalize_action=False; use_delta=False; native_low=[-0.1745000034570694, -0.3490999937057495, -0.5235999822616577, -0.3490999937057495, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0, 0.0, -0.17453299462795258, -0.3490999937057495, 0.0, 0.0]; native_high=[1.9198999404907227, 0.3490999937057495, 1.396299958229065, 0.3490999937057495, 1.745300054550171, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065, 0.26179999113082886, 1.5707999467849731, 0.3490999937057495, 1.745300054550171, 1.396299958229065]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 29,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "centers": [
          [
            0.083,
            0.22,
            1.151
          ],
          [
            0.217,
            0.22,
            1.151
          ]
        ],
        "half": [
          0.026,
          0.036,
          0.018
        ],
        "object": "portafilter",
        "points": [
          [
            -0.067,
            0,
            0.017
          ],
          [
            0.067,
            0,
            0.017
          ]
        ],
        "type": "lugs_engaged"
      },
      {
        "object": "portafilter",
        "support": "group_head",
        "type": "contact"
      },
      {
        "axis": [
          1,
          0,
          0
        ],
        "object": "portafilter",
        "tolerance": 8,
        "type": "orientation",
        "world": [
          1,
          0,
          0
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "high": [
              0.17,
              0.24,
              1.142
            ],
            "low": [
              0.13,
              0.2,
              1.135
            ],
            "object": "portafilter",
            "type": "center"
          },
          {
            "axis": [
              1,
              0,
              0
            ],
            "object": "portafilter",
            "tolerance": 12,
            "type": "orientation",
            "world": [
              0,
              1,
              0
            ]
          }
        ],
        "hold_steps": 2,
        "id": "ears_entered",
        "requires": []
      },
      {
        "conditions": [
          {
            "centers": [
              [
                0.083,
                0.22,
                1.151
              ],
              [
                0.217,
                0.22,
                1.151
              ]
            ],
            "half": [
              0.026,
              0.036,
              0.018
            ],
            "object": "portafilter",
            "points": [
              [
                -0.067,
                0,
                0.017
              ],
              [
                0.067,
                0,
                0.017
              ]
            ],
            "type": "lugs_engaged"
          },
          {
            "object": "portafilter",
            "support": "group_head",
            "type": "contact"
          },
          {
            "axis": [
              1,
              0,
              0
            ],
            "object": "portafilter",
            "tolerance": 8,
            "type": "orientation",
            "world": [
              1,
              0,
              0
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "ears_entered"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "67205387f4223007e4283a2e1e7e368fb5ac16168fb025a63cd7b6079e2f31a5",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/everyday_robot_01/P8 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-everyday_robot_01-P8-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-everyday_robot_09-P9"></a>
## `maniskill_geometry/everyday_robot_09/P9`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 30; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"key": "controls/turn1", "max": 0.4974532925199433, "min": 0.46254670748005666, "type": "joint"}], "instruction": "Rotate the middle dial until its pointer aligns with the narrow gold tick. Release it without moving either neighboring control.", "milestones": [{"conditions": [{"key": "controls/turn1", "max": 0.4974532925199433, "min": 0.46254670748005666, "type": "joint"}], "hold_steps": 2, "id": "complete", "requires": []}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      6.28318977355957,
      6.28318977355957,
      3.1414999961853027,
      6.28318977355957,
      6.28318977355957,
      6.28318977355957,
      0.17453299462795258,
      0.4886919856071472,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      0.785398006439209,
      0.34906598925590515,
      1.5707999467849731,
      1.5707999467849731,
      1.5707999467849731,
      1.0471999645233154,
      1.2217299938201904,
      0.20943999290466309,
      0.6981319785118103,
      1.5707999467849731
    ],
    "low": [
      -6.28318977355957,
      -6.28318977355957,
      -3.1414999961853027,
      -6.28318977355957,
      -6.28318977355957,
      -6.28318977355957,
      -0.5235990285873413,
      -0.6981319785118103,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      0.0,
      -0.34906598925590515,
      -0.26179900765419006,
      0.0,
      0.0,
      -1.0471999645233154,
      0.0,
      -0.20943999290466309,
      -0.6981319785118103,
      -0.26179900765419006
    ],
    "names": [
      "arm.shoulder_pan_joint",
      "arm.shoulder_lift_joint",
      "arm.elbow_joint",
      "arm.wrist_1_joint",
      "arm.wrist_2_joint",
      "arm.wrist_3_joint",
      "hand.hand_rh_WRJ2",
      "hand.hand_rh_WRJ1",
      "hand.hand_rh_FFJ4",
      "hand.hand_rh_FFJ3",
      "hand.hand_rh_FFJ2",
      "hand.hand_rh_FFJ1",
      "hand.hand_rh_MFJ4",
      "hand.hand_rh_MFJ3",
      "hand.hand_rh_MFJ2",
      "hand.hand_rh_MFJ1",
      "hand.hand_rh_RFJ4",
      "hand.hand_rh_RFJ3",
      "hand.hand_rh_RFJ2",
      "hand.hand_rh_RFJ1",
      "hand.hand_rh_LFJ5",
      "hand.hand_rh_LFJ4",
      "hand.hand_rh_LFJ3",
      "hand.hand_rh_LFJ2",
      "hand.hand_rh_LFJ1",
      "hand.hand_rh_THJ5",
      "hand.hand_rh_THJ4",
      "hand.hand_rh_THJ3",
      "hand.hand_rh_THJ2",
      "hand.hand_rh_THJ1"
    ],
    "neutral_action": [
      -2.430368185043335,
      -2.3849759101867676,
      2.2959721088409424,
      -1.376956820487976,
      -1.6293714046478271,
      -0.5064780116081238,
      0.0,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224,
      0.0,
      0.0,
      0.20000000298023224,
      0.20000000298023224,
      0.20000000298023224
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']; normalize_action=False; use_delta=False; native_low=[-6.28318977355957, -6.28318977355957, -3.1414999961853027, -6.28318977355957, -6.28318977355957, -6.28318977355957]; native_high=[6.28318977355957, 6.28318977355957, 3.1414999961853027, 6.28318977355957, 6.28318977355957, 6.28318977355957]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "hand: PDJointPosController; joint order=['hand_rh_WRJ2', 'hand_rh_WRJ1', 'hand_rh_FFJ4', 'hand_rh_FFJ3', 'hand_rh_FFJ2', 'hand_rh_FFJ1', 'hand_rh_MFJ4', 'hand_rh_MFJ3', 'hand_rh_MFJ2', 'hand_rh_MFJ1', 'hand_rh_RFJ4', 'hand_rh_RFJ3', 'hand_rh_RFJ2', 'hand_rh_RFJ1', 'hand_rh_LFJ5', 'hand_rh_LFJ4', 'hand_rh_LFJ3', 'hand_rh_LFJ2', 'hand_rh_LFJ1', 'hand_rh_THJ5', 'hand_rh_THJ4', 'hand_rh_THJ3', 'hand_rh_THJ2', 'hand_rh_THJ1']; normalize_action=False; use_delta=False; native_low=[-0.5235990285873413, -0.6981319785118103, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, 0.0, -0.34906598925590515, -0.26179900765419006, 0.0, 0.0, -1.0471999645233154, 0.0, -0.20943999290466309, -0.6981319785118103, -0.26179900765419006]; native_high=[0.17453299462795258, 0.4886919856071472, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 0.785398006439209, 0.34906598925590515, 1.5707999467849731, 1.5707999467849731, 1.5707999467849731, 1.0471999645233154, 1.2217299938201904, 0.20943999290466309, 0.6981319785118103, 1.5707999467849731]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 30,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "key": "controls/turn1",
        "max": 0.4974532925199433,
        "min": 0.46254670748005666,
        "type": "joint"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "key": "controls/turn1",
            "max": 0.4974532925199433,
            "min": 0.46254670748005666,
            "type": "joint"
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "background_tape",
      "background_box"
    ],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [
      "controls/turn0",
      "controls/turn2"
    ],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "5fa6614f6ab4983aed63592bd88b769654667258dc62732b104b8f2a733a1357",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/everyday_robot_09/P9 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-everyday_robot_09-P9-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="maniskill_geometry-panda-P10"></a>
## `maniskill_geometry/panda/P10`

作者来源：[env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/geometry_dynamics/tasks.json)。Action size: 8; 2400 controls / 120 s; wall: 3600 s.

目标（源数据）：
```json
{"final": [{"force": 0.03, "min_height": 0.96, "object": "washer", "type": "held"}, {"axis": [0, 0, 1], "object": "washer", "tolerance": 8, "type": "orientation", "world": [0, -1, 0]}], "instruction": "Pick up the thin washer from the flat work surface, turn its face upright, and hold it steadily above the mat. Do not sweep it off the surface.", "milestones": [{"conditions": [{"force": 0.03, "min_height": 0.96, "object": "washer", "type": "held"}, {"axis": [0, 0, 1], "object": "washer", "tolerance": 8, "type": "orientation", "world": [0, -1, 0]}], "hold_steps": 2, "id": "complete", "requires": []}]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      2.8973000049591064,
      1.7627999782562256,
      2.8973000049591064,
      -0.0697999969124794,
      2.8973000049591064,
      3.752500057220459,
      2.8973000049591064,
      1.0
    ],
    "low": [
      -2.8973000049591064,
      -1.7627999782562256,
      -2.8973000049591064,
      -3.0717999935150146,
      -2.8973000049591064,
      -0.017500000074505806,
      -2.8973000049591064,
      -1.0
    ],
    "names": [
      "arm.panda_joint1",
      "arm.panda_joint2",
      "arm.panda_joint3",
      "arm.panda_joint4",
      "arm.panda_joint5",
      "arm.panda_joint6",
      "arm.panda_joint7",
      "gripper[0]"
    ],
    "neutral_action": [
      0.0,
      0.39269909262657166,
      0.0,
      -1.9634953737258911,
      0.0,
      2.356194496154785,
      0.7853981852531433,
      1.0
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4', 'panda_joint5', 'panda_joint6', 'panda_joint7']; normalize_action=False; use_delta=False; native_low=[-2.8973000049591064, -1.7627999782562256, -2.8973000049591064, -3.0717999935150146, -2.8973000049591064, -0.017500000074505806, -2.8973000049591064]; native_high=[2.8973000049591064, 1.7627999782562256, 2.8973000049591064, -0.0697999969124794, 2.8973000049591064, 3.752500057220459, 2.8973000049591064]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "gripper: PDJointPosMimicController; joint order=['panda_finger_joint1', 'panda_finger_joint2']; normalize_action=True; use_delta=False; native_low=[-0.009999999776482582]; native_high=[0.03999999910593033]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 8,
    "units": "Per-component target mappings in semantics; rotational joint targets use radians, prismatic targets use metres."
  },
  "observation_spec": {
    "calibration": [
      "intrinsics",
      "world_from_camera",
      "convention",
      "near_m",
      "far_m",
      "pixel_center_offset"
    ],
    "calibration_values": "Measured for each initialization and attached to every authorized camera capture",
    "clock": {
      "physics_step_count": "integer physics substeps",
      "simulation_time_s": "seconds",
      "step_index": "integer control steps"
    },
    "depth": {
      "available": true,
      "encoding": "little-endian float32 metres with uint8 validity mask",
      "height": 480,
      "minimum_level": 1,
      "width": 640
    },
    "privileged_fields": [
      "pieces.<name>.position",
      "pieces.<name>.quaternion",
      "pieces.<name>.linear_velocity",
      "pieces.<name>.angular_velocity",
      "physics.physics_hz",
      "physics.control_hz"
    ],
    "privileged_minimum_level": 3,
    "proprioception": [
      "robots.<id>.joint_positions",
      "robots.<id>.joint_velocities",
      "robots.<id>.previous_action"
    ],
    "proprioception_units": "radians and radians/second for revolute joints; metres and metres/second for prismatic joints",
    "read_only": true,
    "rgb": {
      "encoding": "raw uint8 RGB",
      "height": 480,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "angular_speed_limit_rad_s": 0.15,
    "complete_substep_coverage": true,
    "dropped_object_latch_height_m": 0.025,
    "final": [
      {
        "force": 0.03,
        "min_height": 0.96,
        "object": "washer",
        "type": "held"
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "washer",
        "tolerance": 8,
        "type": "orientation",
        "world": [
          0,
          -1,
          0
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [
      "washer"
    ],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "force": 0.03,
            "min_height": 0.96,
            "object": "washer",
            "type": "held"
          },
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "washer",
            "tolerance": 8,
            "type": "orientation",
            "world": [
              0,
              -1,
              0
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "background_tape",
      "background_box"
    ],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "3dadb15d02f661cc380d155c50dfeb551c20ace81df3366a41a6a352a6eb65ea",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### default — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"authored_light_scale":0.85,"physics_variant":0}` |
| 2 | 0 | nominal | `{"authored_light_scale":0.95,"physics_variant":0}` |
| 3 | 0 | nominal | `{"authored_light_scale":1.05,"physics_variant":0}` |
| 4 | 0 | nominal | `{"authored_light_scale":1.15,"physics_variant":0}` |

```bash
python scripts/environment_runtime.py --task-id maniskill_geometry/panda/P10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_geometry-panda-P10-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

