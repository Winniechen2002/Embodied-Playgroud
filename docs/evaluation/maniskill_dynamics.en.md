# ManiSkill dynamics

[Protocol](../evaluation_protocol.en.md) · [Index](index.en.md) · [JSON](tasks.json)

Embodied Playground paper scope: Launcher uses loaded initialization only. The full 410-task paper setting has 410 groups / 1640 conditions; EP-100 has 100 / 400. This runtime schedule also includes ground and retains 510 groups / 2040 conditions. [EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.en.md)

Each task below has four trials per group at base seed 0. Parameters are private maintainer inputs. Goal strings and field names below are verbatim authoring data, not translated protocol prose.

<a id="maniskill_dynamics-panda-D1"></a>
## `maniskill_dynamics/panda/D1`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 8; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.84, "half": [0.15, 0.12], "object": "orange", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.24, 0.06]}], "instruction": "Stop the orange before it rolls off the counter, leaving it at rest on the green safe mat. Preserve the nearby mug.", "milestones": [{"conditions": [{"min": 0.14, "object": "orange", "type": "speed"}], "hold_steps": 2, "id": "rolling_observed", "requires": []}, {"conditions": [{"bottom": 0.84, "half": [0.15, 0.12], "object": "orange", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.24, 0.06]}], "hold_steps": 2, "id": "complete", "requires": ["rolling_observed"]}]}
```

Native action and scoring contract:
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
        "bottom": 0.84,
        "half": [
          0.15,
          0.12
        ],
        "object": "orange",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.24,
          0.06
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "name": "time_limit",
        "seconds": 5,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "min": 0.14,
            "object": "orange",
            "type": "speed"
          }
        ],
        "hold_steps": 2,
        "id": "rolling_observed",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.84,
            "half": [
              0.15,
              0.12
            ],
            "object": "orange",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.24,
              0.06
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "rolling_observed"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "mug"
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
  "sha256": "587926215af597bc94dddb2073c774fb3f88c227804b967033d8bb375833092e",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/panda/D1 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-panda-D1-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-panda-D2"></a>
## `maniskill_dynamics/panda/D2`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 8; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"frame": "catcher", "high": [0.08, 0.08, 0.065], "low": [-0.08, -0.08, -0.054], "object": "ball", "type": "inside"}, {"object": "ball", "support": "catcher", "type": "contact"}], "instruction": "Move the catcher beneath the ball leaving the ramp, catch it in flight, and retain it after impact.", "milestones": [{"conditions": [{"min": 0.2, "object": "ball", "type": "speed"}], "hold_steps": 2, "id": "ball_in_motion", "requires": []}, {"conditions": [{"min_speed": 0.08, "min_x": 0.34, "object": "ball", "type": "airborne"}], "hold_steps": 2, "id": "airborne", "requires": ["ball_in_motion"]}, {"conditions": [{"frame": "catcher", "high": [0.08, 0.08, 0.065], "low": [-0.08, -0.08, -0.054], "object": "ball", "type": "inside"}, {"object": "ball", "support": "catcher", "type": "contact"}], "hold_steps": 2, "id": "complete", "requires": ["airborne"]}]}
```

