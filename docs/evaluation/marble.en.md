# Launcher

[Protocol](../evaluation_protocol.en.md) · [Index](index.en.md) · [JSON](tasks.json)

Embodied Playground paper scope: Launcher uses loaded initialization only. The full 410-task paper setting has 410 groups / 1640 conditions; EP-100 has 100 / 400. This runtime schedule also includes ground and retains 510 groups / 2040 conditions. [EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.en.md)

Each task below has four trials per group at base seed 0. Parameters are private maintainer inputs. Goal strings and field names below are verbatim authoring data, not translated protocol prose.

<a id="marble-dual-panda-A001"></a>
## `marble/dual-panda/A001`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Two targets, finite mixed ammunition; choose shot order and draw. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.025
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "2a82c5c931c26d8cf8023f1edbd29f7df09404c12d4cf129fb19f28fffd908cb",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A001 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A001-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A001 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A001-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A002"></a>
## `marble/dual-panda/A002`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"A fixed low wall and roof restrict the firing corridor. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "33b17efb322c32bc17a08657bad4cd4b5e2166f0e2996dae106669de7e107c59",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A002 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A002-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A002 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A002-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A003"></a>
## `marble/dual-panda/A003`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Three elevated targets on immovable platforms. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "5933f2f832c0094d2d17e8fc5293b5b4095a2b292c689531d1a3b60b81e3df95",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A003 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A003-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A003 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A003-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A004"></a>
## `marble/dual-panda/A004`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Collapse the bridge onto two sheltered targets. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "abff020957cbbfa8b575df613b3db2a4f10840c1e1d6843b4988b2d1e2e65c5d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A004 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A004-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A004 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A004-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A005"></a>
## `marble/dual-panda/A005`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Arc over a fixed wall, then knock down the wooden tower. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 1."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 1,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "4a72ee08363df4d1175dfbce2dcfd92bcadda43dfb2efc0f7246217a8d280432",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A005 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A005-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A005 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A005-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A006"></a>
## `marble/dual-panda/A006`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"A chain reaction must reach both targets beside a fixed arch. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 3."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 3,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "3f14e12ee2818c99b897c18f0b034549e43ad73a6f3707ce8c5f2fcda533468e",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A006 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A006-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A006 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A006-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A007"></a>
## `marble/dual-panda/A007`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"One near target with a spare shot to learn draw control. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "787d75e4cb550733de8a2bb85abb9c314ed64f2dc7cf0784339ebaf8cc88c588",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A007 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A007-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A007 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A007-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A008"></a>
## `marble/dual-panda/A008`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"One distant target needs more spring energy. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "4978e60fc35f1f568c68c6c2765922a51f484603e69632f5ca37959f6b5e7779",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A008 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A008-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A008 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A008-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A009"></a>
## `marble/dual-panda/A009`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Aim at a single elevated target on a fixed pedestal. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "03bc26ce55d64f001d0ba3d1c956c9f6c4a86be95c859b2637a13c995b54681f",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A009 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A009-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A009 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A009-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A010"></a>
## `marble/dual-panda/A010`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Knock over the movable shield and reach the target behind it. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 1."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 1,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "3e478536adcf211966ca43fa283ffb202edf6c36bff55ecacd236726c6fd273e",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A010 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A010-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A010 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A010-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A011"></a>
## `marble/dual-panda/A011`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear an immovable front wall to hit the target. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "e98b23edbd17cc4a825d69a0b09c268f61fb583b76cb009f01f2019b1a2564cd",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A011 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A011-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A011 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A011-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A012"></a>
## `marble/dual-panda/A012`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Two targets at different elevations require trajectory selection. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "840da78aff20006866d598483bc10d60d44977f866c0c2f2f2991aebde1da787",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A012 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A012-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A012 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A012-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A013"></a>
## `marble/dual-panda/A013`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Thread a shot between a fixed sill and lintel. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "e4b3c801fea947f21acc76911f9b17db99879a117dbe4ca79f42c4db29e8172d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A013 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A013-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A013 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A013-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A014"></a>
## `marble/dual-panda/A014`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Three separated targets with different impulse thresholds. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.012,
      0.018,
      0.025
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "dc635cb8b0d4270dbdc5ca84e40d0362c8b8a3a5e45c9cd97012f5ff435bb5fd",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A014 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A014-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A014 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A014-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A015"></a>
## `marble/dual-panda/A015`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Collapse two separate bridges; only falling wood can pop targets. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "b24c57d281d69296182048ecd39e910f57e558c09d07e4aaab76a179653c7735",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A015 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A015-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A015 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A015-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A016"></a>
## `marble/dual-panda/A016`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"A single projectile must pass the fixed bunker and hit a small target. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "263ced9a62e87e8e8e4ef66ad9fd0a8b0fcb70db638ba14d17c914761435e5dc",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A016 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A016-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A016 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A016-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A017"></a>
## `marble/dual-panda/A017`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Push the wooden roller off its ledge and down the fixed slope. Only the roller can pop both targets. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['roller']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "roller"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "ed9362a61d184bfcff0d9c6b7fb017dc11de9adf762d716d2b9d3eb2e58bf1a4",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A017 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A017-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A017 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A017-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A018"></a>
## `marble/dual-panda/A018`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Dislodge glass columns and the triangular timber roof around a three-piece stone doorway; topple at least two pieces. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "fbc0a6846bafda51a2d117ee3ac11f75eca6f899de115ed59a82809dbb396d0d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A018 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A018-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A018 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A018-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A019"></a>
## `marble/dual-panda/A019`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Dislodge the glass stage of a timber-and-glass stack, tipping its cradle so the stone crown drops onto the target. Only the crown can score damage. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['crown']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "crown"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "099b5de941a20277d57d550edcdd4e775806bfa12fd0da64f5844e77af22b1fc",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A019 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A019-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A019 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A019-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A020"></a>
## `marble/dual-panda/A020`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear two mixed-material houses on different fixed terrain heights, with four different projectile shapes. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "e0ac89e583734eeb22deb2acaa6c8f654dcca436b37bcdfcdf9b2ae9838b7d85",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A020 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A020-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A020 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A020-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A021"></a>
## `marble/dual-panda/A021`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Bounce a released projectile off the fixed rubber bank before it can pop the target. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "edabdeffc1fa8aa1a17bb8434f5f397300531b873e5b83be320b8aa30fa5f939",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A021 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A021-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A021 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A021-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A022"></a>
## `marble/dual-panda/A022`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Hit the glass foregate and round supports; collapse at least two parts of the stone-and-timber roof. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "143617a3af5bda06ec796365cc184771d1087a7bf8e9f1e42d370b2c5d7195da",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A022 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A022-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A022 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A022-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A023"></a>
## `marble/dual-panda/A023`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Break an anchored glass pane and clear the target beyond it; moving the intact pane cannot satisfy the fracture requirement. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['glass_gate']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "glass_gate"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "c04129468e7fb2c9f72bd102543bc3b7e3fcab3a8ebab0d38b8738f4c582da91",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A023 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A023-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A023 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A023-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A024"></a>
## `marble/dual-panda/A024`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Break a clamped glass support and release the guided cradle so its stone crown hits the target. Projectile and glass-fragment hits do not score target damage. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['crown']. Required fractures: ['glass_support']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "crown"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "glass_support"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "634ab0638ddec913397cf6ebfee5ed061b875ca9949f634ed30a202f591b3024",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A024 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A024-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A024 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A024-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A025"></a>
## `marble/dual-panda/A025`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Break both glass barriers and clear the target with a finite sequence of differently shaped projectiles. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['glass_front', 'glass_back']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "glass_front",
      "glass_back"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "f7d5ed30e67c4020116f66d640261f6e1c39032affe607364754d006edf20919",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A025 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A025-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A025 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A025-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A026"></a>
