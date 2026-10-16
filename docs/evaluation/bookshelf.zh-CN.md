# 书架

[Protocol](../evaluation_protocol.zh-CN.md) · [Index](index.zh-CN.md) · [JSON](tasks.json)

Embodied Playground 论文仅评测发射器 loaded 初态：完整 410 项为 410 组／1640 条件，EP-100 为 100 组／400 条件。本运行时清单另保留 ground，共 510 组／2040 条件。[EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.zh-CN.md)

下列每项每组四次，base seed 为 0。参数为维护者私有输入。目标字符串与字段名保留作者配置原文，不作为翻译后的协议正文。

<a id="bookshelf-dual-panda-BooksTableD1"></a>
## `bookshelf/dual-panda/BooksTableD1`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 2700 controls / 90.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Middle layer: the 3 books, standing upright and packed tightly together against one side wall. Objects present: 3 books. All objects start scattered on the desk. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "5943d314b721e1e5668f934d721f3255cb3d806e80853ef3aa4d40770e1fe4d8",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/BooksTableD1 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-BooksTableD1-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-BooksTableD2"></a>
## `bookshelf/dual-panda/BooksTableD2`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 3900 controls / 130.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Middle layer: the 5 books, standing upright and packed tightly together against one side wall. Objects present: 5 books. All objects start scattered on the desk. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "8c475362c7bad0520882a128947209a09775bdb1b0381f57e6e3bda5fa88a2b3",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/BooksTableD2 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-BooksTableD2-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-BooksTableD3"></a>
## `bookshelf/dual-panda/BooksTableD3`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 5700 controls / 190.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Middle layer: the 8 books, standing upright and packed tightly together against one side wall. Objects present: 8 books. 3 books start standing packed together in a row on the desk; the other 5 books and the remaining objects lie scattered on the desk, some on top of each other. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "ea0b71db2db56e9ac9c06b779712f701b468810c60dba48095edc4ac31cde525",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/BooksTableD3 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-BooksTableD3-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-BooksTableD4"></a>
## `bookshelf/dual-panda/BooksTableD4`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 6900 controls / 230.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Middle layer: the 10 books, standing upright and packed tightly together against the left side wall. Objects present: 10 books. 5 books start standing packed together in a row on the desk; the other 5 books and the remaining objects lie scattered on the desk, some on top of each other. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "negative_y"
  },
  "sha256": "a27efac3cbf52f5040556bad39502ee59c9d1f79727a77574fc9a46b01280ec6",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/BooksTableD4 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-BooksTableD4-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfTableD1"></a>
