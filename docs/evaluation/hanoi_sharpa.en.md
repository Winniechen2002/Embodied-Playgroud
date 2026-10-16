# FR3 Sharpa Hanoi

[Protocol](../evaluation_protocol.en.md) · [Index](index.en.md) · [JSON](tasks.json)

Embodied Playground paper scope: Launcher uses loaded initialization only. The full 410-task paper setting has 410 groups / 1640 conditions; EP-100 has 100 / 400. This runtime schedule also includes ground and retains 510 groups / 2040 conditions. [EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.en.md)

Each task below has four trials per group at base seed 0. Parameters are private maintainer inputs. Goal strings and field names below are verbatim authoring data, not translated protocol prose.

<a id="hanoi_sharpa-fr3-sharpa-H01"></a>
## `hanoi_sharpa/fr3-sharpa/H01`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "e81a2e85c6b33d4331e5f0fabc4630bd2e20408947346a8dba73d000ebe10860",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0032314388166335283,-0.0016518225546225218],"board_yaw_deg":0.2442929542467509,"friction":1.162169052271446,"friction_factor":0.9684742102262051,"handle_angles":[0.004263716391029667,-1.042933834805568,0.004263716391029667,1.0514612675876274,0.004263716391029667],"light_intensity":832.9774859904287,"mass_factor":1.0030561419454753,"masses":[0.030091684258364258,0.030091684258364258,0.030091684258364258,0.030091684258364258,0.030091684258364258],"pegs":[[0.6719949648096103,-0.29164918656338373],[0.6732314388166336,-0.0016518225546225218],[0.6744679128236569,0.28834554145413865]],"seed":0,"split":"train","task_id":"H01"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00045262669146850775,0.0005039768713876285],"board_yaw_deg":1.1149715964133824,"friction":1.1667103418826061,"friction_factor":0.9722586182355051,"handle_angles":[0.01945992542363092,-1.0277376257729667,0.01945992542363092,1.0666574766202286,0.01945992542363092],"light_intensity":961.7152295193753,"mass_factor":1.0575273846461235,"masses":[0.031725821539383706,0.031725821539383706,0.031725821539383706,0.031725821539383706,0.031725821539383706],"pegs":[[0.6639043511095355,-0.2894411150002659],[0.6695473733085315,0.0005039768713876285],[0.6751903955075276,0.2904490687430412]],"seed":1,"split":"train","task_id":"H01"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.001686885168658228,-0.0015819534779064211],"board_yaw_deg":0.8461240485757484,"friction":1.1852379917880755,"friction_factor":0.9876983264900631,"handle_angles":[0.014767650527951247,-1.0324299006686464,0.014767650527951247,1.061965201724549,0.014767650527951247],"light_intensity":980.8217733461634,"mass_factor":0.9817214975870425,"masses":[0.029451644927611275,0.029451644927611275,0.029451644927611275,0.029451644927611275,0.029451644927611275],"pegs":[[0.6674044221752674,-0.29155033194478375],[0.6716868851686583,-0.0015819534779064211],[0.6759693481620491,0.28838642498897094]],"seed":2,"split":"train","task_id":"H01"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.00295415594432801,0.0016841050658995104],"board_yaw_deg":-1.4798992028733102,"friction":1.2658981613994431,"friction_factor":1.054915134499536,"handle_angles":[-0.02582911368777879,-1.0730266648843765,-0.02582911368777879,1.0213684375088188,-0.02582911368777879],"light_intensity":904.9521190190306,"mass_factor":1.0665566009923402,"masses":[0.031996698029770204,0.031996698029770204,0.031996698029770204,0.031996698029770204,0.031996698029770204],"pegs":[[0.6804437660753243,-0.28821916456051516],[0.6729541559443281,0.0016841050658995104],[0.6654645458133318,0.29158737469231416]],"seed":3,"split":"train","task_id":"H01"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H01-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H02"></a>
## `hanoi_sharpa/fr3-sharpa/H02`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "72ad898c75dd1a928be9e923ddb92fe3f11c31436955cadb3fd2d39a84fe7d17",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003154834231677923,-0.0008014536981916907],"board_yaw_deg":1.5342569897368976,"friction":1.242560822692309,"friction_factor":1.0354673522435909,"handle_angles":[0.026777836042645713,-1.020419715153952,0.026777836042645713,1.0739753872392432,0.026777836042645713],"light_intensity":715.0153825504372,"mass_factor":1.0397207794557561,"masses":[0.031191623383672682,0.031191623383672682,0.031191623383672682,0.031191623383672682,0.031191623383672682],"pegs":[[0.6587592257048833,-0.3026931852399656],[0.6668451657683221,-0.0008014536981916907],[0.6749311058317609,0.3010902778435822]],"seed":0,"split":"train","task_id":"H02"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0017742372999706945,-0.002119254862747299],"board_yaw_deg":1.4598577707806948,"friction":1.2263376295066495,"friction_factor":1.0219480245888746,"handle_angles":[0.025479324710947795,-1.02171822648565,0.025479324710947795,1.0726768759075453,0.025479324710947795],"light_intensity":740.7179498914741,"mass_factor":1.083578382264096,"masses":[0.032507351467922885,0.032507351467922885,0.032507351467922885,0.032507351467922885,0.032507351467922885],"pegs":[[0.6605318391777589,-0.30402123157180005],[0.6682257627000293,-0.002119254862747299],[0.6759196862222997,0.2997827218463055]],"seed":1,"split":"train","task_id":"H02"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00013549857173629132,-0.0012234290412784566],"board_yaw_deg":-1.2404580285444637,"friction":1.227068887633269,"friction_factor":1.0225574063610574,"handle_angles":[-0.021650076830898694,-1.0688476280274963,-0.021650076830898694,1.025547474365699,-0.021650076830898694],"light_intensity":767.0845949001227,"mass_factor":1.000926978957472,"masses":[0.030027809368724158,0.030027809368724158,0.030027809368724158,0.030027809368724158,0.030027809368724158],"pegs":[[0.6764023138630076,-0.30315265420599835],[0.6698645014282637,-0.0012234290412784566],[0.6633266889935198,0.3007057961234414]],"seed":2,"split":"train","task_id":"H02"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0026657265005053284,0.002903543156251627],"board_yaw_deg":0.5158962209226177,"friction":1.2580274131660223,"friction_factor":1.0483561776383519,"handle_angles":[0.009004087653695737,-1.038193463542902,0.009004087653695737,1.0562016388502933,0.009004087653695737],"light_intensity":913.3425503403378,"mass_factor":1.0895584622381087,"masses":[0.03268675386714326,0.03268675386714326,0.03268675386714326,0.03268675386714326,0.03268675386714326],"pegs":[[0.6699465287719591,-0.2990842148136917],[0.6726657265005054,0.002903543156251627],[0.6753849242290516,0.30489130112619495]],"seed":3,"split":"train","task_id":"H02"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H02 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H02-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H03"></a>
## `hanoi_sharpa/fr3-sharpa/H03`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "7f2773e27f437b2df21426361ad4bf3e4919559bb145c98fe1cc772c06e340a8",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0010766806846944292,-0.003604896591363897],"board_yaw_deg":-1.6498361911163457,"friction":1.2572769770343084,"friction_factor":1.047730814195257,"handle_angles":[-0.028795073653542655,-1.0759926248501404,-0.028795073653542655,1.018402477543055,-0.028795073653542655],"light_intensity":808.89859938333,"mass_factor":1.0488096088209207,"masses":[0.03146428826462762,0.03146428826462762,0.03146428826462762,0.03146428826462762,0.03146428826462762],"pegs":[[0.6801170843731483,-0.3174747280520345],[0.6710766806846945,-0.003604896591363897],[0.6620362769962407,0.3102649348693068]],"seed":0,"split":"train","task_id":"H03"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0018034624448567205,-0.0010928904835403666],"board_yaw_deg":1.105761383344331,"friction":1.1708770343750858,"friction_factor":0.9757308619792382,"handle_angles":[0.019299176880765764,-1.0278983743158319,0.019299176880765764,1.0664967280773634,0.019299176880765764],"light_intensity":840.8985225078694,"mass_factor":0.9780596105852308,"masses":[0.029341788317556922,0.029341788317556922,0.029341788317556922,0.029341788317556922,0.029341788317556922],"pegs":[[0.6621369721867589,-0.31503441635666585],[0.6681965375551433,-0.0010928904835403666],[0.6742561029235277,0.3128486353895851]],"seed":1,"split":"train","task_id":"H03"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0032488066377682804,-0.0034017038109174624],"board_yaw_deg":1.752255385999539,"friction":1.2825221799117776,"friction_factor":1.0687684832598148,"handle_angles":[0.030582625821496102,-1.0166149253751016,0.030582625821496102,1.0777801770180937,0.030582625821496102],"light_intensity":822.7650982956175,"mass_factor":0.9642098972613549,"masses":[0.028926296917840644,0.028926296917840644,0.028926296917840644,0.028926296917840644,0.028926296917840644],"pegs":[[0.6571497457184813,-0.3172548736262697],[0.6667511933622318,-0.0034017038109174624],[0.6763526410059822,0.31045146600443474]],"seed":2,"split":"train","task_id":"H03"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00041188435581213903,-0.002010658741980375],"board_yaw_deg":0.0687980864652098,"friction":1.2658090148365855,"friction_factor":1.0548408456971545,"handle_angles":[0.0012007531278896582,-1.045996798068708,0.0012007531278896582,1.0483983043244873,0.0012007531278896582],"light_intensity":825.0362763494124,"mass_factor":1.066610420738641,"masses":[0.031998312622159235,0.031998312622159235,0.031998312622159235,0.031998312622159235,0.031998312622159235],"pegs":[[0.6692110792526329,-0.3160104323781399],[0.6695881156441879,-0.002010658741980375],[0.6699651520357428,0.3119891148941792]],"seed":3,"split":"train","task_id":"H03"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H03 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H03-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H04"></a>
## `hanoi_sharpa/fr3-sharpa/H04`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 0, 0, 0, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      0,
      0,
      0,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "81c599359f3c5e4667dd24ec7b7472737b492448feff5ff8b9c5414f04041481",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0012477987074479896,0.0014281858785747522],"board_yaw_deg":0.6380175329600435,"friction":1.1748072058307582,"friction_factor":0.9790060048589652,"handle_angles":[0.011135506635604203,-1.0360620445609934,0.011135506635604203,1.0583330578322019,0.011135506635604203],"light_intensity":919.44823440647,"mass_factor":0.9133370497664339,"masses":[0.027400111492993016,0.027400111492993016,0.027400111492993016,0.027400111492993016,0.027400111492993016],"pegs":[[0.6651221011522024,-0.3245516024104709],[0.6687522012925521,0.0014281858785747522],[0.6723823014329018,0.32740797416762035]],"seed":0,"split":"train","task_id":"H04"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003175672106628311,-0.002826460505091538],"board_yaw_deg":1.2897207771487391,"friction":1.1273989348935054,"friction_factor":0.9394991124112545,"handle_angles":[0.022509873992625544,-1.0246876772039721,0.022509873992625544,1.0697074251892231,0.022509873992625544],"light_intensity":830.6767679620899,"mass_factor":0.9250663954498275,"masses":[0.027751991863494824,0.027751991863494824,0.027751991863494824,0.027751991863494824,0.027751991863494824],"pegs":[[0.6594867286618481,-0.3287438728007796],[0.6668243278933718,-0.002826460505091538],[0.6741619271248954,0.3230909517905965]],"seed":1,"split":"train","task_id":"H04"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0018134011946089187,9.326511154020434e-05],"board_yaw_deg":-1.2441792470012984,"friction":1.1815750512218322,"friction_factor":0.9846458760181935,"handle_angles":[-0.021715024345156445,-1.0689125755417541,-0.021715024345156445,1.0254825268514411,-0.021715024345156445],"light_intensity":1026.2123922341557,"mass_factor":1.0772532985235033,"masses":[0.032317598955705094,0.032317598955705094,0.032317598955705094,0.032317598955705094,0.032317598955705094],"pegs":[[0.6752651404060295,-0.32582987651667866],[0.6681865988053911,9.326511154020434e-05],[0.6611080572047527,0.3260164067397591]],"seed":2,"split":"train","task_id":"H04"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0008105006997346998,-0.0034684581798404735],"board_yaw_deg":-1.2862426815802905,"friction":1.2612811334028475,"friction_factor":1.0510676111690396,"handle_angles":[-0.022449169773257092,-1.0696467209698548,-0.022449169773257092,1.0247483814233405,-0.022449169773257092],"light_intensity":1061.8499251536996,"mass_factor":1.0451917131668864,"masses":[0.03135575139500659,0.03135575139500659,0.03135575139500659,0.03135575139500659,0.03135575139500659],"pegs":[[0.6765073139561897,-0.32938631529825846],[0.6691894993002654,-0.0034684581798404735],[0.6618716846443411,0.3224493989385775]],"seed":3,"split":"train","task_id":"H04"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H04 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H04-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H05"></a>
