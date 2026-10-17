# Embodied Playground

> 请按 `Agent.md`，以 **L0** 在 **EP-20** 上测试当前 Agent 的能力，采用 **Pass@1**，并报告五个套件得分、总分和完成覆盖率。

将这句话交给负责组织评测的 Agent。替换 **EP-20** 和 **L0**，即可指定要测的 benchmark 和能力等级。需要参考更多尝试机会时，将 **Pass@1** 换成 **Pass@2**、**Pass@5** 或 **Pass@10**。

[English](README.en.md) · [Agent 操作说明](Agent.zh-CN.md) · [测试规则](rules/rules.zh-CN.md)

Embodied Playground 测试 Agent 能否观察仿真场景、选择动作并完成物理任务，涵盖发射、堆叠、装配、魔方和家居操作。

## 如何测试你的 Agent

1. **准备环境。** 按[安装说明](docs/environment_installation.zh-CN.md)配置 MuJoCo、Isaac Lab、ManiSkill 及所需资产。各 benchmark 会用到这些环境。
2. **接入 Agent。** 让你的评测宿主通过 Python SDK 把观测交给 Agent，并执行它生成的动作。需要的授权工具应提前准备好，具体流程见 [Agent 操作说明](Agent.zh-CN.md)。
3. **发送开头的 prompt。** 整个测试固定 Agent 版本、指令和设置；每个条件使用全新的环境与 Agent 会话。
4. **查看结果。** 以环境返回的最终成功结果计分，同时报告完成覆盖率；未完成的测试不能给出最终 benchmark 总分。

这句 prompt 用于组织评测流程。仓库提供环境和 SDK，各轮会话由你的 Agent 宿主执行。`environment_client.py` 只检查连接，不代表 Agent 已完成解题测试。

## 选择 benchmark

| Benchmark | 任务数 | 条件数 | 用途 |
| --- | ---: | ---: | --- |
| **EP-20** | 20 | 80 | 建议从这里开始 |
| **EP-100** | 100 | 400 | 完整论文基准 |
| **EP-Easy** | 50 | 200 | EP-100 中较容易的一半 |
| **EP-Hard** | 50 | 200 | EP-100 中较难的一半 |
| **Full test** | 410 | 1,640 | playground 中的全部任务 |

每个任务测试四个条件，包括 Full test 在内均使用 Launcher loaded 初始化。任务名单见 [EP 子集定义](docs/ep_subsets/README.zh-CN.md)或[完整任务目录](docs/evaluation/index.zh-CN.md)。Full test 按此初始化方式覆盖全部任务；目录中另外列有 Launcher ground 条件。

完整测试的 prompt：

> 请按 `Agent.md`，以 **L0** 在 **Full test** 上测试当前 Agent 的能力，采用 **Pass@1**，并报告五个套件得分、总分和完成覆盖率。

### 测试某个特定环境

在[任务目录](docs/evaluation/index.zh-CN.md)中找到准确的 `task_id`，然后使用：

> 请按 `Agent.md`，以 **L0** 仅测试环境 **marble/dual-panda/A007**，采用 **Pass@1**，并报告四个条件的结果、任务得分和完成覆盖率。

将 **marble/dual-panda/A007** 换成目标 ID，即可测试该环境的四个条件。能力等级和 Pass@K 上限也可按前文替换。启动环境及接入 Agent 的步骤见 [Agent 操作说明](Agent.zh-CN.md#启动每次尝试仅供宿主)。单环境只报告任务得分，不作为完整 benchmark 总分。

## 选择能力等级

| Level | Agent 可以使用什么 |
| --- | --- |
| **L0** | RGB、公开机器人信息、Python、NumPy、Pillow 和自己编写的算法 |
| **L1** | L0 加上已授权的视觉、几何、IK、规划及代理环境工具 |
| **L2** | L1 加上已授权的预训练抓取／接触工具 |
| **L3** | L2 加上明确开放的仿真器特权信息，只读 |

更高等级不会自动安装或开启工具。测试前固定工具清单与观测配置；所有等级都遵守[规则](rules/rules.zh-CN.md)，都不能直接修改仿真状态。

## 如何看分数

**Pass@1** 表示每个条件只有一次有效尝试。先平均任务的四个条件，再平均套件中的任务，最后让五个套件各占总分的 20%。**Pass@2**、**Pass@5** 和 **Pass@10** 是参考选项，分别允许每个条件最多 2、5、10 次有效尝试，首次成功即停止。测试前声明上限，各档实测分数单独报告；增加尝试次数不改变四个必测条件及其权重。失败、未完成与结果记录方式见 [Agent 操作说明](Agent.zh-CN.md#报告结果)。

[安装](docs/environment_installation.zh-CN.md) · [工具与求解器](docs/embedded_tools.zh-CN.md) · [验证](docs/environment_validation.zh-CN.md) · [全部文档](docs/README.zh-CN.md)

原创代码采用 [Apache-2.0](LICENSE)；原创文档和独立自制非代码资产采用 [CC BY 4.0](LICENSES/CC-BY-4.0.txt)。第三方内容保留原条款，见[许可说明](LICENSING.md)。
