[English](README.en.md) · [简体中文](README.zh-CN.md)

# EP 评测集合：论文定义与使用口径

本文及四份配套说明将当前论文中的 EP-100、EP-20、EP-Easy 和 EP-Hard 定义映射到 Agent-bench 的环境 ID。定义版本为 `paper-loaded-only-v1`。本文记录定义与成员，不包含模型成绩。

## 论文名称与实现名称

展示名称统一使用 Embodied Playground；Agent-bench 是仓库名。下表映射只用于文档，保留所有目录、Python 包、Gym ID、环境 ID 和 CLI。套件只对入选任务适用。

| Paper family | EP suite | Runtime family | Full catalog | EP-100 |
| --- | --- | --- | ---: | ---: |
| Launcher | Launch | `marble` | 100 | 34 |
| Tower of Hanoi | Tower | `hanoi_panda`, `hanoi_sharpa`, `hanoi_floating` | 120 | 21 |
| Kongming lock | Lock | `kongming_lock` | 60 | 16 |
| Rubik’s cube / Pocket cube | Cube | `rubiks_panda`, `rubiks_sharpa`, `pocket_cube` | 80 | 12 |
| Bookshelf / ManiSkill | Home | `bookshelf`, `maniskill_long_horizon`, `maniskill_geometry`, `maniskill_dynamics` | 50 | 17 |

## 四个集合的关系

EP-100 从完整的 410 项环境中选取 100 项，覆盖五个套件（suite）和 16 个任务类型（type）。EP-Easy 与 EP-Hard 互不重叠，各 50 项，合起来恰好是 EP-100。EP-20 是 EP-100 的固定子集，从 Easy 和 Hard 各取 10 项；它不是另加的 20 项任务，也不是训练／测试划分。

同一个配置与不同机器人组合可以构成不同任务。论文编号（例如 `Tower-18`）用于索引；环境 ID（例如 `hanoi_sharpa/fr3-sharpa/H01`）用于实际运行。种子、四次条件和初态模式不增加目录任务数。

| 集合 | 任务 | Launch | Tower | Lock | Cube | Home | 条件 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [EP-100](EP-100.zh-CN.md) | 100 | 34 | 21 | 16 | 12 | 17 | 400 |
| [EP-Easy](EP-Easy.zh-CN.md) | 50 | 17 | 11 | 8 | 6 | 8 | 200 |
| [EP-Hard](EP-Hard.zh-CN.md) | 50 | 17 | 10 | 8 | 6 | 9 | 200 |
| [EP-20](EP-20.zh-CN.md) | 20 | 6 | 4 | 3 | 3 | 4 | 80 |

以上条件数适用于一个固定评测设置；每任务一个组，每组四个条件。Pass@1 每条件一个有效尝试，Pass@2、Pass@5 和 Pass@10 分别最多 2、5、10 次，首次成功即停止。这些参考上限须在运行前声明，条件数不能当成实际执行次数。

## 选择与难度划分

EP-100 优先保留能通过共享运行时评测的任务，以平行夹爪为主，并从每个灵巧手家族较易的原生配置中选取较小样本；各家族仍沿原生难度轴覆盖不同难度。34 项 Launch 来自图谱中已有完整任务成功记录的 80 个场景。选中某场景不表示所有扰动条件都已有成功证明。

Easy／Hard 由任务定义的工作量决定，不随某次模型成绩改变。先在**每个任务类型内部**按工作量升序排序，低分部分进入 Easy，高分部分进入 Hard；奇数类型的中位任务归入相邻分数更接近的一侧，余下并列分配须满足两集合各 50 项，且任一套件在两个集合中的数量差不超过 1。工作量相同时先按机器人形态（平行夹爪优先），再按任务 ID 排序。工作量用于类型内排名，不应跨套件直接比较绝对值。

| 套件 | 工作量分数 |
| --- | --- |
| Launch | 10 × 原生 tier + loaded 难度 D1–D5 的数值 + 必需目标数 |
| Tower | 2 × depth index + 物理主题加 1 + FR3–Sharpa 加 2／floating Sharpa 加 3（Panda 加 0） |
| Lock | 键／键和横杆／完整锁分别为 0／2／4 + hard pose 加 1 + 装配加 0.5 + 双 floating Sharpa 加 2 |
| Cube | 打乱或状态转移的四分之一转数 + Sharpa 形态加 3 |
| Home | 书架使用物体数；ManiSkill 使用有序里程碑与最终谓词的数量 |

`depth index` 将 1、3、9、31 步分别映射为 0、1、2、3。Cube 的四分之一转计数与打乱 token 数不同，例如 EP-20 的 Cube-06（C11）为 14 个四分之一转。原生难度（tier、D1、Hanoi L1 等）、EP 的 Easy／Hard 与权限 L0–L3 是不同维度；ManiSkill 环境 ID 中的 L1 也是任务代码。

