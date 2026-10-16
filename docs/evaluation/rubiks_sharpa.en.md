# Floating Sharpa Rubik's cube

[Protocol](../evaluation_protocol.en.md) · [Index](index.en.md) · [JSON](tasks.json)

Embodied Playground paper scope: Launcher uses loaded initialization only. The full 410-task paper setting has 410 groups / 1640 conditions; EP-100 has 100 / 400. This runtime schedule also includes ground and retains 510 groups / 2040 conditions. [EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.en.md)

Each task below has four trials per group at base seed 0. Parameters are private maintainer inputs. Goal strings and field names below are verbatim authoring data, not translated protocol prose.

<a id="rubiks_sharpa-floating-sharpa-C01"></a>
## `rubiks_sharpa/floating-sharpa/C01`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "c6b136b2f4aba4f555b21155d3f76754f9343eff4e878c8446bd6e46253892ba",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C01-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C02"></a>
## `rubiks_sharpa/floating-sharpa/C02`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "bd1d35f4e14c3dd677bf695bf471d814815892feb9aca5107c7790f5586eaca6",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C02 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C02-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C03"></a>
## `rubiks_sharpa/floating-sharpa/C03`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "6ec8410366c185801eafa5e25dcd7108592260a99283d3ba35c3668580028292",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C03-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C04"></a>
## `rubiks_sharpa/floating-sharpa/C04`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "4b778f9ed806befbf891cf4bd7171350783eaf038f1262f4087a3396bc394485",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C04 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C04-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C05"></a>
## `rubiks_sharpa/floating-sharpa/C05`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "7187ec5e4511b858ed03b6188a9fd13e56072031a26a8aa8fe4518abe55ff8be",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C05 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C05-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C06"></a>
## `rubiks_sharpa/floating-sharpa/C06`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "65b8a2b0286d26162fa801016b318b0dc3db763a6a2023ef55a8a3ab3bf78455",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C06 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C06-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C07"></a>
## `rubiks_sharpa/floating-sharpa/C07`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "723df030fc7fc2bdabd04509cc304a9467c724e1aeaf12f8866e44b330b03a14",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C07-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C08"></a>
## `rubiks_sharpa/floating-sharpa/C08`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "46f760c97a5d00554f251d29f380da72561787ba7525c2e9bc817b0797e262c8",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C08-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C09"></a>
## `rubiks_sharpa/floating-sharpa/C09`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "8039de7c6abeec058a3f0e74f8cf7f98475372a81cc3a95b5169078e216db40c",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C09-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C10"></a>
## `rubiks_sharpa/floating-sharpa/C10`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "3681725df888dd3caefcc3aab6ced0fb5033bdb16e32d0442a21f3ec3904a0c5",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C10-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C11"></a>
## `rubiks_sharpa/floating-sharpa/C11`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "4a2049ca7048c961c953a07671071f47a69e66aa295dd0ccd4aa3234c7157588",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C11 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C11-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C12"></a>
## `rubiks_sharpa/floating-sharpa/C12`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "b0f82eb3362cc75eb3ae7243607368f84d9d6729b9d0bef9e6097260327c6024",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C12 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C12-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C13"></a>
## `rubiks_sharpa/floating-sharpa/C13`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "81d1fc8ab5f72242accbc78a9a10e07dcd3c2dbc5ffb263dc64cb42cf8c364c7",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C13 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C13-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C14"></a>
## `rubiks_sharpa/floating-sharpa/C14`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "c9a9250fa2ad7c9ab76572d2a33f51003fe6e58033f52bcca3e41bde361a0fd1",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C14-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C15"></a>
## `rubiks_sharpa/floating-sharpa/C15`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "1ad47bc5a9a55cc54660588f9f7b31ed2706a6d99e18e9cff43d775f4de875fc",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C15-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C16"></a>
## `rubiks_sharpa/floating-sharpa/C16`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "df2f2012a59dbc205ab20bc0edd5f217ad39e99180eade259025e7ac1b074d17",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C16 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C16-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C17"></a>
## `rubiks_sharpa/floating-sharpa/C17`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "b067949a26b3aaf01b3086655565b3ffc8c3c6e9a4af3c5020422d113d366576",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C17 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C17-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C18"></a>
## `rubiks_sharpa/floating-sharpa/C18`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "0b80ee6a7e107dae4681c2ee4c587344a2dcb1f34837c6b266ec2bc871b95dc4",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C18 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C18-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C19"></a>
## `rubiks_sharpa/floating-sharpa/C19`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "67a0da0e5b77aad14938f821af374fececa77c0cd283d084e2e320eabe4cda52",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C19 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C19-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C20"></a>
## `rubiks_sharpa/floating-sharpa/C20`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "fdfd0fb74bdf66cf5df84dd3df7b5e9435766e234be2ad1abaf993d1955b4e82",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C20 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C20-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C21"></a>
## `rubiks_sharpa/floating-sharpa/C21`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "8ff1ea2107673c8def79b3a05f03f909eccb9dc41945fc0d247434b006012b68",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C21 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C21-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C22"></a>
## `rubiks_sharpa/floating-sharpa/C22`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "354c730aef5e92e878b75c43df43becbe2a60609fd7ff8856517a8a874d61dca",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C22 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C22-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C23"></a>
## `rubiks_sharpa/floating-sharpa/C23`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "d6c5e2d65b78793d491649a74a1045f9780f205a13293fea3886d24d5ffad2be",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C23 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C23-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C24"></a>
## `rubiks_sharpa/floating-sharpa/C24`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "a5eab9d05024d54488fba8fb4fb4107148bb4306a0d4a30f367a575128dcadbb",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C24 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C24-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C25"></a>
## `rubiks_sharpa/floating-sharpa/C25`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "a5a9caa4dcdfe4e92adcf358863f690eff3952f657a8c8762d03efc9df17526a",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C25 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C25-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C26"></a>
## `rubiks_sharpa/floating-sharpa/C26`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "1fa1ea72a065b460a582536153d2bbb7c4a2b63ca35452e700daf388a9ce390b",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C26 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C26-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C27"></a>
## `rubiks_sharpa/floating-sharpa/C27`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "4a50a769c6b156b715ca9fe5a49c3c073077e02c0bafa1d726d03f87fa259e52",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C27 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C27-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C28"></a>
## `rubiks_sharpa/floating-sharpa/C28`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "13667db0da1d41803c535ab75dfb634d40957c22724644471d65c74647cfb9f7",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C28 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C28-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C29"></a>
## `rubiks_sharpa/floating-sharpa/C29`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "1449ced96a79dcfd010855926e8f1a58eb806b55fa18ba4237cd45c6eaf5517c",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C29 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C29-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="rubiks_sharpa-floating-sharpa-C30"></a>
## `rubiks_sharpa/floating-sharpa/C30`

