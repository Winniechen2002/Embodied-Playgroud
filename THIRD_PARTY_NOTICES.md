# Third-party notices / 第三方通知

This is a navigation index, not a replacement for upstream license terms or a
grant for assets whose provenance is unresolved. The project licenses in
[LICENSING.md](LICENSING.md) do not relicense these components.

本文件为通知索引，不替代上游条款，也不授予来源未明确资产的权利。
第三方内容不因项目采用 Apache-2.0／CC BY 4.0 而变更许可。

| Component / 组件 | Retained evidence / 保留的依据 | Scope / 范围 |
| --- | --- | --- |
| Isaac Lab inherited source | [BSD-3-Clause notice](LICENSES/IsaacLab-BSD-3-Clause.txt) | Existing file headers remain; includes inherited setup/configuration code / 保留继承代码文件头 |
| Panda MuJoCo assets | [License](source/agentbench/agentbench_mujoco/assets/panda/LICENSE), [provenance](source/agentbench/agentbench_mujoco/assets/panda/UPSTREAM.json) | Only the identified upstream files / 仅已识别的上游文件 |
| Sharpa FR3 hand component | [License](source/agentbench/agentbench/robot_usds/Sharpa_hand/FR3_Sharpa_right/official_wave_01/LICENSE.txt), [notice](source/agentbench/agentbench/robot_usds/Sharpa_hand/FR3_Sharpa_right/official_wave_01/NOTICE.txt), [provenance](source/agentbench/agentbench/robot_usds/Sharpa_hand/FR3_Sharpa_right/official_wave_01/UPSTREAM.json) | 11 files; does not cover every component of the assembled robot / 11 个文件，不覆盖组合机器人的全部组件 |
| Floating Sharpa hand component | [License](source/agentbench/agentbench/robot_usds/Sharpa_hand/Floating_Sharpa_right/official_wave_01/LICENSE.txt), [notice](source/agentbench/agentbench/robot_usds/Sharpa_hand/Floating_Sharpa_right/official_wave_01/NOTICE.txt), [provenance](source/agentbench/agentbench/robot_usds/Sharpa_hand/Floating_Sharpa_right/official_wave_01/UPSTREAM.json) | 11 pinned upstream files / 11 个固定版本上游文件 |
| Piper files | [Local MIT notice](source/agentbench/agentbench/robot_urdfs/agilex_piper/LICENSE) | Existing local notice; full asset provenance remains subject to review / 保留本地通知，完整资产来源仍需核对 |

ManiSkill's embedded archive contains 444 integrity-checked files. The archive
and its embedded notices are preserved. File integrity does not resolve dataset
or robot-asset grants. YCB, Google Scanned Objects, RoboCasa/Lightwheel and
converted robot components remain separately recorded in
[the license decision inventory](env/runtime/license-decisions.json).

ManiSkill 内嵌归档的 444 个文件及其中的通知保持不变。完整性校验不代表数据集或机器人
资产授权已明确；相关待核对项见上述许可清单。

Optional third-party submodules retain their own licenses and notices and are not
included in the environment public-content allowlist. Isaac Sim is obtained
separately under NVIDIA terms; the project license does not cover the simulator.
可选第三方子模块保留原许可，不进入环境公开内容白名单；Isaac Sim 依 NVIDIA 条款单独获取。