## `hanoi_sharpa/fr3-sharpa/H05`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "67f72a13d9ab7068614c20300365c0c01aee8e2db6827f7f717b601ae3082fe1",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.002753302973197674,0.0029777685257494375],"board_yaw_deg":0.9668955288957992,"friction":1.1275009595685097,"friction_factor":0.9395841329737582,"handle_angles":[0.01687551050204367,-1.030322040694554,0.01687551050204367,1.0640730616986414,0.01687551050204367],"light_intensity":956.9229592231284,"mass_factor":1.0109961688675753,"masses":[0.030329885066027257,0.030329885066027257,0.030329885066027257,0.030329885066027257,0.030329885066027257],"pegs":[[0.5821956752094237,-0.29562953829680605],[0.6672466970268024,0.0029777685257494375],[0.7522977188441811,0.3015850753483049]],"seed":0,"split":"train","task_id":"H05"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003922194705686439,-0.0008612103174578501],"board_yaw_deg":1.9064047962715756,"friction":1.2036615271641697,"friction_factor":1.0030512726368082,"handle_angles":[0.033273040570750714,-1.013924510625847,0.033273040570750714,1.0804705917673483,0.033273040570750714],"light_intensity":706.9222494998155,"mass_factor":0.9552351185590515,"masses":[0.028657053556771544,0.028657053556771544,0.028657053556771544,0.028657053556771544,0.028657053556771544],"pegs":[[0.5761420145661316,-0.2980338092327963],[0.6660778052943136,-0.0008612103174578501],[0.7560135960224956,0.29631138859788064]],"seed":1,"split":"train","task_id":"H05"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0018464606595744973,-0.0023222153736265376],"board_yaw_deg":0.8351555174832945,"friction":1.2163150452948275,"friction_factor":1.013595871079023,"handle_angles":[0.014576213546280557,-1.032621337650317,0.014576213546280557,1.0617737647428782,0.014576213546280557],"light_intensity":728.5307413394411,"mass_factor":1.0190316524282779,"masses":[0.030570949572848335,0.030570949572848335,0.030570949572848335,0.030570949572848335,0.030570949572848335],"pegs":[[0.583789328611969,-0.30112429024621606],[0.6681535393404255,-0.0023222153736265376],[0.7525177500688821,0.296479859498963]],"seed":2,"split":"train","task_id":"H05"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.002218621475400116,0.003843020771890021],"board_yaw_deg":-0.9325544905727161,"friction":1.1815322642811403,"friction_factor":0.9846102202342837,"handle_angles":[-0.016276146314752316,-1.06347369751135,-0.016276146314752316,1.0309214048818454,-0.016276146314752316],"light_intensity":1095.3163556662616,"mass_factor":0.9982962693617253,"masses":[0.02994888808085176,0.02994888808085176,0.02994888808085176,0.02994888808085176,0.02994888808085176],"pegs":[[0.5926746031174205,-0.2974192773802941],[0.6677813785246,0.003843020771890021],[0.7428881539317794,0.30510531892407416]],"seed":3,"split":"train","task_id":"H05"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H05 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H05-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H06"></a>
## `hanoi_sharpa/fr3-sharpa/H06`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "3905ffe731315484822014614be7eecf424c2462015581269cd21b1fdd736d58",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0003303968382561684,0.002226423021806329],"board_yaw_deg":1.125790529274722,"friction":1.1831643947482318,"friction_factor":0.9859703289568599,"handle_angles":[0.019648751423613508,-1.0275487997729842,0.019648751423613508,1.066846302620211,0.019648751423613508],"light_intensity":722.3288154968754,"mass_factor":1.0898617157938997,"masses":[0.03269585147381699,0.03269585147381699,0.03269585147381699,0.03269585147381699,0.03269585147381699],"pegs":[[0.5344612446626504,-0.2951614944985295],[0.8302995119573275,-0.0009171749202525536],[0.5462497369453712,0.30472268719798784]],"seed":0,"split":"train","task_id":"H06"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0026578897269189552,-0.0009177844085959585],"board_yaw_deg":-0.026577087966116686,"friction":1.1577503516866101,"friction_factor":0.9647919597388418,"handle_angles":[-0.0004638576906008993,-1.0476614088871985,-0.0004638576906008993,1.0467336935059968,-0.0004638576906008993],"light_intensity":901.9461843801297,"mass_factor":0.9133439745412653,"masses":[0.027400319236237956,0.027400319236237956,0.027400319236237956,0.027400319236237956,0.027400319236237956],"pegs":[[0.537481281560928,-0.3009780536316186],[0.8273420930599649,-0.0008435671807612934],[0.5372029669565481,0.29902188181919537]],"seed":1,"split":"train","task_id":"H06"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.001754433558394231,-0.003048639411415185],"board_yaw_deg":-1.9008918598349556,"friction":1.1823173913333778,"friction_factor":0.9852644927778148,"handle_angles":[-0.03317682167847853,-1.080374372875076,-0.03317682167847853,1.0140207295181192,-0.03317682167847853],"light_intensity":943.2271921878216,"mass_factor":0.9756687275222478,"masses":[0.02927006182566743,0.02927006182566743,0.02927006182566743,0.02927006182566743,0.02927006182566743],"pegs":[[0.5517771933085558,-0.3071957449738922],[0.8316663855153217,0.002258678303339491],[0.5318747518782257,0.2924740748645855]],"seed":2,"split":"train","task_id":"H06"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003872664129523197,0.0013327119789100883],"board_yaw_deg":-0.5584697065311446,"friction":1.1839240190574516,"friction_factor":0.9866033492145431,"handle_angles":[-0.009747135151614954,-1.0569446863482126,-0.009747135151614954,1.0374504160449827,-0.009747135151614954],"light_intensity":1088.738606000026,"mass_factor":1.0440575425299292,"masses":[0.031321726275897875,0.031321726275897875,0.031321726275897875,0.031321726275897875,0.031321726275897875],"pegs":[[0.5468029337560439,-0.2999201446429172],[0.8338650636582051,0.0028922289088165586],[0.5409547452688948,0.30005135358963947]],"seed":3,"split":"train","task_id":"H06"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H06 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H06-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H07"></a>
## `hanoi_sharpa/fr3-sharpa/H07`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 2, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      2,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "9294bef16660f0b765355c61c030b6dcbf11679c762718e0c4e2f67ac6051a02",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0017399282613210928,0.0020110381248457467],"board_yaw_deg":-0.4949875108505508,"friction":1.2810429506872307,"friction_factor":1.067535792239359,"handle_angles":[-0.00863916182059327,-1.0558367130171908,-0.00863916182059327,1.0385583893760044,-0.00863916182059327],"light_intensity":811.7862019199616,"mass_factor":1.0917126615268733,"masses":[0.0327513798458062,0.0327513798458062,0.0327513798458062,0.0327513798458062,0.0327513798458062],"pegs":[[0.574508157388152,-0.3188409257663973],[0.7719953681593885,-0.027123936919677582],[0.6493217393879301,0.28182780818632186]],"seed":0,"split":"train","task_id":"H07"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0013101247863901114,0.0019277505526196213],"board_yaw_deg":1.2209268683159962,"friction":1.105194991141267,"friction_factor":0.920995825951056,"handle_angles":[0.02130919377817737,-1.0258883574184203,0.02130919377817737,1.068506744974775,0.02130919377817737],"light_intensity":892.6066422069348,"mass_factor":0.9188939153064086,"masses":[0.027566817459192258,0.027566817459192258,0.027566817459192258,0.027566817459192258,0.027566817459192258],"pegs":[[0.5618941524802455,-0.3158688410053428],[0.7680279445518842,-0.030196196591904978],[0.6546605385752541,0.2822903331371858]],"seed":1,"split":"train","task_id":"H07"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003763991443471167,-0.002148841344724774],"board_yaw_deg":-0.17681416138203288,"friction":1.2022700768669285,"friction_factor":1.0018917307224404,"handle_angles":[-0.003085989280269081,-1.0502835404768667,-0.003085989280269081,1.0441115619163286,-0.003085989280269081],"light_intensity":972.3162392427524,"mass_factor":1.0062492642075411,"masses":[0.030187477926226232,0.030187477926226232,0.030187477926226232,0.030187477926226232,0.030187477926226232],"pegs":[[0.5747519826118644,-0.3224559160513722],[0.7738560948088209,-0.031840100056678325],[0.6529000110496997,0.2777881057025136]],"seed":2,"split":"train","task_id":"H07"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003111922650800149,0.0008790403234349711],"board_yaw_deg":1.3867476006888533,"friction":1.2198147594024957,"friction_factor":1.0165122995020799,"handle_angles":[0.024203311526152075,-1.0229942396704454,0.024203311526152075,1.0714008627227498,0.024203311526152075],"light_intensity":1083.1605652100795,"mass_factor":1.079540993871115,"masses":[0.03238622981613345,0.03238622981613345,0.03238622981613345,0.03238622981613345,0.03238622981613345],"pegs":[[0.5653969077012785,-0.31660714135133383],[0.7723566056098458,-0.03153226795559842],[0.6598940459601068,0.28128105125736114]],"seed":3,"split":"train","task_id":"H07"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H07 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H07-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H08"></a>
## `hanoi_sharpa/fr3-sharpa/H08`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 0, 0, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      0,
      0,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "66bdd14c1f97551017b237c775cf8a57977aeb9e8af4c50546e80576aa620312",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0027533778625293483,-0.003399132310784143],"board_yaw_deg":0.11372014028521993,"friction":1.1121551589797725,"friction_factor":0.926795965816477,"handle_angles":[0.001984790873806931,-1.0452127603227908,0.001984790873806931,1.0491823420704045,0.001984790873806931],"light_intensity":741.6396892132141,"mass_factor":1.0519007347120182,"masses":[0.031557022041360544,0.031557022041360544,0.031557022041360544,0.031557022041360544,0.031557022041360544],"pegs":[[0.5319994335832244,-0.38312051328612284],[0.7626738090069946,-0.043577684584273274],[0.6233886090099791,0.3166994768647858]],"seed":0,"split":"train","task_id":"H08"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0035436520442629496,-0.0011834012818803155],"board_yaw_deg":-1.1089536513818141,"friction":1.2737182711165818,"friction_factor":1.0614318925971515,"handle_angles":[-0.019354892468626022,-1.0665524436652236,-0.019354892468626022,1.0278426587279716,-0.019354892468626022],"light_intensity":880.531705240788,"mass_factor":0.9335046569816916,"masses":[0.028005139709450746,0.028005139709450746,0.028005139709450746,0.028005139709450746,0.028005139709450746],"pegs":[[0.5409242739997967,-0.38382174301869443],[0.7643009423991995,-0.039434077712889336],[0.6173598381484527,0.3177889784880944]],"seed":1,"split":"train","task_id":"H08"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.002305704025667601,-0.003992232372640634],"board_yaw_deg":1.9805392364019159,"friction":1.2611607526799682,"friction_factor":1.0509672938999735,"handle_angles":[0.034566930640147764,-1.01263062055645,0.034566930640147764,1.0817644818367453,0.034566930640147764],"light_intensity":1017.8947558612276,"mass_factor":0.9135065361474672,"masses":[0.027405196084424016,0.027405196084424016,0.027405196084424016,0.027405196084424016,0.027405196084424016],"pegs":[[0.5192565188484977,-0.3789268225568544],[0.7608695382200035,-0.047078741546606025],[0.6333947879741485,0.31754460939208096]],"seed":2,"split":"train","task_id":"H08"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003966073213433712,-0.0038807719605331113],"board_yaw_deg":0.9730838614475379,"friction":1.1822487537465498,"friction_factor":0.9852072947887915,"handle_angles":[0.01698351728027985,-1.0302140339163177,0.01698351728027985,1.0641810684768775,0.01698351728027985],"light_intensity":810.1798404381484,"mass_factor":0.9199880386009907,"masses":[0.02759964115802972,0.02759964115802972,0.02759964115802972,0.02759964115802972,0.02759964115802972],"pegs":[[0.5196006907728936,-0.381448391587222],[0.7553416392713631,-0.045403446377445096],[0.621475601877933,0.31692221381319174]],"seed":3,"split":"train","task_id":"H08"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H08 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H08-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H09"></a>
