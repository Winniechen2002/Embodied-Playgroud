# Panda 三阶魔方

[Protocol](../evaluation_protocol.zh-CN.md) · [Index](index.zh-CN.md) · [JSON](tasks.json)

Embodied Playground 论文仅评测发射器 loaded 初态：完整 410 项为 410 组／1640 条件，EP-100 为 100 组／400 条件。本运行时清单另保留 ground，共 510 组／2040 条件。[EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.zh-CN.md)

下列每项每组四次，base seed 为 0。参数为维护者私有输入。目标字符串与字段名保留作者配置原文，不作为翻译后的协议正文。

<a id="rubiks_panda-panda-C01"></a>
## `rubiks_panda/panda/C01`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "03f064cf4eb6bc7d8025abf8232ddc1fd75c005d8b4daa1a42008e2c04eea50a",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C01-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C02"></a>
## `rubiks_panda/panda/C02`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "e423d992e4816f4ec7a6a4178cc93bbe0874a63207c43591c4e585b7fb0ea82f",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C02 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C02-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C03"></a>
## `rubiks_panda/panda/C03`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "24670dcecce6336137573b09c11482072082a93522dd630467431c7d03e5972a",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C03-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C04"></a>
## `rubiks_panda/panda/C04`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "fa7c042481921ddc589aa254118f5bf8d2ae8e719b9e6f0d6d21a853442ff6ce",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C04 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C04-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C05"></a>
## `rubiks_panda/panda/C05`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "dae2c410c3783509b2cbe491d546b9772026ab7b896a7924f25c575ca4691e66",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C05 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C05-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C06"></a>
## `rubiks_panda/panda/C06`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "38d4a9d59b3670a37123d7a5edb8f5217d8a4e5fb7c3cdf7c55160dbad10da52",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C06 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C06-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C07"></a>
## `rubiks_panda/panda/C07`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "4d8f8ca78314a2299811ee86db15cc985e358f3477f4a7f9b76325ebf883a517",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C07-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C08"></a>
## `rubiks_panda/panda/C08`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "d2655c4b264e42f798fa59b54ec38eddff8f7a0f762d0f75c675e6e10c488e85",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C08-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C09"></a>
## `rubiks_panda/panda/C09`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "2b4e7117066bd312b514858138249a5a84793468c531a1ec0765324e9e5223cd",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C09-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C10"></a>
## `rubiks_panda/panda/C10`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "4bfab1a166142dee7d9481d9856ba681c7994f5726d029100e2c393be56b6195",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C10-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C11"></a>
## `rubiks_panda/panda/C11`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "871750d88da8b50f91b71d43502a8af56a2003f8ea606b67dfa55604cfb4cfa8",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C11 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C11-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C12"></a>
## `rubiks_panda/panda/C12`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "c6b844779e77c85783a773965afca02e8db7d87bc93c6c9ec905357ae4d623be",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C12 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C12-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C13"></a>
## `rubiks_panda/panda/C13`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "6b46d8a0b2e62b53d357d46a7021ae4f8a6e0d5999bbb4eb1ee9692a63e26a91",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C13 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C13-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C14"></a>
## `rubiks_panda/panda/C14`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "23061eecd7c7aaf4d46afaa20267ab8b117458f914942b11dc82d1e860c99079",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C14-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C15"></a>
## `rubiks_panda/panda/C15`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "2ea9ce71e66f2a6bf96c40fd981c4d6f68beac0fd8b9b1e9fb7d8960b6008459",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C15-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C16"></a>
## `rubiks_panda/panda/C16`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "0a835381ef53fab4d060a85def7d80d53336d93f691ba487741df0efd8a51ea9",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C16 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C16-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C17"></a>
## `rubiks_panda/panda/C17`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "88ce265db4c96efb9a87d0776c7140aeed420653b1a04cad293e54e855adb2b5",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C17 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C17-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C18"></a>
## `rubiks_panda/panda/C18`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "c0f62bb41e32805a1e751c1b3532088205e0c7fdcb3482966553be60d0faed3d",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C18 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C18-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C19"></a>
## `rubiks_panda/panda/C19`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "c476828e3954ba988de9610346b8fcb55a3f20aab4484da153020ac252485081",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C19 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C19-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C20"></a>
## `rubiks_panda/panda/C20`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "602767a3b106f101f9fb1be03b8bc897d6a6b6eb9d48a04bbf9a14c0c050bc91",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C20 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C20-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C21"></a>
## `rubiks_panda/panda/C21`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "8e134dfbdba175d58473fa928bc85a4994fe05e9b7970da9c2ecb7c0b789bcc9",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C21 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C21-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C22"></a>
## `rubiks_panda/panda/C22`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "8b5ca58798ef0984ad4638c4f3c4b09a584d90938b0e8f617e6cd8bb076a3325",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C22 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C22-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C23"></a>
## `rubiks_panda/panda/C23`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "4ce3276b46765638ccc9b23978562cf6620ab011677513b3ac4a3ef4e543f475",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C23 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C23-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C24"></a>
## `rubiks_panda/panda/C24`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "5a89c2f5744fa530377aedd177c1ff726517491ea8a264f7e94130f0a850f9f5",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C24 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C24-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C25"></a>
## `rubiks_panda/panda/C25`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "5dfc40876d52746077b22ea02675f53be760fc85ca7345e94229f24dbfb3a40a",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C25 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C25-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C26"></a>
## `rubiks_panda/panda/C26`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "8e6b64117d0732fe3797ffa40ae03623a765301a3003155b42023a02180e170f",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C26 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C26-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C27"></a>
## `rubiks_panda/panda/C27`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "6dc139bb82652948ced5faa285a3c774db2adcef0afd7d09021c6029172cacea",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C27 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C27-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C28"></a>
## `rubiks_panda/panda/C28`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "eaee61adfca1a274586bfa9a089c08d7cdc5a868b874c5355aa8f2811959b947",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C28 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C28-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C29"></a>
## `rubiks_panda/panda/C29`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "ea037cb8a36d6bcb3c7d651577c0afd16f1a1f7ec693e009a5f9540c1bdfce23",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C29 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C29-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="rubiks_panda-panda-C30"></a>
## `rubiks_panda/panda/C30`

作者来源：`docs/rubiks_cube.md`。Action size: 8; 109800 controls / 3660 s; wall: 19800 s.

目标（源数据）：
```json
"Restore uniform face colors and return home."
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
      4.560399532318115,
      5.794600009918213,
      4.364999771118164,
      4.234600067138672,
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
      -1.0
    ],
    "names": [
      "panda.panda_joint1",
      "panda.panda_joint2",
      "panda.panda_joint3",
      "panda.panda_joint4",
      "panda.panda_joint5",
      "panda.panda_joint6",
      "panda.panda_joint7",
      "panda.gripper"
    ],
    "neutral_action": [
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
      "Seven arm targets: q=default_q+0.5*action.",
      "Continuous gripper: each finger target is 0.02*(action+1) m."
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
    "arm_home_tolerance_rad": 0.05,
    "core_home_position_tolerance_m": 0.005,
    "core_home_rotation_tolerance_degrees": 2.0,
    "first_violation_sticky": true,
    "goal": "uniform face colors",
    "maximum_contact_force_n": 20.0,
    "mechanism": "hybrid_fixture_v1",
    "physical_cube_measurement_required": true,
    "release": {
      "finger_open_min_m": 0.035
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "60a431e56d36e98220e02005fe725ae5f3d6011ab3f944baf32a2b4d8f435ff9",
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
python scripts/environment_runtime.py --task-id rubiks_panda/panda/C30 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_panda-panda-C30-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