## `marble/dual-panda/A026`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Pop numbered target 1 at the far end before target 2 nearby. An otherwise valid hit in the wrong order fails the episode. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [1, 0] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [
      1,
      0
    ],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "a4065d1ae7dddb7ebbfee18686fd2b4aba60126e842154d4551a57fd9fba8251",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A026 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A026-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A026 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A026-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A027"></a>
## `marble/dual-panda/A027`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"A single projectile must break the glass and clear the target. There is no reserve projectile for recovery. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['glass_screen']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "glass_screen"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "3e1e796a062e8621eebbb363486582d86eb75dcb54ac075bc0b0a5c2b2ad59b3",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A027 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A027-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A027 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A027-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A028"></a>
## `marble/dual-panda/A028`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the distant target while preserving the marked near target. A damaging hit on the protected target is an immediate failure. Target indices are zero-based. Required targets: [1]; protected targets: [0]; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      0
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "d8e574fc96b1a47ad414a9021c56b4fa64d8f204b3643bf81a9c6973af58ab40",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A028 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A028-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A028 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A028-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A029"></a>
## `marble/dual-panda/A029`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Pass the fixed stone sill and break the glass above it, then clear the target. The sill and lintel remain immovable. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['window_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "window_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "efedc53dab5789fbd25bbab8c778aa507faceb153d87b50ad170fa2034937c9c",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A029 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A029-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A029 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A029-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A030"></a>
## `marble/dual-panda/A030`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"The demonstration deliberately underpowers its first shot; subsequent physical reloads must clear the still-present glass and target. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['recovery_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "recovery_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "867f35da5a2d83e42f7956d679019a3b26a1cadb733f72646da3996b45b05e11",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A030 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A030-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A030 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A030-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A031"></a>
## `marble/dual-panda/A031`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Turn the launcher about its vertical column to reach targets in two lateral lanes; the right target is on a fixed raised pedestal. Clear both with three shots. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "e5f5fd7bfbca2fe8cba33d4ed0fd0c335d50533269a8b49d214c3c891df67fdf",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A031 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A031-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A031 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A031-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A032"></a>
## `marble/dual-panda/A032`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the lower and upper pigs in a two-storey timber house and topple at least two structural pieces. The intermediate floor and roof rest on movable side columns. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "2f362b59259bbad2537eba835b2b7ae969d75e6673c50b505fc1fdf83df7cf70",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A032 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A032-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A032 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A032-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A033"></a>
## `marble/dual-panda/A033`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear three vertically separated pigs and topple at least two pieces of the two stacked timber floors. The uppermost storey is open to the sky; four shots are available. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "6130812be20c3c4404421da7105b954a432ff94e7541decc2de168ed9c520958",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A033 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A033-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A033 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A033-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A034"></a>
## `marble/dual-panda/A034`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear two pigs in the low left tower and one high pig in the right tower. A fixed raised foundation and a heavier stone deck give the right tower a different collapse response. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "a3f8bb9125d5321da07f1d9d3b2947858077320ac168311ec249b22d0c27097c",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A034 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A034-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A034 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A034-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A035"></a>
## `marble/dual-panda/A035`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture both anchored load-bearing glass columns and clear both pigs in a two-storey house. Intact glass motion cannot satisfy the fracture rule; pigs remain fixed after floor collapse. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['glass_left', 'glass_right']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "glass_left",
      "glass_right"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "bb0039d91793cc7872d1ee9ce2fb2c479759662ae9dee83cc1b460dd098cfa22",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A035 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A035-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A035 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A035-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A036"></a>