## `hanoi_sharpa/fr3-sharpa/H09`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "567e5b32f36907930ba609ebc0ea82a63101e03edf460b85333116fd3e44187b",
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
| 1 | 0 | train | `{"bases":[0.0,0.025,0.05],"board_shift":[-0.0037825496876967473,0.0018142552307777594],"board_yaw_deg":1.083986480361348,"friction":1.1651844248702663,"friction_factor":0.9709870207252219,"handle_angles":[0.018919133129410372,-1.0282784180671873,0.018919133129410372,1.066116684326008,0.018919133129410372],"light_intensity":753.4396677724748,"mass_factor":1.0593109851884757,"masses":[0.03177932955565427,0.03177932955565427,0.03177932955565427,0.03177932955565427,0.03177932955565427],"pegs":[[0.6606933929932296,-0.2901334880225921],[0.6662174503123033,0.0018142552307777594],[0.671741507631377,0.29376199848414764]],"seed":0,"split":"train","task_id":"H09"}` |
| 2 | 1 | train | `{"bases":[0.0,0.025,0.05],"board_shift":[0.002367220405756794,-0.0004955312773313825],"board_yaw_deg":1.3488664991113697,"friction":1.2393689044955447,"friction_factor":1.032807420412954,"handle_angles":[0.02354216157934257,-1.023655389617255,0.02354216157934257,1.0707397127759402,0.02354216157934257],"light_intensity":763.4751820411952,"mass_factor":0.9474730109967067,"masses":[0.0284241903299012,0.0284241903299012,0.0284241903299012,0.0284241903299012,0.0284241903299012],"pegs":[[0.6654935442024363,-0.2924146169422668],[0.6723672204057568,-0.0004955312773313825],[0.6792408966090773,0.29142355438760403]],"seed":1,"split":"train","task_id":"H09"}` |
| 3 | 2 | train | `{"bases":[0.0,0.025,0.05],"board_shift":[0.001877794405049677,-0.001370282410546612],"board_yaw_deg":0.8506990456547514,"friction":1.2160693961486964,"friction_factor":1.013391163457247,"handle_angles":[0.014847499290248973,-1.0323500519063487,0.014847499290248973,1.0620450504868466,0.014847499290248973],"light_intensity":763.7422945278701,"mass_factor":0.9421577247546999,"masses":[0.028264731742641,0.028264731742641,0.028264731742641,0.028264731742641,0.028264731742641],"pegs":[[0.6675424839016519,-0.2933380975594755],[0.6718777944050497,-0.001370282410546612],[0.6762131049084474,0.2905975327383823]],"seed":2,"split":"train","task_id":"H09"}` |
| 4 | 3 | train | `{"bases":[0.0,0.025,0.05],"board_shift":[-0.0009010555020502161,0.0023278897021996965],"board_yaw_deg":-1.4263215078435418,"friction":1.160110403777893,"friction_factor":0.966758669814911,"handle_angles":[-0.02489400650387993,-1.0720915577004775,-0.02489400650387993,1.0223035446927178,-0.02489400650387993],"light_intensity":837.7949323822983,"mass_factor":1.0907334165241962,"masses":[0.032722002495725884,0.032722002495725884,0.032722002495725884,0.032722002495725884,0.032722002495725884],"pegs":[[0.6763672436346374,-0.2895816370824868],[0.6690989444979498,0.0023278897021996965],[0.6618306453612622,0.2942374164868862]],"seed":3,"split":"train","task_id":"H09"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H09 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H09-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H10"></a>
## `hanoi_sharpa/fr3-sharpa/H10`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 1, 2, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      1,
      2,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "593bb0bdb10a5df55228ad6058c313f7a0fee8a447ae7917b9f38a7b521de8ae",
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
| 1 | 0 | train | `{"bases":[0.0,0.04,0.08],"board_shift":[0.003680357630755758,-0.0036411638898604993],"board_yaw_deg":-0.46236056998479524,"friction":1.1744511617484081,"friction_factor":0.9787093014570069,"handle_angles":[-0.008069714277632345,-1.0552672654742299,-0.008069714277632345,1.0391278369189654,-0.008069714277632345],"light_intensity":820.1794274911807,"mass_factor":0.9885199385974061,"masses":[0.02965559815792218,0.02965559815792218,0.02965559815792218,0.02965559815792218,0.02965559815792218],"pegs":[[0.676133524145802,-0.3076312656597199],[0.6736803576307558,-0.0036411638898604993],[0.6712271911157097,0.30034893787999883]],"seed":0,"split":"train","task_id":"H10"}` |
| 2 | 1 | train | `{"bases":[0.0,0.04,0.08],"board_shift":[-0.003510420374070325,0.0005708739531780793],"board_yaw_deg":0.5439732392287626,"friction":1.2761895763100577,"friction_factor":1.0634913135917148,"handle_angles":[0.009494124067280688,-1.0377034271293168,0.009494124067280688,1.0566916752638784,0.009494124067280688],"light_intensity":825.7825346037828,"mass_factor":0.9092091027553815,"masses":[0.027276273082661444,0.027276273082661444,0.027276273082661444,0.027276273082661444,0.027276273082661444],"pegs":[[0.663603409269058,-0.303415425114183],[0.6664895796259297,0.0005708739531780793],[0.6693757499828014,0.30455717302053914]],"seed":1,"split":"train","task_id":"H10"}` |
| 3 | 2 | train | `{"bases":[0.0,0.04,0.08],"board_shift":[-0.00096660624822144,-0.0018106756808345518],"board_yaw_deg":-1.2910487349761075,"friction":1.2293682004636843,"friction_factor":1.0244735003864036,"handle_angles":[-0.02253305122904075,-1.0697306024256383,-0.02253305122904075,1.024664499967557,-0.02253305122904075],"light_intensity":902.3722981515177,"mass_factor":0.9015371343219362,"masses":[0.027046114029658085,0.027046114029658085,0.027046114029658085,0.027046114029658085,0.027046114029658085],"pegs":[[0.6758828616680931,-0.3057335027097752],[0.6690333937517786,-0.0018106756808345518],[0.6621839258354641,0.3021121513481061]],"seed":2,"split":"train","task_id":"H10"}` |
| 4 | 3 | train | `{"bases":[0.0,0.04,0.08],"board_shift":[0.003995847157585708,-0.001914745638411543],"board_yaw_deg":1.8403061419742541,"friction":1.1984378404985305,"friction_factor":0.9986982004154422,"handle_angles":[0.03211940142212495,-1.0150781497744727,0.03211940142212495,1.0793169526187225,0.03211940142212495],"light_intensity":1040.914439925677,"mass_factor":1.0302489501008587,"masses":[0.03090746850302576,0.03090746850302576,0.03090746850302576,0.03090746850302576,0.03090746850302576],"pegs":[[0.6642332279380163,-0.3057579474152058],[0.6739958471575858,-0.001914745638411543],[0.6837584663771552,0.3019284561383827]],"seed":3,"split":"train","task_id":"H10"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H10 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H10-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H11"></a>
## `hanoi_sharpa/fr3-sharpa/H11`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 1, 1, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      1,
      1,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "905baab9e4af4ab640f925ba5e7ac58a34cc855ac4e1e1deded90f80c403157d",
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
| 1 | 0 | train | `{"bases":[0.065,0.0,0.035],"board_shift":[0.003048578577912135,0.0037242789058069548],"board_yaw_deg":1.2657015561850986,"friction":1.2871975844095684,"friction_factor":1.0726646536746405,"handle_angles":[0.02209065950304597,-1.0251068916935517,0.02209065950304597,1.0692882106996435,0.02209065950304597],"light_intensity":904.6634051652729,"mass_factor":1.0479328668199777,"masses":[0.03143798600459933,0.03143798600459933,0.03143798600459933,0.03143798600459933,0.03143798600459933],"pegs":[[0.6660684979172858,-0.31219862066617904],[0.6730485785779122,0.0037242789058069548],[0.6800286592385386,0.31964717847779295]],"seed":0,"split":"train","task_id":"H11"}` |
| 2 | 1 | train | `{"bases":[0.065,0.0,0.035],"board_shift":[-0.00393913504176925,-0.003057041617878488],"board_yaw_deg":1.545473464760309,"friction":1.1312727933541444,"friction_factor":0.9427273277951204,"handle_angles":[0.02697360046227195,-1.0202239507343256,0.02697360046227195,1.0741711516588697,0.02697360046227195],"light_intensity":883.8396625314227,"mass_factor":1.0996808339987,"masses":[0.032990425019961,0.032990425019961,0.032990425019961,0.032990425019961,0.032990425019961],"pegs":[[0.6575382407747731,-0.3189420917184294],[0.6660608649582308,-0.003057041617878488],[0.6745834891416885,0.3128280084826724]],"seed":1,"split":"train","task_id":"H11"}` |
| 3 | 2 | train | `{"bases":[0.065,0.0,0.035],"board_shift":[0.0039989115331517475,0.001748474516336429],"board_yaw_deg":0.8118874508016514,"friction":1.212973818570789,"friction_factor":1.0108115154756576,"handle_angles":[0.014170109172112292,-1.0330274420244854,0.014170109172112292,1.0613676603687099,0.014170109172112292],"light_intensity":841.5620364566677,"mass_factor":1.0628154640204026,"masses":[0.031884463920612074,0.031884463920612074,0.031884463920612074,0.031884463920612074,0.031884463920612074],"pegs":[[0.6695213068828023,-0.3142198008794621],[0.6739989115331518,0.001748474516336429],[0.6784765161835014,0.31771674991213494]],"seed":2,"split":"train","task_id":"H11"}` |
| 4 | 3 | train | `{"bases":[0.065,0.0,0.035],"board_shift":[-0.0006882012441754269,-0.0034443628074645126],"board_yaw_deg":-0.9318805680810296,"friction":1.163038347467555,"friction_factor":0.9691986228896291,"handle_angles":[-0.016264384148369143,-1.0634619353449668,-0.016264384148369143,1.0309331670482285,-0.016264384148369143],"light_intensity":930.0102769459888,"mass_factor":1.0353557458316243,"masses":[0.031060672374948726,0.031060672374948726,0.031060672374948726,0.031060672374948726,0.031060672374948726],"pegs":[[0.6744511175555516,-0.3194025679585173],[0.6693117987558246,-0.0034443628074645126],[0.6641724799560975,0.31251384234358826]],"seed":3,"split":"train","task_id":"H11"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H11 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H11-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H12"></a>
## `hanoi_sharpa/fr3-sharpa/H12`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 0, 0, 1, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      0,
      0,
      1,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "455649decafbee6c4d550769aeacf8e1afa52445cc356799989e335a330890ca",
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
| 1 | 0 | train | `{"bases":[0.04,0.1,0.0],"board_shift":[0.0038757688243496197,0.0025493223997725325],"board_yaw_deg":-1.9731140899225932,"friction":1.1643886711241327,"friction_factor":0.970323892603444,"handle_angles":[-0.03443733738664072,-1.0816348885832383,-0.03443733738664072,1.012760213809957,-0.03443733738664072],"light_intensity":814.7724221110196,"mass_factor":0.9882023286814561,"masses":[0.029646069860443682,0.029646069860443682,0.029646069860443682,0.029646069860443682,0.029646069860443682],"pegs":[[0.6851689830176511,-0.3252562042668537],[0.6738757688243496,0.0025493223997725325],[0.6625825546310482,0.3303548490663987]],"seed":0,"split":"train","task_id":"H12"}` |
| 2 | 1 | train | `{"bases":[0.04,0.1,0.0],"board_shift":[-0.003497191086575122,0.002853601333867138],"board_yaw_deg":0.32589244500562065,"friction":1.2050738193936443,"friction_factor":1.004228182828037,"handle_angles":[0.005687896172722631,-1.041509655023875,0.005687896172722631,1.0528854473693203,0.005687896172722631],"light_intensity":874.6758870428669,"mass_factor":0.971244727046247,"masses":[0.02913734181138741,0.02913734181138741,0.02913734181138741,0.02913734181138741,0.02913734181138741],"pegs":[[0.664637189028283,-0.32514109292572624],[0.666502808913425,0.002853601333867138],[0.668368428798567,0.3308482955934605]],"seed":1,"split":"train","task_id":"H12"}` |
| 3 | 2 | train | `{"bases":[0.04,0.1,0.0],"board_shift":[0.00020864078432092194,0.0003430032752760508],"board_yaw_deg":-1.8716693466048373,"friction":1.2380334496643166,"friction_factor":1.0316945413869305,"handle_angles":[-0.03266679260690536,-1.079864343803503,-0.03266679260690536,1.0145307585896923,-0.03266679260690536],"light_intensity":856.233576086705,"mass_factor":1.0055898549019,"masses":[0.030167695647057,0.030167695647057,0.030167695647057,0.030167695647057,0.030167695647057],"pegs":[[0.6809214432157118,-0.3274820047153682],[0.670208640784321,0.0003430032752760508],[0.6594958383529301,0.32816801126592027]],"seed":2,"split":"train","task_id":"H12"}` |
| 4 | 3 | train | `{"bases":[0.04,0.1,0.0],"board_shift":[-0.0019088529870841318,-0.002155221530292334],"board_yaw_deg":-0.8468501017384533,"friction":1.1757397830030347,"friction_factor":0.9797831525025289,"handle_angles":[-0.014780322546184966,-1.0619778737427825,-0.014780322546184966,1.0324172286504127,-0.014780322546184966],"light_intensity":977.801356574075,"mass_factor":0.9649357752621497,"masses":[0.028948073257864488,0.028948073257864488,0.028948073257864488,0.028948073257864488,0.028948073257864488],"pegs":[[0.6729389162979551,-0.33011939508124444],[0.6680911470129159,-0.002155221530292334],[0.6632433777278768,0.32580895202065974]],"seed":3,"split":"train","task_id":"H12"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H12 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H12-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H13"></a>
## `hanoi_sharpa/fr3-sharpa/H13`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "b0124e911bacf98aad9fb951e584c6f0819e975ea311945156ca189a9120ded9",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003413780701474842,0.003050615125554117],"board_yaw_deg":0.436342603476801,"friction":1.2235468024369356,"friction_factor":1.019622335364113,"handle_angles":[0.007615615097394234,-1.0395819360992034,0.007615615097394234,1.054813166293992,0.007615615097394234],"light_intensity":769.6927227444506,"mass_factor":1.0082724139765495,"masses":[0.030248172419296487,0.030248172419296487,0.030248172419296487,0.030248172419296487,0.030248172419296487],"pegs":[[0.6643548656439916,-0.28994088826809106],[0.6665862192985252,0.003050615125554117],[0.6688175729530589,0.29604211851919926]],"seed":0,"split":"train","task_id":"H13"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0009640222343067832,0.0009376618143023965],"board_yaw_deg":1.4416771311060192,"friction":1.199345380732257,"friction_factor":0.9994544839435475,"handle_angles":[0.025162012688505996,-1.0220355385080917,0.025162012688505996,1.0723595638851036,0.025162012688505996],"light_intensity":745.5658210683605,"mass_factor":1.0063190999206697,"masses":[0.03018957299762009,0.03018957299762009,0.03018957299762009,0.03018957299762009,0.03018957299762009],"pegs":[[0.6635923304434094,-0.29196958999100886],[0.6709640222343068,0.0009376618143023965],[0.6783357140252043,0.2938449136196136]],"seed":1,"split":"train","task_id":"H13"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0033756332807160856,0.0027083757259884775],"board_yaw_deg":-0.6781543042603224,"friction":1.2144948621093714,"friction_factor":1.0120790517578095,"handle_angles":[-0.011836025445914035,-1.0590335766425116,-0.011836025445914035,1.0353615257506836,-0.011836025445914035],"light_intensity":725.2871391941194,"mass_factor":1.0189293132744863,"masses":[0.03056787939823459,0.03056787939823459,0.03056787939823459,0.03056787939823459,0.03056787939823459],"pegs":[[0.670092241203658,-0.2902711011090974],[0.6666243667192839,0.0027083757259884775],[0.6631564922349099,0.2956878525610743]],"seed":2,"split":"train","task_id":"H13"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0009083504783901471,0.00043678976043962515],"board_yaw_deg":1.757820380314364,"friction":1.2743466442853517,"friction_factor":1.0619555369044598,"handle_angles":[0.030679753295144566,-1.016517797901453,0.030679753295144566,1.0778773044917422,0.030679753295144566],"light_intensity":748.4101058596281,"mass_factor":1.0313935900459246,"masses":[0.030941807701377735,0.030941807701377735,0.030941807701377735,0.030941807701377735,0.030941807701377735],"pegs":[[0.661920592868132,-0.2924253283312303],[0.6709083504783901,0.00043678976043962515],[0.6798961080886483,0.2932989078521096]],"seed":3,"split":"train","task_id":"H13"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H13 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H13-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H14"></a>
## `hanoi_sharpa/fr3-sharpa/H14`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 2, 1, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      2,
      1,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "d9962b41a7cb33cbfc51d17eb18834dc8ad62dfcf5bd8cb4be1a626278595790",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0015363520933486519,-0.00038811338643727925],"board_yaw_deg":0.6192065549548118,"friction":1.1140666496398062,"friction_factor":0.9283888746998384,"handle_angles":[0.010807193133892674,-1.036390358062705,0.010807193133892674,1.0580047443304903,0.010807193133892674],"light_intensity":871.14163684705,"mass_factor":0.9898473586874148,"masses":[0.029695420760622444,0.029695420760622444,0.029695420760622444,0.029695420760622444,0.029695420760622444],"pegs":[[0.6682402223505306,-0.3053703022577196],[0.6715363520933487,-0.00038811338643727925],[0.6748324818361668,0.304594075484845]],"seed":0,"split":"train","task_id":"H14"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0009194847871639929,0.0023176960546735757],"board_yaw_deg":-0.13274863508111845,"friction":1.110135427614744,"friction_factor":0.92511285634562,"handle_angles":[-0.002316900759693967,-1.0495144519562916,-0.002316900759693967,1.0448806504369037,-0.002316900759693967],"light_intensity":901.9556571634121,"mass_factor":1.042971567195395,"masses":[0.03128914701586185,0.03128914701586185,0.03128914701586185,0.03128914701586185,0.03128914701586185],"pegs":[[0.6697871693123191,-0.3026814853212503],[0.6690805152128361,0.0023176960546735757],[0.6683738611133531,0.30731687743059743]],"seed":1,"split":"train","task_id":"H14"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0038986824709618564,-0.0006444601131151102],"board_yaw_deg":1.9954280337622508,"friction":1.2018669579242598,"friction_factor":1.0015557982702166,"handle_angles":[0.03482678917574785,-1.0123707620208497,0.03482678917574785,1.0820243403723455,0.03482678917574785],"light_intensity":1012.4104743304777,"mass_factor":0.9771475530490984,"masses":[0.02931442659147295,0.02931442659147295,0.02931442659147295,0.02931442659147295,0.02931442659147295],"pegs":[[0.6632786589232311,-0.30545951075833117],[0.6738986824709619,-0.0006444601131151102],[0.6845187060186926,0.304170590532101]],"seed":2,"split":"train","task_id":"H14"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003950522599520974,-0.002346562751953613],"board_yaw_deg":-0.5216203274489064,"friction":1.2768869132999496,"friction_factor":1.064072427749958,"handle_angles":[-0.00910399215931437,-1.056301543355912,-0.00910399215931437,1.0380935590372833,-0.00910399215931437],"light_intensity":941.3058163892981,"mass_factor":0.9528365549907685,"masses":[0.028585096649723054,0.028585096649723054,0.028585096649723054,0.028585096649723054,0.028585096649723054],"pegs":[[0.6688261566522659,-0.3073339232315851],[0.666049477400479,-0.002346562751953613],[0.6632727981486922,0.3026407977276779]],"seed":3,"split":"train","task_id":"H14"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H14 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H14-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H15"></a>
## `hanoi_sharpa/fr3-sharpa/H15`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 1, 2, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      1,
      2,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "cef10a8bbc3d6f03bfae8236b04f77f0dbbe764824a9664c6040df7431a0e4a2",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00013957934689855467,-0.002566118561452552],"board_yaw_deg":-1.5719918338049819,"friction":1.1776814993943976,"friction_factor":0.9814012494953314,"handle_angles":[-0.027436433314360433,-1.074633984510958,-0.027436433314360433,1.0197611178822372,-0.027436433314360433],"light_intensity":910.0849557129912,"mass_factor":1.0814981249564575,"masses":[0.03244494374869372,0.03244494374869372,0.03244494374869372,0.03244494374869372,0.03244494374869372],"pegs":[[0.6785566788884546,-0.3194468139228205],[0.6698604206531015,-0.002566118561452552],[0.6611641624177483,0.31431457679991537]],"seed":0,"split":"train","task_id":"H15"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.001128236876303744,-0.0018054345982430715],"board_yaw_deg":0.2333600065522372,"friction":1.1317466056671535,"friction_factor":0.9431221713892947,"handle_angles":[0.00407290045681208,-1.0431246507397856,0.00407290045681208,1.0512704516534097,0.00407290045681208],"light_intensity":756.1481528543568,"mass_factor":0.90870188653597,"masses":[0.027261056596079098,0.027261056596079098,0.027261056596079098,0.027261056596079098,0.027261056596079098],"pegs":[[0.6698371310010901,-0.3188028053217539],[0.6711282368763037,-0.0018054345982430715],[0.6724193427515174,0.3151919361252678]],"seed":1,"split":"train","task_id":"H15"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0034984113708756382,-0.0011961981056254985],"board_yaw_deg":-1.1240842700573026,"friction":1.1379090973628074,"friction_factor":0.9482575811356728,"handle_angles":[-0.019618971582377038,-1.0668165227789748,-0.019618971582377038,1.0275785796142205,-0.019618971582377038],"light_intensity":914.5868745167425,"mass_factor":1.0128020087432896,"masses":[0.030384060262298687,0.030384060262298687,0.030384060262298687,0.030384060262298687,0.030384060262298687],"pegs":[[0.6727204036616448,-0.3181351927711467],[0.6665015886291245,-0.0011961981056254985],[0.6602827735966041,0.31574279655989573]],"seed":2,"split":"train","task_id":"H15"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.00331307564622023,0.0003208272162219146],"board_yaw_deg":-0.49358558712699097,"friction":1.276270221849783,"friction_factor":1.0635585182081526,"handle_angles":[-0.008614693635755332,-1.055812244832353,-0.008614693635755332,1.0385828575608422,-0.008614693635755332],"light_intensity":917.6999023928006,"mass_factor":0.926725371370836,"masses":[0.027801761141125078,0.027801761141125078,0.027801761141125078,0.027801761141125078,0.027801761141125078],"pegs":[[0.6760438997513784,-0.3166674101045132],[0.6733130756462202,0.0003208272162219146],[0.6705822515410621,0.317309064536957]],"seed":3,"split":"train","task_id":"H15"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H15 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H15-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H16"></a>