## `bookshelf/dual-panda/ShelfTableD1`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 5400 controls / 180.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the storage box, standing upright on the desk under the first board. The box has no handles or lid features: carry it between both hands. Middle layer: the 4 books, standing upright and packed tightly together against one side wall. Top layer: the trophy, standing upright, at least 5 cm apart and 2 cm from the side walls. Objects present: 4 books, a trophy and a storage box. All objects start scattered on the desk. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "b03326ce0c44e668656d2369ec9c1df21a0c974b295d114394d742b9691000a1",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfTableD1 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfTableD1-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfTableD2"></a>
## `bookshelf/dual-panda/ShelfTableD2`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 9300 controls / 310.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the 2 storage boxes, standing upright side by side on the desk under the first board. The boxes have no handles or lid features: carry each between both hands. Middle layer: the 6 books, standing upright and packed tightly together against one side wall. Top layer: the trophy, photo frame and desk lamp, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 6 books, a trophy, a photo frame, a desk lamp and 2 storage boxes of different sizes. 3 books start standing packed together in a row on the desk; the other 3 books and the remaining objects lie scattered on the desk. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "63d7e660068db03e584e878be4871677aef1fb473000c0039eb6b36c726f0201",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfTableD2 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfTableD2-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfTableD3"></a>
## `bookshelf/dual-panda/ShelfTableD3`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 10500 controls / 350.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the 2 storage boxes, standing upright side by side on the desk under the first board. The boxes have no handles or lid features: carry each between both hands. Middle layer: the 8 books, standing upright and packed tightly together against one side wall. Top layer: the trophy, photo frame and desk lamp, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 8 books, a trophy, a photo frame, a desk lamp and 2 storage boxes of different sizes. 3 books start standing packed together in a row on the desk; the other 5 books and the remaining objects lie scattered on the desk, some on top of each other. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "132c0df6ea38039ede04f9e857794ac44d39eb40416b1f1f1454afd8bdd4bdbd",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfTableD3 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfTableD3-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfTableD4"></a>
## `bookshelf/dual-panda/ShelfTableD4`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 11700 controls / 390.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the 2 storage boxes, standing upright side by side on the desk under the first board. The boxes have no handles or lid features: carry each between both hands. Middle layer: the 10 books, standing upright and packed tightly together against one side wall. Top layer: the photo frame, desk lamp and globe, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 10 books, a photo frame, a desk lamp, a globe and 2 storage boxes of different sizes. 5 books start standing packed together in a row on the desk; the other 5 books and the remaining objects lie scattered on the desk, some on top of each other. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "ced585b4431527b3265cec5fe757a49998342dc4fd7bc4d2450edd162c482a9b",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfTableD4 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfTableD4-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfCrateD1"></a>
## `bookshelf/dual-panda/ShelfCrateD1`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 6000 controls / 200.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the storage crate, emptied first, standing upright on the desk under the first board. The crate has no handles: hold it by its rim with both arms, or slide it over the desk. Middle layer: the 2 books, standing upright and packed tightly together against one side wall. Top layer: the trophy, standing upright, at least 5 cm apart and 2 cm from the side walls. Objects present: 2 books, a trophy and a storage crate. The shelf stands on the left half of the desk and the crate on the right half. All objects start inside the storage crate on the desk. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "04f78173fa34144347a6912365e370a32f87d22ff2d0fc1be7373046523e5d4c",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfCrateD1 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfCrateD1-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfCrateD2"></a>
## `bookshelf/dual-panda/ShelfCrateD2`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 7200 controls / 240.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the storage crate, emptied first, standing upright on the desk under the first board. The crate has no handles: hold it by its rim with both arms, or slide it over the desk. Middle layer: the 3 books, standing upright and packed tightly together against one side wall. Top layer: the trophy and photo frame, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 3 books, a trophy, a photo frame and a storage crate. The shelf stands on the left half of the desk and the crate on the right half. All objects start jumbled inside the storage crate on the desk, as they fell during the move. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "243ab171122c8fe290a5bb9daed77b51a508cd3a3be193818e81773254ced01a",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfCrateD2 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfCrateD2-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfCrateD3"></a>
## `bookshelf/dual-panda/ShelfCrateD3`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 9000 controls / 300.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the storage crate, emptied first, standing upright on the desk under the first board. The crate has no handles: hold it by its rim with both arms, or slide it over the desk. Middle layer: the 5 books, standing upright and packed tightly together against one side wall. Top layer: the potted plant, photo frame and globe, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 5 books, a potted plant, a photo frame, a globe and a storage crate. The shelf stands on the left half of the desk and the crate on the right half. All objects start jumbled inside the storage crate on the desk, as they fell during the move. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "e7bf9498d52712842d89244d757bc131d2ea7af4eb221b16ec2c4e5c6047b44a",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfCrateD3 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfCrateD3-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfCrateD4"></a>
## `bookshelf/dual-panda/ShelfCrateD4`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 10200 controls / 340.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the storage crate, emptied first, standing upright on the desk under the first board. The crate has no handles: hold it by its rim with both arms, or slide it over the desk. Middle layer: the 7 books, standing upright and packed tightly together against the right side wall. Top layer: the potted plant, photo frame and globe, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 7 books, a potted plant, a photo frame, a globe and a storage crate. The shelf stands on the left half of the desk and the crate on the right half. All objects start jumbled inside the storage crate on the desk, as they fell during the move. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "positive_y"
  },
  "sha256": "87842d18cd208fb73430c230de18edbc6708263d5a6e3a74b6c7b309d9898691",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfCrateD4 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfCrateD4-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfCrateFixD1"></a>