## `marble/dual-panda/A036`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the upper pig while preserving the marked pig directly below it. Falling structural pieces also threaten the protected target; any damaging hit on it fails the episode. Target indices are zero-based. Required targets: [1]; protected targets: [0]; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      0
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "538ddb8a0f1c92d25a33b2456e7d8bc93a25b0b428bdda90ee5e159aaf2cd3a5",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A036 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A036-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A036 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A036-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A037"></a>
## `marble/dual-panda/A037`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Reach the sheltered pig through the opening between a fixed stone sill and lintel. A fixed ceiling removes the easy high arc; decorative movable roof pieces do not need to fall. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "0d4081d3dab27b1deacdc2cc28c907c4dc774dda55bb3dccca003c441177fb8e",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A037 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A037-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A037 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A037-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A038"></a>
## `marble/dual-panda/A038`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Break the anchored outer glass screen, topple at least two logical pieces including that screen, and clear the pig behind an independent timber shield and a stone arch. The layers persist between shots. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Required fractures: ['outer_screen']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "outer_screen"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "a93ea2296dedccc484ecbddcc880d0fdc35e307815d38c4199514a9f7da7070d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A038 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A038-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A038 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A038-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A039"></a>
## `marble/dual-panda/A039`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the falling gabled roof may clear the pig. Geometry, ammunition and scoring match heavy_roof_bunker, while roof mass differs. The pair is not assumed to have a monotonic difficulty order. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 1. Allowed damage sources: ['falling_roof']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "falling_roof"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 1,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "9f0452287499b5cf0015c2925d7a8ef7b6c6cbc1df3ca752af7001d662811c2c",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A039 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A039-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A039 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A039-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A040"></a>
## `marble/dual-panda/A040`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the falling gabled roof may clear the pig. Geometry, ammunition and scoring match light_roof_bunker, while roof mass differs. The pair is not assumed to have a monotonic difficulty order. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 1. Allowed damage sources: ['falling_roof']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "falling_roof"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 1,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "1029d5c408e3a1c0326cc314357319cf5111d664826ea44e73baa63f54b96235",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A040 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A040-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A040 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A040-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A041"></a>
## `marble/dual-panda/A041`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"A released projectile must touch the rear inclined bank before it can damage the sheltered pig. This control uses the stone bank preset; geometry, ammunition and scoring match rubber_return_gallery. The preset changes contact and visual parameters together. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "ea38f4554803d1b1b76a7477f096703030175a16a3a83aad157e0eb8fe2b7778",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A041 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A041-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A041 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A041-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A042"></a>
## `marble/dual-panda/A042`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"A released projectile must touch the rear inclined bank before it can damage the sheltered pig. Compared with stone_return_gallery, only the bank material preset changes. Its friction, compliant contact response and appearance change together; this is not a single-parameter restitution experiment. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "f3a8e973cf4c04e93ecf9c4b6c32ebf75cb46f873ba20de7302050b465664c34",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A042 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A042-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A042 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A042-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A043"></a>
## `marble/dual-panda/A043`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the anchored glass buttress above its fixed pedestal, then make the stone lintel hit the sheltered pig. Only that lintel scores target damage; projectile, gable and glass-fragment hits do not satisfy the causal rule. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['falling_lintel']. Required fractures: ['glass_buttress']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "falling_lintel"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "glass_buttress"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "210e6aca703ba183ae2c9c1b60268d7bf3f3c258665ae41bd0bb859ed08be304",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A043 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A043-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A043 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A043-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A044"></a>
## `marble/dual-panda/A044`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Push the stone roller from its flat ledge onto the descending wedge and into the low-roofed redoubt. Only the roller may clear the pig; direct projectile hits cannot substitute for the gravity chain. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['stone_roller']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "stone_roller"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "33447c2ca61d5ea61391e8f5985a3ebdcf9389da7a5fb3d3282b1d8a7b34c58e",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A044 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A044-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A044 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A044-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A045"></a>
## `marble/dual-panda/A045`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Break the foregate and clear both floors of the offset gatehouse, toppling at least two logical pieces. Glass, floor, round upper columns and gabled roof remain separate physical bodies. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Required fractures: ['glass_foregate']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "glass_foregate"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "5c28c371fdfd0aa6fedf55c9324b890954291869439f9b083f78825e2429a82f",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A045 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A045-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A045 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A045-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A046"></a>
## `marble/dual-panda/A046`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the low western arch bunker and elevated eastern stone hall. Fracture the western screen and topple at least two pieces, changing both yaw and elevation between the two different support systems. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Required fractures: ['west_screen']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "west_screen"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "1f456cafa7f99669cbe4057a0b77274eb7c4ca9405f2c161c34125e6f52e7d36",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A046 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A046-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A046 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A046-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A047"></a>
## `marble/dual-panda/A047`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the upper chamber by targeting its exposed round wooden supports while preserving the marked pig below the movable stone floor. The fixed lower embrasure protects the lower chamber from low direct shots; debris can still violate the protection rule. Target indices are zero-based. Required targets: [1]; protected targets: [0]; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      0
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "b309f17c730913c30bb821a8f9a11d7f71556394235702782201308979978d4f",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A047 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A047-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A047 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A047-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A048"></a>
## `marble/dual-panda/A048`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear numbered targets in far, raised, then near order across three firing lanes. Topple at least one piece while respecting the order; hitting a visible nearer pig first is a task violation. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [1, 2, 0] (empty means unrestricted); minimum toppled structures: 1."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 1,
    "order": [
      1,
      2,
      0
    ],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "421fdeb890d3ced8c0a18e64dc7bc644b86280dc119aea4f55d15e01a809f51d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A048 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A048-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A048 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A048-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A049"></a>