## `hanoi_sharpa/fr3-sharpa/H16`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 0, 0, 1, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      0,
      0,
      1,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "db4dfabdbca47319006b40ee505671fb5d5a024ab7e4704392248bf78e5022ec",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00012067251130303137,-0.0037036446867223702],"board_yaw_deg":-0.8328452909426267,"friction":1.1862388364718015,"friction_factor":0.9885323637265013,"handle_angles":[-0.014535892486678945,-1.0617334436832766,-0.014535892486678945,1.0326616587099187,-0.014535892486678945],"light_intensity":973.0869680465887,"mass_factor":1.0518213734620594,"masses":[0.03155464120386178,0.03155464120386178,0.03155464120386178,0.03155464120386178,0.03155464120386178],"pegs":[[0.6746614677078654,-0.33266888773668984],[0.669879327488697,-0.0037036446867223702],[0.6650971872695287,0.32526159836324514]],"seed":0,"split":"train","task_id":"H16"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0019419281608125175,0.003958439764636646],"board_yaw_deg":1.9519923020134993,"friction":1.2814105638632256,"friction_factor":1.067842136552688,"handle_angles":[0.0340686926437191,-1.0131288585528786,0.0340686926437191,1.0812662438403167,0.0340686926437191],"light_intensity":756.8125568371884,"mass_factor":0.9574486878088119,"masses":[0.028723460634264356,0.028723460634264356,0.028723460634264356,0.028723460634264356,0.028723460634264356],"pegs":[[0.6607354964136734,-0.3248506475299463],[0.6719419281608126,0.003958439764636646],[0.6831483599079518,0.33276752705921964]],"seed":1,"split":"train","task_id":"H16"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0020351446790933085,-0.001603227839280939],"board_yaw_deg":0.5794438435523928,"friction":1.1968381560210022,"friction_factor":0.9973651300175018,"handle_angles":[0.01011320290040017,-1.0370843482961976,0.01011320290040017,1.0573107540969977,0.01011320290040017],"light_intensity":821.9572336105709,"mass_factor":1.02833107927115,"masses":[0.0308499323781345,0.0308499323781345,0.0308499323781345,0.0308499323781345,0.0308499323781345],"pegs":[[0.6646376682830661,-0.33058640343708445],[0.6679648553209068,-0.001603227839280939],[0.6712920423587474,0.3273799477585225]],"seed":2,"split":"train","task_id":"H16"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003767119607964462,-0.003745966611380904],"board_yaw_deg":-1.7788224951713019,"friction":1.23084590101398,"friction_factor":1.0257049175116502,"handle_angles":[-0.03104630934928015,-1.0782438605458777,-0.03104630934928015,1.0161512418473175,-0.03104630934928015],"light_intensity":824.1738094931275,"mass_factor":1.0698961069386543,"masses":[0.03209688320815963,0.03209688320815963,0.03209688320815963,0.03209688320815963,0.03209688320815963],"pegs":[[0.6839797145913903,-0.33258742218489046],[0.6737671196079645,-0.003745966611380904],[0.6635545246245388,0.3250954889621287]],"seed":3,"split":"train","task_id":"H16"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H16 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H16-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H17"></a>
## `hanoi_sharpa/fr3-sharpa/H17`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "72e2b86ec936d13f73e5394ddf969bdc63d76809a3331e6aefe302f77ef5046c",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0033603496973219553,-0.002792307821109007],"board_yaw_deg":-0.8136375572214298,"friction":1.234379484550642,"friction_factor":1.0286495704588683,"handle_angles":[-0.014200654291397717,-1.0613982054879953,-0.014200654291397717,1.0329968969052,-0.014200654291397717],"light_intensity":1072.9817994717228,"mass_factor":0.9409152896769298,"masses":[0.018818305793538596,0.018818305793538596,0.018818305793538596,0.018818305793538596,0.018818305793538596],"pegs":[[0.6775352017399009,-0.29676266450766775],[0.673360349697322,-0.002792307821109007],[0.669185497654743,0.29117804886544973]],"seed":0,"split":"train","task_id":"H17"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0026064424290032752,-0.00016333638894012204],"board_yaw_deg":1.0201397230475018,"friction":1.1250317410179242,"friction_factor":0.9375264508482702,"handle_angles":[0.01780479699756199,-1.0293927541990358,0.01780479699756199,1.0650023481941595,0.01780479699756199],"light_intensity":845.6101141445417,"mass_factor":0.9884541776768753,"masses":[0.019769083553537507,0.019769083553537507,0.019769083553537507,0.019769083553537507,0.019769083553537507],"pegs":[[0.667372108678667,-0.2941167370329709],[0.6726064424290034,-0.00016333638894012204],[0.6778407761793397,0.2937900642550907]],"seed":1,"split":"train","task_id":"H17"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0009801418170811008,0.0005404245771578346],"board_yaw_deg":0.24365583249942802,"friction":1.246272777753368,"friction_factor":1.0385606481278067,"handle_angles":[0.004252596518802824,-1.042944954677795,0.004252596518802824,1.0514501477154004,0.004252596518802824],"light_intensity":950.0074103373945,"mass_factor":1.036864393364609,"masses":[0.02073728786729218,0.02073728786729218,0.02073728786729218,0.02073728786729218,0.02073728786729218],"pegs":[[0.6697298822089638,-0.2934569169940072],[0.6709801418170811,0.0005404245771578346],[0.6722304014251984,0.29453776614832294]],"seed":2,"split":"train","task_id":"H17"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0008715296989188905,-0.0006708887192726798],"board_yaw_deg":-1.5388965532399284,"friction":1.2352676969036123,"friction_factor":1.029389747419677,"handle_angles":[-0.02685881170162896,-1.0740563628982267,-0.02685881170162896,1.0203387394949686,-0.02685881170162896],"light_intensity":928.1646541055433,"mass_factor":1.0624355124825624,"masses":[0.021248710249651248,0.021248710249651248,0.021248710249651248,0.021248710249651248,0.021248710249651248],"pegs":[[0.6787670709576235,-0.29456484991655907],[0.670871529698919,-0.0006708887192726798],[0.6629759884402144,0.2932230724780137]],"seed":3,"split":"train","task_id":"H17"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H17 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H17-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H18"></a>
## `hanoi_sharpa/fr3-sharpa/H18`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 2, 1, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      2,
      1,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "1046ff625b9dbe48d13a27f759508df5a146c15f75ebf74087cee0fcc1028b37",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00026455672631733765,-0.0006320421918994663],"board_yaw_deg":-0.7655520526723627,"friction":1.1219428964731228,"friction_factor":0.9349524137276024,"handle_angles":[-0.013361403914533783,-1.0605589551111314,-0.013361403914533783,1.0338361472820639,-0.013361403914533783],"light_intensity":901.9951496957651,"mass_factor":1.089824377712154,"masses":[0.032694731331364614,0.032694731331364614,0.032694731331364614,0.05994034077416847,0.07628770643985078],"pegs":[[0.6738239112185987,-0.3066047279497353],[0.6697354432736827,-0.0006320421918994663],[0.6656469753287667,0.30534064356593643]],"seed":0,"split":"train","task_id":"H18"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0013148730046068664,-0.00042628842352583044],"board_yaw_deg":-1.7771129149744425,"friction":1.106543194055277,"friction_factor":0.9221193283793975,"handle_angles":[-0.03101647154601806,-1.0782140227426158,-0.03101647154601806,1.0161810796505795,-0.03101647154601806],"light_intensity":743.9507692358055,"mass_factor":1.0221443857222972,"masses":[0.030664331571668913,0.030664331571668913,0.030664331571668913,0.05621794121472634,0.0715501070005608],"pegs":[[0.6781746455975236,-0.3062791109324898],[0.6686851269953932,-0.00042628842352583044],[0.6591956083932627,0.30542653408543813]],"seed":1,"split":"train","task_id":"H18"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0013263353246948308,-0.0017037377429531455],"board_yaw_deg":-0.44426093280231216,"friction":1.1866181929912125,"friction_factor":0.9888484941593438,"handle_angles":[-0.007753816015381626,-1.0549513672119792,-0.007753816015381626,1.039443735181216,-0.007753816015381626],"light_intensity":955.5399674928541,"mass_factor":1.0707133347998452,"masses":[0.03212140004399536,0.03212140004399536,0.03212140004399536,0.058889233413991486,0.07494993343598917],"pegs":[[0.6710463086012955,-0.3076945391746309],[0.6686736646753052,-0.0017037377429531455],[0.6663010207493149,0.30428706368872466]],"seed":2,"split":"train","task_id":"H18"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0024904546470388175,0.001229802389875645],"board_yaw_deg":0.7962487343862779,"friction":1.227602111912135,"friction_factor":1.023001759926779,"handle_angles":[0.01389716207987834,-1.0333003891167194,0.01389716207987834,1.0610947132764759,0.01389716207987834],"light_intensity":829.4147928446325,"mass_factor":1.0695541320626865,"masses":[0.03208662396188059,0.03208662396188059,0.03208662396188059,0.05882547726344776,0.07486878924438806],"pegs":[[0.6682380599319683,-0.30474064902526876],[0.6724904546470388,0.001229802389875645],[0.6767428493621094,0.30720025380502003]],"seed":3,"split":"train","task_id":"H18"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H18 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H18-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H19"></a>
## `hanoi_sharpa/fr3-sharpa/H19`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 2, 0, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      2,
      0,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "50d91bd95de12afc4d52a65beabd687f02304ae9467dce3f829836f274a65a5d",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0011293282479251014,-0.002763609853639115],"board_yaw_deg":-1.4475767465915814,"friction":1.1548398834691072,"friction_factor":0.9623665695575894,"handle_angles":[-0.025264980403330698,-1.0724625315999283,-0.025264980403330698,1.021932570793267,-0.025264980403330698],"light_intensity":703.8180822258022,"mass_factor":0.9453336107136169,"masses":[0.01890667221427234,0.06617335274995319,0.033086676374976594,0.07562668885708936,0.042540012482112755],"pegs":[[0.6769040808100967,-0.3206621224939258],[0.6688706717520749,-0.002763609853639115],[0.6608372626940532,0.3151349027866476]],"seed":0,"split":"train","task_id":"H19"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0010277651294930679,-0.00022304334988548113],"board_yaw_deg":-0.9478598341679083,"friction":1.257709233352858,"friction_factor":1.0480910277940483,"handle_angles":[-0.016543274953637447,-1.063740826150235,-0.016543274953637447,1.0306542762429602,-0.016543274953637447],"light_intensity":965.052898655448,"mass_factor":0.9051283126297596,"masses":[0.018102566252595192,0.06335898188408318,0.03167949094204159,0.07241026501038077,0.04073077406833918],"pegs":[[0.6742327563482295,-0.3181795292308664],[0.6689722348705069,-0.00022304334988548113],[0.6637117133927843,0.3177334425310954]],"seed":1,"split":"train","task_id":"H19"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0021065577614913585,0.0009464405408192596],"board_yaw_deg":1.0192390407207441,"friction":1.1113506581820927,"friction_factor":0.9261255484850772,"handle_angles":[0.017789077125445543,-1.029408474071152,0.017789077125445543,1.0649866283220433,0.017789077125445543],"light_intensity":1071.0669558616205,"mass_factor":0.9758384070041657,"masses":[0.019516768140083313,0.0683086884902916,0.0341543442451458,0.07806707256033325,0.04391272831518746],"pegs":[[0.662236814064822,-0.3170032450349093],[0.6678934422385087,0.0009464405408192596],[0.6735500704121953,0.31889612611654783]],"seed":2,"split":"train","task_id":"H19"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.002365021588300191,-0.003521200691732547],"board_yaw_deg":-1.7559524618354776,"friction":1.1840611615237324,"friction_factor":0.9867176346031103,"handle_angles":[-0.030647151967529155,-1.0778447031641267,-0.030647151967529155,1.0165503992290685,-0.030647151967529155],"light_intensity":889.7397685204555,"mass_factor":1.0329830373884579,"masses":[0.02065966074776916,0.07230881261719206,0.03615440630859603,0.08263864299107664,0.046484236682480605],"pegs":[[0.677379247189505,-0.3213718719604683],[0.6676349784116998,-0.003521200691732547],[0.6578907096338946,0.31432947057700317]],"seed":3,"split":"train","task_id":"H19"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H19 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H19-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H20"></a>
## `hanoi_sharpa/fr3-sharpa/H20`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 0, 2, 1, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      0,
      2,
      1,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "ea9f7065fe38765e05434854d09bb432bfe2fa0f32792f03c9caae3213a27c0c",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.002831442376674264,0.00027950140339747876],"board_yaw_deg":1.6590679470060716,"friction":1.1909888809445917,"friction_factor":0.992490734120493,"handle_angles":[0.02895619818955875,-1.0182413530070389,0.02895619818955875,1.0761537493861564,0.02895619818955875],"light_intensity":859.2354403274527,"mass_factor":1.031364571250111,"masses":[0.1031364571250111,0.06703869713125721,0.09282281141250998,0.04125458285000444,0.07735234284375832],"pegs":[[0.6632772322441577,-0.3295821621295807],[0.6728314423766742,0.00027950140339747876],[0.6823856525091908,0.3301411649363757]],"seed":0,"split":"train","task_id":"H20"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.001363601585732077,0.0029006317225701165],"board_yaw_deg":-1.973076248356273,"friction":1.1234790732770503,"friction_factor":0.9362325610642087,"handle_angles":[-0.034436676926714316,-1.081634228123312,-0.034436676926714316,1.0127608742698833,-0.034436676926714316],"light_intensity":709.2039362097653,"mass_factor":1.0956441936789336,"masses":[0.10956441936789336,0.07121687258913069,0.09860797743110403,0.043825767747157345,0.08217331452592001],"pegs":[[0.6827254590186347,-0.3269037166351712],[0.6713636015857322,0.0029006317225701165],[0.6600017441528296,0.3327049800803114]],"seed":1,"split":"train","task_id":"H20"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.001278383261267809,0.0018555702490706354],"board_yaw_deg":0.07143844153356693,"friction":1.2635207693549957,"friction_factor":1.0529339744624964,"handle_angles":[0.00124683601725421,-1.0459507151793435,0.00124683601725421,1.0484443872138518,0.00124683601725421],"light_intensity":821.7680970069088,"mass_factor":0.9005399316848963,"masses":[0.09005399316848964,0.05853509555951826,0.08104859385164066,0.03602159726739585,0.06754049487636722],"pegs":[[0.6683101609596466,-0.32814417324195366],[0.6687216167387322,0.0018555702490706354],[0.6691330725178178,0.3318553137400949]],"seed":2,"split":"train","task_id":"H20"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.000761585484683068,-0.0015967109096909216],"board_yaw_deg":-0.3277950055637744,"friction":1.1528527303332818,"friction_factor":0.9607106086110682,"handle_angles":[-0.005721102118680994,-1.0529186533152786,-0.005721102118680994,1.0414764490779167,-0.005721102118680994],"light_intensity":710.8907815940928,"mass_factor":0.9597670269331833,"masses":[0.09597670269331833,0.062384856750656914,0.0863790324239865,0.038390681077327335,0.07198252701998874],"pegs":[[0.6726495388847051,-0.3315913103078619],[0.6707615854846831,-0.0015967109096909216],[0.6688736320846611,0.32839788848848]],"seed":3,"split":"train","task_id":"H20"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H20 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H20-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H21"></a>
