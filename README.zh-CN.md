# Embodied Playground

[English](README.en.md) · [简体中文](README.zh-CN.md) · [文档](docs/README.zh-CN.md)

Embodied Playground 是面向闭环物理、策略与空间推理的机器人基准。本仓库提供 410 个任务环境、机器人与场景资产、Python SDK、原生评分器和统一权限网关。实现沿用 Agent-bench 的包名与命令名。

发布版另含 [工具、求解器与第三方源码](docs/embedded_tools.zh-CN.md)，保留固定版本及原许可；使用前需配置独立依赖并明确授权。

| 环境系列 | 任务数 | 运行时 |
| --- | ---: | --- |
| 发射器，双 Panda | 100 | MuJoCo |
| 汉诺塔，Panda / FR3 + Sharpa / 浮动 Sharpa | 120 | Isaac Lab |
| 孔明锁，双 Panda / 双浮动 Sharpa | 60 | Isaac Lab |
| 三阶魔方，Panda / 浮动 Sharpa | 60 | Isaac Lab |
| 二阶魔方，ALOHA / 双 Sharpa | 20 | Isaac Lab |
| 书架整理，双 Panda | 20 | Isaac Lab |
| 家务、精密操作与动态任务 | 30 | ManiSkill |
| **总计** | **410** | |

## 快速开始

使用 Python 3.11，并分别为 MuJoCo、Isaac Lab 和 ManiSkill 配置独立环境。[安装指南](docs/environment_installation.zh-CN.md)列出固定依赖、原生模拟器与资产配置。在仓库根目录，使用已配置的 MuJoCo 环境运行：

```bash
python scripts/environment_release.py catalog --output /tmp/agentbench-catalog.json
python scripts/environment_runtime.py --task-id marble/dual-panda/A001 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/agentbench-session
```

在使用相同环境的第二个终端中连接：

```bash
python scripts/environment_client.py /tmp/agentbench-session/session.json
```

示例客户端读取观测、执行短暂停持并结束回合。Agent 使用 `describe`、`observe`、`step` 和 `finish`；初始化与重置由评测方控制。读取不推进物理时间，重复动作请求 ID 不重复执行动作，已结束的回合拒绝继续步进。

## 评测设置

[EP 子集](docs/ep_subsets/README.zh-CN.md)定义 EP-100、EP-20、EP-Easy 和 EP-Hard，分别包含 100、20、50、50 个任务，分为 Launch、Tower、Lock、Cube、Home 五个套件。

每个任务有四个条件。论文设置中发射器**仅使用 loaded 初始化**：完整 410 个任务对应 1,640 个条件，EP-100 对应 400 个，EP-20 对应 80 个，EP-Easy 与 EP-Hard 各对应 200 个。通用运行时还支持 ground 初始化，共 510 组、2,040 个条件，这是另一套安排。

任务成功率为四个条件的均值，套件成功率为任务均值，子集总分对五个套件等权平均。Pass@1 使用第一次有效尝试；Pass@2 每个条件最多使用两次有效尝试，成功即停止。普通 agent 失败和预算耗尽占用机会。经证据确认的非 agent 基础设施异常保留记录，从有效尝试中剔除，并在相同条件下补跑。详见[协议](docs/evaluation_protocol.zh-CN.md)、[具体条件](docs/evaluation/index.zh-CN.md)与[规则](rules.zh-CN.md)。

## 权限等级

权限版本：`2026-10-09-environment-l0-l3`。

- **L0：** Python 标准库、NumPy、Pillow 与自编算法。
- **L1：** 增加明确授权且已安装的视觉、几何、IK、规划及代理仿真工具。
- **L2：** 增加明确授权且已安装的预训练抓取与接触工具。
- **L3：** 增加声明过的模拟器特权只读字段。

等级不授权状态写入，也不自动安装工具。网关约束其公开接口，不审计外部客户端进程使用的全部库。三阶魔方任务明确使用 `hybrid_fixture_v1` 辅助机构及其物理前置条件。

## 范围与验证

本源码版本包含环境、SDK、规则及配套验证工具，不含模型结果、解题轨迹或排行榜。[验证说明](docs/environment_validation.zh-CN.md)列出工程检查及其局限。

本次公开源码发布的工程验收已通过，采用维护者确认的标准：源码回归、全部 410 项评分夹具与原生安装检查、130 项默认条件物理检查、文档检查及 MuJoCo 导出包烟雾检查。

维护者已确认随本源码提供的完整资产包可按原有适用许可证分发，详见资产许可清单。

## 许可

原创代码使用 [Apache-2.0](LICENSE)，原创文档与独立自制非代码资产使用 [CC BY 4.0](LICENSES/CC-BY-4.0.txt)，版权主体为 Chen Feng。第三方条款与通知继续有效，详见[许可范围](LICENSING.md)、[第三方通知](THIRD_PARTY_NOTICES.md)与[资产来源](docs/environment_assets.zh-CN.md)。
