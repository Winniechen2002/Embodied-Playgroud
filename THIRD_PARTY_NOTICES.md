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
| Piper files | [Local MIT notice](source/agentbench/agentbench/robot_urdfs/agilex_piper/LICENSE) | Original MIT notice retained under the maintainer distribution decision / 按维护者分发决定保留原 MIT 通知 |

ManiSkill's embedded archive contains 444 integrity-checked files. The archive
and its embedded notices are preserved. The maintainer has approved distribution
of the complete included bundle under its original applicable licenses. YCB,
Google Scanned Objects, RoboCasa/Lightwheel and converted robot components retain
their individual license scopes, recorded in
[the license decision inventory](env/runtime/license-decisions.json).

ManiSkill 内嵌归档的 444 个文件及其中的通知保持不变。维护者已确认完整随附资产包
可按原有适用许可证分发；各数据集与机器人组件的许可范围见上述清单。

The [embedded source inventory](third_party/README.md) lists 17 upstream snapshots
and 16 nested dependencies, with original license paths and revisions in
[manifest.json](third_party/manifest.json). GenDexGrasp, DexGraspNet2 and STREAM3D
have no repository-level license file at these revisions; inclusion supplies no
additional license grant. Original upstream code, examples, data and notices
retain their own terms. Isaac Sim is obtained separately under NVIDIA terms.

[内嵌清单](third_party/README.md)记录 17 个上游源码及 16 个嵌套依赖的版本与原始许可路径。
GenDexGrasp、DexGraspNet2 与 STREAM3D 在这些修订中没有仓库级许可文件；内嵌不授予额外权利。
上游代码、示例、数据和通知保留原条款。Isaac Sim 依 NVIDIA 条款单独获取。