## `hanoi_sharpa/fr3-sharpa/H21`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "8461c2ea62c6122fccda6367871a43744c0a9f00aded61bead9bbb8600536237",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0006625129332589932,0.002329715915078293],"board_yaw_deg":-1.8862447673798644,"friction":1.8298741045492135,"friction_factor":1.016596724749563,"handle_angles":[-0.032921181689293165,-1.0801187328858908,-0.032921181689293165,1.0142763695073045,-0.032921181689293165],"light_intensity":713.768085780797,"mass_factor":1.071928210882017,"masses":[0.03215784632646051,0.03215784632646051,0.03215784632646051,0.03215784632646051,0.03215784632646051],"pegs":[[0.6803725073543363,-0.2925104374025162],[0.6706625129332591,0.002329715915078293],[0.6609525185121818,0.2971698692326728]],"seed":0,"split":"train","task_id":"H21"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0036282245595661367,-6.9112370779840225e-06],"board_yaw_deg":0.4605972952898574,"friction":1.7036182122537844,"friction_factor":0.9464545623632136,"handle_angles":[0.008038939328588582,-1.039158611868009,0.008038939328588582,1.0552364905251863,0.008038939328588582],"light_intensity":1033.777282109636,"mass_factor":0.9122553627906553,"masses":[0.02736766088371966,0.02736766088371966,0.02736766088371966,0.02736766088371966,0.02736766088371966],"pegs":[[0.6640003138811305,-0.29499737916794644],[0.6663717754404339,-6.9112370779840225e-06],[0.6687432369997374,0.2949835566937905]],"seed":1,"split":"train","task_id":"H21"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.002301199467499728,-0.0008870063761018532],"board_yaw_deg":-0.448818000987367,"friction":1.7978308009886002,"friction_factor":0.9987948894381112,"handle_angles":[-0.007833351859448716,-1.0550309030560463,-0.007833351859448716,1.039364199337149,-0.007833351859448716],"light_intensity":931.0127887036733,"mass_factor":0.9374006769755635,"masses":[0.028122020309266905,0.028122020309266905,0.028122020309266905,0.028122020309266905,0.028122020309266905],"pegs":[[0.6700096156983923,-0.29587795561568286],[0.6676988005325003,-0.0008870063761018532],[0.6653879853666083,0.2941039428634792]],"seed":2,"split":"train","task_id":"H21"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0028378463219176976,0.002629926171677593],"board_yaw_deg":1.5178154251944374,"friction":1.7471713304542076,"friction_factor":0.9706507391412265,"handle_angles":[0.026490876607200627,-1.020706674589397,0.026490876607200627,1.0736884278037984,0.026490876607200627],"light_intensity":812.1447844227728,"mass_factor":0.9119294250952528,"masses":[0.027357882752857582,0.027357882752857582,0.027357882752857582,0.027357882752857582,0.027357882752857582],"pegs":[[0.6650239517192588,-0.29226656931638095],[0.6728378463219178,0.002629926171677593],[0.6806517409245768,0.2975264216597361]],"seed":3,"split":"train","task_id":"H21"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H21 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H21-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H22"></a>
## `hanoi_sharpa/fr3-sharpa/H22`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "5229e08058bc534dcf2f4d178d4117685e029ef43b8b5a521cd6f31affa97415",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0012154879736029378,0.00018484327009873037],"board_yaw_deg":-0.6280856562971393,"friction":1.2793861319639093,"friction_factor":1.0661551099699245,"handle_angles":[-0.010962162686934536,-1.0581597138835321,-0.010962162686934536,1.0362353885096631,-0.010962162686934536],"light_intensity":862.1651780485586,"mass_factor":1.0243603577317637,"masses":[0.03073081073195291,0.03073081073195291,0.03073081073195291,0.03073081073195291,0.03073081073195291],"pegs":[[0.6745808045164202,-0.3067967109714658],[0.671215487973603,0.00018484327009873037],[0.6678501714307857,0.30716639751166325]],"seed":0,"split":"train","task_id":"H22"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0030032124064611194,0.001813842071971691],"board_yaw_deg":-1.3454822740591479,"friction":1.2115313770758707,"friction_factor":1.009609480896559,"handle_angles":[-0.02348309570955282,-1.0706806469061505,-0.02348309570955282,1.0237144554870448,-0.02348309570955282],"light_intensity":998.9996403111711,"mass_factor":0.9559285331536688,"masses":[0.028677855994610063,0.028677855994610063,0.028677855994610063,0.028677855994610063,0.028677855994610063],"pegs":[[0.6742054353919896,-0.3051015133550872],[0.666996787593539,0.001813842071971691],[0.6597881397950883,0.3087291974990306]],"seed":1,"split":"train","task_id":"H22"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0006969508381973122,0.0017862494817681488],"board_yaw_deg":-1.2386560599526506,"friction":1.1295559985448849,"friction_factor":0.9412966654540708,"handle_angles":[-0.02161862654595403,-1.0688161777425516,-0.02161862654595403,1.0255789246506437,-0.02161862654595403],"light_intensity":1045.7691061661985,"mass_factor":1.0707361147649181,"masses":[0.03212208344294754,0.03212208344294754,0.03212208344294754,0.03212208344294754,0.03212208344294754],"pegs":[[0.6773333522226467,-0.3051420127826647],[0.6706969508381974,0.0017862494817681488],[0.664060549453748,0.30871451174620096]],"seed":2,"split":"train","task_id":"H22"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003159412327571467,-0.00032925659384423734],"board_yaw_deg":1.5946763490578941,"friction":1.217876812346652,"friction_factor":1.01489734362221,"handle_angles":[0.027832352794742627,-1.019365198401855,0.027832352794742627,1.0750299039913402,0.027832352794742627],"light_intensity":898.37446010014,"mass_factor":0.9365867681851564,"masses":[0.02809760304555469,0.02809760304555469,0.02809760304555469,0.02809760304555469,0.02809760304555469],"pegs":[[0.664615983132747,-0.307210357050671],[0.6731594123275715,-0.00032925659384423734],[0.681702841522396,0.3065518438629825]],"seed":3,"split":"train","task_id":"H22"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H22 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H22-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H23"></a>
## `hanoi_sharpa/fr3-sharpa/H23`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 2, 0, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      2,
      0,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "1f0722839bf1a0be09f226c7e1ff6c547a87e873e83aceb313395a14d90c4358",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003038098359136548,-0.0009476032334285938],"board_yaw_deg":-1.7298948707511543,"friction":0.8133114000515326,"friction_factor":1.0166392500644157,"handle_angles":[-0.030192361207969396,-1.077389912404567,-0.030192361207969396,1.0170051899886283,-0.030192361207969396],"light_intensity":1092.3495614724795,"mass_factor":1.0676220146998572,"masses":[0.03202866044099571,0.03202866044099571,0.03202866044099571,0.03202866044099571,0.03202866044099571],"pegs":[[0.6826679983602842,-0.3198022174794324],[0.6730380983591366,-0.0009476032334285938],[0.663408198357989,0.31790701101257524]],"seed":0,"split":"train","task_id":"H23"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.000453594664376217,0.003767984831436401],"board_yaw_deg":0.5998689982095866,"friction":0.7574560296650903,"friction_factor":0.9468200370813629,"handle_angles":[0.010469689099397257,-1.0367278620972005,0.010469689099397257,1.0576672402959948,0.010469689099397257],"light_intensity":878.6282807864742,"mass_factor":0.9067617827439047,"masses":[0.02720285348231714,0.02720285348231714,0.02720285348231714,0.02720285348231714,0.02720285348231714],"pegs":[[0.6671138248569204,-0.3152145318330874],[0.6704535946643763,0.003767984831436401],[0.6737933644718321,0.32275050149596024]],"seed":1,"split":"train","task_id":"H23"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0006535381457319334,-0.003357891163447553],"board_yaw_deg":1.5486799798901816,"friction":0.798767846216272,"friction_factor":0.9984598077703399,"handle_angles":[0.02702956470880324,-1.0201679864877944,0.02702956470880324,1.0742271159054009,0.02702956470880324],"light_intensity":954.7916506321613,"mass_factor":1.0058719774417848,"masses":[0.030176159323253543,0.030176159323253543,0.030176159323253543,0.030176159323253543,0.030176159323253543],"pegs":[[0.6620321568861878,-0.3222413679777497],[0.6706535381457319,-0.003357891163447553],[0.6792749194052761,0.31552558565085465]],"seed":2,"split":"train","task_id":"H23"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0036687705978771918,0.0023034896656165867],"board_yaw_deg":0.27695536318000014,"friction":0.8189455827842944,"friction_factor":1.023681978480368,"handle_angles":[0.004833782968547675,-1.04236376822805,0.004833782968547675,1.0520313341651453,0.004833782968547675],"light_intensity":932.699614143051,"mass_factor":1.0568051619614083,"masses":[0.031704154858842246,0.031704154858842246,0.031704154858842246,0.031704154858842246,0.031704154858842246],"pegs":[[0.6721267998357356,-0.3166927835511229],[0.6736687705978772,0.0023034896656165867],[0.6752107413600188,0.3212997628823561]],"seed":3,"split":"train","task_id":"H23"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H23 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H23-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H24"></a>
## `hanoi_sharpa/fr3-sharpa/H24`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 0, 2, 1, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      0,
      2,
      1,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "afdac808530d5f527f7aad6dff13e115a4130500e671bb4d063c76f6cab54f5c",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0025734010591188182,0.0022945405577812685],"board_yaw_deg":0.4102674529318211,"friction":0.5520860675214836,"friction_factor":1.003792850039061,"handle_angles":[0.007160517867431142,-1.0400370333291664,0.007160517867431142,1.0543580690640288,0.007160517867431142],"light_intensity":888.944536923714,"mass_factor":1.028939567401087,"masses":[0.03086818702203261,0.03086818702203261,0.03086818702203261,0.03086818702203261,0.03086818702203261],"pegs":[[0.6702032898989116,-0.32869697379430635],[0.6725734010591189,0.0022945405577812685],[0.6749435122193261,0.3332860549098689]],"seed":0,"split":"train","task_id":"H24"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0017948115004496627,0.0005358320403230677],"board_yaw_deg":1.5250593118748281,"friction":0.5197800290258028,"friction_factor":0.9450545982287322,"handle_angles":[0.026617306280414806,-1.020580244916183,0.026617306280414806,1.0738148574770123,0.026617306280414806],"light_intensity":1019.4202438140464,"mass_factor":0.927094728797723,"masses":[0.02781284186393169,0.02781284186393169,0.02781284186393169,0.02781284186393169,0.02781284186393169],"pegs":[[0.6629855234098145,-0.3303469212777309],[0.6717948115004497,0.0005358320403230677],[0.6806040995910849,0.3314185853583771]],"seed":1,"split":"train","task_id":"H24"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003956229045723635,-0.003556589001121538],"board_yaw_deg":0.7000206067529822,"friction":0.5562483405916767,"friction_factor":1.011360619257594,"handle_angles":[0.012217664419647991,-1.0349798867769497,0.012217664419647991,1.0594152156162455,0.012217664419647991],"light_intensity":767.148618396255,"mass_factor":0.962011867441402,"masses":[0.028860356023242058,0.028860356023242058,0.028860356023242058,0.028860356023242058,0.028860356023242058],"pegs":[[0.6619998246406616,-0.33453188490432423],[0.6660437709542764,-0.003556589001121538],[0.6700877172678911,0.32741870690208114]],"seed":2,"split":"train","task_id":"H24"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00018684263270476187,-0.003488441653907057],"board_yaw_deg":-0.27403436962718697,"friction":0.5113948900599682,"friction_factor":0.9298088910181239,"handle_angles":[-0.004782802013621559,-1.0519803532102192,-0.004782802013621559,1.042414749182976,-0.004782802013621559],"light_intensity":974.3843705434376,"mass_factor":1.0065434876290593,"masses":[0.030196304628871778,0.030196304628871778,0.030196304628871778,0.030196304628871778,0.030196304628871778],"pegs":[[0.6713962587981622,-0.3344846558163346],[0.6698131573672953,-0.003488441653907057],[0.6682300559364284,0.3275077725085205]],"seed":3,"split":"train","task_id":"H24"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H24 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H24-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H25"></a>
## `hanoi_sharpa/fr3-sharpa/H25`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "2621d52e2bec2030ff3e831db99b8929932523f595638c66ea3633e6e9de6aff",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0011903040423433217,0.002095626166847522],"board_yaw_deg":-1.0625115776585246,"friction":1.1426269403187663,"friction_factor":0.9521891169323053,"handle_angles":[0.24325506242844874,-0.803942488768149,0.24325506242844874,0.7668538380267476,0.24325506242844874],"light_intensity":959.244482877715,"mass_factor":0.9334899382168944,"masses":[0.028004698146506832,0.028004698146506832,0.028004698146506832,0.028004698146506832,0.028004698146506832],"pegs":[[0.6742985016620302,-0.29385347927518557],[0.6688096959576567,0.002095626166847522],[0.6633208902532832,0.29804473160888056]],"seed":0,"split":"train","task_id":"H25"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0011312446520647583,0.0015797334049089864],"board_yaw_deg":-1.3218548531001466,"friction":1.2254540798414166,"friction_factor":1.0212117332011805,"handle_angles":[0.23872866837908588,-0.8084688828175118,0.23872866837908588,0.7623274439773847,0.23872866837908588],"light_intensity":973.9706748987512,"mass_factor":1.067293399657628,"masses":[0.03201880198972884,0.03201880198972884,0.03201880198972884,0.03201880198972884,0.03201880198972884],"pegs":[[0.6756970825199227,-0.2943414958910513],[0.6688687553479353,0.0015797334049089864],[0.662040428175948,0.29750096270086923]],"seed":1,"split":"train","task_id":"H25"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003643131283757107,0.0035176348675585193],"board_yaw_deg":-1.4639934665616159,"friction":1.2803764022011654,"friction_factor":1.066980335167638,"handle_angles":[0.2362478815799637,-0.810949669616634,0.2362478815799637,0.7598466571782626,0.2362478815799637],"light_intensity":960.4660012829929,"mass_factor":1.0025185409584751,"masses":[0.030075556228754255,0.030075556228754255,0.030075556228754255,0.030075556228754255,0.030075556228754255],"pegs":[[0.6739192916026641,-0.29238574422785996],[0.6663568687162429,0.0035176348675585193],[0.6587944458298217,0.299421013962977]],"seed":2,"split":"train","task_id":"H25"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003087253053668726,-0.002987351747905171],"board_yaw_deg":-1.2465913952023269,"friction":1.141468041999269,"friction_factor":0.9512233683327244,"handle_angles":[0.24004226352583896,-0.8071552876707587,0.24004226352583896,0.7636410391241378,0.24004226352583896],"light_intensity":805.2565268642657,"mass_factor":1.067080893208361,"masses":[0.03201242679625083,0.03201242679625083,0.03201242679625083,0.03201242679625083,0.03201242679625083],"pegs":[[0.6733523476482375,-0.2989172953879498],[0.6669127469463313,-0.002987351747905171],[0.6604731462444251,0.2929425918921395]],"seed":3,"split":"train","task_id":"H25"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H25 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H25-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H26"></a>
## `hanoi_sharpa/fr3-sharpa/H26`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "6d773d03806b3204736a80a82b4434e96f979f93c530d21c9f390385e7704584",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.001610054271969024,-0.00038832674395704813],"board_yaw_deg":-0.3443274556249334,"friction":1.2813033298708134,"friction_factor":1.0677527748923445,"handle_angles":[-0.0060096478056697565,0.5175891277926291,-0.5296084234039685,0.5175891277926291,-0.5296084234039685],"light_intensity":745.7386227266278,"mass_factor":1.0475198570132527,"masses":[0.03142559571039758,0.03142559571039758,0.03142559571039758,0.03142559571039758,0.03142559571039758],"pegs":[[0.673461014654562,-0.30838276491721706],[0.6716100542719691,-0.00038832674395704813],[0.6697590938893762,0.30760611142930294]],"seed":0,"split":"train","task_id":"H26"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.001004904173370345,-0.0007854644119331514],"board_yaw_deg":-0.5736596575694801,"friction":1.1361485225968957,"friction_factor":0.9467904354974132,"handle_angles":[-0.01001224981045064,0.5135865257878481,-0.5336110254087495,0.5135865257878481,-0.5336110254087495],"light_intensity":1006.8679068863432,"mass_factor":1.0700718373691442,"masses":[0.032102155121074324,0.032102155121074324,0.032102155121074324,0.032102155121074324,0.032102155121074324],"pegs":[[0.6740886255930357,-0.30877002678837095],[0.6710049041733703,-0.0007854644119331514],[0.6679211827537049,0.3071990979645046]],"seed":1,"split":"train","task_id":"H26"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00360691600012098,-0.0035493225122228836],"board_yaw_deg":-1.7365041237413745,"friction":1.282554899052521,"friction_factor":1.0687957492104343,"handle_angles":[-0.030307714433746018,0.4932910611645528,-0.5539064900320448,0.4932910611645528,-0.5539064900320448],"light_intensity":1014.5597303866829,"mass_factor":0.99012507764768,"masses":[0.0297037523294304,0.0297037523294304,0.0297037523294304,0.0297037523294304,0.0297037523294304],"pegs":[[0.6757264310229308,-0.311407875476644],[0.6663930839998791,-0.0035493225122228836],[0.6570597369768273,0.3043092304521982]],"seed":2,"split":"train","task_id":"H26"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0011449636271923757,0.0017395213110044314],"board_yaw_deg":-0.7296640983818972,"friction":1.2331849170898292,"friction_factor":1.0276540975748578,"handle_angles":[-0.012735040950359934,0.5108637346479389,-0.5363338165486587,0.5108637346479389,-0.5363338165486587],"light_intensity":1071.983722346322,"mass_factor":1.0054473773601806,"masses":[0.03016342132080542,0.03016342132080542,0.03016342132080542,0.03016342132080542,0.03016342132080542],"pegs":[[0.672777322963277,-0.3062355031112728],[0.6688550363728076,0.0017395213110044314],[0.6649327497823383,0.3097145457332816]],"seed":3,"split":"train","task_id":"H26"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H26 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H26-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H27"></a>
## `hanoi_sharpa/fr3-sharpa/H27`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [2, 1, 1, 0, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      2,
      1,
      1,
      0,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "0ea814ff0f06499dbfa9f6fa53b70d9ea1fb343926f7321ccd142aae6cf326f0",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.002003388200551938,-0.002892853301573774],"board_yaw_deg":0.9721143898232487,"friction":1.1398011514493624,"friction_factor":0.9498342928744687,"handle_angles":[0.8023647602058797,-0.5938986413895839,0.3660324472072972,-0.7684315665890169,0.6278318350064467],"light_intensity":743.9258480584333,"mass_factor":1.0464360171310358,"masses":[0.031393080513931075,0.031393080513931075,0.031393080513931075,0.031393080513931075,0.031393080513931075],"pegs":[[0.6665743377032407,-0.3228467959412882],[0.6720033882005519,-0.002892853301573774],[0.6774324386978632,0.3170610893381406]],"seed":0,"split":"train","task_id":"H27"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0030278162315199074,0.002792916922301656],"board_yaw_deg":1.1247847851036898,"friction":1.2734136471920738,"friction_factor":1.0611780393267283,"handle_angles":[0.8050293612738445,-0.5912340403216191,0.3686970482752622,-0.7657669655210521,0.6304964360744115],"light_intensity":810.8974612612005,"mass_factor":1.0233956699808442,"masses":[0.030701870099425325,0.030701870099425325,0.030701870099425325,0.030701870099425325,0.030701870099425325],"pegs":[[0.6606906039361617,-0.31714542362913994],[0.6669721837684801,0.002792916922301656],[0.6732537636007985,0.32273125747374326]],"seed":1,"split":"train","task_id":"H27"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.002900797113996878,-0.0002153264305164],"board_yaw_deg":1.0213539101102593,"friction":1.284923944918585,"friction_factor":1.070769954098821,"handle_angles":[0.8032241519569905,-0.5930392496384731,0.3668918389584081,-0.7675721748379061,0.6286912267575575],"light_intensity":816.7015492460166,"mass_factor":1.0677537436547495,"masses":[0.03203261230964249,0.03203261230964249,0.03203261230964249,0.03203261230964249,0.03203261230964249],"pegs":[[0.6671967828763157,-0.3201644852379375],[0.6729007971139969,-0.0002153264305164],[0.678604811351678,0.31973383237690467]],"seed":2,"split":"train","task_id":"H27"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0022650920915347345,0.0017239888698661328],"board_yaw_deg":1.6935532696873803,"friction":1.1350701046868665,"friction_factor":0.9458917539057221,"handle_angles":[0.8149562440114085,-0.581307157584055,0.37862393101282615,-0.755840082783488,0.6404233188119756],"light_intensity":1053.9466380603135,"mass_factor":1.0510808676879262,"masses":[0.031532426030637786,0.031532426030637786,0.031532426030637786,0.031532426030637786,0.031532426030637786],"pegs":[[0.6582776993482442,-0.31813623248666406],[0.6677349079084653,0.0017239888698661328],[0.6771921164686865,0.3215842102263963]],"seed":3,"split":"train","task_id":"H27"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H27 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H27-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H28"></a>
