# 二阶魔方

[Protocol](../evaluation_protocol.zh-CN.md) · [Index](index.zh-CN.md) · [JSON](tasks.json)

Embodied Playground 论文仅评测发射器 loaded 初态：完整 410 项为 410 组／1640 条件，EP-100 为 100 组／400 条件。本运行时清单另保留 ground，共 510 组／2040 条件。[EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.zh-CN.md)

下列每项每组四次，base seed 为 0。参数为维护者私有输入。目标字符串与字段名保留作者配置原文，不作为翻译后的协议正文。

<a id="pocket_cube-aloha-C01"></a>
## `pocket_cube/aloha/C01`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [1, 2, 3, 0, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      1,
      2,
      3,
      0,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "c083ef7de8d16e8dd1bc6819728f8f10f66787ecc9e5e2a16926db6ea35e4838",
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
| 1 | 0 | train | `{"friction_scale":1.0486650172358334,"light":979.1325413519919,"mass_scale":1.040552136189604,"seed":0,"split":"train","task_id":"C01","x":0.5576431850291448,"y":0.0011950374868153072,"yaw_deg":-1.1479576832404077}` |
| 2 | 1 | train | `{"friction_scale":1.0271815116281053,"light":880.504044732098,"mass_scale":0.9894950176797047,"seed":1,"split":"train","task_id":"C01","x":0.5617891313565202,"y":0.0019898409057200464,"yaw_deg":-1.6536116750751884}` |
| 3 | 2 | train | `{"friction_scale":0.9726823824839432,"light":774.3518937649899,"mass_scale":1.0023950237223886,"seed":2,"split":"train","task_id":"C01","x":0.5598273354272847,"y":-0.00023416940373571218,"yaw_deg":-1.8799845707683245}` |
| 4 | 3 | train | `{"friction_scale":1.0368387376323305,"light":857.6623687460407,"mass_scale":0.9717411134412212,"seed":3,"split":"train","task_id":"C01","x":0.5587068201659846,"y":0.00014698423300446616,"yaw_deg":1.2065577378080428}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C01-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C01"></a>
## `pocket_cube/dual-sharpa/C01`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [1, 2, 3, 0, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      1,
      2,
      3,
      0,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "fa2b16ac023598db6a024ca40022078bb0c186a574762f31f877a78b1621f897",
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
| 1 | 0 | train | `{"friction_scale":1.0486650172358334,"light":979.1325413519919,"mass_scale":1.040552136189604,"seed":0,"split":"train","task_id":"C01","x":0.5576431850291448,"y":0.0011950374868153072,"yaw_deg":-1.1479576832404077}` |
| 2 | 1 | train | `{"friction_scale":1.0271815116281053,"light":880.504044732098,"mass_scale":0.9894950176797047,"seed":1,"split":"train","task_id":"C01","x":0.5617891313565202,"y":0.0019898409057200464,"yaw_deg":-1.6536116750751884}` |
| 3 | 2 | train | `{"friction_scale":0.9726823824839432,"light":774.3518937649899,"mass_scale":1.0023950237223886,"seed":2,"split":"train","task_id":"C01","x":0.5598273354272847,"y":-0.00023416940373571218,"yaw_deg":-1.8799845707683245}` |
| 4 | 3 | train | `{"friction_scale":1.0368387376323305,"light":857.6623687460407,"mass_scale":0.9717411134412212,"seed":3,"split":"train","task_id":"C01","x":0.5587068201659846,"y":0.00014698423300446616,"yaw_deg":1.2065577378080428}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C01-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C03"></a>
## `pocket_cube/aloha/C03`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 5, 1, 3, 4, 6, 2, 7, 0, 1, 2, 0, 0, 2, 1, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      0,
      5,
      1,
      3,
      4,
      6,
      2,
      7,
      0,
      1,
      2,
      0,
      0,
      2,
      1,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "3a0bc5ab80d559ccb1eb4159ddeebaf4ddc608ef6ce2da83838c3c6b5c7175ac",
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
| 1 | 0 | train | `{"friction_scale":0.9923400197705059,"light":756.9223910011606,"mass_scale":1.0068044310588509,"seed":0,"split":"train","task_id":"C03","x":0.5579740519940103,"y":-0.0023379425774133615,"yaw_deg":1.06688429249088}` |
| 2 | 1 | train | `{"friction_scale":1.0420743894137272,"light":982.4304852213438,"mass_scale":0.9414984314157904,"seed":1,"split":"train","task_id":"C03","x":0.5596127418714608,"y":0.0001903286989214984,"yaw_deg":-0.5076603930360482}` |
| 3 | 2 | train | `{"friction_scale":0.9566852974865271,"light":777.0265280345584,"mass_scale":0.9878022988394413,"seed":2,"split":"train","task_id":"C03","x":0.561524942648322,"y":-0.002768980627173089,"yaw_deg":1.7945457818787722}` |
| 4 | 3 | train | `{"friction_scale":1.0018055368505046,"light":947.2047961545909,"mass_scale":0.9507091202953687,"seed":3,"split":"train","task_id":"C03","x":0.5607287766440131,"y":-0.002896207797989082,"yaw_deg":-0.025966316359461228}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C03-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C03"></a>
## `pocket_cube/dual-sharpa/C03`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 5, 1, 3, 4, 6, 2, 7, 0, 1, 2, 0, 0, 2, 1, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      0,
      5,
      1,
      3,
      4,
      6,
      2,
      7,
      0,
      1,
      2,
      0,
      0,
      2,
      1,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "c63c09209211e38ef7b41f55a50bbcc6721b3244f3edd338364ffce9df122ca3",
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
| 1 | 0 | train | `{"friction_scale":0.9923400197705059,"light":756.9223910011606,"mass_scale":1.0068044310588509,"seed":0,"split":"train","task_id":"C03","x":0.5579740519940103,"y":-0.0023379425774133615,"yaw_deg":1.06688429249088}` |
| 2 | 1 | train | `{"friction_scale":1.0420743894137272,"light":982.4304852213438,"mass_scale":0.9414984314157904,"seed":1,"split":"train","task_id":"C03","x":0.5596127418714608,"y":0.0001903286989214984,"yaw_deg":-0.5076603930360482}` |
| 3 | 2 | train | `{"friction_scale":0.9566852974865271,"light":777.0265280345584,"mass_scale":0.9878022988394413,"seed":2,"split":"train","task_id":"C03","x":0.561524942648322,"y":-0.002768980627173089,"yaw_deg":1.7945457818787722}` |
| 4 | 3 | train | `{"friction_scale":1.0018055368505046,"light":947.2047961545909,"mass_scale":0.9507091202953687,"seed":3,"split":"train","task_id":"C03","x":0.5607287766440131,"y":-0.002896207797989082,"yaw_deg":-0.025966316359461228}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C03-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C07"></a>
## `pocket_cube/aloha/C07`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [3, 0, 2, 7, 5, 4, 1, 6, 2, 2, 0, 1, 1, 2, 1, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      3,
      0,
      2,
      7,
      5,
      4,
      1,
      6,
      2,
      2,
      0,
      1,
      1,
      2,
      1,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      3,
      0,
      2,
      7,
      4,
      1,
      6,
      5,
      2,
      2,
      0,
      1,
      2,
      1,
      0,
      1
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "eed9b8d92729680c2e1fcae43c706dec4758d9cd7f3679faa5fd2dbd8f358f20",
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
| 1 | 0 | train | `{"friction_scale":1.0012502433119475,"light":851.5112472329253,"mass_scale":1.0356310767628032,"seed":0,"split":"train","task_id":"C07","x":0.5581019690427548,"y":-0.002932780730325786,"yaw_deg":1.2882560525405538}` |
| 2 | 1 | train | `{"friction_scale":0.9590541803842917,"light":927.6193237585362,"mass_scale":1.0356401561551891,"seed":1,"split":"train","task_id":"C07","x":0.5624546063976921,"y":-0.0009581708872706258,"yaw_deg":-1.7934873680865921}` |
| 3 | 2 | train | `{"friction_scale":0.9587647999662648,"light":866.7621506838843,"mass_scale":0.9437816763446226,"seed":2,"split":"train","task_id":"C07","x":0.5608272466753156,"y":-0.0014884269289959912,"yaw_deg":0.20384289496812213}` |
| 4 | 3 | train | `{"friction_scale":1.0051423850983228,"light":1008.2337340358613,"mass_scale":0.9527571930065459,"seed":3,"split":"train","task_id":"C07","x":0.5584221733976144,"y":0.00082998383671263,"yaw_deg":-0.8893361618839739}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C07-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C07"></a>
## `pocket_cube/dual-sharpa/C07`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [3, 0, 2, 7, 5, 4, 1, 6, 2, 2, 0, 1, 1, 2, 1, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      3,
      0,
      2,
      7,
      5,
      4,
      1,
      6,
      2,
      2,
      0,
      1,
      1,
      2,
      1,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      3,
      0,
      2,
      7,
      4,
      1,
      6,
      5,
      2,
      2,
      0,
      1,
      2,
      1,
      0,
      1
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "490c6cf424fa73bf2f807d2642cc65a91ee216c30fca684a8d8247d689fa14b6",
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
| 1 | 0 | train | `{"friction_scale":1.0012502433119475,"light":851.5112472329253,"mass_scale":1.0356310767628032,"seed":0,"split":"train","task_id":"C07","x":0.5581019690427548,"y":-0.002932780730325786,"yaw_deg":1.2882560525405538}` |
| 2 | 1 | train | `{"friction_scale":0.9590541803842917,"light":927.6193237585362,"mass_scale":1.0356401561551891,"seed":1,"split":"train","task_id":"C07","x":0.5624546063976921,"y":-0.0009581708872706258,"yaw_deg":-1.7934873680865921}` |
| 3 | 2 | train | `{"friction_scale":0.9587647999662648,"light":866.7621506838843,"mass_scale":0.9437816763446226,"seed":2,"split":"train","task_id":"C07","x":0.5608272466753156,"y":-0.0014884269289959912,"yaw_deg":0.20384289496812213}` |
| 4 | 3 | train | `{"friction_scale":1.0051423850983228,"light":1008.2337340358613,"mass_scale":0.9527571930065459,"seed":3,"split":"train","task_id":"C07","x":0.5584221733976144,"y":0.00082998383671263,"yaw_deg":-0.8893361618839739}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C07-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C08"></a>
## `pocket_cube/aloha/C08`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [6, 2, 0, 1, 4, 5, 7, 3, 1, 2, 0, 0, 0, 0, 2, 1]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 2,
    "first_violation_sticky": true,
    "goal": [
      6,
      2,
      0,
      1,
      4,
      5,
      7,
      3,
      1,
      2,
      0,
      0,
      0,
      0,
      2,
      1
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      6,
      2,
      4,
      5,
      7,
      3,
      0,
      0,
      1,
      2,
      0,
      0,
      2,
      1
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "2ac9e72d8a117e7182772729ee8eef855aeb2fe3021c2d4447460509501ea7c0",
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
| 1 | 0 | train | `{"friction_scale":0.9717685686986735,"light":767.0982361617318,"mass_scale":1.0236371790911825,"seed":0,"split":"train","task_id":"C08","x":0.558606935866842,"y":-0.00024012229129746461,"yaw_deg":0.5061164730474519}` |
| 2 | 1 | train | `{"friction_scale":0.9757940304052315,"light":798.0347498540121,"mass_scale":1.001203497824355,"seed":1,"split":"train","task_id":"C08","x":0.5589273927784595,"y":-0.0026930448139487837,"yaw_deg":0.4908845866228839}` |
| 3 | 2 | train | `{"friction_scale":1.005387489199559,"light":965.4159777929844,"mass_scale":1.0200546407739512,"seed":2,"split":"train","task_id":"C08","x":0.5624321089999054,"y":0.0013817954943450249,"yaw_deg":-1.3306024107970358}` |
| 4 | 3 | train | `{"friction_scale":1.0365444992569521,"light":1035.2902454577736,"mass_scale":0.9902568939181158,"seed":3,"split":"train","task_id":"C08","x":0.5602841674682613,"y":-0.0005116796348160852,"yaw_deg":-1.5086610945992796}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C08-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C08"></a>
## `pocket_cube/dual-sharpa/C08`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [6, 2, 0, 1, 4, 5, 7, 3, 1, 2, 0, 0, 0, 0, 2, 1]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 2,
    "first_violation_sticky": true,
    "goal": [
      6,
      2,
      0,
      1,
      4,
      5,
      7,
      3,
      1,
      2,
      0,
      0,
      0,
      0,
      2,
      1
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      6,
      2,
      4,
      5,
      7,
      3,
      0,
      0,
      1,
      2,
      0,
      0,
      2,
      1
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "d366161e01e03d47ee52adf0cde1bf53c305fd19c89b2aa4e6c69b8bc523714a",
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
| 1 | 0 | train | `{"friction_scale":0.9717685686986735,"light":767.0982361617318,"mass_scale":1.0236371790911825,"seed":0,"split":"train","task_id":"C08","x":0.558606935866842,"y":-0.00024012229129746461,"yaw_deg":0.5061164730474519}` |
| 2 | 1 | train | `{"friction_scale":0.9757940304052315,"light":798.0347498540121,"mass_scale":1.001203497824355,"seed":1,"split":"train","task_id":"C08","x":0.5589273927784595,"y":-0.0026930448139487837,"yaw_deg":0.4908845866228839}` |
| 3 | 2 | train | `{"friction_scale":1.005387489199559,"light":965.4159777929844,"mass_scale":1.0200546407739512,"seed":2,"split":"train","task_id":"C08","x":0.5624321089999054,"y":0.0013817954943450249,"yaw_deg":-1.3306024107970358}` |
| 4 | 3 | train | `{"friction_scale":1.0365444992569521,"light":1035.2902454577736,"mass_scale":0.9902568939181158,"seed":3,"split":"train","task_id":"C08","x":0.5602841674682613,"y":-0.0005116796348160852,"yaw_deg":-1.5086610945992796}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C08-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C09"></a>
## `pocket_cube/aloha/C09`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [4, 2, 1, 0, 5, 6, 3, 7, 1, 2, 1, 0, 2, 2, 1, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      4,
      2,
      1,
      0,
      5,
      6,
      3,
      7,
      1,
      2,
      1,
      0,
      2,
      2,
      1,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      4,
      1,
      3,
      0,
      5,
      2,
      6,
      7,
      1,
      2,
      0,
      0,
      2,
      1,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "3ceb2d50f6a46592ff0b28013bb9529bd3879d10f6127b60e166d2fd23a03ee9",
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
| 1 | 0 | train | `{"friction_scale":1.0121601069259696,"light":755.8882673685603,"mass_scale":1.5327823605557405,"seed":0,"split":"train","task_id":"C09","x":0.5571754454984786,"y":-0.0025254131072243525,"yaw_deg":1.0898375430907365}` |
| 2 | 1 | train | `{"friction_scale":0.9541389364325469,"light":783.424691928469,"mass_scale":1.4950607575371653,"seed":1,"split":"train","task_id":"C09","x":0.561894668345135,"y":0.0006503374286921208,"yaw_deg":-1.4360825302259657}` |
| 3 | 2 | train | `{"friction_scale":1.0161311177776498,"light":955.4134989949916,"mass_scale":1.523348883280362,"seed":2,"split":"train","task_id":"C09","x":0.5589946981972524,"y":0.0004221632429327123,"yaw_deg":-1.2258004571727392}` |
| 4 | 3 | train | `{"friction_scale":1.0129105036816044,"light":896.191045698147,"mass_scale":1.5087407027702866,"seed":3,"split":"train","task_id":"C09","x":0.5577022494432821,"y":-0.0029134532380301744,"yaw_deg":-0.6657152117527065}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C09-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C09"></a>
## `pocket_cube/dual-sharpa/C09`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [4, 2, 1, 0, 5, 6, 3, 7, 1, 2, 1, 0, 2, 2, 1, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      4,
      2,
      1,
      0,
      5,
      6,
      3,
      7,
      1,
      2,
      1,
      0,
      2,
      2,
      1,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      4,
      1,
      3,
      0,
      5,
      2,
      6,
      7,
      1,
      2,
      0,
      0,
      2,
      1,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "4b1d3ea4c152ae5e107ddb052a373b2e00638f66de7490956ad3a26549f3af63",
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
| 1 | 0 | train | `{"friction_scale":1.0121601069259696,"light":755.8882673685603,"mass_scale":1.5327823605557405,"seed":0,"split":"train","task_id":"C09","x":0.5571754454984786,"y":-0.0025254131072243525,"yaw_deg":1.0898375430907365}` |
| 2 | 1 | train | `{"friction_scale":0.9541389364325469,"light":783.424691928469,"mass_scale":1.4950607575371653,"seed":1,"split":"train","task_id":"C09","x":0.561894668345135,"y":0.0006503374286921208,"yaw_deg":-1.4360825302259657}` |
| 3 | 2 | train | `{"friction_scale":1.0161311177776498,"light":955.4134989949916,"mass_scale":1.523348883280362,"seed":2,"split":"train","task_id":"C09","x":0.5589946981972524,"y":0.0004221632429327123,"yaw_deg":-1.2258004571727392}` |
| 4 | 3 | train | `{"friction_scale":1.0129105036816044,"light":896.191045698147,"mass_scale":1.5087407027702866,"seed":3,"split":"train","task_id":"C09","x":0.5577022494432821,"y":-0.0029134532380301744,"yaw_deg":-0.6657152117527065}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C09-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C10"></a>
## `pocket_cube/aloha/C10`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 2, 7, 1, 4, 5, 6, 3, 0, 0, 1, 1, 0, 0, 0, 1]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      0,
      2,
      7,
      1,
      4,
      5,
      6,
      3,
      0,
      0,
      1,
      1,
      0,
      0,
      0,
      1
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      1,
      2,
      7,
      3,
      0,
      5,
      6,
      4,
      0,
      0,
      1,
      2,
      1,
      0,
      0,
      2
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "1541ee3733529bc66fa76efb62e8610623bfae5187f3f1303487d15c20ba7e0e",
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
| 1 | 0 | train | `{"friction_scale":0.658829436525723,"light":1000.7306197897699,"mass_scale":0.9591287597472313,"seed":0,"split":"train","task_id":"C10","x":0.5572377976153661,"y":0.0012200366833754672,"yaw_deg":0.5216504112557003}` |
| 2 | 1 | train | `{"friction_scale":0.6385960902356638,"light":840.9793338918462,"mass_scale":0.9933343173466641,"seed":1,"split":"train","task_id":"C10","x":0.5580967293483532,"y":-0.002363690791496645,"yaw_deg":1.8832889141719549}` |
| 3 | 2 | train | `{"friction_scale":0.6618426550581498,"light":1020.2292968874506,"mass_scale":0.9557875213581482,"seed":2,"split":"train","task_id":"C10","x":0.5593846570284652,"y":0.00021163145456806276,"yaw_deg":0.3198286211104322}` |
| 4 | 3 | train | `{"friction_scale":0.6709974271029919,"light":899.5619494997293,"mass_scale":0.9696294409300179,"seed":3,"split":"train","task_id":"C10","x":0.558435628881238,"y":0.002231253613303112,"yaw_deg":-1.6748647835155333}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C10-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C10"></a>
## `pocket_cube/dual-sharpa/C10`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 2, 7, 1, 4, 5, 6, 3, 0, 0, 1, 1, 0, 0, 0, 1]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 1,
    "first_violation_sticky": true,
    "goal": [
      0,
      2,
      7,
      1,
      4,
      5,
      6,
      3,
      0,
      0,
      1,
      1,
      0,
      0,
      0,
      1
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      1,
      2,
      7,
      3,
      0,
      5,
      6,
      4,
      0,
      0,
      1,
      2,
      1,
      0,
      0,
      2
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "e9a61464194a05bbd446d33798c8f2e251e7e8a963aed3eb01da77ef8d35dddf",
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
| 1 | 0 | train | `{"friction_scale":0.658829436525723,"light":1000.7306197897699,"mass_scale":0.9591287597472313,"seed":0,"split":"train","task_id":"C10","x":0.5572377976153661,"y":0.0012200366833754672,"yaw_deg":0.5216504112557003}` |
| 2 | 1 | train | `{"friction_scale":0.6385960902356638,"light":840.9793338918462,"mass_scale":0.9933343173466641,"seed":1,"split":"train","task_id":"C10","x":0.5580967293483532,"y":-0.002363690791496645,"yaw_deg":1.8832889141719549}` |
| 3 | 2 | train | `{"friction_scale":0.6618426550581498,"light":1020.2292968874506,"mass_scale":0.9557875213581482,"seed":2,"split":"train","task_id":"C10","x":0.5593846570284652,"y":0.00021163145456806276,"yaw_deg":0.3198286211104322}` |
| 4 | 3 | train | `{"friction_scale":0.6709974271029919,"light":899.5619494997293,"mass_scale":0.9696294409300179,"seed":3,"split":"train","task_id":"C10","x":0.558435628881238,"y":0.002231253613303112,"yaw_deg":-1.6748647835155333}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C10-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C14"></a>
## `pocket_cube/aloha/C14`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 1, 2, 7, 3, 6, 5, 4, 2, 2, 2, 0, 0, 2, 0, 1]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 3,
    "first_violation_sticky": true,
    "goal": [
      0,
      1,
      2,
      7,
      3,
      6,
      5,
      4,
      2,
      2,
      2,
      0,
      0,
      2,
      0,
      1
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      6,
      2,
      3,
      4,
      5,
      7,
      0,
      0,
      1,
      2,
      1,
      0,
      0,
      2
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "ee386102507234beb7cffd8ce748e567f34ccad954d67ab2c1b4b934637c2e25",
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
| 1 | 0 | train | `{"friction_scale":0.999496849406437,"light":1008.7645214682011,"mass_scale":0.9829737797225898,"seed":0,"split":"train","task_id":"C14","x":0.5595307183646947,"y":-0.0014249986609514097,"yaw_deg":1.908487849276248}` |
| 2 | 1 | train | `{"friction_scale":1.0310183223812923,"light":948.8854026587289,"mass_scale":0.971113724911072,"seed":1,"split":"train","task_id":"C14","x":0.560558351353766,"y":0.0013460438660139445,"yaw_deg":-0.00574054348798958}` |
| 3 | 2 | train | `{"friction_scale":1.0110906469222094,"light":827.1802248064389,"mass_scale":1.0337236623647779,"seed":2,"split":"train","task_id":"C14","x":0.5606448767139941,"y":0.002518911093397516,"yaw_deg":-0.5890508744935392}` |
| 4 | 3 | train | `{"friction_scale":0.9614840404843704,"light":837.4881484220718,"mass_scale":0.9858458626425513,"seed":3,"split":"train","task_id":"C14","x":0.5575655113612609,"y":-0.0017369640721668301,"yaw_deg":1.2001158575098478}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C14-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C14"></a>
## `pocket_cube/dual-sharpa/C14`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 1, 2, 7, 3, 6, 5, 4, 2, 2, 2, 0, 0, 2, 0, 1]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 3,
    "first_violation_sticky": true,
    "goal": [
      0,
      1,
      2,
      7,
      3,
      6,
      5,
      4,
      2,
      2,
      2,
      0,
      0,
      2,
      0,
      1
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      6,
      2,
      3,
      4,
      5,
      7,
      0,
      0,
      1,
      2,
      1,
      0,
      0,
      2
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "4a8dcc525a750a4c781ebb207d6c9a8dfe38eb2d3739981fb9fe91f01e44db09",
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
| 1 | 0 | train | `{"friction_scale":0.999496849406437,"light":1008.7645214682011,"mass_scale":0.9829737797225898,"seed":0,"split":"train","task_id":"C14","x":0.5595307183646947,"y":-0.0014249986609514097,"yaw_deg":1.908487849276248}` |
| 2 | 1 | train | `{"friction_scale":1.0310183223812923,"light":948.8854026587289,"mass_scale":0.971113724911072,"seed":1,"split":"train","task_id":"C14","x":0.560558351353766,"y":0.0013460438660139445,"yaw_deg":-0.00574054348798958}` |
| 3 | 2 | train | `{"friction_scale":1.0110906469222094,"light":827.1802248064389,"mass_scale":1.0337236623647779,"seed":2,"split":"train","task_id":"C14","x":0.5606448767139941,"y":0.002518911093397516,"yaw_deg":-0.5890508744935392}` |
| 4 | 3 | train | `{"friction_scale":0.9614840404843704,"light":837.4881484220718,"mass_scale":0.9858458626425513,"seed":3,"split":"train","task_id":"C14","x":0.5575655113612609,"y":-0.0017369640721668301,"yaw_deg":1.2001158575098478}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C14-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C15"></a>
## `pocket_cube/aloha/C15`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 3,
    "first_violation_sticky": true,
    "goal": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      7,
      3,
      5,
      2,
      6,
      4,
      2,
      2,
      1,
      2,
      2,
      1,
      0,
      2
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "d2ec7593aaa9ffb3c2485e8e0786cc7a836b346ee808cec6df23ad66247d9cab",
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
| 1 | 0 | train | `{"friction_scale":1.0047629582020634,"light":828.2986993552274,"mass_scale":0.9680832192743435,"seed":0,"split":"train","task_id":"C15","x":0.558939547901272,"y":0.0013159434555285697,"yaw_deg":1.4750671619535813}` |
| 2 | 1 | train | `{"friction_scale":0.9515518811209933,"light":824.1683872019277,"mass_scale":0.9750057904558471,"seed":1,"split":"train","task_id":"C15","x":0.5608505321720921,"y":-0.0018373531116858016,"yaw_deg":1.7671817303712203}` |
| 3 | 2 | train | `{"friction_scale":1.0326981253831826,"light":751.9032829369887,"mass_scale":0.9656130019335214,"seed":2,"split":"train","task_id":"C15","x":0.5585867771864724,"y":-0.0025815925154904066,"yaw_deg":-1.650905561935481}` |
| 4 | 3 | train | `{"friction_scale":1.047450008090959,"light":919.1618687039104,"mass_scale":0.990264251338948,"seed":3,"split":"train","task_id":"C15","x":0.5622005159582045,"y":0.000756819558762163,"yaw_deg":-0.9181019530491601}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C15-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C15"></a>
## `pocket_cube/dual-sharpa/C15`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 3,
    "first_violation_sticky": true,
    "goal": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      1,
      7,
      3,
      5,
      2,
      6,
      4,
      2,
      2,
      1,
      2,
      2,
      1,
      0,
      2
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "08d6fe14b87e048c60b1a1e58ca727b9fc1432108390daf51bddccfea0a3761b",
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
| 1 | 0 | train | `{"friction_scale":1.0047629582020634,"light":828.2986993552274,"mass_scale":0.9680832192743435,"seed":0,"split":"train","task_id":"C15","x":0.558939547901272,"y":0.0013159434555285697,"yaw_deg":1.4750671619535813}` |
| 2 | 1 | train | `{"friction_scale":0.9515518811209933,"light":824.1683872019277,"mass_scale":0.9750057904558471,"seed":1,"split":"train","task_id":"C15","x":0.5608505321720921,"y":-0.0018373531116858016,"yaw_deg":1.7671817303712203}` |
| 3 | 2 | train | `{"friction_scale":1.0326981253831826,"light":751.9032829369887,"mass_scale":0.9656130019335214,"seed":2,"split":"train","task_id":"C15","x":0.5585867771864724,"y":-0.0025815925154904066,"yaw_deg":-1.650905561935481}` |
| 4 | 3 | train | `{"friction_scale":1.047450008090959,"light":919.1618687039104,"mass_scale":0.990264251338948,"seed":3,"split":"train","task_id":"C15","x":0.5622005159582045,"y":0.000756819558762163,"yaw_deg":-0.9181019530491601}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C15-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C17"></a>
## `pocket_cube/aloha/C17`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 7, 2, 6, 4, 1, 5, 3, 0, 1, 0, 1, 2, 1, 0, 1]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 4,
    "first_violation_sticky": true,
    "goal": [
      0,
      7,
      2,
      6,
      4,
      1,
      5,
      3,
      0,
      1,
      0,
      1,
      2,
      1,
      0,
      1
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      7,
      0,
      2,
      3,
      4,
      1,
      5,
      6,
      1,
      2,
      0,
      0,
      2,
      1,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "cbd014e430a03e748859e55b0fb9290c1642e0deee8e330ff38696a84c834534",
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
| 1 | 0 | train | `{"friction_scale":1.0044301436046306,"light":867.2456338793747,"mass_scale":1.0006611233985427,"seed":0,"split":"train","task_id":"C17","x":0.5600721287543732,"y":-0.0009169166306055468,"yaw_deg":-1.6737249150352786}` |
| 2 | 1 | train | `{"friction_scale":1.0392001461937836,"light":902.6188281852426,"mass_scale":0.9839893097191639,"seed":1,"split":"train","task_id":"C17","x":0.5598562276958209,"y":-0.0020048441400791137,"yaw_deg":-1.767149256138557}` |
| 3 | 2 | train | `{"friction_scale":0.9573619286535933,"light":917.0938890855799,"mass_scale":0.9422217688543275,"seed":2,"split":"train","task_id":"C17","x":0.5615512824134609,"y":-6.359849045821115e-06,"yaw_deg":1.5392944957855081}` |
| 4 | 3 | train | `{"friction_scale":0.9733282834404722,"light":834.3127004236686,"mass_scale":1.0312117017285611,"seed":3,"split":"train","task_id":"C17","x":0.5585397697386317,"y":-0.0008991029060627753,"yaw_deg":-0.3552987381777446}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C17 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C17-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C17"></a>
## `pocket_cube/dual-sharpa/C17`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 7, 2, 6, 4, 1, 5, 3, 0, 1, 0, 1, 2, 1, 0, 1]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 4,
    "first_violation_sticky": true,
    "goal": [
      0,
      7,
      2,
      6,
      4,
      1,
      5,
      3,
      0,
      1,
      0,
      1,
      2,
      1,
      0,
      1
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      7,
      0,
      2,
      3,
      4,
      1,
      5,
      6,
      1,
      2,
      0,
      0,
      2,
      1,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "f515a4038a9101806bb433fe2939856efd4651a3f2055e256b2edd95b13dcd57",
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
| 1 | 0 | train | `{"friction_scale":1.0044301436046306,"light":867.2456338793747,"mass_scale":1.0006611233985427,"seed":0,"split":"train","task_id":"C17","x":0.5600721287543732,"y":-0.0009169166306055468,"yaw_deg":-1.6737249150352786}` |
| 2 | 1 | train | `{"friction_scale":1.0392001461937836,"light":902.6188281852426,"mass_scale":0.9839893097191639,"seed":1,"split":"train","task_id":"C17","x":0.5598562276958209,"y":-0.0020048441400791137,"yaw_deg":-1.767149256138557}` |
| 3 | 2 | train | `{"friction_scale":0.9573619286535933,"light":917.0938890855799,"mass_scale":0.9422217688543275,"seed":2,"split":"train","task_id":"C17","x":0.5615512824134609,"y":-6.359849045821115e-06,"yaw_deg":1.5392944957855081}` |
| 4 | 3 | train | `{"friction_scale":0.9733282834404722,"light":834.3127004236686,"mass_scale":1.0312117017285611,"seed":3,"split":"train","task_id":"C17","x":0.5585397697386317,"y":-0.0008991029060627753,"yaw_deg":-0.3552987381777446}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C17 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C17-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-aloha-C20"></a>
## `pocket_cube/aloha/C20`

作者来源：`env/cube20/README.md`。Action size: 16; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      5.942948205130441,
      4.889521598815918,
      2.025993381227766,
      2.3444851807185585,
      4.056250708443778,
      8.318304334368024,
      0.03999999910593033,
      0.0,
      9.02320384979248,
      4.898664270128523,
      2.04024110521589,
      7.704555647713798,
      4.0468195506504605,
      3.5357740947178433,
      0.03999999910593033,
      0.0
    ],
    "low": [
      -9.017015184674944,
      -4.086456298828125,
      -6.451319285801479,
      -7.628823689052037,
      -2.9250655855451315,
      -3.6496680123465404,
      0.0,
      -0.03999999910593033,
      -5.936759540012905,
      -4.077313627515521,
      -6.43707139151437,
      -2.2687528814588274,
      -2.934496743338449,
      -8.432198251996722,
      0.0,
      -0.03999999910593033
    ],
    "names": [
      "left_arm.joint1",
      "left_arm.joint2",
      "left_arm.joint3",
      "left_arm.joint4",
      "left_arm.joint5",
      "left_arm.joint6",
      "left_gripper.gripper_joint1",
      "left_gripper.gripper_joint2",
      "right_arm.joint1",
      "right_arm.joint2",
      "right_arm.joint3",
      "right_arm.joint4",
      "right_arm.joint5",
      "right_arm.joint6",
      "right_gripper.gripper_joint1",
      "right_gripper.gripper_joint2"
    ],
    "neutral_action": [
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.03959999978542328,
      -0.03959999978542328
    ],
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_arm: joint target = offset + scale * action; offset=[0.5379616618156433, 1.4302597045898438, -0.709097683429718, 0.9247592091560364, -0.19795741140842438, -0.8170113563537598]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "left_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]",
      "right_arm: joint target = offset + scale * action; offset=[-0.540127694606781, 1.4270597696304321, -0.7140843868255615, -0.9512655138969421, -0.19465647637844086, 0.8568742275238037]; scale=[0.35, 0.35, 0.35, 0.35, 0.35, 0.35]",
      "right_gripper: joint target = offset + scale * action; offset=[0.0, 0.0]; scale=[1.0, 1.0]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 4,
    "first_violation_sticky": true,
    "goal": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      2,
      6,
      7,
      4,
      1,
      5,
      3,
      2,
      0,
      1,
      0,
      2,
      1,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "1e1302977554c6c660719380f6907498d090fdb4ade08d57557904d50e64ab99",
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
| 1 | 0 | train | `{"friction_scale":0.713601376093123,"light":922.193748131637,"mass_scale":1.269630427601631,"seed":0,"split":"train","task_id":"C20","x":0.5601555649243806,"y":-0.02313628587160721,"yaw_deg":14.42716231584663}` |
| 2 | 1 | train | `{"friction_scale":0.7371540489055721,"light":996.3502064977382,"mass_scale":1.316839103540846,"seed":1,"split":"train","task_id":"C20","x":0.5623833876472348,"y":-0.023515687126497663,"yaw_deg":14.8260299792474}` |
| 3 | 2 | train | `{"friction_scale":0.7634483946440962,"light":828.5306550262862,"mass_scale":1.2006199263616855,"seed":2,"split":"train","task_id":"C20","x":0.5603307580190638,"y":-0.02210792350893249,"yaw_deg":13.71494057488559}` |
| 4 | 3 | train | `{"friction_scale":0.7352145404530734,"light":912.4413972759504,"mass_scale":1.2004057076020416,"seed":3,"split":"train","task_id":"C20","x":0.5625392958372262,"y":-0.022922659457220364,"yaw_deg":15.967379121007049}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/aloha/C20 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-aloha-C20-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

<a id="pocket_cube-dual-sharpa-C20"></a>
## `pocket_cube/dual-sharpa/C20`

作者来源：`env/cube20/README.md`。Action size: 56; 18000 controls / 300 s; wall: 3600 s.

目标（源数据）：
```json
{"stable_seconds": 1, "state": [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0]}
```

原生动作与评分合同：
```json
{
  "action_spec": {
    "control_period_s": 0.016666666666666666,
    "high": [
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0,
      1.0
    ],
    "low": [
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0,
      -1.0
    ],
    "names": [
      "left_translation.right_x_joint",
      "left_translation.right_y_joint",
      "left_translation.right_z_joint",
      "left_rotation.right_roll_joint",
      "left_rotation.right_pitch_joint",
      "left_rotation.right_yaw_joint",
      "left_hand.right_index_MCP_FE",
      "left_hand.right_index_MCP_AA",
      "left_hand.right_index_PIP",
      "left_hand.right_index_DIP",
      "left_hand.right_middle_MCP_FE",
      "left_hand.right_middle_MCP_AA",
      "left_hand.right_middle_PIP",
      "left_hand.right_middle_DIP",
      "left_hand.right_ring_MCP_FE",
      "left_hand.right_ring_MCP_AA",
      "left_hand.right_ring_PIP",
      "left_hand.right_ring_DIP",
      "left_hand.right_pinky_CMC",
      "left_hand.right_pinky_MCP_FE",
      "left_hand.right_pinky_MCP_AA",
      "left_hand.right_pinky_PIP",
      "left_hand.right_pinky_DIP",
      "left_hand.right_thumb_CMC_FE",
      "left_hand.right_thumb_CMC_AA",
      "left_hand.right_thumb_MCP_FE",
      "left_hand.right_thumb_MCP_AA",
      "left_hand.right_thumb_IP",
      "right_translation.right_x_joint",
      "right_translation.right_y_joint",
      "right_translation.right_z_joint",
      "right_rotation.right_roll_joint",
      "right_rotation.right_pitch_joint",
      "right_rotation.right_yaw_joint",
      "right_hand.right_index_MCP_FE",
      "right_hand.right_index_MCP_AA",
      "right_hand.right_index_PIP",
      "right_hand.right_index_DIP",
      "right_hand.right_middle_MCP_FE",
      "right_hand.right_middle_MCP_AA",
      "right_hand.right_middle_PIP",
      "right_hand.right_middle_DIP",
      "right_hand.right_ring_MCP_FE",
      "right_hand.right_ring_MCP_AA",
      "right_hand.right_ring_PIP",
      "right_hand.right_ring_DIP",
      "right_hand.right_pinky_CMC",
      "right_hand.right_pinky_MCP_FE",
      "right_hand.right_pinky_MCP_AA",
      "right_hand.right_pinky_PIP",
      "right_hand.right_pinky_DIP",
      "right_hand.right_thumb_CMC_FE",
      "right_hand.right_thumb_CMC_AA",
      "right_hand.right_thumb_MCP_FE",
      "right_hand.right_thumb_MCP_AA",
      "right_hand.right_thumb_IP"
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
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
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
    "physics_period_s": 0.004166666666666667,
    "semantics": [
      "left_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "left_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "left_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]",
      "right_translation: current joint position + scale * action; scale=[0.02, 0.02, 0.02]",
      "right_rotation: current joint position + scale * action; scale=[0.08, 0.08, 0.08]",
      "right_hand: current joint position + scale * action; scale=[0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]"
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
    "active_face": -1,
    "angular_speed_limit_rad_s": 0.05,
    "detent_tolerance_degrees": 1.0,
    "expected_committed_quarter_turns": 4,
    "first_violation_sticky": true,
    "goal": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "immutable_scene_fingerprint": true,
    "initial": [
      0,
      2,
      6,
      7,
      4,
      1,
      5,
      3,
      2,
      0,
      1,
      0,
      2,
      1,
      0,
      0
    ],
    "penetration_limit_m": 0.00025,
    "physical_goal_required": true,
    "stable_seconds": 1.0
  },
  "sha256": "b88f390b40a4954dc231bc1931b122d5f68aa364f271207dd747fd361d9e2e8d",
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
| 1 | 0 | train | `{"friction_scale":0.713601376093123,"light":922.193748131637,"mass_scale":1.269630427601631,"seed":0,"split":"train","task_id":"C20","x":0.5601555649243806,"y":-0.02313628587160721,"yaw_deg":14.42716231584663}` |
| 2 | 1 | train | `{"friction_scale":0.7371540489055721,"light":996.3502064977382,"mass_scale":1.316839103540846,"seed":1,"split":"train","task_id":"C20","x":0.5623833876472348,"y":-0.023515687126497663,"yaw_deg":14.8260299792474}` |
| 3 | 2 | train | `{"friction_scale":0.7634483946440962,"light":828.5306550262862,"mass_scale":1.2006199263616855,"seed":2,"split":"train","task_id":"C20","x":0.5603307580190638,"y":-0.02210792350893249,"yaw_deg":13.71494057488559}` |
| 4 | 3 | train | `{"friction_scale":0.7352145404530734,"light":912.4413972759504,"mass_scale":1.2004057076020416,"seed":3,"split":"train","task_id":"C20","x":0.5625392958372262,"y":-0.022922659457220364,"yaw_deg":15.967379121007049}` |

```bash
python scripts/environment_runtime.py --task-id pocket_cube/dual-sharpa/C20 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/pocket_cube-dual-sharpa-C20-default-trial1
```

以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。