当前修订按 loaded 难度计算 Launch 工作量，**Launch-15（A029）为 Easy，Launch-17（A055）为 Hard**。精确成员以四份配套文档和 `tasks.json` 为准。

## 共同评测设置

协议为 `environment-four-trial-v2`，权限版本为 `2026-10-09-environment-l0-l3`。标准 base seed 为 0；固定任务、初态、操作／观测档位、权限、工具授权、预算、协议与实现版本，以及 agent 版本、代码和指令后构成评测组。更换这些设置须另报结果。

- **Launch 只评测 loaded**：第一发预装，任务要求的后续装填仍由 agent 完成。ground 初态不计入四个 EP 集合，也不参与 Launch 工作量分数。
- 其余任务使用 default 初态。每条件重新初始化环境和 agent 会话；回合内保留损伤、弹药消耗和状态，初始化与 reset 由评测端管理。
- Launch 四条件使用 22／24／26／28 N/m 弹簧及规定偏移和背景；Hanoi、Pocket 使用连续种子和有界姿态／物性／光照扰动；Bookshelf 使用原生布局采样。
- Rubik、Lock、ManiSkill 保持作者物理布局，仅使用 0.85／0.95／1.05／1.15 光照倍率；ManiSkill 固定 `physics_variant=0`。这些条件不能解释成四个不同谜题或四次重试。
- 任务成功由独立评分器按目标、全过程规则、物理约束及释放／稳定要求判定，且必须在预算内成立。权限提高不改变任务规则。

精确条件和环境预算参见[逐任务协议](../evaluation/index.zh-CN.md)及[条件清单](../evaluation/tasks.json)。按本文成员和 initial mode 筛选后使用，不能直接将通用清单的全部组计入 EP。

## 评分

对于已完整评测的组，令四个条件的成功指示为 z1…z4：

```text
任务成功率 S_task = (z1 + z2 + z3 + z4) / 4
四条件全成功 A_task = z1 × z2 × z3 × z4
套件成功率 S_suite = 该集合在此套件中的任务成功率均值
集合成功率 S = (S_Launch + S_Tower + S_Lock + S_Cube + S_Home) / 5
```

五个套件各占 **20%**，不能用全部成功条件数除以总条件数代替论文主指标。全成功指标也按任务、套件、五套件的相同顺序聚合；它不同于平均条件成功率。

Pass@K（K = 1、2、5 或 10）使用同一条件按时间顺序最早 K 次有效尝试中的任一次成功。Pass@5 和 Pass@10 是 playground 新增的参考上限。各个要求的档位从同一组有序记录中分别统计，不能由 Pass@1 概率推算。只有前 K 次中成功或累计 K 次有效失败，该条件在此档位才算完成，否则该档位仍为 partial。首次成功即停止，各次尝试相互隔离，条件和单次预算保持一致。四个条件始终各占任务分母的四分之一。论文实验扩展中，普通 agent 失败及预算耗尽（包括墙钟超时）占用机会，经确认的基础设施异常不占用；须保留全部记录和排除依据。

仍有 invalid 或 missing 条件时标为 partial，保留固定分母、已观测成功下界、完成覆盖率和缺失／无效计数，最终指标不定义。不同权限、工具和尝试预算的结果分开报告。Time@S 统计成功尝试达到成功事件的墙钟时间均值；Tok@S 统计成功尝试的输入（含缓存）与输出 token 均值，缺失用量不能按零处理。

## 与现有仓库协议的边界

[通用评测协议](../evaluation_protocol.zh-CN.md)覆盖 loaded 与 ground：完整 410 项为 510 组、2040 条件；论文 loaded-only 口径为 410 组、1640 条件。EP-100 则固定为 100 组、400 条件。三个数字的适用范围不同。

论文基础协议把墙钟超时、拒绝动作、agent 异常等列为 invalid，并规定不得替换已完成的失败或无效尝试；论文实验章节另行定义基于原因审计的 Pass@1／Pass@2 扩展。仓库现有协议也采用原因审计的异常计数。复现实验时要声明使用的口径，不能仅凭运行时终止标签推断机会是否被消耗；本文不改写原协议或运行时代码。

## 定义索引

[tasks.json](tasks.json)记录精确环境 ID、子集成员及 `paper-loaded-only-v1` 定义。选择依据为环境修订 `a58a288` 的 `agentbench-curated-v2`、原索引版本 `1.4`。

EP-100 包含 100 个任务；Easy 与 Hard 各 50 个、互不重叠且并集为 EP-100；EP-20 从二者各取十个。该文件是文档成员索引，不是评测运行器配置。修改定义时同步两种语言与索引。