## `hanoi_sharpa/fr3-sharpa/H28`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 0, 2, 2, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      0,
      2,
      2,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "67e4579d2bfdfdb94aed7230f75a52171e753c5d2dbf7ba09188ce36fcd2f98c",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0034720770947711897,-0.0006338591654502915],"board_yaw_deg":0.9707520828388312,"friction":1.2502035270287901,"friction_factor":1.0418362725239918,"handle_angles":[1.064140371262728,-0.8557218059310344,0.5405415956644292,-1.0302547311304673,0.8023409834635786],"light_intensity":920.5030203437307,"mass_factor":1.0064975923120643,"masses":[0.030194927769361928,0.030194927769361928,0.030194927769361928,0.030194927769361928,0.030194927769361928],"pegs":[[0.6609031757581438,-0.3325862084861492],[0.6665279229052289,-0.0006338591654502915],[0.6721526700523139,0.33131849015524867]],"seed":0,"split":"train","task_id":"H28"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0023389727305670282,-0.002130077276961319],"board_yaw_deg":1.3780271492348675,"friction":1.1054140573732314,"friction_factor":0.9211783811443595,"handle_angles":[1.0712486621326174,-0.848613515061145,0.5476498865343186,-1.0231464402605779,0.809449274333468],"light_intensity":828.3182940191141,"mass_factor":1.0848478709024059,"masses":[0.032545436127072176,0.032545436127072176,0.032545436127072176,0.032545436127072176,0.032545436127072176],"pegs":[[0.6596768282418474,-0.33403405822007665],[0.667661027269433,-0.002130077276961319],[0.6756452262970186,0.32977390366615406]],"seed":1,"split":"train","task_id":"H28"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003131352954846541,-0.0015085712555459644],"board_yaw_deg":0.37845723586308444,"friction":1.1765376781269,"friction_factor":0.98044806510575,"handle_angles":[1.0538028760404052,-0.8660593011533572,0.5302041004421064,-1.04059222635279,0.7920034882412559],"light_intensity":928.6895598490424,"mass_factor":1.0430238481077792,"masses":[0.03129071544323337,0.03129071544323337,0.03129071544323337,0.03129071544323337,0.03129071544323337],"pegs":[[0.6646756951436213,-0.3335013286493746],[0.6668686470451535,-0.0015085712555459644],[0.6690615989466856,0.3304841861382826]],"seed":2,"split":"train","task_id":"H28"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.00044399711938046104,0.0017441821075469789],"board_yaw_deg":0.7548502841040658,"friction":1.2902408299610766,"friction_factor":1.0752006916342305,"handle_angles":[1.060372174013828,-0.8594900031799342,0.5367733984155294,-1.0340229283793672,0.7985727862146789],"light_intensity":1086.2342830402845,"mass_factor":0.9091988513396593,"masses":[0.027275965540189778,0.027275965540189778,0.027275965540189778,0.027275965540189778,0.027275965540189778],"pegs":[[0.6660701488752625,-0.33022700557526596],[0.6704439971193805,0.0017441821075469789],[0.6748178453634985,0.3337153697903599]],"seed":3,"split":"train","task_id":"H28"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H28 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H28-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H29"></a>
## `hanoi_sharpa/fr3-sharpa/H29`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "af89c77ff0cc32c0588193ce29857c6bf937f8ddd201c03168755a7ff09a57cf",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003225215416403578,7.064817038807903e-05],"board_yaw_deg":1.1193361300605775,"friction":1.2777933617045352,"friction_factor":1.064827801420446,"handle_angles":[0.019536100906088552,-1.027661450290509,0.019536100906088552,1.0667336521026862,0.019536100906088552],"light_intensity":1021.2921946216183,"mass_factor":1.0332642603825515,"masses":[0.030997927811476544,0.030997927811476544,0.030997927811476544,0.030997927811476544,0.030997927811476544],"pegs":[[0.6674233625188554,-0.29687267723524413],[0.6732252154164036,7.064817038807903e-05],[0.6790270683139518,0.29701397357602033]],"seed":0,"split":"train","task_id":"H29"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0015859633133386236,-0.0014761648398815975],"board_yaw_deg":-0.31111615783939994,"friction":1.1998541938036997,"friction_factor":0.9998784948364164,"handle_angles":[-0.005430001310451897,-1.0526275525070494,-0.005430001310451897,1.0417675498861458,-0.005430001310451897],"light_intensity":1026.4975563476435,"mass_factor":1.0400451736351943,"masses":[0.03120135520905583,0.03120135520905583,0.03120135520905583,0.03120135520905583,0.03120135520905583],"pegs":[[0.6731986657774499,-0.2984717863408765],[0.6715859633133386,-0.0014761648398815975],[0.6699732608492274,0.2955194566611133]],"seed":1,"split":"train","task_id":"H29"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0012137154529995313,0.0028539338568213963],"board_yaw_deg":-0.21697696394178867,"friction":1.1839733262936913,"friction_factor":0.9866444385780762,"handle_angles":[-0.0037869624217652265,-1.0509845136183629,-0.0037869624217652265,1.0434105887748324,-0.0037869624217652265],"light_intensity":953.9303373136775,"mass_factor":1.0417232134823193,"masses":[0.03125169640446958,0.03125169640446958,0.03125169640446958,0.03125169640446958,0.03125169640446958],"pegs":[[0.6699110096979639,-0.29414393649469267],[0.6687862845470005,0.0028539338568213963],[0.6676615593960371,0.2998518042083355]],"seed":2,"split":"train","task_id":"H29"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0017285832260478834,0.003969203048380786],"board_yaw_deg":1.3392468044540462,"friction":1.292130719649087,"friction_factor":1.0767755997075725,"handle_angles":[0.023374266234535767,-1.0238232849620619,0.023374266234535767,1.0705718174311334,0.023374266234535767],"light_intensity":759.1377635776053,"mass_factor":1.0990528520280072,"masses":[0.03297158556084021,0.03297158556084021,0.03297158556084021,0.03297158556084021,0.03297158556084021],"pegs":[[0.6647870582856895,-0.2929496667317367],[0.6717285832260479,0.003969203048380786],[0.6786701081664063,0.3008880728284983]],"seed":3,"split":"train","task_id":"H29"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H29 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H29-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H30"></a>
## `hanoi_sharpa/fr3-sharpa/H30`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 1, 2, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      1,
      2,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "594958c3cbe348fa9cd05ee40bb5b02484f4213dff903501b9ab7a4e43af5418",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0013114163409342194,2.4103334064295547e-05],"board_yaw_deg":1.1983082562373146,"friction":1.2837377756989719,"friction_factor":1.0697814797491432,"handle_angles":[0.020914424525173017,-1.0262831266714245,0.020914424525173017,1.0681119757217707,0.020914424525173017],"light_intensity":1072.804708790142,"mass_factor":0.9380315511472258,"masses":[0.028140946534416775,0.028140946534416775,0.028140946534416775,0.028140946534416775,0.028140946534416775],"pegs":[[0.6648493302869374,-0.3089083187971046],[0.6713114163409343,2.4103334064295547e-05],[0.6777735023949312,0.30895652546523317]],"seed":0,"split":"train","task_id":"H30"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0038221692498139875,-0.003590720144984338],"board_yaw_deg":0.7756178098570954,"friction":1.2390725693951685,"friction_factor":1.0325604744959738,"handle_angles":[0.013537084519113644,-1.033660466677484,0.013537084519113644,1.0607346357157112,0.013537084519113644],"light_intensity":804.4967593245524,"mass_factor":1.0531187569131402,"masses":[0.031593562707394204,0.031593562707394204,0.031593562707394204,0.031593562707394204,0.031593562707394204],"pegs":[[0.6696393378886328,-0.3125624080417946],[0.673822169249814,-0.003590720144984338],[0.6780050006109951,0.3053809677518259]],"seed":1,"split":"train","task_id":"H30"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.00033996774701620193,-0.003175378631865482],"board_yaw_deg":-1.0913218786590664,"friction":1.1912769964343577,"friction_factor":0.9927308303619649,"handle_angles":[-0.019047159981650748,-1.0662447111782485,-0.019047159981650748,1.0281503912149468,-0.019047159981650748],"light_intensity":1098.4087128108395,"mass_factor":0.9439467723355186,"masses":[0.028318403170065558,0.028318403170065558,0.028318403170065558,0.028318403170065558,0.028318403170065558],"pegs":[[0.6755452488184108,-0.31211932860657854],[0.6696600322529839,-0.003175378631865482],[0.6637748156875569,0.30576857134284763]],"seed":2,"split":"train","task_id":"H30"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0035646028797928714,0.0019055374434801013],"board_yaw_deg":-1.882141457931032,"friction":1.274209724124114,"friction_factor":1.061841436770095,"handle_angles":[-0.03284956542918285,-1.0800471166257806,-0.03284956542918285,1.0143479857674147,-0.03284956542918285],"light_intensity":836.1445258511567,"mass_factor":1.0791819342272202,"masses":[0.03237545802681661,0.03237545802681661,0.03237545802681661,0.03237545802681661,0.03237545802681661],"pegs":[[0.6837132931358906,-0.30692775753309104],[0.6735646028797929,0.0019055374434801013],[0.6634159126236953,0.31073883242005124]],"seed":3,"split":"train","task_id":"H30"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H30 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H30-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H31"></a>
## `hanoi_sharpa/fr3-sharpa/H31`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [2, 1, 1, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      2,
      1,
      1,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "f5c7cde2439a7820f3af5c9bd299d9809ad311c565ea5f219c6a6b338afc83e0",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0034610888015192067,-0.0005840002317426608],"board_yaw_deg":0.2615368940988567,"friction":1.1945088622867697,"friction_factor":0.9954240519056414,"handle_angles":[0.004564679917464778,-1.0426328712791328,0.004564679917464778,1.0517622311140624,0.004564679917464778],"light_intensity":1095.783920739934,"mass_factor":1.0777793763347852,"masses":[0.03233338129004355,0.03233338129004355,0.03233338129004355,0.03233338129004355,0.03233338129004355],"pegs":[[0.671995831636449,-0.32158065601095825],[0.6734610888015192,-0.0005840002317426608],[0.6749263459665894,0.32041265554747295]],"seed":0,"split":"train","task_id":"H31"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0029262420099899693,0.003307150877499399],"board_yaw_deg":-1.6041152532486067,"friction":1.1197166003251469,"friction_factor":0.9330971669376225,"handle_angles":[-0.02799709275065085,-1.0751946439472484,-0.02799709275065085,1.0192004584459469,-0.02799709275065085],"light_intensity":781.9181153067526,"mass_factor":1.0655791541666984,"masses":[0.03196737462500095,0.03196737462500095,0.03196737462500095,0.03196737462500095,0.03196737462500095],"pegs":[[0.6819121347627489,-0.3175670514688967],[0.67292624200999,0.003307150877499399],[0.663940349257231,0.32418135322389546]],"seed":1,"split":"train","task_id":"H31"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003955825055938515,0.0028743266028908995],"board_yaw_deg":-0.1169349345268964,"friction":1.2652587915270939,"friction_factor":1.0543823262725782,"handle_angles":[-0.00204089961809834,-1.049238450814696,-0.00204089961809834,1.0451566515784994,-0.00204089961809834],"light_intensity":875.9639230465166,"mass_factor":0.9621414414617188,"masses":[0.02886424324385156,0.02886424324385156,0.02886424324385156,0.02886424324385156,0.02886424324385156],"pegs":[[0.67461095337855,-0.31812500487130535],[0.6739558250559385,0.0028743266028908995],[0.673300696733327,0.3238736580770871]],"seed":2,"split":"train","task_id":"H31"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0011587180454351738,0.0001140922917310081],"board_yaw_deg":-1.0509231367965381,"friction":1.2107276010233252,"friction_factor":1.0089396675194378,"handle_angles":[-0.018342068922486365,-1.065539620119084,-0.018342068922486365,1.0288554822741112,-0.018342068922486365],"light_intensity":700.4774894127287,"mass_factor":1.0553238561340752,"masses":[0.031659715684022254,0.031659715684022254,0.031659715684022254,0.031659715684022254,0.031659715684022254],"pegs":[[0.6747287559437817,-0.3208319119675935],[0.6688412819545648,0.0001140922917310081],[0.662953807965348,0.32106009655105544]],"seed":3,"split":"train","task_id":"H31"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H31 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H31-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H32"></a>
