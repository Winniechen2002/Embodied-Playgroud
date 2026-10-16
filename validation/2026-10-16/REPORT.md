# 2026-10-16 验收记录

**完整发布验收结论：未通过（NOT_QUALIFIED）。** 本次修改通过源码回归和已执行的原生检查，但这些结果不能替代全部发布条件。未创建正式 release 或发布标签。

本记录检验代码提交 `216d3ad`，原始结果与文件校验值见 [summary.json](summary.json)。报告目录不属于独立环境包的源码清单。下列“通过”仅针对各行所述范围。

| 检查 | 结果与范围 |
| --- | --- |
| 源码测试 | 269 项通过，0 失败；见 [JUnit](reports/tests-final.xml) |
| 评分端点夹具 | MuJoCo 100、Isaac 280、ManiSkill 30；共 410 项，检查初始/目标等人工状态，不等于原生完成任务 |
| 原生安装检查 | MuJoCo 100、Isaac 280、ManiSkill 30 项通过，共 410 项；Isaac 10 类渲染检查通过 |
| 默认条件物理检查 | MuJoCo 100 项、ManiSkill 30 项均为 `passed_probe`；没有执行 Isaac 完整物理条件矩阵 |
| 文档 | 1,440 个本地 Markdown 链接目标有效；权限文档和双语评测协议生成一致；未把远程 URL/页内锚点检查算入此结果 |
| 公共内容 | 742 个文件，静态内容审计无问题；资产分发状态为维护者声明可分发，原有第三方许可保留 |
| 独立导出包 | staging 构建及 410 项目录加载通过，MuJoCo A001 的原生渲染/网关/退出冒烟通过；没有完成导出包的 Isaac、ManiSkill 验证 |

## 未达到的发布条件

1. 工程验收 union 矩阵有 **9,390 个条件**，本次未执行完整矩阵。默认条件检查、安装步进和评分端点夹具均不能代替它。
2. 当前三个原生物理验证器输出 `passed_probe`，缺少发布门禁要求的 `necessary_geometry` 与完整原生 `scorer` 测量。静态覆盖检查见 [validator-coverage.json](reports/validator-coverage.json)。不能将状态直接改成 `passed` 来绕过门禁。
3. 没有完整且绑定最终源码的全局 `local_contact` 验收证据。ManiSkill 动态条件还要求触发、接触、终态审计。
4. 本次使用现有、隔离且版本受校验的原生运行时，未从空环境重新安装所有模拟器；独立分发包只完成 MuJoCo 冒烟。
5. 导出器修复之前取得的报告保留原始源码指纹；它们对最终版本的严格门禁属于过期证据，没有重写指纹或伪造通过状态。

[严格门禁结果](reports/gate-summary.json) 为 0/9,390 个条件具备完整合格证据，输入格式无错误。这表示证据不足，不表示已实测 9,390 个条件全部失败。

因此 `release_ready`、`environment_qualified` 均保持 `false`。代码可以同步到开发仓库；本记录不宣告完整环境包已经通过发布验收。

## 复现与证据解释

源码测试、最终 MuJoCo/ManiSkill 安装检查、最终评分端点检查和并发 ManiSkill 默认条件检查基于 `216d3ad`。Isaac 安装检查、MuJoCo 默认条件物理检查和 ManiSkill L1 在 `22f994a` 启动；其后唯一代码修复是导出器对已经清理过的场景保留原始字节，并补充导出回归测试。原始报告中记录的源码指纹优先于本段概述。

ManiSkill 最初串行运行在 L1 完成后被主动中断，以便将余下 29 项按任务分成独立进程并发执行。原始中断报告与后续逐任务报告一并保留，汇总只计已记录的条件，没有将中断的整次运行记为通过。

原生运行硬件为 NVIDIA RTX 4090，驱动 580.173.02。解释器及包版本记录于原始安装/物理报告中。运行方式按项目文档分开使用 MuJoCo、Isaac、ManiSkill 解释器，不在同一 Python 环境混装三个后端。以下变量应指向按仓库安装文档配置好的各自运行时；`OUT` 为可写输出目录。

```bash
"$MUJOCO_PYTHON" -m pytest -q tests
"$MUJOCO_PYTHON" scripts/check_tool_policy_docs.py
"$MUJOCO_PYTHON" scripts/export_evaluation_protocol.py --check
"$MUJOCO_PYTHON" scripts/environment_release.py audit --output "$OUT/audit.json"
"$MUJOCO_PYTHON" scripts/validate_environment_contracts.py --backend mujoco --output "$OUT/contracts-mujoco.json"
"$MUJOCO_PYTHON" scripts/validate_source_installation.py --backend mujoco --output "$OUT/install-mujoco.json"
"$MUJOCO_PYTHON" scripts/validate_environment_physics.py --workers 4 --output "$OUT/physics-mujoco.json"
```

Isaac 使用仓库启动器，并设置 `ISAACSIM_PATH`、`ISAACLAB_PATH`、`AGENTBENCH_ISAAC_PYTHON`：

```bash
bash scripts/run_isaac_binary.sh scripts/validate_environment_contracts.py --backend isaac --output "$OUT/contracts-isaac.json"
bash scripts/run_isaac_binary.sh scripts/validate_isaac_installation.py --isaac-root "$ISAACSIM_PATH" --isaac-lab-root "$ISAACLAB_PATH" --jobs 2 --output "$OUT/install-isaac.json"
```

ManiSkill 设置 `AGENTBENCH_MANISKILL_ASSETS` 并使当前仓库的 `env/maniskill_lgd`、`source/agentbench`、`source/agentbench_platform`、`source/agentbench_sdk` 位于该解释器的模块路径中：

```bash
"$MANISKILL_PYTHON" scripts/validate_environment_contracts.py --backend maniskill --output "$OUT/contracts-maniskill.json"
"$MANISKILL_PYTHON" scripts/validate_source_installation.py --backend maniskill --output "$OUT/install-maniskill.json"
"$MANISKILL_PYTHON" scripts/validate_maniskill_environments.py --default-configurations --output "$OUT/physics-maniskill.json"
```

最后一条可串行执行全部 30 项；本次并发运行实际使用的逐任务命令见 [execution.json](reports/maniskill-tasks/execution.json)。每个报告只覆盖其指定任务。

## 本次额外修复

- 修正 Isaac 依赖归属检查：先解析虚拟环境根目录的符号链接，避免误拒绝正常安装的依赖。
- 修正导出器：已清理过的场景定义保留原始字节，避免 `ast.unparse` 跨 Python 版本格式差异破坏源码指纹。导出回归和实际包内目录/冒烟验证通过。

此前要求的 ManiSkill 保存夹具哈希删除、正常 LFS 内容忽略、资产分发声明与原许可保留、按后端拆分验证命令、任务来源路径修正，均已包含在本次检查的源码中。