## `bookshelf/dual-panda/ShelfCrateFixD1`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 1500 controls / 50.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Middle layer: the 4 books, standing upright and packed tightly together against one side wall. Top layer: the trophy and photo frame, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 4 books, a trophy and a photo frame. All objects start on the shelf. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "f0c6e11030881d43d52d5b4fe5dce6a2c20fe7004adda985dba3d201df9f7208",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfCrateFixD1 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfCrateFixD1-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfCrateFixD2"></a>
## `bookshelf/dual-panda/ShelfCrateFixD2`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 7200 controls / 240.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the storage crate, emptied first, standing upright on the desk under the first board. The crate has no handles: hold it by its rim with both arms, or slide it over the desk. Middle layer: the 3 books, standing upright and packed tightly together against one side wall. Top layer: the potted plant and globe, standing upright, at least 5 cm apart and 2 cm from the side walls. Objects present: 3 books, a potted plant, a globe and a storage crate. The shelf stands on the left half of the desk and the crate on the right half. All objects start inside the storage crate on the desk. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "11d6f7adabc031b7d02631f28f657fd0e3a80ba296c87052064fd2527d255a6f",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfCrateFixD2 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfCrateFixD2-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfCrateFixD3"></a>
## `bookshelf/dual-panda/ShelfCrateFixD3`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 9000 controls / 300.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the storage crate, emptied first, standing upright on the desk under the first board. The crate has no handles: hold it by its rim with both arms, or slide it over the desk. Middle layer: the 5 books, standing upright and packed tightly together against one side wall. Top layer: the potted plant, photo frame and globe, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 5 books, a potted plant, a photo frame, a globe and a storage crate. The shelf stands on the left half of the desk and the crate on the right half. All objects start jumbled inside the storage crate on the desk, as they fell during the move. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "9e0427943bbff55ec051f0b230e09b92fb794178b53c505eac0f631a05fc3a70",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfCrateFixD3 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfCrateFixD3-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-ShelfCrateFixD4"></a>
## `bookshelf/dual-panda/ShelfCrateFixD4`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 9000 controls / 300.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the storage crate, emptied first, standing upright on the desk under the first board. The crate has no handles: hold it by its rim with both arms, or slide it over the desk. Middle layer: the 5 books, standing upright and packed tightly together against one side wall. Top layer: the potted plant, photo frame and globe, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Objects present: 5 books, a potted plant, a photo frame, a globe and a storage crate. The shelf stands on the left half of the desk and the crate on the right half. All objects start jumbled inside the storage crate on the desk, as they fell during the move. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "5de5667ed555d9aacf599a8b960e17992747140c10bd14086a4db0609ad9f77b",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/ShelfCrateFixD4 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-ShelfCrateFixD4-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-TableCleanD1"></a>
## `bookshelf/dual-panda/TableCleanD1`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 3900 controls / 130.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Middle layer: the 3 books, standing upright and packed tightly together against one side wall. Trash: the crumpled paper balls and the empty drink cans go into the waste bin standing on the floor beside the desk's left edge; nothing else goes into the bin. Objects present: 3 books and 2 pieces of trash (a crumpled paper ball and an empty drink can). All objects start scattered on the desk. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "5bb7f897970e17ccb90b568e0a257a9cd17e64f838f57c6c4f8f11273c010876",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/TableCleanD1 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-TableCleanD1-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-TableCleanD2"></a>
## `bookshelf/dual-panda/TableCleanD2`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 6900 controls / 230.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Middle layer: the 4 books, standing upright and packed tightly together against one side wall. Top layer: the trophy and photo frame, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Trash: the crumpled paper balls and the empty drink cans go into the waste bin standing on the floor beside the desk's left edge; nothing else goes into the bin. Objects present: 4 books, a trophy, a photo frame and 4 pieces of trash (2 crumpled paper balls and 2 empty drink cans). All objects start scattered on the desk. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "abc5fe95b5f4adf2896e3b994cb68f365b7c4533209ff4529ff134066992b2cd",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/TableCleanD2 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-TableCleanD2-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-TableCleanD3"></a>
## `bookshelf/dual-panda/TableCleanD3`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 12300 controls / 410.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the 2 storage boxes, standing upright side by side on the desk under the first board. The boxes have no handles or lid features: carry each between both hands. Middle layer: the 7 books, standing upright and packed tightly together against one side wall. Top layer: the trophy, photo frame and desk lamp, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Trash: the crumpled paper balls and the empty drink cans go into the waste bin standing on the floor beside the desk's left edge; nothing else goes into the bin. Objects present: 7 books, a trophy, a photo frame, a desk lamp, 2 storage boxes of different sizes and 4 pieces of trash (2 crumpled paper balls and 2 empty drink cans). 3 books start standing packed together in a row on the desk; the other 4 books and the remaining objects lie scattered on the desk, some on top of each other. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "be1fe1bed1552c8b4127cc090e2d43974908e85860b0e29c27867961a0a3583e",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/TableCleanD3 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-TableCleanD3-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="bookshelf-dual-panda-TableCleanD4"></a>
## `bookshelf/dual-panda/TableCleanD4`

