# ManiSkill long horizon

[Protocol](../evaluation_protocol.en.md) · [Index](index.en.md) · [JSON](tasks.json)

Embodied Playground paper scope: Launcher uses loaded initialization only. The full 410-task paper setting has 410 groups / 1640 conditions; EP-100 has 100 / 400. This runtime schedule also includes ground and retains 510 groups / 2040 conditions. [EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.en.md)

Each task below has four trials per group at base seed 0. Parameters are private maintainer inputs. Goal strings and field names below are verbatim authoring data, not translated protocol prose.

<a id="maniskill_long_horizon-fetch-L1"></a>
## `maniskill_long_horizon/fetch/L1`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 13; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"key": "desk_drawer/slide", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.016, "frame": "desk_drawer/tray", "half": [0.075, 0.13], "object": "marker", "support": "desk_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}, {"bottom": 0.016, "frame": "desk_drawer/tray", "half": [0.095, 0.13], "object": "tape", "support": "desk_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [0.11, 0]}, {"bottom": 0.024, "frame": "book_rack", "half": [0.108, 0.111], "object": "blue_book", "support": "book_rack", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}, {"bottom": 0.024, "frame": "book_rack", "half": [0.108, 0.111], "object": "red_book", "support": "book_rack", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}, {"half": [0.29, 0.18], "type": "clear", "xy": [0.03, 0.0], "z": 0.76}], "instruction": "Clear the central writing area. Put the two books in the rear book rack and the marker and tape in the left drawer, then close the drawer. Leave the mug and remote on your colleague’s right-hand mat exactly where they are.", "milestones": [{"conditions": [{"key": "desk_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}], "id": "drawer_access", "requires": []}, {"conditions": [{"key": "desk_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}, {"bottom": 0.016, "frame": "desk_drawer/tray", "half": [0.075, 0.13], "object": "marker", "support": "desk_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}], "id": "drawer_marker", "requires": ["drawer_access"]}, {"conditions": [{"key": "desk_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}, {"bottom": 0.016, "frame": "desk_drawer/tray", "half": [0.095, 0.13], "object": "tape", "support": "desk_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [0.11, 0]}], "id": "drawer_tape", "requires": ["drawer_access"]}, {"conditions": [{"key": "desk_drawer/slide", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "drawer_closed", "requires": ["drawer_marker", "drawer_tape"]}, {"conditions": [{"bottom": 0.024, "frame": "book_rack", "half": [0.108, 0.111], "object": "blue_book", "support": "book_rack", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}], "id": "blue_book_stored", "requires": []}, {"conditions": [{"bottom": 0.024, "frame": "book_rack", "half": [0.108, 0.111], "object": "red_book", "support": "book_rack", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}], "id": "red_book_stored", "requires": []}, {"conditions": [{"half": [0.29, 0.18], "type": "clear", "xy": [0.03, 0.0], "z": 0.76}], "id": "writing_area_clear", "requires": ["blue_book_stored", "red_book_stored", "drawer_closed"]}]}
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
        "key": "desk_drawer/slide",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.016,
        "frame": "desk_drawer/tray",
        "half": [
          0.075,
          0.13
        ],
        "object": "marker",
        "support": "desk_drawer/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.12,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "desk_drawer/tray",
        "half": [
          0.095,
          0.13
        ],
        "object": "tape",
        "support": "desk_drawer/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.11,
          0
        ]
      },
      {
        "bottom": 0.024,
        "frame": "book_rack",
        "half": [
          0.108,
          0.111
        ],
        "object": "blue_book",
        "support": "book_rack",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.12,
          0
        ]
      },
      {
        "bottom": 0.024,
        "frame": "book_rack",
        "half": [
          0.108,
          0.111
        ],
        "object": "red_book",
        "support": "book_rack",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.12,
          0
        ]
      },
      {
        "half": [
          0.29,
          0.18
        ],
        "type": "clear",
        "xy": [
          0.03,
          0.0
        ],
        "z": 0.76
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
            "key": "desk_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          }
        ],
        "id": "drawer_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "desk_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "desk_drawer/tray",
            "half": [
              0.075,
              0.13
            ],
            "object": "marker",
            "support": "desk_drawer/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.12,
              0
            ]
          }
        ],
        "id": "drawer_marker",
        "requires": [
          "drawer_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "desk_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "desk_drawer/tray",
            "half": [
              0.095,
              0.13
            ],
            "object": "tape",
            "support": "desk_drawer/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.11,
              0
            ]
          }
        ],
        "id": "drawer_tape",
        "requires": [
          "drawer_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "desk_drawer/slide",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "drawer_closed",
        "requires": [
          "drawer_marker",
          "drawer_tape"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.024,
            "frame": "book_rack",
            "half": [
              0.108,
              0.111
            ],
            "object": "blue_book",
            "support": "book_rack",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.12,
              0
            ]
          }
        ],
        "id": "blue_book_stored",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.024,
            "frame": "book_rack",
            "half": [
              0.108,
              0.111
            ],
            "object": "red_book",
            "support": "book_rack",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.12,
              0
            ]
          }
        ],
        "id": "red_book_stored",
        "requires": []
      },
      {
        "conditions": [
          {
            "half": [
              0.29,
              0.18
            ],
            "type": "clear",
            "xy": [
              0.03,
              0.0
            ],
            "z": 0.76
          }
        ],
        "id": "writing_area_clear",
        "requires": [
          "blue_book_stored",
          "red_book_stored",
          "drawer_closed"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "colleague_mug",
      "colleague_remote"
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
  "sha256": "406360e58eff8f9c6c601fd110dc0288695c2566650d72c3d0ff507e0955d448",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/fetch/L1 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-fetch-L1-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-everyday_robot_09-L2"></a>
## `maniskill_long_horizon/everyday_robot_09/L2`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 30; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"key": "pantry/door", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.016, "frame": "pantry/body", "half": [0.115, 0.125], "object": "sugar", "support": "pantry/body", "tolerance": 0.016, "type": "region", "xy": [-0.125, 0]}, {"bottom": 0.016, "frame": "pantry/body", "half": [0.11, 0.12], "object": "flour", "support": "pantry/body", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}, {"key": "utensils/slide", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.016, "frame": "utensils/tray", "half": [0.09, 0.13], "object": "spoon", "support": "utensils/tray", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}, {"bottom": 0.016, "frame": "utensils/tray", "half": [0.09, 0.15], "object": "fork", "support": "utensils/tray", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}, {"key": "oven/rack0_joint", "max": 0.01, "min": -0.005, "type": "joint"}, {"key": "oven/door_joint", "max": 0.03, "min": -0.012, "type": "joint"}, {"key": "oven/knob_temp_joint", "max": 0.04, "min": -0.02, "type": "joint"}, {"key": "oven/knob_time_joint", "max": 0.04, "min": -0.02, "type": "joint"}], "instruction": "Put the sugar and flour containers in the cupboard and the spoon and fork in the utensil drawer. Retract the oven rack before closing the oven door, set both oven knobs to OFF, and close the cupboard and drawer. Leave the cooling loaf untouched.", "milestones": [{"conditions": [{"key": "pantry/door", "max": -1.0, "min": -1.61, "type": "joint"}], "id": "pantry_access", "requires": []}, {"conditions": [{"key": "pantry/door", "max": -1.0, "min": -1.61, "type": "joint"}, {"bottom": 0.016, "frame": "pantry/body", "half": [0.115, 0.125], "object": "sugar", "support": "pantry/body", "tolerance": 0.016, "type": "region", "xy": [-0.125, 0]}], "id": "pantry_sugar", "requires": ["pantry_access"]}, {"conditions": [{"key": "pantry/door", "max": -1.0, "min": -1.61, "type": "joint"}, {"bottom": 0.016, "frame": "pantry/body", "half": [0.11, 0.12], "object": "flour", "support": "pantry/body", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}], "id": "pantry_flour", "requires": ["pantry_access"]}, {"conditions": [{"key": "pantry/door", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "pantry_closed", "requires": ["pantry_sugar", "pantry_flour"]}, {"conditions": [{"key": "utensils/slide", "max": 0.32, "min": 0.24, "type": "joint"}], "id": "utensils_access", "requires": []}, {"conditions": [{"key": "utensils/slide", "max": 0.32, "min": 0.24, "type": "joint"}, {"bottom": 0.016, "frame": "utensils/tray", "half": [0.09, 0.13], "object": "spoon", "support": "utensils/tray", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}], "id": "utensils_spoon", "requires": ["utensils_access"]}, {"conditions": [{"key": "utensils/slide", "max": 0.32, "min": 0.24, "type": "joint"}, {"bottom": 0.016, "frame": "utensils/tray", "half": [0.09, 0.15], "object": "fork", "support": "utensils/tray", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}], "id": "utensils_fork", "requires": ["utensils_access"]}, {"conditions": [{"key": "utensils/slide", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "utensils_closed", "requires": ["utensils_spoon", "utensils_fork"]}, {"conditions": [{"key": "oven/door_joint", "max": 1.15, "min": 0.9, "type": "joint"}, {"key": "oven/rack0_joint", "max": 0.33, "min": 0.18, "type": "joint"}], "id": "rack_access", "requires": []}, {"conditions": [{"key": "oven/rack0_joint", "max": 0.01, "min": -0.005, "type": "joint"}, {"key": "oven/door_joint", "max": 1.15, "min": 0.7, "type": "joint"}], "id": "rack_retracted", "requires": ["rack_access"]}, {"conditions": [{"key": "oven/door_joint", "max": 0.03, "min": -0.012, "type": "joint"}], "id": "oven_closed", "requires": ["rack_retracted"]}, {"conditions": [{"key": "oven/knob_temp_joint", "max": 0.04, "min": -0.02, "type": "joint"}, {"key": "oven/knob_time_joint", "max": 0.04, "min": -0.02, "type": "joint"}], "id": "oven_off", "requires": []}]}
```

Native action and scoring contract:
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
      -1.0122119188308716,
      -2.943399429321289,
      2.3753585815429688,
      -0.9286360740661621,
      -1.4763082265853882,
      0.9050933122634888,
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
        "key": "pantry/door",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.016,
        "frame": "pantry/body",
        "half": [
          0.115,
          0.125
        ],
        "object": "sugar",
        "support": "pantry/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.125,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "pantry/body",
        "half": [
          0.11,
          0.12
        ],
        "object": "flour",
        "support": "pantry/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.12,
          0
        ]
      },
      {
        "key": "utensils/slide",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.016,
        "frame": "utensils/tray",
        "half": [
          0.09,
          0.13
        ],
        "object": "spoon",
        "support": "utensils/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.12,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "utensils/tray",
        "half": [
          0.09,
          0.15
        ],
        "object": "fork",
        "support": "utensils/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.12,
          0
        ]
      },
      {
        "key": "oven/rack0_joint",
        "max": 0.01,
        "min": -0.005,
        "type": "joint"
      },
      {
        "key": "oven/door_joint",
        "max": 0.03,
        "min": -0.012,
        "type": "joint"
      },
      {
        "key": "oven/knob_temp_joint",
        "max": 0.04,
        "min": -0.02,
        "type": "joint"
      },
      {
        "key": "oven/knob_time_joint",
        "max": 0.04,
        "min": -0.02,
        "type": "joint"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [
      {
        "conditions": [
          {
            "key": "oven/door_joint",
            "max": 0.15,
            "min": -0.01,
            "type": "joint"
          },
          {
            "key": "oven/rack0_joint",
            "max": 0.4,
            "min": 0.08,
            "type": "joint"
          }
        ],
        "name": "closed_oven_with_extended_rack"
      }
    ],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "key": "pantry/door",
            "max": -1.0,
            "min": -1.61,
            "type": "joint"
          }
        ],
        "id": "pantry_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "pantry/door",
            "max": -1.0,
            "min": -1.61,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "pantry/body",
            "half": [
              0.115,
              0.125
            ],
            "object": "sugar",
            "support": "pantry/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.125,
              0
            ]
          }
        ],
        "id": "pantry_sugar",
        "requires": [
          "pantry_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "pantry/door",
            "max": -1.0,
            "min": -1.61,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "pantry/body",
            "half": [
              0.11,
              0.12
            ],
            "object": "flour",
            "support": "pantry/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.12,
              0
            ]
          }
        ],
        "id": "pantry_flour",
        "requires": [
          "pantry_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "pantry/door",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "pantry_closed",
        "requires": [
          "pantry_sugar",
          "pantry_flour"
        ]
      },
      {
        "conditions": [
          {
            "key": "utensils/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          }
        ],
        "id": "utensils_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "utensils/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "utensils/tray",
            "half": [
              0.09,
              0.13
            ],
            "object": "spoon",
            "support": "utensils/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.12,
              0
            ]
          }
        ],
        "id": "utensils_spoon",
        "requires": [
          "utensils_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "utensils/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "utensils/tray",
            "half": [
              0.09,
              0.15
            ],
            "object": "fork",
            "support": "utensils/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.12,
              0
            ]
          }
        ],
        "id": "utensils_fork",
        "requires": [
          "utensils_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "utensils/slide",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "utensils_closed",
        "requires": [
          "utensils_spoon",
          "utensils_fork"
        ]
      },
      {
        "conditions": [
          {
            "key": "oven/door_joint",
            "max": 1.15,
            "min": 0.9,
            "type": "joint"
          },
          {
            "key": "oven/rack0_joint",
            "max": 0.33,
            "min": 0.18,
            "type": "joint"
          }
        ],
        "id": "rack_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "oven/rack0_joint",
            "max": 0.01,
            "min": -0.005,
            "type": "joint"
          },
          {
            "key": "oven/door_joint",
            "max": 1.15,
            "min": 0.7,
            "type": "joint"
          }
        ],
        "id": "rack_retracted",
        "requires": [
          "rack_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "oven/door_joint",
            "max": 0.03,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "oven_closed",
        "requires": [
          "rack_retracted"
        ]
      },
      {
        "conditions": [
          {
            "key": "oven/knob_temp_joint",
            "max": 0.04,
            "min": -0.02,
            "type": "joint"
          },
          {
            "key": "oven/knob_time_joint",
            "max": 0.04,
            "min": -0.02,
            "type": "joint"
          }
        ],
        "id": "oven_off",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "cooling_loaf"
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
  "sha256": "077dfe337c9836dce70f018fabac21383890788aaaaec65670b6369ddcb50e3a",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/everyday_robot_09/L2 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-everyday_robot_09-L2-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-fetch-L3"></a>
## `maniskill_long_horizon/fetch/L3`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 13; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"key": "mug_cupboard/door", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.8, "half": [0.085, 0.12], "object": "mug_one", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [-0.29, -0.04]}, {"bottom": 0.8, "half": [0.085, 0.12], "object": "mug_two", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.29, -0.04]}, {"key": "spoon_drawer/slide", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.8, "half": [0.085, 0.12], "object": "spoon_one", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [-0.1, -0.06]}, {"bottom": 0.8, "half": [0.085, 0.12], "object": "spoon_two", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.48, -0.06]}, {"bottom": 0.024, "frame": "book_rest", "half": [0.105, 0.108], "object": "reading_book", "support": "book_rest", "tolerance": 0.016, "type": "region", "xy": [0, 0]}, {"axis": [0, 0, 1], "object": "mug_one", "tolerance": 12, "type": "orientation", "world": [0, 0, 1]}, {"axis": [0, 0, 1], "object": "mug_two", "tolerance": 12, "type": "orientation", "world": [0, 0, 1]}], "instruction": "Take two mugs from the rear cupboard and two spoons from the drawer. Move the book off the serving area, arrange one mug and one spoon at each of the two front settings, and close both storage units. Leave the third setting at the back right undisturbed.", "milestones": [{"conditions": [{"key": "mug_cupboard/door", "max": -1, "min": -1.61, "type": "joint"}], "id": "mugs_access", "requires": []}, {"conditions": [{"key": "mug_cupboard/door", "max": -1, "min": -1.61, "type": "joint"}, {"bottom": 0.8, "half": [0.085, 0.12], "object": "mug_one", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [-0.29, -0.04]}], "id": "mugs_mug_one", "requires": ["mugs_access"]}, {"conditions": [{"key": "mug_cupboard/door", "max": -1, "min": -1.61, "type": "joint"}, {"bottom": 0.8, "half": [0.085, 0.12], "object": "mug_two", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.29, -0.04]}], "id": "mugs_mug_two", "requires": ["mugs_access"]}, {"conditions": [{"key": "mug_cupboard/door", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "mugs_closed", "requires": ["mugs_mug_one", "mugs_mug_two"]}, {"conditions": [{"key": "spoon_drawer/slide", "max": 0.32, "min": 0.24, "type": "joint"}], "id": "spoons_access", "requires": []}, {"conditions": [{"key": "spoon_drawer/slide", "max": 0.32, "min": 0.24, "type": "joint"}, {"bottom": 0.8, "half": [0.085, 0.12], "object": "spoon_one", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [-0.1, -0.06]}], "id": "spoons_spoon_one", "requires": ["spoons_access"]}, {"conditions": [{"key": "spoon_drawer/slide", "max": 0.32, "min": 0.24, "type": "joint"}, {"bottom": 0.8, "half": [0.085, 0.12], "object": "spoon_two", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.48, -0.06]}], "id": "spoons_spoon_two", "requires": ["spoons_access"]}, {"conditions": [{"key": "spoon_drawer/slide", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "spoons_closed", "requires": ["spoons_spoon_one", "spoons_spoon_two"]}, {"conditions": [{"bottom": 0.024, "frame": "book_rest", "half": [0.105, 0.108], "object": "reading_book", "support": "book_rest", "tolerance": 0.016, "type": "region", "xy": [0, 0]}], "id": "serving_area_cleared", "requires": []}]}
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
        "key": "mug_cupboard/door",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.8,
        "half": [
          0.085,
          0.12
        ],
        "object": "mug_one",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.29,
          -0.04
        ]
      },
      {
        "bottom": 0.8,
        "half": [
          0.085,
          0.12
        ],
        "object": "mug_two",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.29,
          -0.04
        ]
      },
      {
        "key": "spoon_drawer/slide",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.8,
        "half": [
          0.085,
          0.12
        ],
        "object": "spoon_one",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.1,
          -0.06
        ]
      },
      {
        "bottom": 0.8,
        "half": [
          0.085,
          0.12
        ],
        "object": "spoon_two",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.48,
          -0.06
        ]
      },
      {
        "bottom": 0.024,
        "frame": "book_rest",
        "half": [
          0.105,
          0.108
        ],
        "object": "reading_book",
        "support": "book_rest",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0,
          0
        ]
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "mug_one",
        "tolerance": 12,
        "type": "orientation",
        "world": [
          0,
          0,
          1
        ]
      },
      {
        "axis": [
          0,
          0,
          1
        ],
        "object": "mug_two",
        "tolerance": 12,
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
            "key": "mug_cupboard/door",
            "max": -1,
            "min": -1.61,
            "type": "joint"
          }
        ],
        "id": "mugs_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "mug_cupboard/door",
            "max": -1,
            "min": -1.61,
            "type": "joint"
          },
          {
            "bottom": 0.8,
            "half": [
              0.085,
              0.12
            ],
            "object": "mug_one",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.29,
              -0.04
            ]
          }
        ],
        "id": "mugs_mug_one",
        "requires": [
          "mugs_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "mug_cupboard/door",
            "max": -1,
            "min": -1.61,
            "type": "joint"
          },
          {
            "bottom": 0.8,
            "half": [
              0.085,
              0.12
            ],
            "object": "mug_two",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.29,
              -0.04
            ]
          }
        ],
        "id": "mugs_mug_two",
        "requires": [
          "mugs_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "mug_cupboard/door",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "mugs_closed",
        "requires": [
          "mugs_mug_one",
          "mugs_mug_two"
        ]
      },
      {
        "conditions": [
          {
            "key": "spoon_drawer/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          }
        ],
        "id": "spoons_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "spoon_drawer/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          },
          {
            "bottom": 0.8,
            "half": [
              0.085,
              0.12
            ],
            "object": "spoon_one",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.1,
              -0.06
            ]
          }
        ],
        "id": "spoons_spoon_one",
        "requires": [
          "spoons_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "spoon_drawer/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          },
          {
            "bottom": 0.8,
            "half": [
              0.085,
              0.12
            ],
            "object": "spoon_two",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.48,
              -0.06
            ]
          }
        ],
        "id": "spoons_spoon_two",
        "requires": [
          "spoons_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "spoon_drawer/slide",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "spoons_closed",
        "requires": [
          "spoons_spoon_one",
          "spoons_spoon_two"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.024,
            "frame": "book_rest",
            "half": [
              0.105,
              0.108
            ],
            "object": "reading_book",
            "support": "book_rest",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0,
              0
            ]
          }
        ],
        "id": "serving_area_cleared",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "third_mug",
      "third_spoon"
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
  "sha256": "8cd22c09d388c256d133879a799be6dd41aa67c24e45afa186fa5c72986867ad",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/fetch/L3 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-fetch-L3-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-everyday_robot_03-L4"></a>
## `maniskill_long_horizon/everyday_robot_03/L4`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 23; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.009, "frame": "repair_case/body", "half": [0.105, 0.175], "object": "phillips", "support": "repair_case/body", "tolerance": 0.016, "type": "region", "xy": [-0.19, 0]}, {"bottom": 0.009, "frame": "repair_case/body", "half": [0.11, 0.048], "object": "handle", "support": "repair_case/body", "tolerance": 0.016, "type": "region", "xy": [0.17, 0.07]}, {"bottom": 0.009, "frame": "repair_case/body", "half": [0.035, 0.035], "object": "M4_screw_1", "support": "repair_case/body", "tolerance": 0.016, "type": "region", "xy": [0.1, -0.09]}, {"bottom": 0.009, "frame": "repair_case/body", "half": [0.035, 0.035], "object": "M4_screw_2", "support": "repair_case/body", "tolerance": 0.016, "type": "region", "xy": [0.22, -0.09]}, {"key": "repair_case/lid", "max": 0.02, "min": -0.03, "type": "joint"}, {"key": "repair_case/latch", "max": 0.006, "min": -0.003, "type": "joint"}], "instruction": "Prepare a kit for replacing the loose cabinet handle: pack the Phillips screwdriver, replacement handle, and both slim M4 screws into the open repair case. Leave the drill, wrench, and larger M6 screw on the bench. Close the lid and engage the latch.", "milestones": [{"conditions": [{"key": "repair_case/lid", "max": -1.1, "min": -1.66, "type": "joint"}, {"key": "repair_case/latch", "max": 0.05, "min": 0.035, "type": "joint"}], "id": "case_access", "requires": []}, {"conditions": [{"bottom": 0.009, "frame": "repair_case/body", "half": [0.105, 0.175], "object": "phillips", "support": "repair_case/body", "tolerance": 0.016, "type": "region", "xy": [-0.19, 0]}, {"key": "repair_case/lid", "max": -0.7, "min": -1.66, "type": "joint"}], "id": "packed_phillips", "requires": ["case_access"]}, {"conditions": [{"bottom": 0.009, "frame": "repair_case/body", "half": [0.11, 0.048], "object": "handle", "support": "repair_case/body", "tolerance": 0.016, "type": "region", "xy": [0.17, 0.07]}, {"key": "repair_case/lid", "max": -0.7, "min": -1.66, "type": "joint"}], "id": "packed_handle", "requires": ["case_access"]}, {"conditions": [{"bottom": 0.009, "frame": "repair_case/body", "half": [0.035, 0.035], "object": "M4_screw_1", "support": "repair_case/body", "tolerance": 0.016, "type": "region", "xy": [0.1, -0.09]}, {"key": "repair_case/lid", "max": -0.7, "min": -1.66, "type": "joint"}], "id": "packed_M4_screw_1", "requires": ["case_access"]}, {"conditions": [{"bottom": 0.009, "frame": "repair_case/body", "half": [0.035, 0.035], "object": "M4_screw_2", "support": "repair_case/body", "tolerance": 0.016, "type": "region", "xy": [0.22, -0.09]}, {"key": "repair_case/lid", "max": -0.7, "min": -1.66, "type": "joint"}], "id": "packed_M4_screw_2", "requires": ["case_access"]}, {"conditions": [{"key": "repair_case/lid", "max": 0.02, "min": -0.03, "type": "joint"}], "id": "case_closed", "requires": ["packed_phillips", "packed_handle", "packed_M4_screw_1", "packed_M4_screw_2"]}, {"conditions": [{"key": "repair_case/latch", "max": 0.006, "min": -0.003, "type": "joint"}], "id": "case_secured", "requires": ["case_closed"]}]}
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
        "bottom": 0.009,
        "frame": "repair_case/body",
        "half": [
          0.105,
          0.175
        ],
        "object": "phillips",
        "support": "repair_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.19,
          0
        ]
      },
      {
        "bottom": 0.009,
        "frame": "repair_case/body",
        "half": [
          0.11,
          0.048
        ],
        "object": "handle",
        "support": "repair_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.17,
          0.07
        ]
      },
      {
        "bottom": 0.009,
        "frame": "repair_case/body",
        "half": [
          0.035,
          0.035
        ],
        "object": "M4_screw_1",
        "support": "repair_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.1,
          -0.09
        ]
      },
      {
        "bottom": 0.009,
        "frame": "repair_case/body",
        "half": [
          0.035,
          0.035
        ],
        "object": "M4_screw_2",
        "support": "repair_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.22,
          -0.09
        ]
      },
      {
        "key": "repair_case/lid",
        "max": 0.02,
        "min": -0.03,
        "type": "joint"
      },
      {
        "key": "repair_case/latch",
        "max": 0.006,
        "min": -0.003,
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
            "key": "repair_case/lid",
            "max": -1.1,
            "min": -1.66,
            "type": "joint"
          },
          {
            "key": "repair_case/latch",
            "max": 0.05,
            "min": 0.035,
            "type": "joint"
          }
        ],
        "id": "case_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "repair_case/body",
            "half": [
              0.105,
              0.175
            ],
            "object": "phillips",
            "support": "repair_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.19,
              0
            ]
          },
          {
            "key": "repair_case/lid",
            "max": -0.7,
            "min": -1.66,
            "type": "joint"
          }
        ],
        "id": "packed_phillips",
        "requires": [
          "case_access"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "repair_case/body",
            "half": [
              0.11,
              0.048
            ],
            "object": "handle",
            "support": "repair_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.17,
              0.07
            ]
          },
          {
            "key": "repair_case/lid",
            "max": -0.7,
            "min": -1.66,
            "type": "joint"
          }
        ],
        "id": "packed_handle",
        "requires": [
          "case_access"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "repair_case/body",
            "half": [
              0.035,
              0.035
            ],
            "object": "M4_screw_1",
            "support": "repair_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.1,
              -0.09
            ]
          },
          {
            "key": "repair_case/lid",
            "max": -0.7,
            "min": -1.66,
            "type": "joint"
          }
        ],
        "id": "packed_M4_screw_1",
        "requires": [
          "case_access"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "repair_case/body",
            "half": [
              0.035,
              0.035
            ],
            "object": "M4_screw_2",
            "support": "repair_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.22,
              -0.09
            ]
          },
          {
            "key": "repair_case/lid",
            "max": -0.7,
            "min": -1.66,
            "type": "joint"
          }
        ],
        "id": "packed_M4_screw_2",
        "requires": [
          "case_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "repair_case/lid",
            "max": 0.02,
            "min": -0.03,
            "type": "joint"
          }
        ],
        "id": "case_closed",
        "requires": [
          "packed_phillips",
          "packed_handle",
          "packed_M4_screw_1",
          "packed_M4_screw_2"
        ]
      },
      {
        "conditions": [
          {
            "key": "repair_case/latch",
            "max": 0.006,
            "min": -0.003,
            "type": "joint"
          }
        ],
        "id": "case_secured",
        "requires": [
          "case_closed"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "drill",
      "wrench",
      "M6_screw"
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
  "sha256": "4c02e981494e8faaddb451fca76395b5df4ee43d2e79a41298831acdcdcb7796",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/everyday_robot_03/L4 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-everyday_robot_03-L4-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-fetch-L5"></a>
## `maniskill_long_horizon/fetch/L5`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 13; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"key": "cup_store/door", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.016, "frame": "cup_store/body", "half": [0.105, 0.15], "object": "clean_mug_one", "support": "cup_store/body", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}, {"bottom": 0.016, "frame": "cup_store/body", "half": [0.105, 0.15], "object": "clean_mug_two", "support": "cup_store/body", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}, {"key": "cutlery/slide", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.016, "frame": "cutlery/tray", "half": [0.105, 0.15], "object": "clean_spoon", "support": "cutlery/tray", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}, {"bottom": 0.016, "frame": "cutlery/tray", "half": [0.105, 0.15], "object": "clean_fork", "support": "cutlery/tray", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}, {"key": "dishwasher/rack1_joint", "max": 0.009, "min": -0.004, "type": "joint"}, {"key": "dishwasher/door_joint", "max": 0.025, "min": -0.01, "type": "joint"}], "instruction": "Open the dishwasher and extend its upper rack. Put both mugs in the cupboard and the spoon and fork in the drawer; leave the bowl in the lower rack. Retract the upper rack before closing the dishwasher, then close the cupboard and drawer.", "milestones": [{"conditions": [{"key": "dishwasher/door_joint", "max": 0.63, "min": 0.54, "type": "joint"}], "id": "dishwasher_open", "requires": []}, {"conditions": [{"key": "dishwasher/door_joint", "max": 0.63, "min": 0.54, "type": "joint"}, {"key": "dishwasher/rack1_joint", "max": 0.3, "min": 0.24, "type": "joint"}], "id": "upper_rack_extended", "requires": ["dishwasher_open"]}, {"conditions": [{"key": "cup_store/door", "max": -1, "min": -1.61, "type": "joint"}], "id": "cups_access", "requires": []}, {"conditions": [{"key": "cup_store/door", "max": -1, "min": -1.61, "type": "joint"}, {"bottom": 0.016, "frame": "cup_store/body", "half": [0.105, 0.15], "object": "clean_mug_one", "support": "cup_store/body", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}], "id": "cups_clean_mug_one", "requires": ["cups_access", "upper_rack_extended"]}, {"conditions": [{"key": "cup_store/door", "max": -1, "min": -1.61, "type": "joint"}, {"bottom": 0.016, "frame": "cup_store/body", "half": [0.105, 0.15], "object": "clean_mug_two", "support": "cup_store/body", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}], "id": "cups_clean_mug_two", "requires": ["cups_access", "upper_rack_extended"]}, {"conditions": [{"key": "cup_store/door", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "cups_closed", "requires": ["cups_clean_mug_one", "cups_clean_mug_two"]}, {"conditions": [{"key": "cutlery/slide", "max": 0.32, "min": 0.24, "type": "joint"}], "id": "cutlery_access", "requires": []}, {"conditions": [{"key": "cutlery/slide", "max": 0.32, "min": 0.24, "type": "joint"}, {"bottom": 0.016, "frame": "cutlery/tray", "half": [0.105, 0.15], "object": "clean_spoon", "support": "cutlery/tray", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}], "id": "cutlery_clean_spoon", "requires": ["cutlery_access", "upper_rack_extended"]}, {"conditions": [{"key": "cutlery/slide", "max": 0.32, "min": 0.24, "type": "joint"}, {"bottom": 0.016, "frame": "cutlery/tray", "half": [0.105, 0.15], "object": "clean_fork", "support": "cutlery/tray", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}], "id": "cutlery_clean_fork", "requires": ["cutlery_access", "upper_rack_extended"]}, {"conditions": [{"key": "cutlery/slide", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "cutlery_closed", "requires": ["cutlery_clean_spoon", "cutlery_clean_fork"]}, {"conditions": [{"key": "dishwasher/rack1_joint", "max": 0.009, "min": -0.004, "type": "joint"}, {"key": "dishwasher/door_joint", "max": 0.63, "min": 0.54, "type": "joint"}], "id": "upper_rack_retracted", "requires": ["cups_clean_mug_one", "cups_clean_mug_two", "cutlery_clean_spoon", "cutlery_clean_fork"]}, {"conditions": [{"key": "dishwasher/door_joint", "max": 0.025, "min": -0.01, "type": "joint"}], "id": "dishwasher_closed", "requires": ["upper_rack_retracted"]}]}
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
        "key": "cup_store/door",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.016,
        "frame": "cup_store/body",
        "half": [
          0.105,
          0.15
        ],
        "object": "clean_mug_one",
        "support": "cup_store/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.12,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "cup_store/body",
        "half": [
          0.105,
          0.15
        ],
        "object": "clean_mug_two",
        "support": "cup_store/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.12,
          0
        ]
      },
      {
        "key": "cutlery/slide",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.016,
        "frame": "cutlery/tray",
        "half": [
          0.105,
          0.15
        ],
        "object": "clean_spoon",
        "support": "cutlery/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.12,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "cutlery/tray",
        "half": [
          0.105,
          0.15
        ],
        "object": "clean_fork",
        "support": "cutlery/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.12,
          0
        ]
      },
      {
        "key": "dishwasher/rack1_joint",
        "max": 0.009,
        "min": -0.004,
        "type": "joint"
      },
      {
        "key": "dishwasher/door_joint",
        "max": 0.025,
        "min": -0.01,
        "type": "joint"
      }
    ],
    "first_violation_sticky": true,
    "forbidden": [
      {
        "conditions": [
          {
            "key": "dishwasher/door_joint",
            "max": 0.18,
            "min": -0.01,
            "type": "joint"
          },
          {
            "key": "dishwasher/rack1_joint",
            "max": 0.4,
            "min": 0.09,
            "type": "joint"
          }
        ],
        "name": "door_closed_onto_extended_rack"
      }
    ],
    "held_goal_objects": [],
    "history_rules": [],
    "linear_speed_limit_m_s": 0.025,
    "milestones": [
      {
        "conditions": [
          {
            "key": "dishwasher/door_joint",
            "max": 0.63,
            "min": 0.54,
            "type": "joint"
          }
        ],
        "id": "dishwasher_open",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "dishwasher/door_joint",
            "max": 0.63,
            "min": 0.54,
            "type": "joint"
          },
          {
            "key": "dishwasher/rack1_joint",
            "max": 0.3,
            "min": 0.24,
            "type": "joint"
          }
        ],
        "id": "upper_rack_extended",
        "requires": [
          "dishwasher_open"
        ]
      },
      {
        "conditions": [
          {
            "key": "cup_store/door",
            "max": -1,
            "min": -1.61,
            "type": "joint"
          }
        ],
        "id": "cups_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "cup_store/door",
            "max": -1,
            "min": -1.61,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "cup_store/body",
            "half": [
              0.105,
              0.15
            ],
            "object": "clean_mug_one",
            "support": "cup_store/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.12,
              0
            ]
          }
        ],
        "id": "cups_clean_mug_one",
        "requires": [
          "cups_access",
          "upper_rack_extended"
        ]
      },
      {
        "conditions": [
          {
            "key": "cup_store/door",
            "max": -1,
            "min": -1.61,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "cup_store/body",
            "half": [
              0.105,
              0.15
            ],
            "object": "clean_mug_two",
            "support": "cup_store/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.12,
              0
            ]
          }
        ],
        "id": "cups_clean_mug_two",
        "requires": [
          "cups_access",
          "upper_rack_extended"
        ]
      },
      {
        "conditions": [
          {
            "key": "cup_store/door",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "cups_closed",
        "requires": [
          "cups_clean_mug_one",
          "cups_clean_mug_two"
        ]
      },
      {
        "conditions": [
          {
            "key": "cutlery/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          }
        ],
        "id": "cutlery_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "cutlery/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "cutlery/tray",
            "half": [
              0.105,
              0.15
            ],
            "object": "clean_spoon",
            "support": "cutlery/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.12,
              0
            ]
          }
        ],
        "id": "cutlery_clean_spoon",
        "requires": [
          "cutlery_access",
          "upper_rack_extended"
        ]
      },
      {
        "conditions": [
          {
            "key": "cutlery/slide",
            "max": 0.32,
            "min": 0.24,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "cutlery/tray",
            "half": [
              0.105,
              0.15
            ],
            "object": "clean_fork",
            "support": "cutlery/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.12,
              0
            ]
          }
        ],
        "id": "cutlery_clean_fork",
        "requires": [
          "cutlery_access",
          "upper_rack_extended"
        ]
      },
      {
        "conditions": [
          {
            "key": "cutlery/slide",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "cutlery_closed",
        "requires": [
          "cutlery_clean_spoon",
          "cutlery_clean_fork"
        ]
      },
      {
        "conditions": [
          {
            "key": "dishwasher/rack1_joint",
            "max": 0.009,
            "min": -0.004,
            "type": "joint"
          },
          {
            "key": "dishwasher/door_joint",
            "max": 0.63,
            "min": 0.54,
            "type": "joint"
          }
        ],
        "id": "upper_rack_retracted",
        "requires": [
          "cups_clean_mug_one",
          "cups_clean_mug_two",
          "cutlery_clean_spoon",
          "cutlery_clean_fork"
        ]
      },
      {
        "conditions": [
          {
            "key": "dishwasher/door_joint",
            "max": 0.025,
            "min": -0.01,
            "type": "joint"
          }
        ],
        "id": "dishwasher_closed",
        "requires": [
          "upper_rack_retracted"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "lower_bowl"
    ],
    "protected_angle_tolerance_degrees": 20.0,
    "protected_joints": [
      "dishwasher/rack0_joint"
    ],
    "protected_position_tolerance_m": 0.025,
    "protected_prismatic_tolerance_m": 0.008,
    "protected_revolute_tolerance_rad": 0.045,
    "release_force_n": 0.05,
    "revolute_speed_limit_rad_s": 0.03,
    "stable_seconds": 1.0
  },
  "sha256": "6207da29993359d673f0e90530e91107e95d266d645e6f5321c3b2cc9b1b31c9",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/fetch/L5 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-fetch-L5-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-fetch-L6"></a>
## `maniskill_long_horizon/fetch/L6`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 13; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.008, "frame": "basket", "half": [0.09, 0.16], "object": "water_1", "support": "basket", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}, {"bottom": 0.008, "frame": "basket", "half": [0.09, 0.16], "object": "water_2", "support": "basket", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}, {"bottom": 0.073, "frame": "basket", "half": [0.263, 0.183], "object": "basket_divider", "support": "basket", "tolerance": 0.016, "type": "region", "xy": [0, 0]}, {"bottom": 0.097, "frame": "basket", "half": [0.13, 0.16], "object": "snack_box", "support": "basket_divider", "tolerance": 0.016, "type": "region", "xy": [-0.11, 0]}, {"bottom": 0.097, "frame": "basket", "half": [0.1, 0.13], "object": "picnic_apple", "support": "basket_divider", "tolerance": 0.016, "type": "region", "xy": [0.15, 0.02]}, {"key": "fridge/fridge_left_door_joint", "max": 0.025, "min": -0.01, "type": "joint"}, {"key": "fridge/fridge_right_door_joint", "max": 0.025, "min": -0.01, "type": "joint"}, {"key": "snack_cupboard/door", "max": 0.025, "min": -0.01, "type": "joint"}], "instruction": "Pack the two water bottles from the refrigerator into the lower layer of the basket, place the rigid divider over them, then add the snack box and apple above it. Take the snack box from the cupboard, preserve the work lunch on the separate side stand, and close both refrigerator doors and the cupboard.", "milestones": [{"conditions": [{"key": "fridge/fridge_left_door_joint", "max": 1.58, "min": 1.05, "type": "joint"}, {"key": "fridge/fridge_right_door_joint", "max": 1.58, "min": 1.05, "type": "joint"}], "id": "fridge_access", "requires": []}, {"conditions": [{"bottom": 0.008, "frame": "basket", "half": [0.09, 0.16], "object": "water_1", "support": "basket", "tolerance": 0.016, "type": "region", "xy": [-0.12, 0]}], "id": "water_1_packed", "requires": ["fridge_access"]}, {"conditions": [{"bottom": 0.008, "frame": "basket", "half": [0.09, 0.16], "object": "water_2", "support": "basket", "tolerance": 0.016, "type": "region", "xy": [0.12, 0]}], "id": "water_2_packed", "requires": ["fridge_access"]}, {"conditions": [{"bottom": 0.073, "frame": "basket", "half": [0.263, 0.183], "object": "basket_divider", "support": "basket", "tolerance": 0.016, "type": "region", "xy": [0, 0]}], "id": "divider_installed", "requires": ["water_1_packed", "water_2_packed"]}, {"conditions": [{"key": "snack_cupboard/door", "max": -1, "min": -1.61, "type": "joint"}], "id": "snack_storage_open", "requires": []}, {"conditions": [{"bottom": 0.097, "frame": "basket", "half": [0.13, 0.16], "object": "snack_box", "support": "basket_divider", "tolerance": 0.016, "type": "region", "xy": [-0.11, 0]}], "id": "snack_box_packed", "requires": ["divider_installed", "snack_storage_open"]}, {"conditions": [{"bottom": 0.097, "frame": "basket", "half": [0.1, 0.13], "object": "picnic_apple", "support": "basket_divider", "tolerance": 0.016, "type": "region", "xy": [0.15, 0.02]}], "id": "picnic_apple_packed", "requires": ["divider_installed"]}, {"conditions": [{"key": "fridge/fridge_left_door_joint", "max": 0.025, "min": -0.01, "type": "joint"}], "id": "left_fridge_closed", "requires": ["snack_box_packed", "picnic_apple_packed"]}, {"conditions": [{"key": "fridge/fridge_right_door_joint", "max": 0.025, "min": -0.01, "type": "joint"}], "id": "right_fridge_closed", "requires": ["snack_box_packed", "picnic_apple_packed"]}, {"conditions": [{"key": "snack_cupboard/door", "max": 0.025, "min": -0.01, "type": "joint"}], "id": "pantry_closed", "requires": ["snack_box_packed", "picnic_apple_packed"]}]}
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
        "bottom": 0.008,
        "frame": "basket",
        "half": [
          0.09,
          0.16
        ],
        "object": "water_1",
        "support": "basket",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.12,
          0
        ]
      },
      {
        "bottom": 0.008,
        "frame": "basket",
        "half": [
          0.09,
          0.16
        ],
        "object": "water_2",
        "support": "basket",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.12,
          0
        ]
      },
      {
        "bottom": 0.073,
        "frame": "basket",
        "half": [
          0.263,
          0.183
        ],
        "object": "basket_divider",
        "support": "basket",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0,
          0
        ]
      },
      {
        "bottom": 0.097,
        "frame": "basket",
        "half": [
          0.13,
          0.16
        ],
        "object": "snack_box",
        "support": "basket_divider",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.11,
          0
        ]
      },
      {
        "bottom": 0.097,
        "frame": "basket",
        "half": [
          0.1,
          0.13
        ],
        "object": "picnic_apple",
        "support": "basket_divider",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.15,
          0.02
        ]
      },
      {
        "key": "fridge/fridge_left_door_joint",
        "max": 0.025,
        "min": -0.01,
        "type": "joint"
      },
      {
        "key": "fridge/fridge_right_door_joint",
        "max": 0.025,
        "min": -0.01,
        "type": "joint"
      },
      {
        "key": "snack_cupboard/door",
        "max": 0.025,
        "min": -0.01,
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
            "key": "fridge/fridge_left_door_joint",
            "max": 1.58,
            "min": 1.05,
            "type": "joint"
          },
          {
            "key": "fridge/fridge_right_door_joint",
            "max": 1.58,
            "min": 1.05,
            "type": "joint"
          }
        ],
        "id": "fridge_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.008,
            "frame": "basket",
            "half": [
              0.09,
              0.16
            ],
            "object": "water_1",
            "support": "basket",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.12,
              0
            ]
          }
        ],
        "id": "water_1_packed",
        "requires": [
          "fridge_access"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.008,
            "frame": "basket",
            "half": [
              0.09,
              0.16
            ],
            "object": "water_2",
            "support": "basket",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.12,
              0
            ]
          }
        ],
        "id": "water_2_packed",
        "requires": [
          "fridge_access"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.073,
            "frame": "basket",
            "half": [
              0.263,
              0.183
            ],
            "object": "basket_divider",
            "support": "basket",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0,
              0
            ]
          }
        ],
        "id": "divider_installed",
        "requires": [
          "water_1_packed",
          "water_2_packed"
        ]
      },
      {
        "conditions": [
          {
            "key": "snack_cupboard/door",
            "max": -1,
            "min": -1.61,
            "type": "joint"
          }
        ],
        "id": "snack_storage_open",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.097,
            "frame": "basket",
            "half": [
              0.13,
              0.16
            ],
            "object": "snack_box",
            "support": "basket_divider",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.11,
              0
            ]
          }
        ],
        "id": "snack_box_packed",
        "requires": [
          "divider_installed",
          "snack_storage_open"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.097,
            "frame": "basket",
            "half": [
              0.1,
              0.13
            ],
            "object": "picnic_apple",
            "support": "basket_divider",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.15,
              0.02
            ]
          }
        ],
        "id": "picnic_apple_packed",
        "requires": [
          "divider_installed"
        ]
      },
      {
        "conditions": [
          {
            "key": "fridge/fridge_left_door_joint",
            "max": 0.025,
            "min": -0.01,
            "type": "joint"
          }
        ],
        "id": "left_fridge_closed",
        "requires": [
          "snack_box_packed",
          "picnic_apple_packed"
        ]
      },
      {
        "conditions": [
          {
            "key": "fridge/fridge_right_door_joint",
            "max": 0.025,
            "min": -0.01,
            "type": "joint"
          }
        ],
        "id": "right_fridge_closed",
        "requires": [
          "snack_box_packed",
          "picnic_apple_packed"
        ]
      },
      {
        "conditions": [
          {
            "key": "snack_cupboard/door",
            "max": 0.025,
            "min": -0.01,
            "type": "joint"
          }
        ],
        "id": "pantry_closed",
        "requires": [
          "snack_box_packed",
          "picnic_apple_packed"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "work_lunch"
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
  "sha256": "134bf62547790be77eb11d70952a2ce1e3707345bbf3f8c85df68d9507cc573f",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/fetch/L6 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-fetch-L6-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-fetch-L7"></a>
## `maniskill_long_horizon/fetch/L7`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 13; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"key": "toy_drawer/slide", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.016, "frame": "toy_drawer/tray", "half": [0.06, 0.09], "object": "construction_1", "support": "toy_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [-0.16, 0]}, {"bottom": 0.016, "frame": "toy_drawer/tray", "half": [0.06, 0.09], "object": "construction_2", "support": "toy_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [0.0, 0]}, {"bottom": 0.016, "frame": "toy_drawer/tray", "half": [0.06, 0.09], "object": "construction_3", "support": "toy_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [0.16, 0]}, {"bottom": 0.764, "half": [0.105, 0.13], "object": "drawing_book", "support": "activity_mat", "tolerance": 0.016, "type": "region", "xy": [0.03, -0.06]}, {"bottom": 0.764, "half": [0.017, 0.09], "object": "colored_marker_1", "support": "activity_mat", "tolerance": 0.016, "type": "region", "xy": [0.23, -0.08]}, {"bottom": 0.764, "half": [0.017, 0.09], "object": "colored_marker_2", "support": "activity_mat", "tolerance": 0.016, "type": "region", "xy": [0.273, -0.08]}, {"bottom": 0.764, "half": [0.017, 0.09], "object": "colored_marker_3", "support": "activity_mat", "tolerance": 0.016, "type": "region", "xy": [0.316, -0.08]}], "instruction": "Set out exactly three colored markers and the drawing book on the activity mat. Put the three construction blocks in the drawer and close it. Leave the toy airplane and the extra black marker on the side shelf.", "milestones": [{"conditions": [{"key": "toy_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}], "id": "toys_access", "requires": []}, {"conditions": [{"key": "toy_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}, {"bottom": 0.016, "frame": "toy_drawer/tray", "half": [0.06, 0.09], "object": "construction_1", "support": "toy_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [-0.16, 0]}], "id": "toys_construction_1", "requires": ["toys_access"]}, {"conditions": [{"key": "toy_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}, {"bottom": 0.016, "frame": "toy_drawer/tray", "half": [0.06, 0.09], "object": "construction_2", "support": "toy_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [0.0, 0]}], "id": "toys_construction_2", "requires": ["toys_access"]}, {"conditions": [{"key": "toy_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}, {"bottom": 0.016, "frame": "toy_drawer/tray", "half": [0.06, 0.09], "object": "construction_3", "support": "toy_drawer/tray", "tolerance": 0.016, "type": "region", "xy": [0.16, 0]}], "id": "toys_construction_3", "requires": ["toys_access"]}, {"conditions": [{"key": "toy_drawer/slide", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "toys_closed", "requires": ["toys_construction_1", "toys_construction_2", "toys_construction_3"]}, {"conditions": [{"bottom": 0.764, "half": [0.105, 0.13], "object": "drawing_book", "support": "activity_mat", "tolerance": 0.016, "type": "region", "xy": [0.03, -0.06]}], "id": "drawing_book_ready", "requires": []}, {"conditions": [{"bottom": 0.764, "half": [0.017, 0.09], "object": "colored_marker_1", "support": "activity_mat", "tolerance": 0.016, "type": "region", "xy": [0.23, -0.08]}], "id": "colored_marker_1_ready", "requires": []}, {"conditions": [{"bottom": 0.764, "half": [0.017, 0.09], "object": "colored_marker_2", "support": "activity_mat", "tolerance": 0.016, "type": "region", "xy": [0.273, -0.08]}], "id": "colored_marker_2_ready", "requires": []}, {"conditions": [{"bottom": 0.764, "half": [0.017, 0.09], "object": "colored_marker_3", "support": "activity_mat", "tolerance": 0.016, "type": "region", "xy": [0.316, -0.08]}], "id": "colored_marker_3_ready", "requires": []}]}
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
        "key": "toy_drawer/slide",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.016,
        "frame": "toy_drawer/tray",
        "half": [
          0.06,
          0.09
        ],
        "object": "construction_1",
        "support": "toy_drawer/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.16,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "toy_drawer/tray",
        "half": [
          0.06,
          0.09
        ],
        "object": "construction_2",
        "support": "toy_drawer/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.0,
          0
        ]
      },
      {
        "bottom": 0.016,
        "frame": "toy_drawer/tray",
        "half": [
          0.06,
          0.09
        ],
        "object": "construction_3",
        "support": "toy_drawer/tray",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.16,
          0
        ]
      },
      {
        "bottom": 0.764,
        "half": [
          0.105,
          0.13
        ],
        "object": "drawing_book",
        "support": "activity_mat",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.03,
          -0.06
        ]
      },
      {
        "bottom": 0.764,
        "half": [
          0.017,
          0.09
        ],
        "object": "colored_marker_1",
        "support": "activity_mat",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.23,
          -0.08
        ]
      },
      {
        "bottom": 0.764,
        "half": [
          0.017,
          0.09
        ],
        "object": "colored_marker_2",
        "support": "activity_mat",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.273,
          -0.08
        ]
      },
      {
        "bottom": 0.764,
        "half": [
          0.017,
          0.09
        ],
        "object": "colored_marker_3",
        "support": "activity_mat",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.316,
          -0.08
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
            "key": "toy_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          }
        ],
        "id": "toys_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "toy_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "toy_drawer/tray",
            "half": [
              0.06,
              0.09
            ],
            "object": "construction_1",
            "support": "toy_drawer/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.16,
              0
            ]
          }
        ],
        "id": "toys_construction_1",
        "requires": [
          "toys_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "toy_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "toy_drawer/tray",
            "half": [
              0.06,
              0.09
            ],
            "object": "construction_2",
            "support": "toy_drawer/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.0,
              0
            ]
          }
        ],
        "id": "toys_construction_2",
        "requires": [
          "toys_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "toy_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          },
          {
            "bottom": 0.016,
            "frame": "toy_drawer/tray",
            "half": [
              0.06,
              0.09
            ],
            "object": "construction_3",
            "support": "toy_drawer/tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.16,
              0
            ]
          }
        ],
        "id": "toys_construction_3",
        "requires": [
          "toys_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "toy_drawer/slide",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "toys_closed",
        "requires": [
          "toys_construction_1",
          "toys_construction_2",
          "toys_construction_3"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.764,
            "half": [
              0.105,
              0.13
            ],
            "object": "drawing_book",
            "support": "activity_mat",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.03,
              -0.06
            ]
          }
        ],
        "id": "drawing_book_ready",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.764,
            "half": [
              0.017,
              0.09
            ],
            "object": "colored_marker_1",
            "support": "activity_mat",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.23,
              -0.08
            ]
          }
        ],
        "id": "colored_marker_1_ready",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.764,
            "half": [
              0.017,
              0.09
            ],
            "object": "colored_marker_2",
            "support": "activity_mat",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.273,
              -0.08
            ]
          }
        ],
        "id": "colored_marker_2_ready",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.764,
            "half": [
              0.017,
              0.09
            ],
            "object": "colored_marker_3",
            "support": "activity_mat",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.316,
              -0.08
            ]
          }
        ],
        "id": "colored_marker_3_ready",
        "requires": []
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "airplane",
      "black_marker"
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
  "sha256": "65bd0e4c65f3ba82499f638b59c0a1bf3f8205c67d67e8734b46321ecc28a91e",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/fetch/L7 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-fetch-L7-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-fetch-L8"></a>
## `maniskill_long_horizon/fetch/L8`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 13; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.84, "half": [0.114, 0.114], "object": "matching_saucer", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.27, 0.07]}, {"bottom": 0.858, "half": [0.095, 0.095], "object": "large_planter", "support": "matching_saucer", "tolerance": 0.016, "type": "region", "xy": [0.27, 0.07]}, {"bottom": 0.84, "half": [0.064, 0.06], "object": "soil_container", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.64, 0.06]}, {"key": "garden_drawer/slide", "max": 0.012, "min": -0.012, "type": "joint"}, {"bottom": 0.84, "half": [0.05, 0.132], "object": "scoop", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.48, 0.04]}, {"bottom": 0.024, "frame": "garden_shelf", "half": [0.087, 0.108], "object": "spare_saucer_1", "support": "garden_shelf", "tolerance": 0.016, "type": "region", "xy": [-0.16, 0]}, {"bottom": 0.024, "frame": "garden_shelf", "half": [0.087, 0.108], "object": "spare_saucer_2", "support": "garden_shelf", "tolerance": 0.016, "type": "region", "xy": [0.12000000000000002, 0]}, {"half": [0.075, 0.095], "type": "clear", "xy": [-0.01, 0.12], "z": 0.84}], "instruction": "Choose the planter that leaves space around the seedling pot, place it on its matching saucer, and set the scoop and sealed soil container beside the clear central work area. Put the two spare saucers on the rear shelf. Leave the existing potted plant and the small seedling pot undisturbed.", "milestones": [{"conditions": [{"bottom": 0.84, "half": [0.114, 0.114], "object": "matching_saucer", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.27, 0.07]}], "id": "matching_saucer_selected", "requires": []}, {"conditions": [{"bottom": 0.858, "half": [0.095, 0.095], "object": "large_planter", "support": "matching_saucer", "tolerance": 0.016, "type": "region", "xy": [0.27, 0.07]}], "id": "fitting_planter_selected", "requires": ["matching_saucer_selected"]}, {"conditions": [{"bottom": 0.84, "half": [0.064, 0.06], "object": "soil_container", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.64, 0.06]}], "id": "soil_ready", "requires": []}, {"conditions": [{"key": "garden_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}], "id": "scoop_access", "requires": []}, {"conditions": [{"key": "garden_drawer/slide", "max": 0.32, "min": 0.23, "type": "joint"}, {"bottom": 0.84, "half": [0.05, 0.132], "object": "scoop", "support": "worktop", "tolerance": 0.016, "type": "region", "xy": [0.48, 0.04]}], "id": "scoop_scoop", "requires": ["scoop_access"]}, {"conditions": [{"key": "garden_drawer/slide", "max": 0.012, "min": -0.012, "type": "joint"}], "id": "scoop_closed", "requires": ["scoop_scoop"]}, {"conditions": [{"bottom": 0.024, "frame": "garden_shelf", "half": [0.087, 0.108], "object": "spare_saucer_1", "support": "garden_shelf", "tolerance": 0.016, "type": "region", "xy": [-0.16, 0]}], "id": "spare_saucer_1_stored", "requires": []}, {"conditions": [{"bottom": 0.024, "frame": "garden_shelf", "half": [0.087, 0.108], "object": "spare_saucer_2", "support": "garden_shelf", "tolerance": 0.016, "type": "region", "xy": [0.12000000000000002, 0]}], "id": "spare_saucer_2_stored", "requires": []}, {"conditions": [{"half": [0.075, 0.095], "type": "clear", "xy": [-0.01, 0.12], "z": 0.84}], "id": "workspace_clear", "requires": ["spare_saucer_1_stored", "spare_saucer_2_stored"]}]}
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
        "bottom": 0.84,
        "half": [
          0.114,
          0.114
        ],
        "object": "matching_saucer",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.27,
          0.07
        ]
      },
      {
        "bottom": 0.858,
        "half": [
          0.095,
          0.095
        ],
        "object": "large_planter",
        "support": "matching_saucer",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.27,
          0.07
        ]
      },
      {
        "bottom": 0.84,
        "half": [
          0.064,
          0.06
        ],
        "object": "soil_container",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.64,
          0.06
        ]
      },
      {
        "key": "garden_drawer/slide",
        "max": 0.012,
        "min": -0.012,
        "type": "joint"
      },
      {
        "bottom": 0.84,
        "half": [
          0.05,
          0.132
        ],
        "object": "scoop",
        "support": "worktop",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.48,
          0.04
        ]
      },
      {
        "bottom": 0.024,
        "frame": "garden_shelf",
        "half": [
          0.087,
          0.108
        ],
        "object": "spare_saucer_1",
        "support": "garden_shelf",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.16,
          0
        ]
      },
      {
        "bottom": 0.024,
        "frame": "garden_shelf",
        "half": [
          0.087,
          0.108
        ],
        "object": "spare_saucer_2",
        "support": "garden_shelf",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.12000000000000002,
          0
        ]
      },
      {
        "half": [
          0.075,
          0.095
        ],
        "type": "clear",
        "xy": [
          -0.01,
          0.12
        ],
        "z": 0.84
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
            "bottom": 0.84,
            "half": [
              0.114,
              0.114
            ],
            "object": "matching_saucer",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.27,
              0.07
            ]
          }
        ],
        "id": "matching_saucer_selected",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.858,
            "half": [
              0.095,
              0.095
            ],
            "object": "large_planter",
            "support": "matching_saucer",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.27,
              0.07
            ]
          }
        ],
        "id": "fitting_planter_selected",
        "requires": [
          "matching_saucer_selected"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.84,
            "half": [
              0.064,
              0.06
            ],
            "object": "soil_container",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.64,
              0.06
            ]
          }
        ],
        "id": "soil_ready",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "garden_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          }
        ],
        "id": "scoop_access",
        "requires": []
      },
      {
        "conditions": [
          {
            "key": "garden_drawer/slide",
            "max": 0.32,
            "min": 0.23,
            "type": "joint"
          },
          {
            "bottom": 0.84,
            "half": [
              0.05,
              0.132
            ],
            "object": "scoop",
            "support": "worktop",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.48,
              0.04
            ]
          }
        ],
        "id": "scoop_scoop",
        "requires": [
          "scoop_access"
        ]
      },
      {
        "conditions": [
          {
            "key": "garden_drawer/slide",
            "max": 0.012,
            "min": -0.012,
            "type": "joint"
          }
        ],
        "id": "scoop_closed",
        "requires": [
          "scoop_scoop"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.024,
            "frame": "garden_shelf",
            "half": [
              0.087,
              0.108
            ],
            "object": "spare_saucer_1",
            "support": "garden_shelf",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.16,
              0
            ]
          }
        ],
        "id": "spare_saucer_1_stored",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.024,
            "frame": "garden_shelf",
            "half": [
              0.087,
              0.108
            ],
            "object": "spare_saucer_2",
            "support": "garden_shelf",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.12000000000000002,
              0
            ]
          }
        ],
        "id": "spare_saucer_2_stored",
        "requires": []
      },
      {
        "conditions": [
          {
            "half": [
              0.075,
              0.095
            ],
            "type": "clear",
            "xy": [
              -0.01,
              0.12
            ],
            "z": 0.84
          }
        ],
        "id": "workspace_clear",
        "requires": [
          "spare_saucer_1_stored",
          "spare_saucer_2_stored"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "small_planter",
      "seedling_pot",
      "established_plant_pot"
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
  "sha256": "f374e65927e4c078ccf19186012febc962be1de4055735bfef94c7f83f71e3f7",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/fetch/L8 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-fetch-L8-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-everyday_robot_01-L9"></a>
## `maniskill_long_horizon/everyday_robot_01/L9`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 29; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.009, "frame": "camera_case/body", "half": [0.027, 0.22], "object": "divider_1", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [-0.07, 0]}, {"bottom": 0.009, "frame": "camera_case/body", "half": [0.027, 0.22], "object": "divider_2", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [0.15, 0]}, {"bottom": 0.009, "frame": "camera_case/body", "half": [0.12, 0.18], "object": "camera", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [-0.22, 0]}, {"bottom": 0.009, "frame": "camera_case/body", "half": [0.075, 0.1], "object": "lens", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [0.055, 0]}, {"bottom": 0.009, "frame": "camera_case/body", "half": [0.065, 0.06], "object": "battery_1", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [0.27, -0.07]}, {"bottom": 0.009, "frame": "camera_case/body", "half": [0.065, 0.06], "object": "battery_2", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [0.27, 0.07]}, {"bottom": 0.004, "frame": "side_mat", "half": [0.1, 0.1], "object": "rim_cloth_block", "support": "side_mat", "tolerance": 0.016, "type": "region", "xy": [0, 0]}, {"key": "camera_case/lid", "max": 0.02, "min": -0.03, "type": "joint"}, {"key": "camera_case/latch", "max": 0.006, "min": -0.003, "type": "joint"}], "instruction": "Place the two padded dividers into their slots in the camera case. Pack the camera in the wide compartment, the lens in the middle compartment, and both batteries in the small compartment. Remove the cloth block from the lid rim, put it on the side mat, then close the case and engage the latch.", "milestones": [{"conditions": [{"key": "camera_case/lid", "max": -1.1, "min": -1.66, "type": "joint"}, {"key": "camera_case/latch", "max": 0.05, "min": 0.035, "type": "joint"}], "id": "case_open", "requires": []}, {"conditions": [{"bottom": 0.009, "frame": "camera_case/body", "half": [0.027, 0.22], "object": "divider_1", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [-0.07, 0]}], "id": "divider_1_installed", "requires": ["case_open"]}, {"conditions": [{"bottom": 0.009, "frame": "camera_case/body", "half": [0.027, 0.22], "object": "divider_2", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [0.15, 0]}], "id": "divider_2_installed", "requires": ["case_open"]}, {"conditions": [{"bottom": 0.009, "frame": "camera_case/body", "half": [0.12, 0.18], "object": "camera", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [-0.22, 0]}, {"key": "camera_case/lid", "max": -0.8, "min": -1.66, "type": "joint"}], "id": "camera_packed", "requires": ["divider_1_installed", "divider_2_installed"]}, {"conditions": [{"bottom": 0.009, "frame": "camera_case/body", "half": [0.075, 0.1], "object": "lens", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [0.055, 0]}, {"key": "camera_case/lid", "max": -0.8, "min": -1.66, "type": "joint"}], "id": "lens_packed", "requires": ["divider_1_installed", "divider_2_installed"]}, {"conditions": [{"bottom": 0.009, "frame": "camera_case/body", "half": [0.065, 0.06], "object": "battery_1", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [0.27, -0.07]}, {"key": "camera_case/lid", "max": -0.8, "min": -1.66, "type": "joint"}], "id": "battery_1_packed", "requires": ["divider_1_installed", "divider_2_installed"]}, {"conditions": [{"bottom": 0.009, "frame": "camera_case/body", "half": [0.065, 0.06], "object": "battery_2", "support": "camera_case/body", "tolerance": 0.016, "type": "region", "xy": [0.27, 0.07]}, {"key": "camera_case/lid", "max": -0.8, "min": -1.66, "type": "joint"}], "id": "battery_2_packed", "requires": ["divider_1_installed", "divider_2_installed"]}, {"conditions": [{"bottom": 0.004, "frame": "side_mat", "half": [0.1, 0.1], "object": "rim_cloth_block", "support": "side_mat", "tolerance": 0.016, "type": "region", "xy": [0, 0]}], "id": "lid_rim_clear", "requires": ["case_open"]}, {"conditions": [{"key": "camera_case/lid", "max": 0.02, "min": -0.03, "type": "joint"}], "id": "case_closed", "requires": ["camera_packed", "lens_packed", "battery_1_packed", "battery_2_packed", "lid_rim_clear"]}, {"conditions": [{"key": "camera_case/latch", "max": 0.006, "min": -0.003, "type": "joint"}], "id": "latch_secured", "requires": ["case_closed"]}]}
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
        "bottom": 0.009,
        "frame": "camera_case/body",
        "half": [
          0.027,
          0.22
        ],
        "object": "divider_1",
        "support": "camera_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.07,
          0
        ]
      },
      {
        "bottom": 0.009,
        "frame": "camera_case/body",
        "half": [
          0.027,
          0.22
        ],
        "object": "divider_2",
        "support": "camera_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.15,
          0
        ]
      },
      {
        "bottom": 0.009,
        "frame": "camera_case/body",
        "half": [
          0.12,
          0.18
        ],
        "object": "camera",
        "support": "camera_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.22,
          0
        ]
      },
      {
        "bottom": 0.009,
        "frame": "camera_case/body",
        "half": [
          0.075,
          0.1
        ],
        "object": "lens",
        "support": "camera_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.055,
          0
        ]
      },
      {
        "bottom": 0.009,
        "frame": "camera_case/body",
        "half": [
          0.065,
          0.06
        ],
        "object": "battery_1",
        "support": "camera_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.27,
          -0.07
        ]
      },
      {
        "bottom": 0.009,
        "frame": "camera_case/body",
        "half": [
          0.065,
          0.06
        ],
        "object": "battery_2",
        "support": "camera_case/body",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.27,
          0.07
        ]
      },
      {
        "bottom": 0.004,
        "frame": "side_mat",
        "half": [
          0.1,
          0.1
        ],
        "object": "rim_cloth_block",
        "support": "side_mat",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0,
          0
        ]
      },
      {
        "key": "camera_case/lid",
        "max": 0.02,
        "min": -0.03,
        "type": "joint"
      },
      {
        "key": "camera_case/latch",
        "max": 0.006,
        "min": -0.003,
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
            "key": "camera_case/lid",
            "max": -1.1,
            "min": -1.66,
            "type": "joint"
          },
          {
            "key": "camera_case/latch",
            "max": 0.05,
            "min": 0.035,
            "type": "joint"
          }
        ],
        "id": "case_open",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "camera_case/body",
            "half": [
              0.027,
              0.22
            ],
            "object": "divider_1",
            "support": "camera_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.07,
              0
            ]
          }
        ],
        "id": "divider_1_installed",
        "requires": [
          "case_open"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "camera_case/body",
            "half": [
              0.027,
              0.22
            ],
            "object": "divider_2",
            "support": "camera_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.15,
              0
            ]
          }
        ],
        "id": "divider_2_installed",
        "requires": [
          "case_open"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "camera_case/body",
            "half": [
              0.12,
              0.18
            ],
            "object": "camera",
            "support": "camera_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.22,
              0
            ]
          },
          {
            "key": "camera_case/lid",
            "max": -0.8,
            "min": -1.66,
            "type": "joint"
          }
        ],
        "id": "camera_packed",
        "requires": [
          "divider_1_installed",
          "divider_2_installed"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "camera_case/body",
            "half": [
              0.075,
              0.1
            ],
            "object": "lens",
            "support": "camera_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.055,
              0
            ]
          },
          {
            "key": "camera_case/lid",
            "max": -0.8,
            "min": -1.66,
            "type": "joint"
          }
        ],
        "id": "lens_packed",
        "requires": [
          "divider_1_installed",
          "divider_2_installed"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "camera_case/body",
            "half": [
              0.065,
              0.06
            ],
            "object": "battery_1",
            "support": "camera_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.27,
              -0.07
            ]
          },
          {
            "key": "camera_case/lid",
            "max": -0.8,
            "min": -1.66,
            "type": "joint"
          }
        ],
        "id": "battery_1_packed",
        "requires": [
          "divider_1_installed",
          "divider_2_installed"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.009,
            "frame": "camera_case/body",
            "half": [
              0.065,
              0.06
            ],
            "object": "battery_2",
            "support": "camera_case/body",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.27,
              0.07
            ]
          },
          {
            "key": "camera_case/lid",
            "max": -0.8,
            "min": -1.66,
            "type": "joint"
          }
        ],
        "id": "battery_2_packed",
        "requires": [
          "divider_1_installed",
          "divider_2_installed"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.004,
            "frame": "side_mat",
            "half": [
              0.1,
              0.1
            ],
            "object": "rim_cloth_block",
            "support": "side_mat",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0,
              0
            ]
          }
        ],
        "id": "lid_rim_clear",
        "requires": [
          "case_open"
        ]
      },
      {
        "conditions": [
          {
            "key": "camera_case/lid",
            "max": 0.02,
            "min": -0.03,
            "type": "joint"
          }
        ],
        "id": "case_closed",
        "requires": [
          "camera_packed",
          "lens_packed",
          "battery_1_packed",
          "battery_2_packed",
          "lid_rim_clear"
        ]
      },
      {
        "conditions": [
          {
            "key": "camera_case/latch",
            "max": 0.006,
            "min": -0.003,
            "type": "joint"
          }
        ],
        "id": "latch_secured",
        "requires": [
          "case_closed"
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
  "sha256": "a979301e6e469009e4be6c35de764917ac0a834af99a1667418b1dabb6f473ad",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/everyday_robot_01/L9 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-everyday_robot_01-L9-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="maniskill_long_horizon-everyday_robot_09-L10"></a>
## `maniskill_long_horizon/everyday_robot_09/L10`

Authoring source: [env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json](../../env/maniskill_lgd/agentbench_maniskill/long_horizon/tasks.json). Action size: 30; 6000 controls / 300 s; wall: 3600 s.

Goal (source data):
```json
{"final": [{"bottom": 0.844, "half": [0.13, 0.102], "object": "target_book", "support": "reading_mat", "tolerance": 0.016, "type": "region", "xy": [-0.22, -0.12]}, {"bottom": 0.024, "frame": "bookcase", "half": [0.095, 0.065], "object": "small_box", "support": "bookcase", "tolerance": 0.016, "type": "region", "xy": [0.02, -0.11]}, {"bottom": 0.024, "frame": "bookcase", "half": [0.083, 0.074], "object": "shelf_mug", "support": "bookcase", "tolerance": 0.016, "type": "region", "xy": [0.24, -0.1]}], "instruction": "Retrieve the book behind the small box beside the mug and put it on the reading mat. Temporarily move the box and mug to the side tray to create access, then restore them to their original places. Leave the other book and remote undisturbed.", "milestones": [{"conditions": [{"bottom": 0.008, "frame": "side_tray", "half": [0.102, 0.1], "object": "small_box", "support": "side_tray", "tolerance": 0.016, "type": "region", "xy": [-0.1, 0]}], "id": "box_temporarily_moved", "requires": []}, {"conditions": [{"bottom": 0.008, "frame": "side_tray", "half": [0.087, 0.1], "object": "shelf_mug", "support": "side_tray", "tolerance": 0.016, "type": "region", "xy": [0.1, 0]}], "id": "mug_temporarily_moved", "requires": []}, {"conditions": [{"bottom": 0.844, "half": [0.13, 0.102], "object": "target_book", "support": "reading_mat", "tolerance": 0.016, "type": "region", "xy": [-0.22, -0.12]}], "id": "book_retrieved", "requires": ["box_temporarily_moved", "mug_temporarily_moved"]}, {"conditions": [{"bottom": 0.024, "frame": "bookcase", "half": [0.095, 0.065], "object": "small_box", "support": "bookcase", "tolerance": 0.016, "type": "region", "xy": [0.02, -0.11]}], "id": "small_box_restored", "requires": ["book_retrieved"]}, {"conditions": [{"bottom": 0.024, "frame": "bookcase", "half": [0.083, 0.074], "object": "shelf_mug", "support": "bookcase", "tolerance": 0.016, "type": "region", "xy": [0.24, -0.1]}], "id": "shelf_mug_restored", "requires": ["book_retrieved"]}]}
```

Native action and scoring contract:
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
        "bottom": 0.844,
        "half": [
          0.13,
          0.102
        ],
        "object": "target_book",
        "support": "reading_mat",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          -0.22,
          -0.12
        ]
      },
      {
        "bottom": 0.024,
        "frame": "bookcase",
        "half": [
          0.095,
          0.065
        ],
        "object": "small_box",
        "support": "bookcase",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.02,
          -0.11
        ]
      },
      {
        "bottom": 0.024,
        "frame": "bookcase",
        "half": [
          0.083,
          0.074
        ],
        "object": "shelf_mug",
        "support": "bookcase",
        "tolerance": 0.016,
        "type": "region",
        "xy": [
          0.24,
          -0.1
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
            "bottom": 0.008,
            "frame": "side_tray",
            "half": [
              0.102,
              0.1
            ],
            "object": "small_box",
            "support": "side_tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.1,
              0
            ]
          }
        ],
        "id": "box_temporarily_moved",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.008,
            "frame": "side_tray",
            "half": [
              0.087,
              0.1
            ],
            "object": "shelf_mug",
            "support": "side_tray",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.1,
              0
            ]
          }
        ],
        "id": "mug_temporarily_moved",
        "requires": []
      },
      {
        "conditions": [
          {
            "bottom": 0.844,
            "half": [
              0.13,
              0.102
            ],
            "object": "target_book",
            "support": "reading_mat",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              -0.22,
              -0.12
            ]
          }
        ],
        "id": "book_retrieved",
        "requires": [
          "box_temporarily_moved",
          "mug_temporarily_moved"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.024,
            "frame": "bookcase",
            "half": [
              0.095,
              0.065
            ],
            "object": "small_box",
            "support": "bookcase",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.02,
              -0.11
            ]
          }
        ],
        "id": "small_box_restored",
        "requires": [
          "book_retrieved"
        ]
      },
      {
        "conditions": [
          {
            "bottom": 0.024,
            "frame": "bookcase",
            "half": [
              0.083,
              0.074
            ],
            "object": "shelf_mug",
            "support": "bookcase",
            "tolerance": 0.016,
            "type": "region",
            "xy": [
              0.24,
              -0.1
            ]
          }
        ],
        "id": "shelf_mug_restored",
        "requires": [
          "book_retrieved"
        ]
      }
    ],
    "no_fall_min_height_m": 0.035,
    "prismatic_speed_limit_m_s": 0.008,
    "protected": [
      "red_book",
      "remote"
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
  "sha256": "db17b93829a4a4e7b12803eb72ac39322a1817e2cdcc1586f4ec451a44576d2b",
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
python scripts/environment_runtime.py --task-id maniskill_long_horizon/everyday_robot_09/L10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/maniskill_long_horizon-everyday_robot_09-L10-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