## `marble/dual-panda/A049`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the target behind two fixed apertures at different heights. Neither frame moves; all hits obey the normal target damage rule. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "e9abbabd28b16710570d19303f12f879af1b9efec55be756a2269c86d9aa631f",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A049 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A049-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A049 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A049-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A050"></a>
## `marble/dual-panda/A050`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear an elevated target between a raised foundation and an inclined fixed ceiling. The ceiling and front sill cannot be toppled. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "ce964b51d7226cf11249fda90b833d3697216b45a8f3d9033aa12bb64a4e7566",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A050 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A050-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A050 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A050-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A051"></a>
## `marble/dual-panda/A051`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the raised front target while preserving the marked rear target below its fixed canopy. Any damaging protected-target hit fails the task. Target indices are zero-based. Required targets: [0]; protected targets: [1]; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      1
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "055436fcb57977aa1f49c500f7cc10c56f9a654900dc1d78eaf8a8b8eb5911a7",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A051 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A051-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A051 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A051-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A052"></a>
## `marble/dual-panda/A052`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the numbered targets in far-low, middle, near-high order. A damaging hit in any other order fails the task; all three supports remain fixed. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [2, 1, 0] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [
      2,
      1,
      0
    ],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "cac22ee48c87dc5fc2e87b27a83817acdead83b0d3ed9ed83e19f1414f352f1a",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A052 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A052-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A052 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A052-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A053"></a>
## `marble/dual-panda/A053`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"A projectile must contact the named descending ramp before it may damage the target beyond it. Direct untouched flights do not score. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "3ed961ac992df8d83e581199a10e01e61a7ffbb7629b61e1985b5b2677aff165",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A053 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A053-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A053 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A053-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A054"></a>
## `marble/dual-panda/A054`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only projectiles that first touch the uphill ramp may damage the target on the upper landing. The ramp and landing are fixed. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "c89a76295652f1c4be193290e6e16ef947fae56ee855a55cf4eb3516053277d9",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A054 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A054-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A054 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A054-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A055"></a>
## `marble/dual-panda/A055`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the lower relay ball may clear the target. The upper roller and all projectiles are excluded as damage sources; using the upper roller to transfer momentum is an available strategy, not an extra rule. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['relay_ball']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "relay_ball"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "07035d547dc8fe49565aba3114da7557812ad9998dfacfe7511efdc470bdcc12",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A055 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A055-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A055 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A055-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A056"></a>
## `marble/dual-panda/A056`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the wooden rectangular ram may clear the target. It starts on a level ledge connected to a descent; projectiles cannot score directly. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['sliding_ram']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "sliding_ram"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "251c7b85419df68c5eaf421bec21bb0424b733adc1e4fb086baf74f0a32eff46",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A056 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A056-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A056 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A056-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A057"></a>
## `marble/dual-panda/A057`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear both targets using either of the two stone rollers. The broad timber pusher and all projectiles are excluded from target damage. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['left_roller', 'right_roller']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "left_roller",
      "right_roller"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "5a0065f2ef92a80496f1bc8ef9a164c39bceff3db6d3973e9f44ff8a9ec5cae1",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A057 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A057-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A057 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A057-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A058"></a>