## `hanoi_sharpa/fr3-sharpa/H32`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 0, 2, 2, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      0,
      2,
      2,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "a4706e9bcac125187e05c816b765d5af27677922ac5e717af9a08c93d44822cd",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.002164367800735734,-0.0037898594673082767],"board_yaw_deg":1.749707995960863,"friction":1.131508757690283,"friction_factor":0.9429239647419024,"handle_angles":[0.030538165477988703,-1.016659385718609,0.030538165477988703,1.0777357166745862,0.030538165477988703],"light_intensity":742.9363229864056,"mass_factor":0.9264666909709494,"masses":[0.02779400072912848,0.02779400072912848,0.02779400072912848,0.02779400072912848,0.02779400072912848],"pegs":[[0.6619967392222751,-0.336634597038883],[0.6721643678007357,-0.0037898594673082767],[0.6823319963791964,0.3290548781042665]],"seed":0,"split":"train","task_id":"H32"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.002220158620010717,0.0020441097614582837],"board_yaw_deg":-1.0203367467028872,"friction":1.2925236905923878,"friction_factor":1.0771030754936566,"handle_angles":[-0.017808235709052777,-1.0650057869056504,-0.017808235709052777,1.0293893154875449,-0.017808235709052777],"light_intensity":1032.3517360068108,"mass_factor":0.9478756130558117,"masses":[0.02843626839167435,0.02843626839167435,0.02843626839167435,0.02843626839167435,0.02843626839167435],"pegs":[[0.6781499876751929,-0.33090308894634923],[0.6722201586200107,0.0020441097614582837],[0.6662903295648286,0.33499130846926584]],"seed":1,"split":"train","task_id":"H32"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0018179764396622686,0.003510538467996484],"board_yaw_deg":1.5482264979750036,"friction":1.1912649158127286,"friction_factor":0.9927207631772739,"handle_angles":[0.027021649956285133,-1.0201759012403124,0.027021649956285133,1.0742192011528828,0.027021649956285133],"light_intensity":926.0152033263724,"mass_factor":0.9478611745545701,"masses":[0.028435835236637102,0.028435835236637102,0.028435835236637102,0.028435835236637102,0.028435835236637102],"pegs":[[0.6628208620006889,-0.32936789569644737],[0.6718179764396623,0.003510538467996484],[0.6808150908786358,0.33638897263244033]],"seed":2,"split":"train","task_id":"H32"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0019870597507987515,0.0037609814043462796],"board_yaw_deg":-1.4050829093500874,"friction":1.1269122360455999,"friction_factor":0.939093530038,"handle_angles":[-0.024523323031660042,-1.0717208742282576,-0.024523323031660042,1.0226742281649377,-0.024523323031660042],"light_intensity":977.5232274582552,"mass_factor":1.038106192977234,"masses":[0.03114318578931702,0.03114318578931702,0.03114318578931702,0.03114318578931702,0.03114318578931702],"pegs":[[0.6761783883202577,-0.3291388916172559],[0.6680129402492013,0.0037609814043462796],[0.659847492178145,0.33666085442594845]],"seed":3,"split":"train","task_id":"H32"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H32 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H32-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H33"></a>
## `hanoi_sharpa/fr3-sharpa/H33`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "d4830baecaa0336c6095c7f84a6e3265881811d511039a20ad44be185bda0f1c",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.001251579516491835,-0.0033028576884005186],"board_yaw_deg":1.631332491753761,"friction":1.2899825773237639,"friction_factor":1.0749854811031365,"handle_angles":[0.028472123175866376,-1.0187254280207312,0.028472123175866376,1.075669674372464,0.028472123175866376],"light_intensity":722.6491963940466,"mass_factor":1.0229359455599445,"masses":[0.030688078366798335,0.030688078366798335,0.030688078366798335,0.030688078366798335,0.030688078366798335],"pegs":[[0.6602648741000094,-0.3011820772401494],[0.6687484204835082,-0.0033028576884005186],[0.677231966867007,0.2945763618633484]],"seed":0,"split":"train","task_id":"H33"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0029113952243615252,0.0019888646501536526],"board_yaw_deg":-1.446725827057916,"friction":1.1947230273969147,"friction_factor":0.9956025228307623,"handle_angles":[-0.025250129055798702,-1.0724476802523963,-0.025250129055798702,1.021947422140799,-0.025250129055798702],"light_intensity":762.8409002103944,"mass_factor":0.9883382150338581,"masses":[0.02965014645101574,0.02965014645101574,0.02965014645101574,0.02965014645101574,0.02965014645101574],"pegs":[[0.67461234369099,-0.2959161426134599],[0.6670886047756385,0.0019888646501536526],[0.659564865860287,0.29989387191376715]],"seed":1,"split":"train","task_id":"H33"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0007217645693586565,0.001276676683484478],"board_yaw_deg":-0.9855063716330246,"friction":1.116555505675683,"friction_factor":0.9304629213964026,"handle_angles":[-0.017200330984379127,-1.0643978821809768,-0.017200330984379127,1.0299972202122185,-0.017200330984379127],"light_intensity":785.8696530996722,"mass_factor":1.0061756556683163,"masses":[0.03018526967004949,0.03018526967004949,0.03018526967004949,0.03018526967004949,0.03018526967004949],"pegs":[[0.6744036813268842,-0.29667924254680145],[0.6692782354306414,0.001276676683484478],[0.6641527895343985,0.2992325959137704]],"seed":2,"split":"train","task_id":"H33"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003984521043234189,-0.000614280221633857],"board_yaw_deg":0.9382598704476173,"friction":1.2026736244300362,"friction_factor":1.0022280203583636,"handle_angles":[0.016375723978646364,-1.0308218272179512,0.016375723978646364,1.063573275175244,0.016375723978646364],"light_intensity":982.3917343745718,"mass_factor":1.0614546748049065,"masses":[0.031843640244147195,0.031843640244147195,0.031843640244147195,0.031843640244147195,0.031843640244147195],"pegs":[[0.661135731313667,-0.29857432462849665],[0.6660154789567658,-0.000614280221633857],[0.6708952265998647,0.29734576418522896]],"seed":3,"split":"train","task_id":"H33"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H33 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H33-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H34"></a>
## `hanoi_sharpa/fr3-sharpa/H34`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 2, 1, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      2,
      1,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "433bab64895fbbc7c09830ef4851e5d3c2948c3678605db5828896aeb138ff0f",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.003988919792507499,-0.0021799540418167714],"board_yaw_deg":-1.2057380981763084,"friction":1.2902297161201999,"friction_factor":1.0751914301001666,"handle_angles":[-0.02104409972991122,-1.068241650926509,-0.02104409972991122,1.0261534514666864,-0.02104409972991122],"light_intensity":712.2987353973357,"mass_factor":0.9594900439809018,"masses":[0.02878470131942705,0.02878470131942705,0.02878470131942705,0.02878470131942705,0.02878470131942705],"pegs":[[0.68051210921367,-0.31211131418430965],[0.6739889197925075,-0.0021799540418167714],[0.667465730371345,0.30775140610067614]],"seed":0,"split":"train","task_id":"H34"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.0038648076896382003,-0.0031280853782975648],"board_yaw_deg":-1.4210364218386538,"friction":1.1385687740407213,"friction_factor":0.9488073117006012,"handle_angles":[-0.02480176435184356,-1.0719993155484413,-0.02480176435184356,1.022395786844754,-0.02480176435184356],"light_intensity":754.1844145037645,"mass_factor":1.045561791839728,"masses":[0.03136685375519184,0.03136685375519184,0.03136685375519184,0.03136685375519184,0.03136685375519184],"pegs":[[0.6815525664234896,-0.31303274550081023],[0.6738648076896382,-0.0031280853782975648],[0.6661770489557868,0.3067765747442151]],"seed":1,"split":"train","task_id":"H34"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.002620949836822554,0.0009138329339344651],"board_yaw_deg":-0.2955078809901863,"friction":1.2662237612472942,"friction_factor":1.0551864677060785,"handle_angles":[-0.005157585488870312,-1.052355136685468,-0.005157585488870312,1.0420399657077273,-0.005157585488870312],"light_intensity":836.4147364831124,"mass_factor":1.022930893973649,"masses":[0.03068792681920947,0.03068792681920947,0.03068792681920947,0.03068792681920947,0.03068792681920947],"pegs":[[0.6689778945763116,-0.30908204396855365],[0.6673790501631774,0.0009138329339344651],[0.6657802057500433,0.31090970983642263]],"seed":2,"split":"train","task_id":"H34"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[1.3436748814029009e-05,0.00089054734097861],"board_yaw_deg":1.7438761548536925,"friction":1.2476465405678545,"friction_factor":1.0397054504732122,"handle_angles":[0.030436380649215427,-1.0167611705473822,0.030436380649215427,1.077633931845813,0.030436380649215427],"light_intensity":765.9961398208666,"mass_factor":1.0574696405360942,"masses":[0.03172408921608282,0.03172408921608282,0.03172408921608282,0.03172408921608282,0.03172408921608282],"pegs":[[0.6605796154449679,-0.30896587588695307],[0.6700134367488141,0.00089054734097861],[0.6794472580526603,0.31074697056891026]],"seed":3,"split":"train","task_id":"H34"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H34 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H34-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H35"></a>
