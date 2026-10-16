# 环境验证

[English](environment_validation.en.md) · [文档](README.zh-CN.md)

验证检查环境实现、资产加载、原生动作与观测、评分、权限及回合生命周期，不代表 agent 表现，也不证明每个种子均可求解。完整工程验收尚未完成。

## 本地检查

按[安装指南](environment_installation.zh-CN.md)使用对应模拟器的独立环境。先运行仅依赖 CPU 的契约检查，再执行原生检查：

```bash
python scripts/environment_release.py catalog --output /tmp/agentbench-catalog.json
python scripts/validate_environment_contracts.py --output /tmp/agentbench-contracts.json
python scripts/environment_release.py matrix --matrix union --output /tmp/agentbench-conditions.json
python scripts/environment_smoke.py --task-id marble/dual-panda/A001 --output /tmp/agentbench-smoke.json
```

目录包含 410 个任务。烟雾检查覆盖实际观测、时间推进、重复请求 ID、结束行为与进程退出。短探针不等于完整时长或全条件通过。Isaac 原生检查需要配置好的 GPU 运行时；ManiSkill 检查需要其独立依赖与资产。

## 工程条件矩阵

矩阵版本为 `environment-conditions-v3`：

| 选择 | 唯一条件 | 成员关系数 |
| --- | ---: | ---: |
| legacy | 4,970 | 4,970 |
| protocol，基准种子 0/1/2 | 5,160 | 6,120 |
| union | 9,390 | 11,090 |

成员关系数保留组间重叠。这些工程数量与论文评测分母不同。基准种子为 0 的通用安排包含 loaded 与 ground，共 510 组、2,040 个条件；论文 loaded-only 设置为 410 组、1,640 个条件，EP-100 为 400 个条件。详见[EP 定义](ep_subsets/README.zh-CN.md)。

矩阵工具包括 `validate_environment_physics.py`、`validate_isaac_environments.py` 和 `validate_maniskill_environments.py`。在对应模拟器运行时中查看各工具的 `--help`。恢复检查时保留相同的条件选择、源码身份与预算；源码变化后需要新证据。

## 验收与局限

必需检查覆盖契约、必要几何条件、物理、原生动作与观测、评分、四个权限等级、生命周期与重复初始化。静态场景至少稳定 2 秒并保持 3 秒，指定支撑场景仍需完整时长检查；动态检查覆盖触发、接触、有限状态与终止。符合预期的不操作任务失败，本身不等于环境缺陷。

记录绑定实际初始化、源码／目录／资产／评分器版本、物理步数、测量值与失败原因。未知条件、重复记录、过期源码、跳过项、缺失测量或时长不足均不能通过验收；`passed_probe` 只是部分证据。完整验收还需要干净安装检查、资产来源与许可审查。

本源码目录用于审核，不声明 `environment_qualified`、`source_release_ready` 或分发验证已经完成。运行时兼容、原生安装探针、完整工程验收及再分发权利是不同结论，报告中应保留这些区别。

## 契约变更

动作契约记录维度、限制、关节顺序、映射及控制／物理周期。指纹变化可能阻止任务发现；`revalidate_action_contracts.py` 仅接受测得的原生记录，并检查覆盖范围与语义是否保持。仅更新指纹不足以批准动作行为变化。批准契约变更后，用 `export_evaluation_protocol.py` 重新生成各任务的协议文档。