Authoring provenance: `docs/rubiks_cube.md`. Action size: 28; 109800 controls / 3660 s; wall: 19800 s.

Goal (source data):
```json
"Restore uniform face colors and return home."
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
      0.0
    ],
    "names": [
      "sharpa.right_x_joint",
      "sharpa.right_y_joint",
      "sharpa.right_z_joint",
      "sharpa.right_roll_joint",
      "sharpa.right_pitch_joint",
      "sharpa.right_yaw_joint",
      "sharpa.right_index_MCP_FE",
      "sharpa.right_index_MCP_AA",
      "sharpa.right_index_PIP",
      "sharpa.right_index_DIP",
      "sharpa.right_middle_MCP_FE",
      "sharpa.right_middle_MCP_AA",
      "sharpa.right_middle_PIP",
      "sharpa.right_middle_DIP",
      "sharpa.right_ring_MCP_FE",
      "sharpa.right_ring_MCP_AA",
      "sharpa.right_ring_PIP",
      "sharpa.right_ring_DIP",
      "sharpa.right_pinky_CMC",
      "sharpa.right_pinky_MCP_FE",
      "sharpa.right_pinky_MCP_AA",
      "sharpa.right_pinky_PIP",
      "sharpa.right_pinky_DIP",
      "sharpa.right_thumb_CMC_FE",
      "sharpa.right_thumb_CMC_AA",
      "sharpa.right_thumb_MCP_FE",
      "sharpa.right_thumb_MCP_AA",
      "sharpa.right_thumb_IP"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order.",
      "Absolute native joint target in the declared joint order."
    ],
    "size": 28,
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
      "contact_force_max_n": 0.1,
      "finger_home_tolerance_rad": 0.05
    },
    "stable_seconds": 0.5,
    "support_gap_m": 0.002
  },
  "sha256": "64e9c2b6fd695c7352fb49f8b7290c874d33dbc51446d0de5d5027b763d7aaee",
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
python scripts/environment_runtime.py --task-id rubiks_sharpa/floating-sharpa/C30 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/rubiks_sharpa-floating-sharpa-C30-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