## `marble/dual-panda/A058`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the long balanced beam may clear the target below its far end. The beam is a free rigid body resting on a fixed narrow fulcrum, with no hinge or motor. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['balanced_beam']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "balanced_beam"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "ba8f0f6467317232f49a726764eb7a4ef8b9198ff33e186540de1f2df9fc60c9",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A058 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A058-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A058 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A058-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A059"></a>
## `marble/dual-panda/A059`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the long beam may damage the target below its front span. One support is movable and the rear bearing is fixed; both remain ordinary contact supports. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['heel_beam']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "heel_beam"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "4fdf31d5ebe1716afa5bb1c95a0698a7b75bca51b3f3ad0928256056ce98ae1e",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A059 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A059-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A059 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A059-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A060"></a>
## `marble/dual-panda/A060`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the bridge slab may clear both sheltered targets, and at least two logical pieces must topple. Both piers are movable; the raised stone stop behind the bridge is fixed. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Allowed damage sources: ['wide_slab']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "wide_slab"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "9489299fdbd668f6875218884b6db836fff8c39adc3be624d5ab4da239a5be8f",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A060 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A060-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A060 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A060-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A061"></a>
## `marble/dual-panda/A061`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the target and topple at least three pieces from the free stack of round packing blocks and its timber cap. Direct and structural hits use the normal damage rule. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 3."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 3,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "9d19b6c7e405f0b091322fad802dac919bc6309691743e79043d27cd8143b858",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A061 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A061-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A061 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A061-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A062"></a>
## `marble/dual-panda/A062`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the overhanging beam may clear the target beneath its far end. A small load rests near the beam support; the load itself cannot damage the target. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['overhang_beam']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "overhang_beam"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "cc504868425147bbfec06817fabc0a42713d7a2ce606037b4845d239536b587d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A062 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A062-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A062 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A062-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A063"></a>
## `marble/dual-panda/A063`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the lower beam may clear the target; the upper roof and the projectiles cannot score. Topple at least two pieces. An upper-to-lower cascade is an available route rather than a required event sequence. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Allowed damage sources: ['lower_scoring_beam']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "lower_scoring_beam"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "6df62a9ec8202c6abc6ed180616a40ea3091ddb9d479d6b786ea4746444422ed",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A063 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A063-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A063 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A063-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A064"></a>
## `marble/dual-panda/A064`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the anchored low glass transom and clear the raised target beyond it. The fixed sill below the glass cannot be moved. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['low_glass_transom']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "low_glass_transom"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "140c3bf9845fd442db95ad989cebbdd6c47aedfe11e0fe00b71ba3101965889d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A064 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A064-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A064 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A064-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A065"></a>
## `marble/dual-panda/A065`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the anchored high glass transom and clear the ground target below the fixed rear canopy. Hitting the low target alone is insufficient. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['high_transom']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "high_transom"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "f00cb1dfc2daaf8b20d18dc4ce692d090304b5110e74609afec3399ba59ac400",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A065 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A065-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A065 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A065-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A066"></a>
## `marble/dual-panda/A066`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the middle anchored glass, topple at least three logical pieces, and clear the target behind two timber shutters. Damage persists across the four shots. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 3. Required fractures: ['laminate_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 3,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "laminate_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "372b8d6e28d84f3cd5d2eb8fa618c910e9d56a58c6893b377ae133b3b4ca9995",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A066 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A066-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A066 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A066-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A067"></a>
## `marble/dual-panda/A067`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the anchored glass support and clear the ground target while preserving the marked upper target. Targets remain fixed sensors even if their supporting floor moves. Target indices are zero-based. Required targets: [0]; protected targets: [1]; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['lower_glass_support']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      1
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [
      "lower_glass_support"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "cf5fddc85c7df3cd9b26192cbdf01338d8339a44c3e00bbaf6f42cf5f48e8c43",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A067 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A067-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A067 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A067-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A068"></a>
## `marble/dual-panda/A068`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Break the elevated glass screen and clear the rear target while preserving the marked target in the near recess. Fragments can damage the protected target. Target indices are zero-based. Required targets: [1]; protected targets: [0]; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['overwell_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      0
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [
      "overwell_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "828f8a80f9af3da210ecbfd2031627908bc35d2085cf2400347d98d0271985b8",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A068 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A068-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A068 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A068-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A069"></a>
## `marble/dual-panda/A069`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the front pane, topple at least four pieces including the pane, and clear the target using only the final domino. A complete chain reaction is an available route, not a separately detected event. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 4. Allowed damage sources: ['relay_3']. Required fractures: ['relay_screen']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "relay_3"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 4,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "relay_screen"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "c571615029a237959c98fe47a1cfa6196222a7aeb1f188b7905ba97b1c668eac",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A069 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A069-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A069 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A069-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A070"></a>
## `marble/dual-panda/A070`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the tall stone striker may clear the target; topple at least two logical pieces. A separate rubber pad lies in front of it and can alter contact transmission. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Allowed damage sources: ['stone_striker']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "stone_striker"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "2adb3186332518d0e918ae7d8eacd994c284e84cf631bace977c9ce9fadc268f",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A070 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A070-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A070 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A070-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A071"></a>
## `marble/dual-panda/A071`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the separate stone crown may clear the target beyond the arch. The arch is one rigid movable body and does not disassemble into individual masonry stones. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['separate_crown']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "separate_crown"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "7923fa84d9020581f8f16a99dfb2e0ade7843a9abc018dda79edcb01aaf7742a",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A071 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A071-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A071 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A071-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A072"></a>
## `marble/dual-panda/A072`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Topple the timber shutter and clear the target beyond the fixed sill and lintel. The shutter remains a physical body after it moves and may obstruct later shots. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 1."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 1,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "e1dbf397312ceda0f412abd1c26233762c5cc700ca15dfb1a3697e37b51f3bf9",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A072 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A072-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A072 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A072-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A073"></a>
## `marble/dual-panda/A073`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the near target before the sheltered far target, and topple at least two structural pieces. Both projectile and structure damage are allowed; a far-first collapse violates the target order. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [0, 1] (empty means unrestricted); minimum toppled structures: 2."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [
      0,
      1
    ],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "f4c162196e9e36b95e5957fcd0ac4ae1a4e66b57ba5725a9ac59abfd246fc273",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A073 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A073-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A073 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A073-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A074"></a>
## `marble/dual-panda/A074`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the anchored glass, topple at least three logical pieces, and clear the target using only the stone lintel. Neither the front timber shutter nor the glass fragments may substitute for the lintel. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 3. Allowed damage sources: ['scoring_stone_lintel']. Required fractures: ['middle_glass_lock']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "scoring_stone_lintel"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 3,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "middle_glass_lock"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "08323041705f4d3a60b6c6d60f3b15cf2effb5535d06519e3bb7632475ac4fc2",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A074 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A074-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A074 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A074-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A075"></a>
## `marble/dual-panda/A075`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear three separated ground targets across a fan. Four spherical shots permit one correction; no obstacle or ordering rule substitutes for bearing control. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "c2802afa193c6a7daa31256e80d5c31f93de08586540a738275525712b5782dd",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A075 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A075-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A075 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A075-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A076"></a>
## `marble/dual-panda/A076`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Reach a left-lane target through a fixed sill/lintel window; a central stone wall blocks the zero-yaw route. A loose rear banner is optional debris. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "c9b1178d44b72e10d1030ef8eb09c8a0bdc0d4edd2904dc6353f4433eb823abd",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A076 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A076-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A076 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A076-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A077"></a>
## `marble/dual-panda/A077`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the left target beyond a high sill and the right target below a low ceiling. The two immovable constraints demand different trajectory heights. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "a0c5a7a8bb12e46ff6067805e3072f02fe39540684d39ca4cb1dbddbc2f93411",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A077 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A077-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A077 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A077-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A078"></a>
## `marble/dual-panda/A078`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear one ground target and two targets on fixed platforms of different heights. No collapse can lower a target, and each platform occupies a separate bearing. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "bd6dd54b778af875e8c696ac058726ecd8aa74de51cbc4079975acbc2b562658",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A078 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A078-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A078 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A078-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A079"></a>
## `marble/dual-panda/A079`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the western screen, clear both pigs, and topple two logical pieces. The eastern timber shield moves as one rigid body while the western glass splits into fragments. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Required fractures: ['west_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "west_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "e5d8cd15d10d7b8bcd405dd022fa8e4d3a084ae86df9a3f7237d99974ad1bbae",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A079 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A079-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A079 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A079-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A080"></a>
## `marble/dual-panda/A080`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear both wings and topple the rubber screen. One low stone barricade is immovable; the opposite tall rubber screen is a movable dissipative rigid body. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 1."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 1,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "ff61b31cd8985f5a367dea40959db2d2bfd2dfc281d745243de01f05648dbaea",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A080 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A080-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A080 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A080-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A081"></a>
## `marble/dual-panda/A081`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear targets inside two staggered rigid arches and topple at least one arch. Both apertures face the launcher; each arch is one movable compound rigid body. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 1."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 1,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "42b2a2d3b218474542f11cf11bb32bb7e358e60033d24527221fed845ca1a3bd",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A081 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A081-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A081 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A081-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A082"></a>
## `marble/dual-panda/A082`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only the long stone roof may clear the pig. Four round columns support an oblique roof, so removing one column need not be enough to destabilize its support polygon. Target indices are zero-based. Required targets: [0]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['skew_roof']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "skew_roof"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "49bea04cf529e71f14022b46f42c7dfb481cd0cff83ce8b754a456a6d81cc820",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A082 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A082-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A082 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A082-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A083"></a>
## `marble/dual-panda/A083`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear both lateral shelters using only their flat roof slabs. Direct ammunition, side-wall and crown-cap hits on pigs do not score; collapse persists while the launcher changes bearing. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['west_roof', 'east_roof']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "west_roof",
      "east_roof"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "756dac101e909f1513fe48f504e27f73be0f60e66aa98a5c7a25675a7963a1cc",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A083 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A083-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A083 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A083-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A084"></a>
## `marble/dual-panda/A084`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear both targets using either of the two terminal dominoes. Multi-piece chain reactions are available strategies, not required event sequences; the two terminal bodies form a shared damage-source whitelist. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['west_domino2', 'east_domino2']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "west_domino2",
      "east_domino2"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "78708c5a5fa0ebff277fce24b224e1cd34aff97dda483622ef4b05f386dab362",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A084 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A084-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A084 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A084-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A085"></a>
## `marble/dual-panda/A085`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Only a shared broad roof may clear both side-by-side pigs. Four corner columns support one roof; partial collapse can clear one chamber while leaving the other intact. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['shared_roof']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "shared_roof"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "22cca220eac7382f75727b2342017016313541aa274c4ac443ca5e5715c5ccbe",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A085 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A085-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A085 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A085-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A086"></a>
## `marble/dual-panda/A086`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the load-bearing glass panel, clear its sheltered target, and clear a separate open right target. The annex roof is supported by glass at the front and timber at the rear. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['annex_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "annex_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "93ee001049e9ecab4d90b9a2c4b9ccddb4d156874b18404a360db13e76e26a7d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A086 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A086-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A086 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A086-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A087"></a>
## `marble/dual-panda/A087`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear a lower sheltered pig and a raised pig whose pavilion sits behind and to the side. Topple two dynamic pieces; the fixed raised terrace itself cannot collapse. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "f8dd8aabb3950a4db98e7c7e8a223705386c445988cca8d72794040f4e48c6ea",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A087 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A087-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A087 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A087-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A088"></a>
## `marble/dual-panda/A088`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the left sheltered pig using only its flat roof slab while preserving the marked right pig. A fixed divider separates floor-level debris routes, but trajectories can still pass above it. Target indices are zero-based. Required targets: [0]; protected targets: [1]; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['attack_roof']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "attack_roof"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      1
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "e679836e3142e8120eaed49b8c36eab6e79f4f3193cde8af1ef86887ece9b07c",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A088 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A088-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A088 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A088-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A089"></a>
## `marble/dual-panda/A089`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear two pigs on separate fixed balconies and a lower pig between them. Each balcony has its own movable parapet; at least one parapet must be toppled. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 1."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 1,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "c8bd147664d2640f8d9f36c426c774ce2c348fb5ce8741a6d1216ddecab490ab",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A089 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A089-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A089 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A089-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A090"></a>
## `marble/dual-panda/A090`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the low western glass gate and clear both its pig and the eastern pig under a stone crown. Target order is unrestricted. At least two logical pieces must topple in total across the two independent zones. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Required fractures: ['western_gate']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "western_gate"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "66b6e6efd00075de77b589407530e1908a4d636af58c07208d3bb71d3c8d6a21",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A090 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A090-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A090 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A090-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A091"></a>
## `marble/dual-panda/A091`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the right, left, then central target in that marked order. The central target is closer, so a distance-only sweep violates the rule. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [2, 0, 1] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [
      2,
      0,
      1
    ],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "aeb00de8793c53e7dd38aa967b46f610c104a6854554a17418dbf9ff680aa36d",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A091 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A091-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A091 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A091-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A092"></a>
