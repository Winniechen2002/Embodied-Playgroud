# Kongming lock

[Protocol](../evaluation_protocol.en.md) · [Index](index.en.md) · [JSON](tasks.json)

Embodied Playground paper scope: Launcher uses loaded initialization only. The full 410-task paper setting has 410 groups / 1640 conditions; EP-100 has 100 / 400. This runtime schedule also includes ground and retains 510 groups / 2040 conditions. [EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.en.md)

Each task below has four trials per group at base seed 0. Parameters are private maintainer inputs. Goal strings and field names below are verbatim authoring data, not translated protocol prose.

<a id="kongming_lock-dual-panda-A01"></a>
## `kongming_lock/dual-panda/A01`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A01", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.9,
          -0.3,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.95,
          -0.5,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.75,
          -0.48,
          0.625
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.95,
          -0.65,
          0.7
        ],
        [
          0.0,
          -0.7071067811865476,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.8,
          -0.08,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "a4420927866d090bc9b6c4cb4e5110f44e81085f101d64e8e27532fd4a371485",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A01-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A02"></a>
## `kongming_lock/dual-panda/A02`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A02", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.9103856624426466,
          -0.30142726087799204,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "frame_x1": [
        [
          0.9776265458967653,
          -0.49630841335895826,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "frame_y0": [
        [
          0.7766444914234631,
          -0.493815667946655,
          0.625
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.9906999073089141,
          -0.6457376180727201,
          0.7
        ],
        [
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.7915919292289872,
          -0.09098000157257383,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "72f8e6eeea83511d7f65ce1458f2d559a67dd05af3fe12448e0afee74af7a8cc",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A02 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A02-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A03"></a>
## `kongming_lock/dual-panda/A03`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A03", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.8880922167940517,
          -0.2962895579770553,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "frame_x1": [
        [
          0.9204708031491072,
          -0.4998862847327873,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "frame_y0": [
        [
          0.7229749783857113,
          -0.4625312422214207,
          0.625
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.9073974417369586,
          -0.6493154894465492,
          0.7
        ],
        [
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.8076470103893619,
          -0.06841115012210547,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "09bbe479ab5a4e06255ebd4f35ec3d0d201cc3c6f43032ce4350d3103510f01e",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A03-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A04"></a>
## `kongming_lock/dual-panda/A04`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A04", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.9240560039025206,
          -0.23071269037027628,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "frame_x1": [
        [
          1.0080260270865171,
          -0.4189918320893714,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "frame_y0": [
        [
          0.8075915129307369,
          -0.4340253125625133,
          0.625
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          1.034073253736557,
          -0.5667129950412025,
          0.7
        ],
        [
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.7873726295145752,
          -0.031419802474283595,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "63af955ade912a1b1c163b79c76dff0767661689047abf2f9fcd4f1e6d5b4b64",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A04 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A04-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A05"></a>
## `kongming_lock/dual-panda/A05`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A05", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.8698670973023626,
          -0.36017196143704844,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "frame_x1": [
        [
          0.8843778494195867,
          -0.5658159209228366,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "frame_y0": [
        [
          0.6908892623704839,
          -0.5113901303292063,
          0.625
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.8583306227695472,
          -0.7135370838746679,
          0.7
        ],
        [
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.8095889210878664,
          -0.1261494380076697,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "1940fde65a92ef02e8ecd86ab8b3bbb3f61795f84d7a9824f7be30b4e148b6de",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A05 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A05-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A06"></a>
## `kongming_lock/dual-panda/A06`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A06", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "61c7a93d0c8b5b8f0f605cfb0bf07aba4c4edfd91125a4df5a649a9a5db29a68",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A06 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A06-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A07"></a>
## `kongming_lock/dual-panda/A07`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A07", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "6e8288e01619465d8c2b669417ea9c449c7754a51d1e59fa741efc3c4295080e",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A07-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A08"></a>
## `kongming_lock/dual-panda/A08`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A08", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "4ccf9ed862c5930618e76971cd1e41889c98a7e8245de53fc449c9ed9c29e18b",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A08-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A09"></a>
## `kongming_lock/dual-panda/A09`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A09", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "4b38b533cbcb0507bc5728d752fccb61df320d39b5dd55dc9a309699823a7594",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A09-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A10"></a>
## `kongming_lock/dual-panda/A10`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A10", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "a8ac28f26be2a74b258417a5be46c2e1c1bb9dce4ee236eb4398e8355e63794f",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A10-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A11"></a>
## `kongming_lock/dual-panda/A11`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A11", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.95,
          -0.65,
          0.7
        ],
        [
          0.0,
          -0.7071067811865476,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "89ff98b01b9093101ca90b0e16f850b2cbced144cd874f4d86927e37c5a5f1b4",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A11 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A11-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A12"></a>
## `kongming_lock/dual-panda/A12`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A12", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.9906999073089141,
          -0.6457376180727201,
          0.7
        ],
        [
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "92d3a9ba0d2fef5f43c9dc9e539b88df840f4a544ebaba26aa99ea0c836fd3aa",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A12 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A12-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A13"></a>
## `kongming_lock/dual-panda/A13`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A13", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.9073974417369586,
          -0.6493154894465492,
          0.7
        ],
        [
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "6f36611a162c49766d77a576fe138a3a78a32f7d1aaa0a1dfdd065c11efc6eac",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A13 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A13-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A14"></a>
## `kongming_lock/dual-panda/A14`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A14", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          1.034073253736557,
          -0.5667129950412025,
          0.7
        ],
        [
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "8e92a5a719fe93e1b7359077ff94f24d0ef62b6be57e6c364eb9a4e6a5293389",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A14-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-A15"></a>
## `kongming_lock/dual-panda/A15`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A15", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.8583306227695472,
          -0.7135370838746679,
          0.7
        ],
        [
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "461e5e5746c4067b89749c0061bbc2a8305c9703a6114fba5334d4d45d06a2d0",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/A15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-A15-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D01"></a>
## `kongming_lock/dual-panda/D01`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D01", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.9,
          -0.3,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.95,
          -0.5,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.75,
          -0.48,
          0.625
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.95,
          -0.65,
          0.7
        ],
        [
          0.0,
          -0.7071067811865476,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.8,
          -0.08,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "9473bd0ce2269c66270d646cf9d19b0dd0fb0afca57dbd747a45fc92d3ca941a",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D01-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D02"></a>
## `kongming_lock/dual-panda/D02`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D02", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.9103856624426466,
          -0.30142726087799204,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "frame_x1": [
        [
          0.9776265458967653,
          -0.49630841335895826,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "frame_y0": [
        [
          0.7766444914234631,
          -0.493815667946655,
          0.625
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.9906999073089141,
          -0.6457376180727201,
          0.7
        ],
        [
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.7915919292289872,
          -0.09098000157257383,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "6ca2a44ea45734685f5095e11d77431a5a910314b8c10d8ec9a921b577e1a8cc",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D02 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D02-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D03"></a>
## `kongming_lock/dual-panda/D03`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D03", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.8880922167940517,
          -0.2962895579770553,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "frame_x1": [
        [
          0.9204708031491072,
          -0.4998862847327873,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "frame_y0": [
        [
          0.7229749783857113,
          -0.4625312422214207,
          0.625
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.9073974417369586,
          -0.6493154894465492,
          0.7
        ],
        [
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.8076470103893619,
          -0.06841115012210547,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "66e22f8d7485b9ea5c6a6dbb65956b3fc808b1c36688f2bc51aca93529e609f0",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D03-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D04"></a>
## `kongming_lock/dual-panda/D04`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D04", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.9240560039025206,
          -0.23071269037027628,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "frame_x1": [
        [
          1.0080260270865171,
          -0.4189918320893714,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "frame_y0": [
        [
          0.8075915129307369,
          -0.4340253125625133,
          0.625
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          1.034073253736557,
          -0.5667129950412025,
          0.7
        ],
        [
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.7873726295145752,
          -0.031419802474283595,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "4c363137d5a831d47c86b6f688a1dab74dc63c9524bd2f91abc555decc8d4240",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D04 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D04-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D05"></a>
## `kongming_lock/dual-panda/D05`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D05", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.8698670973023626,
          -0.36017196143704844,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "frame_x1": [
        [
          0.8843778494195867,
          -0.5658159209228366,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "frame_y0": [
        [
          0.6908892623704839,
          -0.5113901303292063,
          0.625
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.8583306227695472,
          -0.7135370838746679,
          0.7
        ],
        [
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.8095889210878664,
          -0.1261494380076697,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "f94fe386e73d0bbefa5d9d8597a8ca2412d2747880b6173e408b923ba9f2db9d",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D05 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D05-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D06"></a>
## `kongming_lock/dual-panda/D06`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D06", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "8fa5fdf2f420414a35c2e8c3edff1dad2f8c01a54d09ae3877ee173c69716f9f",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D06 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D06-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D07"></a>
## `kongming_lock/dual-panda/D07`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D07", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "dd844fd181a71a9c213e47ae3c1fd247574ec3a9559154ca77f2c39acb3f9e55",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D07-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D08"></a>
## `kongming_lock/dual-panda/D08`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D08", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "29f2191ad7dcc756198ceab310c448d03a3313a98d290ae4abf632ba5db935b3",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D08-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D09"></a>
## `kongming_lock/dual-panda/D09`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D09", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "8c83e0bf8c8e6c25849f3a893fc7751c446cbf03a8a622e1bb1398af8b2fe346",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D09-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D10"></a>
## `kongming_lock/dual-panda/D10`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D10", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "faa4ca480b801c0b352108c69c137991c6836a742957f50528739985142cd1f0",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D10-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D11"></a>
## `kongming_lock/dual-panda/D11`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D11", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.95,
          -0.65,
          0.7
        ],
        [
          0.0,
          -0.7071067811865476,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "44c1e78446046326b69278faedc6b9da913058fa31252b3319ffab468cb99f70",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D11 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D11-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D12"></a>
## `kongming_lock/dual-panda/D12`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D12", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.9906999073089141,
          -0.6457376180727201,
          0.7
        ],
        [
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "60b18e98fb27a5dafc0c6d08209469280c5b27127894294fc225ebef244bf4e7",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D12 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D12-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D13"></a>
## `kongming_lock/dual-panda/D13`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D13", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.9073974417369586,
          -0.6493154894465492,
          0.7
        ],
        [
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "acf80f117ef1095c8d0cf16d04b46defd99923fb1223422872b1520a193f95a7",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D13 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D13-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D14"></a>
## `kongming_lock/dual-panda/D14`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D14", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          1.034073253736557,
          -0.5667129950412025,
          0.7
        ],
        [
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "a203b27e696d7b221a8ab445d9a7b80e3d7fcb13296d7df5d10b8055fe8be492",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D14-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-panda-D15"></a>
## `kongming_lock/dual-panda/D15`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 16; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D15", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      7.354599952697754,
      1.0
    ],
    "low": [
      -7.354599952697754,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.174999952316284,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left.panda_joint1",
      "left.panda_joint2",
      "left.panda_joint3",
      "left.panda_joint4",
      "left.panda_joint5",
      "left.panda_joint6",
      "left.panda_joint7",
      "left.gripper",
      "right.panda_joint1",
      "right.panda_joint2",
      "right.panda_joint3",
      "right.panda_joint4",
      "right.panda_joint5",
      "right.panda_joint6",
      "right.panda_joint7",
      "right.gripper"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Seven arm targets per side: q=default_q+0.5*action.",
      "Eighth coordinate is continuous: each finger target is 0.02*(action+1) m."
    ],
    "size": 16,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_open_min_m": 0.035,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.8583306227695472,
          -0.7135370838746679,
          0.7
        ],
        [
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "778383c1bef49328f2c8acea170b2922c0cbff7e3be4ee019db7eb88f7633445",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-panda/D15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-panda-D15-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A01"></a>
## `kongming_lock/dual-floating-sharpa/A01`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A01", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.9,
          -0.3,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.95,
          -0.5,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.75,
          -0.48,
          0.625
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.95,
          -0.65,
          0.7
        ],
        [
          0.0,
          -0.7071067811865476,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.8,
          -0.08,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "60cf2386c3c3cdbe225c5edf3ad41d722ead77305784a0926dd292921347e357",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A01-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A02"></a>
## `kongming_lock/dual-floating-sharpa/A02`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A02", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.9103856624426466,
          -0.30142726087799204,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "frame_x1": [
        [
          0.9776265458967653,
          -0.49630841335895826,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "frame_y0": [
        [
          0.7766444914234631,
          -0.493815667946655,
          0.625
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.9906999073089141,
          -0.6457376180727201,
          0.7
        ],
        [
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.7915919292289872,
          -0.09098000157257383,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "8d55a09e3f3713e6fce64ceecce32fa5aab0aa0eb4387d34f01d4909942c14b1",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A02 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A02-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A03"></a>
## `kongming_lock/dual-floating-sharpa/A03`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A03", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.8880922167940517,
          -0.2962895579770553,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "frame_x1": [
        [
          0.9204708031491072,
          -0.4998862847327873,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "frame_y0": [
        [
          0.7229749783857113,
          -0.4625312422214207,
          0.625
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.9073974417369586,
          -0.6493154894465492,
          0.7
        ],
        [
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.8076470103893619,
          -0.06841115012210547,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "3176f02f28389efc04f83d7b0d823aee83ddabf800529d52d36bf66bf7c12457",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A03-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A04"></a>
## `kongming_lock/dual-floating-sharpa/A04`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A04", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.9240560039025206,
          -0.23071269037027628,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "frame_x1": [
        [
          1.0080260270865171,
          -0.4189918320893714,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "frame_y0": [
        [
          0.8075915129307369,
          -0.4340253125625133,
          0.625
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          1.034073253736557,
          -0.5667129950412025,
          0.7
        ],
        [
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.7873726295145752,
          -0.031419802474283595,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "fcde7d7b2e357564e87dfbc1718e590779a5acca6ac0afb32d0570cf01c6fa7e",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A04 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A04-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A05"></a>
## `kongming_lock/dual-floating-sharpa/A05`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A05", "description": "Assemble all six wooden pieces in the marked goal regions.", "goal": "assembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.8698670973023626,
          -0.36017196143704844,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "frame_x1": [
        [
          0.8843778494195867,
          -0.5658159209228366,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "frame_y0": [
        [
          0.6908892623704839,
          -0.5113901303292063,
          0.625
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.8583306227695472,
          -0.7135370838746679,
          0.7
        ],
        [
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.8095889210878664,
          -0.1261494380076697,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "984b996591041b15e056193a0236c0837f932e12ee1a8f89f7e266951823d371",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A05 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A05-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A06"></a>
## `kongming_lock/dual-floating-sharpa/A06`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A06", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "09b6b99f8fb0e000c95d58c22ebe219e2af8815e3f8e1f47c8102b01e5f2e1df",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A06 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A06-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A07"></a>
## `kongming_lock/dual-floating-sharpa/A07`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A07", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "ff1a1338f96050e8c945efe4481ebd8620c0aacc880da608ebfedba6abfa864e",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A07-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A08"></a>
## `kongming_lock/dual-floating-sharpa/A08`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A08", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "63e421b8c5336c8147a07ea12417595f0519ab24d9178b0fdc3b146ddf1383b4",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A08-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A09"></a>
## `kongming_lock/dual-floating-sharpa/A09`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A09", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "ae39ff9318e271a6c7eafb4f38af7b53f5f8f9b0ccb7ec7f509f53f91869da36",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A09-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A10"></a>
## `kongming_lock/dual-floating-sharpa/A10`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A10", "description": "Assemble key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_only", "target_pieces": ["key"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "3764678f8610ecdfd1c258f01d312a02e30d6f93ddb257d75362f799747a5ce6",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A10-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A11"></a>
## `kongming_lock/dual-floating-sharpa/A11`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A11", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.95,
          -0.65,
          0.7
        ],
        [
          0.0,
          -0.7071067811865476,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "4c3143664bac30c4b62fe24f75b093e252a7761ad9bbbfb9c3a494b9d83e9bc4",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A11 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A11-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A12"></a>
## `kongming_lock/dual-floating-sharpa/A12`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A12", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.9906999073089141,
          -0.6457376180727201,
          0.7
        ],
        [
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "c93eb8f657e1982aba445d436d49ed3598de0afe9dc11785d3cb4b468a15de8b",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A12 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A12-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A13"></a>
## `kongming_lock/dual-floating-sharpa/A13`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A13", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.9073974417369586,
          -0.6493154894465492,
          0.7
        ],
        [
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "d9f8833b1b3dbf622f92bd5ffbf5713fd9c85caa1e141b2f475a32beb2dbb277",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A13 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A13-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A14"></a>
## `kongming_lock/dual-floating-sharpa/A14`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A14", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          1.034073253736557,
          -0.5667129950412025,
          0.7
        ],
        [
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "2cf3afba1ea141e7bd6e4fe620eb60d29e82a9cc9ef24f7c91b8152e811005b5",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A14-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-A15"></a>
## `kongming_lock/dual-floating-sharpa/A15`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "A15", "description": "Assemble key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "assembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "assemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.08,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.8583306227695472,
          -0.7135370838746679,
          0.7
        ],
        [
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.0075,
    "stable_seconds": 2.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "8ea5ce276a93885cfc9100a4c75a2f2da1c35a8fa0f720bd8f6fade330cf2b74",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/A15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-A15-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D01"></a>
## `kongming_lock/dual-floating-sharpa/D01`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D01", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.9,
          -0.3,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.95,
          -0.5,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.75,
          -0.48,
          0.625
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.95,
          -0.65,
          0.7
        ],
        [
          0.0,
          -0.7071067811865476,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.8,
          -0.08,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "d6bc241a6735dbfd9067164da8dc5b1c41cf81c46d589ed3d2747a810fc50bce",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D01-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D02"></a>
## `kongming_lock/dual-floating-sharpa/D02`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D02", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.9103856624426466,
          -0.30142726087799204,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "frame_x1": [
        [
          0.9776265458967653,
          -0.49630841335895826,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "frame_y0": [
        [
          0.7766444914234631,
          -0.493815667946655,
          0.625
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.9906999073089141,
          -0.6457376180727201,
          0.7
        ],
        [
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.7915919292289872,
          -0.09098000157257383,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "2f47ffdf3e2943d9d5079f7f3275fbd1aeb9498dc9ec8467efba828dcf00bdaa",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D02 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D02-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D03"></a>
## `kongming_lock/dual-floating-sharpa/D03`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D03", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.8880922167940517,
          -0.2962895579770553,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "frame_x1": [
        [
          0.9204708031491072,
          -0.4998862847327873,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "frame_y0": [
        [
          0.7229749783857113,
          -0.4625312422214207,
          0.625
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.9073974417369586,
          -0.6493154894465492,
          0.7
        ],
        [
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.8076470103893619,
          -0.06841115012210547,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "31ea6d2d2cab24644e35e6769b9edd11c6865513a1dd03d0a45197ba1c863a1b",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D03-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D04"></a>
## `kongming_lock/dual-floating-sharpa/D04`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D04", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.9240560039025206,
          -0.23071269037027628,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "frame_x1": [
        [
          1.0080260270865171,
          -0.4189918320893714,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "frame_y0": [
        [
          0.8075915129307369,
          -0.4340253125625133,
          0.625
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          1.034073253736557,
          -0.5667129950412025,
          0.7
        ],
        [
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.7873726295145752,
          -0.031419802474283595,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "111d50c756468232aec7a267f83c1dc52b8997fc066b79c8b8e8bb61fe32a8e6",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D04 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D04-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D05"></a>
## `kongming_lock/dual-floating-sharpa/D05`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D05", "description": "Remove and park all six wooden pieces in the marked goal regions.", "goal": "disassembled", "subtask": "complete", "target_pieces": ["frame_x0", "frame_x1", "frame_y0", "frame_y1", "frame_z0", "key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.8698670973023626,
          -0.36017196143704844,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "frame_x1": [
        [
          0.8843778494195867,
          -0.5658159209228366,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "frame_y0": [
        [
          0.6908892623704839,
          -0.5113901303292063,
          0.625
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.8583306227695472,
          -0.7135370838746679,
          0.7
        ],
        [
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.8095889210878664,
          -0.1261494380076697,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "ac3132ca210915c83a098eb60319fae0407a9b7768628c42edcd260d77334fdc",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D05 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D05-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D06"></a>
## `kongming_lock/dual-floating-sharpa/D06`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D06", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "ef0f5f0abb99ddbafc5d8b67cd053b98969acb87a10406f26dcb814ea096449f",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D06 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D06-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D07"></a>
## `kongming_lock/dual-floating-sharpa/D07`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D07", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "4edd94ab78a70ac83b24534e59aa2e0bbf7439ab060f0f93b5255d52e5012839",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D07-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D08"></a>
## `kongming_lock/dual-floating-sharpa/D08`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D08", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "312a231dcc310a50e594692fe17f8e23ef160077277a8ab744b55a76b6995a8f",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D08-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D09"></a>
## `kongming_lock/dual-floating-sharpa/D09`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D09", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "c5c5f29e4a3d11d7c3910e72ea4b509adad0d32f6b50c6088328282c0b513524",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D09-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D10"></a>
## `kongming_lock/dual-floating-sharpa/D10`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D10", "description": "Remove and park key in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_only", "target_pieces": ["key"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "d156afe20de9dde7021a2b4506d4f9d6d98e790d73426e67d50934f2f9be4235",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D10-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D11"></a>
## `kongming_lock/dual-floating-sharpa/D11`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D11", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.95,
          -0.65,
          0.7
        ],
        [
          0.0,
          -0.7071067811865476,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.55,
          -0.65,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7,
          -0.025000000000000005,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_x1": [
        [
          0.7,
          0.025,
          0.7
        ],
        [
          1.0,
          0.0,
          0.0,
          0.0
        ]
      ],
      "frame_y0": [
        [
          0.7,
          0.0,
          0.6749999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_y1": [
        [
          0.7,
          0.0,
          0.7249999999999999
        ],
        [
          0.7071067811865476,
          0.0,
          0.0,
          0.7071067811865476
        ]
      ],
      "frame_z0": [
        [
          0.6749999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ],
      "key": [
        [
          0.7249999999999999,
          0.0,
          0.7
        ],
        [
          0.7071067811865476,
          0.0,
          -0.7071067811865476,
          0.0
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "08d878c51b92c942d79ceb062bd1046ea7bbfff2b3348494245e741c2b44d11c",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D11 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D11-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D12"></a>
## `kongming_lock/dual-floating-sharpa/D12`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D12", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.9906999073089141,
          -0.6457376180727201,
          0.7
        ],
        [
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.592222028072216,
          -0.6805999151717834,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6871788935686914,
          -0.04490486745229365,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.6828211064313084,
          0.00490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.6849999999999999,
          -0.02,
          0.6749999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_y1": [
        [
          0.6849999999999999,
          -0.02,
          0.7249999999999999
        ],
        [
          0.6755902076156602,
          0.0,
          0.0,
          0.7372773368101241
        ]
      ],
      "frame_z0": [
        [
          0.6600951325477062,
          -0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7099048674522935,
          -0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "b202094c36222d478ffe66b97c47c99a53d0f105daca0ee07269307446658ad9",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D12 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D12-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D13"></a>
## `kongming_lock/dual-floating-sharpa/D13`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D13", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.9073974417369586,
          -0.6493154894465492,
          0.7
        ],
        [
          0.0308435645972319,
          -0.7064337722128922,
          0.0308435645972319,
          0.7064337722128922
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.5089195625002604,
          -0.6144531923474859,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7128211064313085,
          -0.004904867452293644,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_x1": [
        [
          0.7171788935686915,
          0.04490486745229364,
          0.7
        ],
        [
          0.9990482215818578,
          0.0,
          0.0,
          -0.043619387365336
        ]
      ],
      "frame_y0": [
        [
          0.715,
          0.02,
          0.6749999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_y1": [
        [
          0.715,
          0.02,
          0.7249999999999999
        ],
        [
          0.7372773368101241,
          0.0,
          0.0,
          0.6755902076156602
        ]
      ],
      "frame_z0": [
        [
          0.6900951325477063,
          0.022178893568691457,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ],
      "key": [
        [
          0.7399048674522936,
          0.017821106431308555,
          0.7
        ],
        [
          0.7064337722128922,
          -0.0308435645972319,
          -0.7064337722128922,
          -0.0308435645972319
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "99e288ff05dfff94651784c3e7213aa4c4f1b687087cc96bde74794a9ab34ae7",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D13 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D13-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D14"></a>
## `kongming_lock/dual-floating-sharpa/D14`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D14", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          1.034073253736557,
          -0.5667129950412025,
          0.7
        ],
        [
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.6401501525316735,
          -0.6361722661079747,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.6793412044416732,
          0.005379806174694794,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.6706587955583266,
          0.0546201938253052,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.6749999999999999,
          0.03,
          0.6749999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_y1": [
        [
          0.6749999999999999,
          0.03,
          0.7249999999999999
        ],
        [
          0.6427876096865394,
          0.0,
          0.0,
          0.766044443118978
        ]
      ],
      "frame_z0": [
        [
          0.6503798061746947,
          0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ],
      "key": [
        [
          0.699620193825305,
          0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "00edd6653e00faf511e2a12d0cf2b4cd6a92e436a90356b53e71a35e7cbdfeae",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D14-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="kongming_lock-dual-floating-sharpa-D15"></a>
## `kongming_lock/dual-floating-sharpa/D15`

Authoring source: [source/agentbench_platform/agentbench_platform/kongming_cases.py](../../source/agentbench_platform/agentbench_platform/kongming_cases.py). Action size: 56; 36000 controls / 1200 s; wall: 3600 s.

Goal (source data):
```json
{"case_id": "D15", "description": "Remove and park key, frame_y1 in the marked goal regions. Keep all other pieces in their assembled configuration.", "goal": "disassembled", "subtask": "key_plus_bar", "target_pieces": ["key", "frame_y1"], "task": "disassemble"}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813,
      2.0,
      2.0,
      2.0,
      3.1415927410125732,
      3.1415927410125732,
      3.1415927410125732,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      0.26179996132850647,
      1.5707999467849731,
      0.3490999639034271,
      1.7452999353408813,
      1.3962998390197754,
      1.919899821281433,
      0.3490999639034271,
      1.3962998390197754,
      0.3490999639034271,
      1.7452999353408813
    ],
    "low": [
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0,
      -2.0,
      -2.0,
      -2.0,
      -3.1415927410125732,
      -3.1415927410125732,
      -3.1415927410125732,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      0.0,
      -0.1745329201221466,
      -0.3490999639034271,
      0.0,
      0.0,
      -0.1745000034570694,
      -0.3490999639034271,
      -0.5235999226570129,
      -0.3490999639034271,
      0.0
    ],
    "names": [
      "left.sharpa.right_x_joint",
      "left.sharpa.right_y_joint",
      "left.sharpa.right_z_joint",
      "left.sharpa.right_roll_joint",
      "left.sharpa.right_pitch_joint",
      "left.sharpa.right_yaw_joint",
      "left.sharpa.right_index_MCP_FE",
      "left.sharpa.right_index_MCP_AA",
      "left.sharpa.right_index_PIP",
      "left.sharpa.right_index_DIP",
      "left.sharpa.right_middle_MCP_FE",
      "left.sharpa.right_middle_MCP_AA",
      "left.sharpa.right_middle_PIP",
      "left.sharpa.right_middle_DIP",
      "left.sharpa.right_ring_MCP_FE",
      "left.sharpa.right_ring_MCP_AA",
      "left.sharpa.right_ring_PIP",
      "left.sharpa.right_ring_DIP",
      "left.sharpa.right_pinky_CMC",
      "left.sharpa.right_pinky_MCP_FE",
      "left.sharpa.right_pinky_MCP_AA",
      "left.sharpa.right_pinky_PIP",
      "left.sharpa.right_pinky_DIP",
      "left.sharpa.right_thumb_CMC_FE",
      "left.sharpa.right_thumb_CMC_AA",
      "left.sharpa.right_thumb_MCP_FE",
      "left.sharpa.right_thumb_MCP_AA",
      "left.sharpa.right_thumb_IP",
      "right.sharpa.right_x_joint",
      "right.sharpa.right_y_joint",
      "right.sharpa.right_z_joint",
      "right.sharpa.right_roll_joint",
      "right.sharpa.right_pitch_joint",
      "right.sharpa.right_yaw_joint",
      "right.sharpa.right_index_MCP_FE",
      "right.sharpa.right_index_MCP_AA",
      "right.sharpa.right_index_PIP",
      "right.sharpa.right_index_DIP",
      "right.sharpa.right_middle_MCP_FE",
      "right.sharpa.right_middle_MCP_AA",
      "right.sharpa.right_middle_PIP",
      "right.sharpa.right_middle_DIP",
      "right.sharpa.right_ring_MCP_FE",
      "right.sharpa.right_ring_MCP_AA",
      "right.sharpa.right_ring_PIP",
      "right.sharpa.right_ring_DIP",
      "right.sharpa.right_pinky_CMC",
      "right.sharpa.right_pinky_MCP_FE",
      "right.sharpa.right_pinky_MCP_AA",
      "right.sharpa.right_pinky_PIP",
      "right.sharpa.right_pinky_DIP",
      "right.sharpa.right_thumb_CMC_FE",
      "right.sharpa.right_thumb_CMC_AA",
      "right.sharpa.right_thumb_MCP_FE",
      "right.sharpa.right_thumb_MCP_AA",
      "right.sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      -1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.5707963705062866,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order.",
      "Absolute native joint target in the declared left-then-right order."
    ],
    "size": 56,
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
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
    "angle_tolerance_rad": 0.25,
    "angular_speed_limit_rad_s": 0.1,
    "complete_substep_coverage": true,
    "finger_home_tolerance_rad": 0.05,
    "first_violation_sticky": true,
    "forbidden_contact_force_limit_n": 0.5,
    "goal_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.8583306227695472,
          -0.7135370838746679,
          0.7
        ],
        [
          0.06162841671621935,
          -0.7044160264027587,
          0.06162841671621935,
          0.7044160264027587
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.46440752156466414,
          -0.6440778128078957,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "initial_state": {
      "frame_x0": [
        [
          0.7206587955583267,
          -0.054620193825305204,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_x1": [
        [
          0.7293412044416733,
          -0.005379806174694798,
          0.7
        ],
        [
          0.9961946980917455,
          0.0,
          0.0,
          -0.08715574274765817
        ]
      ],
      "frame_y0": [
        [
          0.725,
          -0.03,
          0.6749999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_y1": [
        [
          0.725,
          -0.03,
          0.7249999999999999
        ],
        [
          0.766044443118978,
          0.0,
          0.0,
          0.6427876096865394
        ]
      ],
      "frame_z0": [
        [
          0.7003798061746948,
          -0.025658795558326737,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ],
      "key": [
        [
          0.7496201938253051,
          -0.03434120444167324,
          0.7
        ],
        [
          0.7044160264027587,
          -0.06162841671621935,
          -0.7044160264027587,
          -0.06162841671621935
        ]
      ]
    },
    "linear_speed_limit_m_s": 0.01,
    "penetration_limit_m": 0.002,
    "position_tolerance_m": 0.025,
    "stable_seconds": 1.0,
    "support_tolerance_m": 0.002,
    "target_pieces": [
      "key",
      "frame_y1"
    ],
    "tcp_clearance_min_m": 0.13
  },
  "sha256": "78c3952d7641ef0768bba26a3d51010213211945328560cbe396194128e9012c",
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
| 1 | 0 | nominal | `{"authored_sky_light_scale":0.85}` |
| 2 | 0 | nominal | `{"authored_sky_light_scale":0.95}` |
| 3 | 0 | nominal | `{"authored_sky_light_scale":1.05}` |
| 4 | 0 | nominal | `{"authored_sky_light_scale":1.15}` |

```bash
python scripts/environment_runtime.py --task-id kongming_lock/dual-floating-sharpa/D15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/kongming_lock-dual-floating-sharpa-D15-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