Native action and scoring contract:
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
        "frame": "catcher",
        "high": [
          0.08,
          0.08,
          0.065
        ],
        "low": [
          -0.08,
          -0.08,
          -0.054
        ],
        "object": "ball",
        "type": "inside"
      },
      {
        "object": "ball",
        "support": "catcher",
        "type": "contact"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "name": "time_limit",
        "seconds": 8,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "min": 0.2,
            "object": "ball",
            "type": "speed"
          }
        ],
        "hold_steps": 2,
        "id": "ball_in_motion",
        "requires": []
      },
      {
        "conditions": [
          {
            "min_speed": 0.08,
            "min_x": 0.34,
            "object": "ball",
            "type": "airborne"
          }
        ],
        "hold_steps": 2,
        "id": "airborne",
        "requires": [
          "ball_in_motion"
        ]
      },
      {
        "conditions": [
          {
            "frame": "catcher",
            "high": [
              0.08,
              0.08,
              0.065
            ],
            "low": [
              -0.08,
              -0.08,
              -0.054
            ],
            "object": "ball",
            "type": "inside"
          },
          {
            "object": "ball",
            "support": "catcher",
            "type": "contact"
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "airborne"
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
  "sha256": "0e49df47801a8e29d26f1e5a849b0109cab572568c047a5514bf79b45ee37705",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/panda/D2 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-panda-D2-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-panda-D3"></a>
## `maniskill_dynamics/panda/D3`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 8; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.84, "half": [0.105, 0.105], "object": "puck", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.43, 0.1]}], "instruction": "Give the puck one push so that it coasts to rest inside the gold scoring rectangle. Disengage after the push; do not correct it a second time.", "milestones": [{"conditions": [{"min_force": 0.05, "object": "puck", "type": "robot_contact"}], "hold_steps": 2, "id": "pushed", "requires": []}, {"conditions": [{"min": 0.08, "object": "puck", "type": "speed"}, {"max_force": 0.02, "object": "puck", "type": "robot_contact"}], "hold_steps": 2, "id": "coasting", "requires": ["pushed"]}, {"conditions": [{"bottom": 0.84, "half": [0.105, 0.105], "object": "puck", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.43, 0.1]}], "hold_steps": 2, "id": "complete", "requires": ["coasting"]}]}
```

Native action and scoring contract:
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
        "bottom": 0.84,
        "half": [
          0.105,
          0.105
        ],
        "object": "puck",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.43,
          0.1
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "name": "second_push",
        "object": "puck",
        "type": "single_push"
      },
      {
        "name": "time_limit",
        "seconds": 7,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "min_force": 0.05,
            "object": "puck",
            "type": "robot_contact"
          }
        ],
        "hold_steps": 2,
        "id": "pushed",
        "requires": []
      },
      {
        "conditions": [
          {
            "min": 0.08,
            "object": "puck",
            "type": "speed"
          },
          {
            "max_force": 0.02,
            "object": "puck",
            "type": "robot_contact"
          }
        ],
        "hold_steps": 2,
        "id": "coasting",
        "requires": [
          "pushed"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.84,
            "half": [
              0.105,
              0.105
            ],
            "object": "puck",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.43,
              0.1
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "coasting"
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
  "sha256": "3d496a8ab7eed9f330351093b491e855bb1e887e541904e6b9198485fb4df4a3",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/panda/D3 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-panda-D3-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-everyday_robot_01-D4"></a>
## `maniskill_dynamics/everyday_robot_01/D4`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 29; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.845, "half": [0.19, 0.15], "object": "tray", "support": "tray_dock", "tolerance": 0.016, "type": "region", "xy": [0.39, 0.3]}, {"object": "cup_one", "support": "tray", "type": "contact"}, {"object": "cup_two", "support": "tray", "type": "contact"}, {"object": "sugar_cube", "support": "tray", "type": "contact"}], "instruction": "Carry the loaded tray from the left station to the green docking mat. Keep both cups upright and all loose contents inside the tray.", "milestones": [{"conditions": [{"min": 0.89, "object": "tray", "type": "height"}, {"min": 0.03, "object": "tray", "type": "speed"}], "hold_steps": 2, "id": "tray_carried", "requires": []}, {"conditions": [{"bottom": 0.845, "half": [0.19, 0.15], "object": "tray", "support": "tray_dock", "tolerance": 0.016, "type": "region", "xy": [0.39, 0.3]}, {"object": "cup_one", "support": "tray", "type": "contact"}, {"object": "cup_two", "support": "tray", "type": "contact"}, {"object": "sugar_cube", "support": "tray", "type": "contact"}], "hold_steps": 2, "id": "complete", "requires": ["tray_carried"]}]}
```

Native action and scoring contract:
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
        "bottom": 0.845,
        "half": [
          0.19,
          0.15
        ],
        "object": "tray",
        "support": "tray_dock",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.39,
          0.3
        ]
      },
      {
        "object": "cup_one",
        "support": "tray",
        "type": "contact"
      },
      {
        "object": "cup_two",
        "support": "tray",
        "type": "contact"
      },
      {
        "object": "sugar_cube",
        "support": "tray",
        "type": "contact"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "degrees": 15,
        "name": "cup_tipped",
        "objects": [
          "cup_one",
          "cup_two"
        ],
        "type": "upright"
      },
      {
        "name": "payload_left_tray",
        "objects": [
          "cup_one",
          "cup_two",
          "sugar_cube"
        ],
        "type": "retain",
        "volume": {
          "frame": "tray",
          "high": [
            0.17,
            0.13,
            0.2
          ],
          "low": [
            -0.17,
            -0.13,
            -0.026
          ]
        }
      },
      {
        "name": "time_limit",
        "seconds": 12,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "min": 0.89,
            "object": "tray",
            "type": "height"
          },
          {
            "min": 0.03,
            "object": "tray",
            "type": "speed"
          }
        ],
        "hold_steps": 2,
        "id": "tray_carried",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.845,
            "half": [
              0.19,
              0.15
            ],
            "object": "tray",
            "support": "tray_dock",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.39,
              0.3
            ]
          },
          {
            "object": "cup_one",
            "support": "tray",
            "type": "contact"
          },
          {
            "object": "cup_two",
            "support": "tray",
            "type": "contact"
          },
          {
            "object": "sugar_cube",
            "support": "tray",
            "type": "contact"
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "tray_carried"
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
  "sha256": "a55519aa6d966eb712fc0b891e2bd3124015d797ea57c59d5eb088be2d4603e3",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/everyday_robot_01/D4 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-everyday_robot_01-D4-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-panda-D5"></a>
## `maniskill_dynamics/panda/D5`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 8; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.84, "half": [0.083, 0.083], "object": "bottle", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.41, 0.09]}, {"axis": [0, 0, 1], "object": "bottle", "tolerance": 8, "type": "orientation", "world": [0, 0, 1]}], "instruction": "Push the tall bottle near its base, around the guide block, and onto the green target. Keep it upright and on the counter throughout.", "milestones": [{"conditions": [{"high": [0.32, 0.43, 1.2], "low": [-0.04, 0.23, 0.825], "object": "bottle", "type": "inside"}], "hold_steps": 2, "id": "around_obstacle", "requires": []}, {"conditions": [{"bottom": 0.84, "half": [0.083, 0.083], "object": "bottle", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.41, 0.09]}, {"axis": [0, 0, 1], "object": "bottle", "tolerance": 8, "type": "orientation", "world": [0, 0, 1]}], "hold_steps": 2, "id": "complete", "requires": ["around_obstacle"]}]}
```

Native action and scoring contract:
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
        "bottom": 0.84,
        "half": [
          0.083,
          0.083
        ],
        "object": "bottle",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.41,
          0.09
        ]
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "bottle",
        "tolerance": 8,
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
    "history_rules": [
      {
        "degrees": 12,
        "name": "bottle_tipped",
        "objects": [
          "bottle"
        ],
        "type": "upright"
      },
      {
        "max_bottom": 0.875,
        "name": "bottle_lifted",
        "object": "bottle",
        "type": "no_lift"
      },
      {
        "max_height": 0.91,
        "name": "pushed_too_high",
        "object": "bottle",
        "type": "low_push"
      },
      {
        "name": "time_limit",
        "seconds": 10,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "high": [
              0.32,
              0.43,
              1.2
            ],
            "low": [
              -0.04,
              0.23,
              0.825
            ],
            "object": "bottle",
            "type": "inside"
          }
        ],
        "hold_steps": 2,
        "id": "around_obstacle",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.84,
            "half": [
              0.083,
              0.083
            ],
            "object": "bottle",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.41,
              0.09
            ]
          },
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "bottle",
            "tolerance": 8,
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
        "requires": [
          "around_obstacle"
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
  "sha256": "829a0c6b3ecddb761fea53eb2c476fa0ea06537a99ece0fde550513639ca4d95",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/panda/D5 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-panda-D5-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-panda-D6"></a>
## `maniskill_dynamics/panda/D6`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 8; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"key": "drawer/slide", "max": 0.008, "min": -0.005, "type": "joint"}, {"bottom": 0.016, "frame": "drawer/tray", "half": [0.052, 0.052], "object": "container_one", "tolerance": 0.01, "type": "region", "xy": [-0.15, 0]}, {"bottom": 0.016, "frame": "drawer/tray", "half": [0.052, 0.052], "object": "container_two", "tolerance": 0.01, "type": "region", "xy": [0.15, 0]}, {"bottom": 0.016, "frame": "drawer/tray", "half": [0.052, 0.052], "object": "block_0", "tolerance": 0.01, "type": "region", "xy": [0, 0.08]}, {"bottom": 0.056, "frame": "drawer/tray", "half": [0.052, 0.052], "object": "block_1", "tolerance": 0.01, "type": "region", "xy": [0, 0.08]}], "instruction": "Close the extended drawer within five seconds without tipping the two containers or scattering the small block stack.", "milestones": [{"conditions": [{"key": "drawer/slide", "min": 0.015, "type": "joint_speed"}], "hold_steps": 2, "id": "drawer_moving", "requires": []}, {"conditions": [{"key": "drawer/slide", "max": 0.008, "min": -0.005, "type": "joint"}, {"bottom": 0.016, "frame": "drawer/tray", "half": [0.052, 0.052], "object": "container_one", "tolerance": 0.01, "type": "region", "xy": [-0.15, 0]}, {"bottom": 0.016, "frame": "drawer/tray", "half": [0.052, 0.052], "object": "container_two", "tolerance": 0.01, "type": "region", "xy": [0.15, 0]}, {"bottom": 0.016, "frame": "drawer/tray", "half": [0.052, 0.052], "object": "block_0", "tolerance": 0.01, "type": "region", "xy": [0, 0.08]}, {"bottom": 0.056, "frame": "drawer/tray", "half": [0.052, 0.052], "object": "block_1", "tolerance": 0.01, "type": "region", "xy": [0, 0.08]}], "hold_steps": 2, "id": "complete", "requires": ["drawer_moving"]}]}
```

Native action and scoring contract:
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
        "key": "drawer/slide",
        "max": 0.008,
        "min": -0.005,
        "type": "joint"
      },
      {
        "bottom": 0.016,
        "frame": "drawer/tray",
        "half": [
          0.052,
          0.052
        ],
        "object": "container_one",
        "tolerance": 0.01,
        "type": "region",
        "xy": [
          -0.15,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "drawer/tray",
        "half": [
          0.052,
          0.052
        ],
        "object": "container_two",
        "tolerance": 0.01,
        "type": "region",
        "xy": [
          0.15,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "drawer/tray",
        "half": [
          0.052,
          0.052
        ],
        "object": "block_0",
        "tolerance": 0.01,
        "type": "region",
        "xy": [
          0,
          0.08
        ]
      },
      {
        "bottom": 0.056,
        "frame": "drawer/tray",
        "half": [
          0.052,
          0.052
        ],
        "object": "block_1",
        "tolerance": 0.01,
        "type": "region",
        "xy": [
          0,
          0.08
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "degrees": 15,
        "name": "contents_tipped",
        "objects": [
          "container_one",
          "container_two"
        ],
        "type": "upright"
      },
      {
        "name": "contents_scattered",
        "objects": [
          "container_one",
          "container_two",
          "block_0",
          "block_1"
        ],
        "type": "retain",
        "volume": {
          "frame": "drawer/tray",
          "high": [
            0.28,
            0.205,
            0.245
          ],
          "low": [
            -0.28,
            -0.205,
            0.002
          ]
        }
      },
      {
        "name": "time_limit",
        "seconds": 5,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "key": "drawer/slide",
            "min": 0.015,
            "type": "joint_speed"
          }
        ],
        "hold_steps": 2,
        "id": "drawer_moving",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "drawer/slide",
            "max": 0.008,
            "min": -0.005,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "drawer/tray",
            "half": [
              0.052,
              0.052
            ],
            "object": "container_one",
            "tolerance": 0.01,
            "type": "region",
            "xy": [
              -0.15,
              0
            ]
          },
          {
            "bottom": 0.016,
            "frame": "drawer/tray",
            "half": [
              0.052,
              0.052
            ],
            "object": "container_two",
            "tolerance": 0.01,
            "type": "region",
            "xy": [
              0.15,
              0
            ]
          },
          {
            "bottom": 0.016,
            "frame": "drawer/tray",
            "half": [
              0.052,
              0.052
            ],
            "object": "block_0",
            "tolerance": 0.01,
            "type": "region",
            "xy": [
              0,
              0.08
            ]
          },
          {
            "bottom": 0.056,
            "frame": "drawer/tray",
            "half": [
              0.052,
              0.052
            ],
            "object": "block_1",
            "tolerance": 0.01,
            "type": "region",
            "xy": [
              0,
              0.08
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "drawer_moving"
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
  "sha256": "87b81cb3ac13aaef76b9b06bdeb742d16887ae842c747f94dc24f6c90f74995d",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/panda/D6 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-panda-D6-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-everyday_robot_03-D7"></a>
## `maniskill_dynamics/everyday_robot_03/D7`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 23; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"count": 8, "frame": "receiver", "high": [0.042, 0.042, 0.07], "low": [-0.042, -0.042, -0.064], "names": ["bead_0", "bead_1", "bead_2", "bead_3", "bead_4", "bead_5", "bead_6", "bead_7", "bead_8", "bead_9", "bead_10", "bead_11"], "type": "bead_count"}, {"count": 4, "frame": "pouring_cup", "high": [0.067, 0.067, 0.07], "low": [-0.067, -0.067, -0.064], "names": ["bead_0", "bead_1", "bead_2", "bead_3", "bead_4", "bead_5", "bead_6", "bead_7", "bead_8", "bead_9", "bead_10", "bead_11"], "type": "bead_count"}], "instruction": "Pour exactly eight of the twelve beads into the narrow receiving cup. Keep the other four in the pouring cup and leave no beads on the worktop.", "milestones": [{"conditions": [{"axis": [0, 0, 1], "object": "pouring_cup", "tolerance": 22, "type": "orientation", "world": [0.9, 0, 0.435]}], "hold_steps": 2, "id": "pouring_tilt", "requires": []}, {"conditions": [{"count": 8, "frame": "receiver", "high": [0.042, 0.042, 0.07], "low": [-0.042, -0.042, -0.064], "names": ["bead_0", "bead_1", "bead_2", "bead_3", "bead_4", "bead_5", "bead_6", "bead_7", "bead_8", "bead_9", "bead_10", "bead_11"], "type": "bead_count"}, {"count": 4, "frame": "pouring_cup", "high": [0.067, 0.067, 0.07], "low": [-0.067, -0.067, -0.064], "names": ["bead_0", "bead_1", "bead_2", "bead_3", "bead_4", "bead_5", "bead_6", "bead_7", "bead_8", "bead_9", "bead_10", "bead_11"], "type": "bead_count"}], "hold_steps": 2, "id": "complete", "requires": ["pouring_tilt"]}]}
```

Native action and scoring contract:
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
        "count": 8,
        "frame": "receiver",
        "high": [
          0.042,
          0.042,
          0.07
        ],
        "low": [
          -0.042,
          -0.042,
          -0.064
        ],
        "names": [
          "bead_0",
          "bead_1",
          "bead_2",
          "bead_3",
          "bead_4",
          "bead_5",
          "bead_6",
          "bead_7",
          "bead_8",
          "bead_9",
          "bead_10",
          "bead_11"
        ],
        "type": "bead_count"
      },
      {
        "count": 4,
        "frame": "pouring_cup",
        "high": [
          0.067,
          0.067,
          0.07
        ],
        "low": [
          -0.067,
          -0.067,
          -0.064
        ],
        "names": [
          "bead_0",
          "bead_1",
          "bead_2",
          "bead_3",
          "bead_4",
          "bead_5",
          "bead_6",
          "bead_7",
          "bead_8",
          "bead_9",
          "bead_10",
          "bead_11"
        ],
        "type": "bead_count"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "name": "time_limit",
        "seconds": 18,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "axis": [
              0,
              0,
              1
            ],
            "object": "pouring_cup",
            "tolerance": 22,
            "type": "orientation",
            "world": [
              0.9,
              0,
              0.435
            ]
          }
        ],
        "hold_steps": 2,
        "id": "pouring_tilt",
        "requires": []
      },
      {
        "conditions": [
          {
            "count": 8,
            "frame": "receiver",
            "high": [
              0.042,
              0.042,
              0.07
            ],
            "low": [
              -0.042,
              -0.042,
              -0.064
            ],
            "names": [
              "bead_0",
              "bead_1",
              "bead_2",
              "bead_3",
              "bead_4",
              "bead_5",
              "bead_6",
              "bead_7",
              "bead_8",
              "bead_9",
              "bead_10",
              "bead_11"
            ],
            "type": "bead_count"
          },
          {
            "count": 4,
            "frame": "pouring_cup",
            "high": [
              0.067,
              0.067,
              0.07
            ],
            "low": [
              -0.067,
              -0.067,
              -0.064
            ],
            "names": [
              "bead_0",
              "bead_1",
              "bead_2",
              "bead_3",
              "bead_4",
              "bead_5",
              "bead_6",
              "bead_7",
              "bead_8",
              "bead_9",
              "bead_10",
              "bead_11"
            ],
            "type": "bead_count"
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "pouring_tilt"
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
  "sha256": "d5e0316f810c355f9382e1e3a9191ca3f38cba5b1494e23550afc749b2b2d34a",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/everyday_robot_03/D7 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-everyday_robot_03-D7-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-panda-D8"></a>
## `maniskill_dynamics/panda/D8`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 8; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"key": "cabinet/close", "max": 0.035, "min": -0.012, "type": "joint"}], "instruction": "Guide the spring-closing cabinet door shut gently. Avoid slamming it into the frame or allowing it to rebound.", "milestones": [{"conditions": [{"key": "cabinet/close", "min": 0.1, "type": "joint_speed"}], "hold_steps": 2, "id": "spring_motion", "requires": []}, {"conditions": [{"key": "cabinet/close", "max": 0.035, "min": -0.012, "type": "joint"}], "hold_steps": 2, "id": "complete", "requires": ["spring_motion"]}]}
```

Native action and scoring contract:
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
        "key": "cabinet/close",
        "max": 0.035,
        "min": -0.012,
        "type": "joint"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "joint": "cabinet/close",
        "max_speed": 0.45,
        "name": "door_slam",
        "type": "soft_close"
      },
      {
        "closed": 0.035,
        "joint": "cabinet/close",
        "name": "door_rebounded",
        "reopened": 0.09,
        "type": "no_rebound"
      },
      {
        "name": "time_limit",
        "seconds": 7,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "key": "cabinet/close",
            "min": 0.1,
            "type": "joint_speed"
          }
        ],
        "hold_steps": 2,
        "id": "spring_motion",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "cabinet/close",
            "max": 0.035,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "spring_motion"
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
  "sha256": "e283e13e16297b744a4d51afb3311e3b7ba5ec72421fa2042a6838ef38edc0ab",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/panda/D8 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-panda-D8-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-everyday_robot_01-D9"></a>
## `maniskill_dynamics/everyday_robot_01/D9`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 29; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.01, "frame": "maze/board", "half": [0.035, 0.035], "object": "ball", "support": "maze/board", "tolerance": 0.006, "type": "region", "xy": [0.185, 0.115]}], "instruction": "Tilt the maze to guide the ball through the two gates to the green goal. Avoid the red trap zones and never touch the ball directly.", "milestones": [{"conditions": [{"frame": "maze/board", "high": [-0.034999999999999996, -0.09, 0.09], "low": [-0.11499999999999999, -0.17, 0.0], "object": "ball", "type": "inside"}], "hold_steps": 2, "id": "gate_0", "requires": []}, {"conditions": [{"frame": "maze/board", "high": [0.11499999999999999, 0.17, 0.09], "low": [0.034999999999999996, 0.09, 0.0], "object": "ball", "type": "inside"}], "hold_steps": 2, "id": "gate_1", "requires": ["gate_0"]}, {"conditions": [{"bottom": 0.01, "frame": "maze/board", "half": [0.035, 0.035], "object": "ball", "support": "maze/board", "tolerance": 0.006, "type": "region", "xy": [0.185, 0.115]}], "hold_steps": 2, "id": "complete", "requires": ["gate_1"]}]}
```

Native action and scoring contract:
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
        "bottom": 0.01,
        "frame": "maze/board",
        "half": [
          0.035,
          0.035
        ],
        "object": "ball",
        "support": "maze/board",
        "tolerance": 0.006,
        "type": "region",
        "xy": [
          0.185,
          0.115
        ]
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [
      {
        "conditions": [
          {
            "frame": "maze/board",
            "high": [
              -0.123,
              0.137,
              0.1
            ],
            "low": [
              -0.197,
              0.063,
              0
            ],
            "object": "ball",
            "type": "inside"
          }
        ],
        "name": "trap_-0.16"
      },
      {
        "conditions": [
          {
            "frame": "maze/board",
            "high": [
              0.197,
              -0.063,
              0.1
            ],
            "low": [
              0.123,
              -0.137,
              0
            ],
            "object": "ball",
            "type": "inside"
          }
        ],
        "name": "trap_0.16"
      }
    ],
    "held_goal_objects": [],
    "history_rules": [
      {
        "name": "direct_ball_contact",
        "objects": [
          "ball"
        ],
        "type": "no_contact"
      },
      {
        "name": "time_limit",
        "seconds": 20,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "frame": "maze/board",
            "high": [
              -0.034999999999999996,
              -0.09,
              0.09
            ],
            "low": [
              -0.11499999999999999,
              -0.17,
              0.0
            ],
            "object": "ball",
            "type": "inside"
          }
        ],
        "hold_steps": 2,
        "id": "gate_0",
        "requires": []
      },
      {
        "conditions": [
          {
            "frame": "maze/board",
            "high": [
              0.11499999999999999,
              0.17,
              0.09
            ],
            "low": [
              0.034999999999999996,
              0.09,
              0.0
            ],
            "object": "ball",
            "type": "inside"
          }
        ],
        "hold_steps": 2,
        "id": "gate_1",
        "requires": [
          "gate_0"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.01,
            "frame": "maze/board",
            "half": [
              0.035,
              0.035
            ],
            "object": "ball",
            "support": "maze/board",
            "tolerance": 0.006,
            "type": "region",
            "xy": [
              0.185,
              0.115
            ]
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "gate_1"
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
  "sha256": "abea2570defd9fb733f0542b404d04797431a255bdbd09e0134ffa5eb13211d8",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/everyday_robot_01/D9 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-everyday_robot_01-D9-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_dynamics-fetch-D10"></a>
## `maniskill_dynamics/fetch/D10`

Authoring provenance: `env/maniskill_lgd/README.md`. Action size: 13; 2400 controls / 120 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"frame": "cart/chassis", "tolerance": 0.055, "type": "frame_region", "xy": [0.65, 0.16]}, {"axis": [1, 0, 0], "frame": "cart/chassis", "tolerance": 5, "type": "frame_orientation", "world": [1, 0, 0]}, {"object": "load_box", "support": "cart/chassis", "type": "contact"}], "instruction": "Push the loaded cart into the green parking bay and stop it accurately. Keep its load upright and inside the upper tray.", "milestones": [{"conditions": [{"key": "cart/wheel0", "min": 0.08, "type": "joint_speed"}], "hold_steps": 2, "id": "wheels_rolling", "requires": []}, {"conditions": [{"frame": "cart/chassis", "tolerance": 0.055, "type": "frame_region", "xy": [0.65, 0.16]}, {"axis": [1, 0, 0], "frame": "cart/chassis", "tolerance": 5, "type": "frame_orientation", "world": [1, 0, 0]}, {"object": "load_box", "support": "cart/chassis", "type": "contact"}], "hold_steps": 2, "id": "complete", "requires": ["wheels_rolling"]}]}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.05,
    "high": [
      1.6055999994277954,
      1.5180000066757202,
      null,
      2.250999927520752,
      null,
      2.1600000858306885,
      null,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.6055999994277954,
      -1.2209999561309814,
      null,
      -2.250999927520752,
      null,
      -2.1600000858306885,
      null,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "arm.shoulder_pan_joint",
      "arm.shoulder_lift_joint",
      "arm.upperarm_roll_joint",
      "arm.elbow_flex_joint",
      "arm.forearm_roll_joint",
      "arm.wrist_flex_joint",
      "arm.wrist_roll_joint",
      "gripper[0]",
      "body.head_pan_joint",
      "body.head_tilt_joint",
      "body.torso_lift_joint",
      "base[0]",
      "base[1]"
    ],
    "neutral_action": [
      -0.3700000047683716,
      -1.031999945640564,
      0.6949999928474426,
      0.9549999833106995,
      -0.10000000149011612,
      2.0769999027252197,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'upperarm_roll_joint', 'elbow_flex_joint', 'forearm_roll_joint', 'wrist_flex_joint', 'wrist_roll_joint']; normalize_action=False; use_delta=False; native_low=[-1.6055999994277954, -1.2209999561309814, -inf, -2.250999927520752, -inf, -2.1600000858306885, -inf]; native_high=[1.6055999994277954, 1.5180000066757202, inf, 2.250999927520752, inf, 2.1600000858306885, inf]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'upperarm_roll_joint', 'elbow_flex_joint', 'forearm_roll_joint', 'wrist_flex_joint', 'wrist_roll_joint']; normalize_action=False; use_delta=False; native_low=[-1.6055999994277954, -1.2209999561309814, -inf, -2.250999927520752, -inf, -2.1600000858306885, -inf]; native_high=[1.6055999994277954, 1.5180000066757202, inf, 2.250999927520752, inf, 2.1600000858306885, inf]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'upperarm_roll_joint', 'elbow_flex_joint', 'forearm_roll_joint', 'wrist_flex_joint', 'wrist_roll_joint']; normalize_action=False; use_delta=False; native_low=[-1.6055999994277954, -1.2209999561309814, -inf, -2.250999927520752, -inf, -2.1600000858306885, -inf]; native_high=[1.6055999994277954, 1.5180000066757202, inf, 2.250999927520752, inf, 2.1600000858306885, inf]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'upperarm_roll_joint', 'elbow_flex_joint', 'forearm_roll_joint', 'wrist_flex_joint', 'wrist_roll_joint']; normalize_action=False; use_delta=False; native_low=[-1.6055999994277954, -1.2209999561309814, -inf, -2.250999927520752, -inf, -2.1600000858306885, -inf]; native_high=[1.6055999994277954, 1.5180000066757202, inf, 2.250999927520752, inf, 2.1600000858306885, inf]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'upperarm_roll_joint', 'elbow_flex_joint', 'forearm_roll_joint', 'wrist_flex_joint', 'wrist_roll_joint']; normalize_action=False; use_delta=False; native_low=[-1.6055999994277954, -1.2209999561309814, -inf, -2.250999927520752, -inf, -2.1600000858306885, -inf]; native_high=[1.6055999994277954, 1.5180000066757202, inf, 2.250999927520752, inf, 2.1600000858306885, inf]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'upperarm_roll_joint', 'elbow_flex_joint', 'forearm_roll_joint', 'wrist_flex_joint', 'wrist_roll_joint']; normalize_action=False; use_delta=False; native_low=[-1.6055999994277954, -1.2209999561309814, -inf, -2.250999927520752, -inf, -2.1600000858306885, -inf]; native_high=[1.6055999994277954, 1.5180000066757202, inf, 2.250999927520752, inf, 2.1600000858306885, inf]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "arm: PDJointPosController; joint order=['shoulder_pan_joint', 'shoulder_lift_joint', 'upperarm_roll_joint', 'elbow_flex_joint', 'forearm_roll_joint', 'wrist_flex_joint', 'wrist_roll_joint']; normalize_action=False; use_delta=False; native_low=[-1.6055999994277954, -1.2209999561309814, -inf, -2.250999927520752, -inf, -2.1600000858306885, -inf]; native_high=[1.6055999994277954, 1.5180000066757202, inf, 2.250999927520752, inf, 2.1600000858306885, inf]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "gripper: PDJointPosMimicController; joint order=['l_gripper_finger_joint', 'r_gripper_finger_joint']; normalize_action=True; use_delta=False; native_low=[-0.009999999776482582]; native_high=[0.05000000074505806]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "body: PDJointPosController; joint order=['head_pan_joint', 'head_tilt_joint', 'torso_lift_joint']; normalize_action=True; use_delta=True; native_low=[-0.10000000149011612, -0.10000000149011612, -0.10000000149011612]; native_high=[0.10000000149011612, 0.10000000149011612, 0.10000000149011612]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "body: PDJointPosController; joint order=['head_pan_joint', 'head_tilt_joint', 'torso_lift_joint']; normalize_action=True; use_delta=True; native_low=[-0.10000000149011612, -0.10000000149011612, -0.10000000149011612]; native_high=[0.10000000149011612, 0.10000000149011612, 0.10000000149011612]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "body: PDJointPosController; joint order=['head_pan_joint', 'head_tilt_joint', 'torso_lift_joint']; normalize_action=True; use_delta=True; native_low=[-0.10000000149011612, -0.10000000149011612, -0.10000000149011612]; native_high=[0.10000000149011612, 0.10000000149011612, 0.10000000149011612]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "base: PDBaseForwardVelController; joint order=['root_x_axis_joint', 'root_y_axis_joint', 'root_z_rotation_joint']; normalize_action=True; use_delta=False; native_low=[-1.0, -3.140000104904175]; native_high=[1.0, 3.140000104904175]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second.",
      "base: PDBaseForwardVelController; joint order=['root_x_axis_joint', 'root_y_axis_joint', 'root_z_rotation_joint']; normalize_action=True; use_delta=False; native_low=[-1.0, -3.140000104904175]; native_high=[1.0, 3.140000104904175]; rotational position targets use radians, prismatic position targets use metres; velocity controllers use units per second."
    ],
    "size": 13,
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
        "frame": "cart/chassis",
        "tolerance": 0.055,
        "type": "frame_region",
        "xy": [
          0.65,
          0.16
        ]
      },
      {
        "axis": [
          1,
          0,
          0
        ],
        "frame": "cart/chassis",
        "tolerance": 5,
        "type": "frame_orientation",
        "world": [
          1,
          0,
          0
        ]
      },
      {
        "object": "load_box",
        "support": "cart/chassis",
        "type": "contact"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [],
    "held_goal_objects": [],
    "history_rules": [
      {
        "degrees": 12,
        "name": "load_tipped",
        "objects": [
          "load_box"
        ],
        "type": "upright"
      },
      {
        "name": "load_left_cart",
        "objects": [
          "load_box"
        ],
        "type": "retain",
        "volume": {
          "frame": "cart/chassis",
          "high": [
            0.23,
            0.17,
            0.75
          ],
          "low": [
            -0.23,
            -0.17,
            0.415
          ]
        }
      },
      {
        "name": "time_limit",
        "seconds": 15,
        "type": "deadline"
      }
    ],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "key": "cart/wheel0",
            "min": 0.08,
            "type": "joint_speed"
          }
        ],
        "hold_steps": 2,
        "id": "wheels_rolling",
        "requires": []
      },
      {
        "conditions": [
          {
            "frame": "cart/chassis",
            "tolerance": 0.055,
            "type": "frame_region",
            "xy": [
              0.65,
              0.16
            ]
          },
          {
            "axis": [
              1,
              0,
              0
            ],
            "frame": "cart/chassis",
            "tolerance": 5,
            "type": "frame_orientation",
            "world": [
              1,
              0,
              0
            ]
          },
          {
            "object": "load_box",
            "support": "cart/chassis",
            "type": "contact"
          }
        ],
        "hold_steps": 2,
        "id": "complete",
        "requires": [
          "wheels_rolling"
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
  "sha256": "b6afc3e60f1f756ed500c2396554206f21d8ec80e6eba16d484da2e7d250580b",
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
python scripts/environment_runtime.py --task-id maniskill_dynamics/fetch/D10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_dynamics-fetch-D10-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