## `marble/dual-panda/A092`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the upper pig, then the pig below it, then the separate right courtyard. The two vertically aligned targets are separated by a fixed slab, with loose outer pennants as optional obstacles. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [1, 0, 2] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [
      1,
      0,
      2
    ],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "2c935e062f7bb0b9ba204cdbcbed3b5335d61f2902aca001ad6b19ee036317a1",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A092 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A092-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A092 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A092-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A093"></a>
## `marble/dual-panda/A093`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the glass wing, then the timber wing, then the open center; fracture the glass screen as a separate requirement. The visible central pig is deliberately last. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [0, 1, 2] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['ordered_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [
      0,
      1,
      2
    ],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "ordered_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "db409906960e0f42fe0b6fd3267ea114c195c827b99fc2dbfc1f46778a7188db",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A093 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A093-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A093 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A093-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A094"></a>
## `marble/dual-panda/A094`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear far-left, middle-right, then near-center targets. Each lies in a different bearing, and a low central parapet prevents a single straight ground sweep. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [2, 1, 0] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [
      2,
      1,
      0
    ],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "12e07a6474e1162aefdf06cf50a4650f7e7d27818dbbc994a2214f41f7a0b1be",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A094 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A094-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A094 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A094-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A095"></a>
## `marble/dual-panda/A095`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear both outer targets while preserving the central marked pig. A narrow central low shield protects against some ground shots but does not block high arcs or lateral debris. Target indices are zero-based. Required targets: [0, 1]; protected targets: [2]; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      2
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "3a0d80f93cd040f8110fd86a4cd88bc2b909f4eb9f7576025754ef6946f33b4b",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A095 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A095-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"studio","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"dusk","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A095 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A095-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A096"></a>
## `marble/dual-panda/A096`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear the west and central pigs using only their separate flat roof slabs while preserving the exposed right pig. The protected annex has no roof to remove; overshoot and debris still count against protection. Target indices are zero-based. Required targets: [0, 1]; protected targets: [2]; required order: [] (empty means unrestricted); minimum toppled structures: 0. Allowed damage sources: ['west_roof', 'middle_roof']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": [
      "west_roof",
      "middle_roof"
    ],
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      2
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "568f83259b8d38a149a64f4b25466c282a7d7bee7a8ee03139e619beaa890d3c",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A096 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A096-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"park","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"desert","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A096 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A096-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A097"></a>
## `marble/dual-panda/A097`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Preserve the high marked lookout on a fixed deck while clearing a lower left pig and the right courtyard. A loose lower shield can be pushed without moving the lookout deck. Target indices are zero-based. Required targets: [0, 2]; protected targets: [1]; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      1
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "2a0b40b7b1d5dbba0efab2cf2f6752d06ec7af414961622f7fe135eb2d596844",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A097 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A097-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"snow","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"studio","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"dusk","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"park","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A097 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A097-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A098"></a>
## `marble/dual-panda/A098`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Fracture the left glass screen and clear its pig while preserving a neighboring right pig. A second angled rigid wooden screen can redirect later collisions toward either region. Target indices are zero-based. Required targets: [0]; protected targets: [1]; required order: [] (empty means unrestricted); minimum toppled structures: 0. Required fractures: ['refuge_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [
      1
    ],
    "protected_observation_seconds": 3.0,
    "required_fractures": [
      "refuge_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 3.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "b4209c5c9a133ab674227aff61d9848374e15fcaeaa81e5f723d64e890a9dfe3",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A098 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A098-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"desert","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"snow","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"studio","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A098 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A098-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A099"></a>
## `marble/dual-panda/A099`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"A released projectile must first contact the broad inclined rear bank before it can clear either target. Two short fixed side roofs constrain high escape routes; the bank spans both lateral lanes. Target indices are zero-based. Required targets: [0, 1]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 0."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018
    ],
    "minimum_toppled": 0,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "87e03e3f915d5b740ce820cc16c29f191f5e69c47e67a0e41c2b1f826b641f4c",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A099 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A099-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A099 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A099-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="marble-dual-panda-A100"></a>