作者来源：`env/organize_bookshelf/task.md`。Action size: 16; 12300 controls / 410.0 s; wall: 3600 s.

目标（源数据）：
```json
"Organize the shelf in front of you. Bottom layer: the 2 storage boxes, standing upright side by side on the desk under the first board. The boxes have no handles or lid features: carry each between both hands. Middle layer: the 7 books, standing upright and packed tightly together against one side wall. Top layer: the trophy, photo frame and desk lamp, standing upright, at least 5 cm apart and 2 cm from the side walls. The photo frame must face outward. Trash: the crumpled paper balls and the empty drink cans go into the waste bin standing on the floor beside the desk's left edge; nothing else goes into the bin. Objects present: 7 books, a trophy, a photo frame, a desk lamp, 2 storage boxes of different sizes and 4 pieces of trash (2 crumpled paper balls and 2 empty drink cans). 3 books start standing packed together in a row on the desk; the other 4 books and the remaining objects lie scattered on the desk, some on top of each other. The task is complete once every object rests released and still in its place."
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234600067138672,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
      1.0,
      7.354599952697754,
      5.085599899291992,
      5.794600009918213,
      4.560400009155273,
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
      -3.1750001907348633,
      -7.354599952697754,
      -1.0,
      -4.234600067138672,
      -1.9656000137329102,
      -5.794600009918213,
      -1.4436001777648926,
      -5.794600009918213,
      -3.1750001907348633,
      -4.234600067138672,
      -1.0
    ],
    "names": [
      "left_arm.panda_joint1",
      "left_arm.panda_joint2",
      "left_arm.panda_joint3",
      "left_arm.panda_joint4",
      "left_arm.panda_joint5",
      "left_arm.panda_joint6",
      "left_arm.panda_joint7",
      "left_gripper",
      "right_arm.panda_joint1",
      "right_arm.panda_joint2",
      "right_arm.panda_joint3",
      "right_arm.panda_joint4",
      "right_arm.panda_joint5",
      "right_arm.panda_joint6",
      "right_arm.panda_joint7",
      "right_gripper"
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
      "left_arm: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "left_gripper: negative closes, nonnegative opens",
      "right_arm: joint target = offset + scale * action; offset=[-0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, -0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "right_gripper: negative closes, nonnegative opens"
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
    "arm_speed_factor_limit": 1.1,
    "arm_speed_limit_rad_s": [
      2.175,
      2.175,
      2.175,
      2.175,
      2.61,
      2.61,
      2.61
    ],
    "book_pack_alignment_degrees": 3.0,
    "book_pack_max_gap_m": 0.006,
    "containment_tolerance_m": 0.002,
    "display_min_gap_m": 0.05,
    "display_wall_margin_m": 0.02,
    "first_violation_sticky": true,
    "frame_facing_degrees": 20.0,
    "layer_rules": {
      "bin": "trash objects, inside the waste bin standing on the floor beside the desk",
      "bottom": "the storage crate or boxes, standing upright on the desk under the first board",
      "middle": "the books, standing upright and packed tightly together against one side wall",
      "top": "the display objects, standing upright, at least 5 cm apart and 2 cm from the side walls; a photo frame faces outward"
    },
    "penetration_limit_m": 0.005,
    "release_distance_m": 0.05,
    "release_force_n": 0.1,
    "stable_seconds": 0.5,
    "still_angular_rad_s": 0.15,
    "still_linear_m_s": 0.03,
    "support_tolerance_m": 0.004,
    "upright_tolerance_degrees": 10.0,
    "wall_anchor": "either"
  },
  "sha256": "d35dc6bef1e9661a81f08b3c3f04c615164f8453222d3ea65bff7ad297643fb3",
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
| 1 | 0 | nominal | `{"native_layout_seed":0}` |
| 2 | 1 | nominal | `{"native_layout_seed":1}` |
| 3 | 2 | nominal | `{"native_layout_seed":2}` |
| 4 | 3 | nominal | `{"native_layout_seed":3}` |

```bash
python scripts/environment_runtime.py --task-id bookshelf/dual-panda/TableCleanD4 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/bookshelf-dual-panda-TableCleanD4-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