## `hanoi_sharpa/fr3-sharpa/H35`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [2, 1, 1, 2, 1], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      2,
      1,
      1,
      2,
      1
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "82da62597d6e0231dfe4f965a7ce0a272bbb5fd20a3cf1a0946cf779717f1331",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.003103673984794563,-0.0028280476749412923],"board_yaw_deg":-0.35044583764855375,"friction":1.190123308101644,"friction_factor":0.9917694234180366,"handle_angles":[-0.0061164337168767655,-1.0533139849134745,-0.0061164337168767655,1.0410811174797208,-0.0061164337168767655],"light_intensity":1012.042627043837,"mass_factor":1.0211666844175844,"masses":[0.03063500053252753,0.03063500053252753,0.03063500053252753,0.03063500053252753,0.03063500053252753],"pegs":[[0.6688658053920323,-0.32482202456113124],[0.6668963260152054,-0.0028280476749412923],[0.6649268466383785,0.3191659292112487]],"seed":0,"split":"train","task_id":"H35"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-1.5063044351296019e-05,0.002786688161416996],"board_yaw_deg":-0.9665585162982395,"friction":1.1251010861437654,"friction_factor":0.9375842384531378,"handle_angles":[-0.016869628522595555,-1.0640671797191932,-0.016869628522595555,1.030327922674002,-0.016869628522595555],"light_intensity":728.615993351607,"mass_factor":1.0283600558810466,"masses":[0.030850801676431398,0.030850801676431398,0.030850801676431398,0.030850801676431398,0.030850801676431398],"pegs":[[0.6754166996989106,-0.3191674948421603],[0.6699849369556488,0.002786688161416996],[0.6645531742123869,0.3247408711649942]],"seed":1,"split":"train","task_id":"H35"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0005534561437829364,0.0022551064207354415],"board_yaw_deg":1.1136808841982893,"friction":1.1401149408362539,"friction_factor":0.9500957840302117,"handle_angles":[0.019437398245781837,-1.0277601529508158,0.019437398245781837,1.0666349494423795,0.019437398245781837],"light_intensity":935.1141159285987,"mass_factor":1.0888652830284573,"masses":[0.03266595849085372,0.03266595849085372,0.03266595849085372,0.03266595849085372,0.03266595849085372],"pegs":[[0.6631880957250509,-0.3196840676898246],[0.6694465438562172,0.0022551064207354415],[0.6757049919873834,0.3241942805312955]],"seed":2,"split":"train","task_id":"H35"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0034300255197032333,-0.0016357834622987486],"board_yaw_deg":1.8693047040828992,"friction":1.263147573127055,"friction_factor":1.052622977605879,"handle_angles":[0.03262552180926488,-1.0145720293873328,0.03262552180926488,1.0798230730058624,0.03262552180926488],"light_intensity":893.1672305904702,"mass_factor":0.916418677090817,"masses":[0.02749256031272451,0.02749256031272451,0.02749256031272451,0.02749256031272451,0.02749256031272451],"pegs":[[0.6560664200628852,-0.3234644262904356],[0.6665699744802968,-0.0016357834622987486],[0.6770735288977083,0.3201928593658381]],"seed":3,"split":"train","task_id":"H35"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H35 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H35-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H36"></a>
## `hanoi_sharpa/fr3-sharpa/H36`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 1, 1, 0, 0], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      1,
      1,
      0,
      0
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "ffb55be1d1e86dfc1167e99c3c13d4bd32314c6100719e146a362a8ed5c81678",
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
| 1 | 0 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0017312456538532129,0.002635598543487983],"board_yaw_deg":-1.4430845233336056,"friction":1.1393579957699875,"friction_factor":0.9494649964749897,"handle_angles":[-0.025186576316744355,-1.072384127513342,-0.025186576316744355,1.0220109748798534,-0.025186576316744355],"light_intensity":859.0138895942432,"mass_factor":1.0037964800105035,"masses":[0.030113894400315103,0.030113894400315103,0.030113894400315103,0.030113894400315103,0.030113894400315103],"pegs":[[0.6766801814528836,-0.33125846833106437],[0.6682687543461469,0.002635598543487983],[0.6598573272394102,0.33652966541804036]],"seed":0,"split":"train","task_id":"H36"}` |
| 2 | 1 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0035580841094921558,0.001814994618351081],"board_yaw_deg":0.0357104218890929,"friction":1.1206351650157231,"friction_factor":0.9338626375131026,"handle_angles":[0.0006232644392409244,-1.0465742867573566,0.0006232644392409244,1.0478208156358386,0.0006232644392409244],"light_intensity":1072.1092369542755,"mass_factor":0.9948093832824776,"masses":[0.029844281498474328,0.029844281498474328,0.029844281498474328,0.029844281498474328,0.029844281498474328],"pegs":[[0.6662337455812789,-0.3321849405090712],[0.6664419158905078,0.001814994618351081],[0.6666500861997368,0.3358149297457734]],"seed":1,"split":"train","task_id":"H36"}` |
| 3 | 2 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[-0.0039409603120656375,-0.0016805001334679753],"board_yaw_deg":-1.0069618439081698,"friction":1.1268485853153727,"friction_factor":0.9390404877628106,"handle_angles":[-0.01757479961815077,-1.0647723508147484,-0.01757479961815077,1.0296227515784468,-0.01757479961815077],"light_intensity":731.0628496822476,"mass_factor":0.9440353416633583,"masses":[0.028321060249900748,0.028321060249900748,0.028321060249900748,0.028321060249900748,0.028321060249900748],"pegs":[[0.6719287205846143,-0.3356289195730143],[0.6660590396879345,-0.0016805001334679753],[0.6601893587912546,0.3322679193060783]],"seed":2,"split":"train","task_id":"H36"}` |
| 4 | 3 | train | `{"bases":[0.0,0.0,0.0],"board_shift":[0.002344177876047824,-0.0017905210018850197],"board_yaw_deg":0.38315371288530664,"friction":1.2375081809718684,"friction_factor":1.031256817476557,"handle_angles":[0.006687293831089624,-1.040510257365508,0.006687293831089624,1.0538848450276872,0.006687293831089624],"light_intensity":796.7107587143131,"mass_factor":0.9676825014833501,"masses":[0.0290304750445005,0.0290304750445005,0.0290304750445005,0.0290304750445005,0.0290304750445005],"pegs":[[0.6701106383838275,-0.33578305280661963],[0.6723441778760478,-0.0017905210018850197],[0.6745777173682682,0.33220201080284956]],"seed":3,"split":"train","task_id":"H36"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H36 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H36-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H37"></a>
## `hanoi_sharpa/fr3-sharpa/H37`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 0, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      0,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "45a6bc8f699a3e8b18350f33029dd0e94a7f0b29145230e86f909abf39294f6b",
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
| 1 | 0 | train | `{"bases":[0.0,0.02,0.01],"board_shift":[0.0027292906591291043,0.0024811219337152576],"board_yaw_deg":-1.02635103509187,"friction":1.2878405560419954,"friction_factor":1.0732004633683296,"handle_angles":[0.3311526455552609,-0.45424551784218736,0.5929520333544103,-0.3669790552424709,0.4184191081549774],"light_intensity":1050.0453369555519,"mass_factor":0.9450178181220349,"masses":[0.028350534543661047,0.028350534543661047,0.028350534543661047,0.028350534543661047,0.028350534543661047],"pegs":[[0.6180946786977279,-0.2975456421654683],[0.8027084338278498,0.004809714024488128],[0.6073831550801727,0.30035841641064687]],"seed":0,"split":"train","task_id":"H37"}` |
| 2 | 1 | train | `{"bases":[0.0,0.02,0.01],"board_shift":[-0.0020926937005443917,0.0018804524835139586],"board_yaw_deg":0.5004458043221804,"friction":1.2004365882787111,"friction_factor":1.0003638235655927,"handle_angles":[0.3578002774120792,-0.4275978859853691,0.6195996652112287,-0.3403314233856526,0.4450667400117957],"light_intensity":747.0609308603803,"mass_factor":1.051171217858799,"masses":[0.03153513653576397,0.03153513653576397,0.03153513653576397,0.03153513653576397,0.03153513653576397],"pegs":[[0.6052980345207924,-0.29658408324451097],[0.7979023474669904,0.0007449914093530213],[0.6105211554619328,0.30139310612614906]],"seed":1,"split":"train","task_id":"H37"}` |
| 3 | 2 | train | `{"bases":[0.0,0.02,0.01],"board_shift":[-0.0010596179982345836,-0.0038261437492739634],"board_yaw_deg":-1.175372414645173,"friction":1.1774862864978322,"friction_factor":0.9812385720815269,"handle_angles":[0.32855173182619163,-0.45684643157125665,0.590351119625341,-0.36957996897154016,0.4158181944259081],"light_intensity":804.6222129839562,"mass_factor":0.9834551801373846,"masses":[0.02950365540412154,0.02950365540412154,0.02950365540412154,0.02950365540412154,0.02950365540412154],"pegs":[[0.6150862976850953,-0.30399399279779044],[0.7989130290720751,-0.0011594953778644064],[0.6028197151766114,0.2938801837256337]],"seed":2,"split":"train","task_id":"H37"}` |
| 4 | 3 | train | `{"bases":[0.0,0.02,0.01],"board_shift":[-0.0022073513707059345,0.0010479783044606528],"board_yaw_deg":-0.450166917505362,"friction":1.2917978403317152,"friction_factor":1.0764982002764294,"handle_angles":[0.34120895550484365,-0.44418920789260463,0.603008343303993,-0.35692274529288814,0.42847541810456014],"light_intensity":729.6056862616443,"mass_factor":1.0375825216813679,"masses":[0.031127475650441036,0.031127475650441036,0.031127475650441036,0.031127475650441036,0.031127475650441036],"pegs":[[0.610143687947292,-0.29841420183233885],[0.7977886361481059,0.0020693641321142707],[0.6054453131400853,0.2995673407541953]],"seed":3,"split":"train","task_id":"H37"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H37 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H37-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H38"></a>
## `hanoi_sharpa/fr3-sharpa/H38`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [0, 0, 2, 1, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      0,
      0,
      2,
      1,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      1,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "e4e0f9ce481b142b813a8232fdac61730404f52f6d2b2ed6078553b03730bdf0",
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
| 1 | 0 | train | `{"bases":[0.0,0.03,0.01],"board_shift":[-0.0023364365647019617,0.0014431894528912261],"board_yaw_deg":1.6311049344899158,"friction":1.131645609250573,"friction_factor":0.9430380077088109,"handle_angles":[0.3775340019512413,-0.40786416144620696,0.6393333897503908,-0.3205976988464905,0.4648004645509578],"light_intensity":923.3959100181726,"mass_factor":1.0403090708066638,"masses":[0.040572053761459885,0.040572053761459885,0.040572053761459885,0.040572053761459885,0.040572053761459885],"pegs":[[0.5988354755598567,-0.3077229379275359],[0.7976108886754683,-0.0022571703843986815],[0.6165402741659669,0.3140250336062014]],"seed":0,"split":"train","task_id":"H38"}` |
| 2 | 1 | train | `{"bases":[0.0,0.03,0.01],"board_shift":[0.0017513265746389322,-0.0025308663415493744],"board_yaw_deg":-1.0729266027743931,"friction":1.2447535464079271,"friction_factor":1.037294622006606,"handle_angles":[0.3303397485482154,-0.4550584148492329,0.5921391363473648,-0.3677919522495164,0.4176062111479319],"light_intensity":739.6051759040671,"mass_factor":0.9859547871239193,"masses":[0.03845223669783285,0.03845223669783285,0.03845223669783285,0.03845223669783285,0.03845223669783285],"pegs":[[0.6175853235854543,-0.31459983967945687],[0.8017285338928201,-9.661537532157285e-05],[0.6059383689624258,0.3072911061044556]],"seed":1,"split":"train","task_id":"H38"}` |
| 3 | 2 | train | `{"bases":[0.0,0.03,0.01],"board_shift":[-0.002276205509383447,-0.0010284816840292158],"board_yaw_deg":-0.023745494914005905,"friction":1.120921722390516,"friction_factor":0.93410143532543,"handle_angles":[0.3486514133301009,-0.43674675006734737,0.6104508011292503,-0.3494802874676309,0.4359178759298174],"light_intensity":730.2698265147745,"mass_factor":1.0037041067783565,"masses":[0.0391444601643559,0.0391444601643559,0.0391444601643559,0.0391444601643559,0.0391444601643559],"pegs":[[0.6078526895680553,-0.3120533211990616],[0.7977237833263413,-0.0009746048666320661],[0.6075949097186628,0.30994662538417506]],"seed":2,"split":"train","task_id":"H38"}` |
| 4 | 3 | train | `{"bases":[0.0,0.03,0.01],"board_shift":[-0.0008766517731784949,0.002735858322463587],"board_yaw_deg":-1.057315890166039,"friction":1.243247936264784,"friction_factor":1.03603994688732,"handle_angles":[0.33061220688181375,-0.4547859565156345,0.5924115946809632,-0.36751949391591804,0.41787866948153024],"light_intensity":936.5434671477378,"mass_factor":0.9039385362172768,"masses":[0.03525360291247379,0.03525360291247379,0.03525360291247379,0.03525360291247379,0.03525360291247379],"pegs":[[0.6148723214567124,-0.3093183454537216],[0.7991012139526219,0.005134695825466313],[0.6033948066346533,0.3125757505574155]],"seed":3,"split":"train","task_id":"H38"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H38 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H38-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H39"></a>
## `hanoi_sharpa/fr3-sharpa/H39`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [2, 1, 1, 2, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      2,
      1,
      1,
      2,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      1,
      2,
      0,
      1
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "e18a76755a5afde1bbfbec83ea10b6639b427cba12815527a7aed581b80f6369",
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
| 1 | 0 | train | `{"bases":[0.0,0.04,0.01],"board_shift":[-0.0033502553915986813,-0.0004605504167594696],"board_yaw_deg":-1.4906878703635018,"friction":1.2318335866554506,"friction_factor":1.0265279888795422,"handle_angles":[0.3230484389414804,-0.4623497244559679,0.5848478267406299,-0.3750832618562514,0.4103149015411969],"light_intensity":902.3885055801513,"mass_factor":1.072942258502501,"masses":[0.05150122840812005,0.05150122840812005,0.05150122840812005,0.05150122840812005,0.05150122840812005],"pegs":[[0.6150727264898967,-0.32491210489293],[0.7966057482198379,0.0029213315067098617],[0.5982673747778876,0.3208692668992855]],"seed":0,"split":"train","task_id":"H39"}` |
| 2 | 1 | train | `{"bases":[0.0,0.04,0.01],"board_shift":[0.00046545418292111496,0.0012768567639124023],"board_yaw_deg":0.2281081473258848,"friction":1.1679766895953867,"friction_factor":0.9733139079961557,"handle_angles":[0.3530470886203269,-0.43235107477712137,0.6148464764194763,-0.3450846121774049,0.4403135512200434],"light_intensity":938.9956415697869,"mass_factor":0.9412106342414428,"masses":[0.045178110443589256,0.045178110443589256,0.045178110443589256,0.045178110443589256,0.045178110443589256],"pegs":[[0.6091799931415717,-0.32148170976058627],[0.8004644239175266,0.0007592971623671854],[0.611751866238481,0.32451317061291435]],"seed":1,"split":"train","task_id":"H39"}` |
| 3 | 2 | train | `{"bases":[0.0,0.04,0.01],"board_shift":[0.0015846316947718151,-0.0005524489748878949],"board_yaw_deg":1.1356116989116087,"friction":1.2547231084206718,"friction_factor":1.04560259035056,"handle_angles":[0.36888601356904,-0.4165121498284083,0.6306854013681894,-0.3292456872286918,0.4561524761687565],"light_intensity":921.7757654494761,"mass_factor":1.0282505558261494,"masses":[0.04935602667965518,0.04935602667965518,0.04935602667965518,0.04935602667965518,0.04935602667965518],"pegs":[[0.6051949229161714,-0.32229987564415064],[0.8015590980042478,-0.003128901490830668],[0.6179979100338562,0.32357324155524514]],"seed":2,"split":"train","task_id":"H39"}` |
| 4 | 3 | train | `{"bases":[0.0,0.04,0.01],"board_shift":[0.0022058947804945083,0.0016230729847055239],"board_yaw_deg":1.5283587136973942,"friction":1.278381126816459,"friction_factor":1.0653176056803826,"handle_angles":[0.37574074210443076,-0.4096574212930175,0.6375401299035802,-0.32239095869330103,0.46300720470414725],"light_intensity":928.4627905656214,"mass_factor":1.021281601008264,"masses":[0.049021516848396667,0.049021516848396667,0.049021516848396667,0.049021516848396667,0.049021516848396667],"pegs":[[0.6036122717373399,-0.31966171482482275],[0.8021596467828174,-0.0018442517071543306],[0.6208422082830435,0.3261084682021045]],"seed":3,"split":"train","task_id":"H39"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H39 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H39-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

<a id="hanoi_sharpa-fr3-sharpa-H40"></a>
## `hanoi_sharpa/fr3-sharpa/H40`

Authoring provenance: `env/sharpa_hanoi40/README.md`. Action size: 29; 18000 controls / 600 s; wall: 3600 s.

Goal (source data):
```json
{"ring_pegs": [1, 1, 1, 0, 2], "stable_seconds": 1}
```

Native action and scoring contract:
```json
{
  "action_spec": {
    "control_period_s": 0.03333333333333333,
    "high": [
      4.234599590301514,
      5.085599899291992,
      5.794599533081055,
      4.560400009155273,
      5.794599533081055,
      4.364999771118164,
      4.234599590301514,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      2.6179996132850647,
      15.707999467849731,
      3.4909996390342712,
      17.452999353408813,
      13.962998390197754,
      19.19899821281433,
      3.4909996390342712,
      13.962998390197754,
      3.4909996390342712,
      17.452999353408813
    ],
    "low": [
      -7.354599475860596,
      -1.965599775314331,
      -5.794599533081055,
      -1.4435997009277344,
      -5.794599533081055,
      -3.1750001907348633,
      -7.354599475860596,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      0.0,
      -1.745329201221466,
      -3.4909996390342712,
      0.0,
      0.0,
      -1.745000034570694,
      -3.4909996390342712,
      -5.235999226570129,
      -3.4909996390342712,
      0.0
    ],
    "names": [
      "arm_action.panda_joint1",
      "arm_action.panda_joint2",
      "arm_action.panda_joint3",
      "arm_action.panda_joint4",
      "arm_action.panda_joint5",
      "arm_action.panda_joint6",
      "arm_action.panda_joint7",
      "hand_action.right_index_MCP_FE",
      "hand_action.right_index_MCP_AA",
      "hand_action.right_index_PIP",
      "hand_action.right_index_DIP",
      "hand_action.right_middle_MCP_FE",
      "hand_action.right_middle_MCP_AA",
      "hand_action.right_middle_PIP",
      "hand_action.right_middle_DIP",
      "hand_action.right_ring_MCP_FE",
      "hand_action.right_ring_MCP_AA",
      "hand_action.right_ring_PIP",
      "hand_action.right_ring_DIP",
      "hand_action.right_pinky_CMC",
      "hand_action.right_pinky_MCP_FE",
      "hand_action.right_pinky_MCP_AA",
      "hand_action.right_pinky_PIP",
      "hand_action.right_pinky_DIP",
      "hand_action.right_thumb_CMC_FE",
      "hand_action.right_thumb_CMC_AA",
      "hand_action.right_thumb_MCP_FE",
      "hand_action.right_thumb_MCP_AA",
      "hand_action.right_thumb_IP"
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
      0.0
    ],
    "physics_period_s": 0.008333333333333333,
    "semantics": [
      "arm_action: joint target = offset + scale * action; offset=[0.7799999713897705, -0.7799999713897705, 0.0, -2.3499999046325684, 0.0, 1.5700000524520874, 0.7799999713897705]; scale=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]",
      "hand_action: joint target = offset + scale * action; offset=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; scale=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]"
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
      "pieces",
      "robot_bodies",
      "jacobians",
      "contacts",
      "geometry",
      "physics",
      "diagnostics"
    ],
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
    "first_violation_sticky": true,
    "goal_ring_pegs": [
      1,
      1,
      1,
      0,
      2
    ],
    "gripper_closed_half_width_m": null,
    "initial_ring_pegs": [
      0,
      0,
      0,
      0,
      0
    ],
    "penetration_limit_m": 0.005,
    "rules": [
      "top_ring_only",
      "smaller_on_larger",
      "finite_state",
      "workspace_bounds"
    ],
    "seat_xy_tolerance_m": 0.022,
    "seat_z_tolerance_m": 0.016,
    "stable_seconds": 1.0
  },
  "sha256": "84ffa2d45cbef07a1f2e5a70e0cf33ea5e36377b68e0e2931083f703d282b03f",
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
| 1 | 0 | train | `{"bases":[0.0,0.05,0.01],"board_shift":[-0.0009557305372919247,0.001103199672450466],"board_yaw_deg":-0.5433958364150033,"friction":1.1400298375814204,"friction_factor":0.9500248646511836,"handle_angles":[0.3395818039117956,-0.4458163594856527,0.601381191710945,-0.3585498968859362,0.4268482665115121],"light_intensity":738.5774658335978,"mass_factor":0.9423123459660914,"masses":[0.0537118037200672,0.0537118037200672,0.0537118037200672,0.0537118037200672,0.0537118037200672],"pegs":[[0.6122240758006561,-0.33445076855353684],[0.7990384229425765,0.0023361072328246177],[0.6058698599125739,0.3355190993811693]],"seed":0,"split":"train","task_id":"H40"}` |
| 2 | 1 | train | `{"bases":[0.0,0.05,0.01],"board_shift":[-0.002210774632221709,0.00042804158157005735],"board_yaw_deg":0.5584772400288776,"friction":1.2092291581315626,"friction_factor":1.0076909651096355,"handle_angles":[0.3588131170348205,-0.4265850463626278,0.6206125048339699,-0.3393185837629113,0.446079579634537],"light_intensity":929.5397864473515,"mass_factor":1.0187148566321917,"masses":[0.05806674682803493,0.05806674682803493,0.05806674682803493,0.05806674682803493,0.05806674682803493],"pegs":[[0.6045267930042646,-0.3339712177648762],[0.7977830498182263,-0.0008390830161311247],[0.6110573582385707,0.33599695440281746]],"seed":1,"split":"train","task_id":"H40"}` |
| 3 | 2 | train | `{"bases":[0.0,0.05,0.01],"board_shift":[0.0037113916504528644,-0.003712687774851815],"board_yaw_deg":0.8780787418859313,"friction":1.2609336515570033,"friction_factor":1.0507780429641695,"handle_angles":[0.36439121553654485,-0.4210069478609034,0.6261906033356942,-0.33374048526118694,0.45165767813626134],"light_intensity":945.7162338715873,"mass_factor":0.9474391676901962,"masses":[0.05400403255834118,0.05400403255834118,0.05400403255834118,0.05400403255834118,0.05400403255834118],"pegs":[[0.6085846411611647,-0.337753862438554],[0.8036961256061678,-0.005704907256238571],[0.6188522338729273,0.3321674587178227]],"seed":2,"split":"train","task_id":"H40"}` |
| 4 | 3 | train | `{"bases":[0.0,0.05,0.01],"board_shift":[-0.0023643929894112737,0.0007468503681086109],"board_yaw_deg":0.7979557660731333,"friction":1.290757753111778,"friction_factor":1.0756314609264817,"handle_angles":[0.36299280580211574,-0.42240535759533254,0.6247921936012651,-0.33513889499561605,0.4502592684018322],"light_intensity":1059.928711408897,"mass_factor":1.0397895632758805,"masses":[0.05926800510672518,0.05926800510672518,0.05926800510672518,0.05926800510672518,0.05926800510672518],"pegs":[[0.6029760464786934,-0.3333850715307458],[0.797622999808723,-0.0010635953072894232],[0.612306804959591,0.33654995289040734]],"seed":3,"split":"train","task_id":"H40"}` |

```bash
python scripts/environment_runtime.py --task-id hanoi_sharpa/fr3-sharpa/H40 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi_sharpa-fr3-sharpa-H40-default-trial1
```

Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.