## `marble/dual-panda/A100`

Authoring source: [source/agentbench/agentbench_mujoco/campaign_scene.py](../../source/agentbench/agentbench_mujoco/campaign_scene.py). Action size: 16; 7500 controls / 150 s; wall: 600 s.

Goal (source data):
```json
"Clear a western pig behind a fixed stone sill, a central pig behind breakable glass, and an eastern pig under a movable timber roof. Fracture the glass and topple two logical pieces. Target indices are zero-based. Required targets: [0, 1, 2]; protected targets: []; required order: [] (empty means unrestricted); minimum toppled structures: 2. Required fractures: ['central_glass']."
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.02,
    "high": [
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0,
      2.8973,
      1.7628,
      2.8973,
      -0.0698,
      2.8973,
      3.7525,
      2.8973,
      1.0
    ],
    "low": [
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0,
      -2.8973,
      -1.7628,
      -2.8973,
      -3.0718,
      -2.8973,
      -0.0175,
      -2.8973,
      -1.0
    ],
    "names": [
      "left_0",
      "left_1",
      "left_2",
      "left_3",
      "left_4",
      "left_5",
      "left_6",
      "left_gripper",
      "right_0",
      "right_1",
      "right_2",
      "right_3",
      "right_4",
      "right_5",
      "right_6",
      "right_gripper"
    ],
    "neutral_action": [
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0,
      0.0,
      -0.4,
      0.0,
      -2.2,
      0.0,
      1.9,
      0.7854,
      1.0
    ],
    "physics_period_s": 0.001,
    "semantics": [
      "Seven absolute arm joint targets in radians, then binary gripper (-1 closed, +1 open), per arm."
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
      "available": false
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
      "encoding": "PNG",
      "height": 400,
      "minimum_level": 0,
      "width": 640
    },
    "unknown_fields": "denied"
  },
  "scoring": {
    "damage_sources": {},
    "damage_window_s": 0.03,
    "impulse_thresholds_N_s": [
      0.018,
      0.018,
      0.018
    ],
    "minimum_toppled": 2,
    "order": [],
    "protected_indices": [],
    "protected_observation_seconds": 0.0,
    "required_fractures": [
      "central_glass"
    ],
    "required_targets": "all except protected indices",
    "stability_seconds": 0.0,
    "target_threshold_comparison": "strict accumulated impulse > threshold"
  },
  "sha256": "73b2194e4d118c28c377fc9e8efca18e1ee71056dd167959e6f8042821f3e90a",
  "termination": {
    "finish": "owner/client submission evaluates existing evidence; no extra physics or stability credit",
    "success": "goal and required continuous stability with no prior violation",
    "timeout": "budget exhausted without qualified success",
    "violation": "first violation terminates and denies success"
  }
}
```

### loaded — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A100 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/marble-dual-panda-A100-loaded-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

### ground — 4 trials

| Trial | Reset seed | Split | Parameters / 参数 |
| ---: | ---: | --- | --- |
| 1 | 0 | nominal | `{"ammunition_offset_m":[-0.012,-0.008,0.0],"background":"dusk","background_motion":"static","launcher_offset_m":[-0.012,0.0,0.0],"spring_stiffness":22.0}` |
| 2 | 0 | nominal | `{"ammunition_offset_m":[-0.004,0.008,0.0],"background":"park","background_motion":"static","launcher_offset_m":[-0.004,0.0,0.0],"spring_stiffness":24.0}` |
| 3 | 0 | nominal | `{"ammunition_offset_m":[0.004,-0.008,0.0],"background":"desert","background_motion":"drift","launcher_offset_m":[0.004,0.0,0.0],"spring_stiffness":26.0}` |
| 4 | 0 | nominal | `{"ammunition_offset_m":[0.012,0.008,0.0],"background":"snow","background_motion":"pulse","launcher_offset_m":[0.012,0.0,0.0],"spring_stiffness":28.0}` |

```bash
python scripts/environment_runtime.py --task-id marble/dual-panda/A100 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode ground --headless --output /tmp/marble-dual-panda-A100-ground-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

