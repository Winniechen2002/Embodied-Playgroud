<!-- bilingual-navigation:start -->
[English](rules.en.md) | [简体中文](rules.zh-CN.md) | [原文](rules.md) | [全部文档](docs/README.zh-CN.md)
<!-- bilingual-navigation:end -->

当前目录任务采用[四条件协议](docs/evaluation_protocol.zh-CN.md)与冷启动尝试。Pass@2 仅适用于预先声明的实验。经确认的非 agent 异常按[共同计次规则](#non-agent-failures)补跑。环境网关不计量模型 token 或图像读取次数。

<a id="section-1"></a>
# 共享智能体规则

这些规则适用于所有评测档位和智能体模型。请通读一次本文件、选定等级及其继承的档位，以及选定环境的任务说明；之后只需重读变更部分。`task.md` 指环境的任务说明，并不要求仓库根目录存在该文件。[环境文档](docs/evaluation/index.zh-CN.md) 索引了不同机器人共享的规范任务要求。机器人专用任务文件定义控制接口、已声明的安装例外和评测器集成。

<a id="section-2"></a>
## 能力等级档位

能力档位为 Level 0、Level 1、Level 2 和 Level 3。Level 0 允许代码和自行实现的算法；Level 1 明确增加预置工具权限，Level 2/3 再增加下表列出的权限。只有较高等级的明确授权才能覆盖较低等级的限制。共同预算和物理约束始终适用。能力档位版本为 `2026-10-09-environment-l0-l3`，记录为 `capability_profile_version`；预算版本保持不变并单独记录。

| 等级 | 新增能力 | 档位文档 |
| --- | --- | --- |
| Level 0 | 允许代码及自写算法；不提供预置领域工具或外部视觉模型 | [rules_model_only.md](rules_model_only.zh-CN.md) |
| Level 1 | 视觉、几何、IK/规划、由观测重建的代理仿真中的强化学习 | [Vision_rules.md](Vision_rules.zh-CN.md) |
| Level 2 | 预训练抓取/接触模型 | [rules_grasp.md](rules_grasp.zh-CN.md) |
| Level 3 | 原始仿真器的特权读取和训练 | [rules_privileged.md](rules_privileged.zh-CN.md) |

所有能力等级（包括 Level 0）均可获得公开任务条件。
发射器任务中，宿主必须在每个回合的第一个动作之前，提供该回合实际配置的弹簧刚度
`variation_request.spring_stiffness`，将 `variation_request.spring_stiffness_unit`
设为 `N/m`，并记录 `task_metadata_version: public-spring-v1`。
标准四次测试分别为 22、24、26、28 N/m；legacy 使用实际配置值，默认 25 N/m。
这属于公开任务信息，不是工具输出或特权状态读取。
详见[四次测试协议](docs/evaluation/marble.zh-CN.md)。
模型无需从外观或试探交互中猜测刚度，仍须按所选等级自行决定并执行机器人动作；
此公开项不授予其他隐藏动力学、物体位姿或测评器状态的访问权限。

<a id="non-agent-failures"></a>
<a id="section-3"></a>
## 非 agent 异常与有效尝试计数

尝试计数补充规则：`non-agent-exclusion-v1`（2026-10-15），在评测元数据中记录为 `attempt_accounting_version`。适用于全部能力等级及预先声明的尝试上限，优先于旧文档中“所有异常均消耗次数”或“异常不得补跑”的笼统表述；不改变任务条件、原生成功判据、权限版本或预算版本。

- **经证据确认并非 agent 操作导致的失败或中断，不计入有效尝试次数，不作为任务失败计入成绩；为同一测试条件补跑，不占用下一次有效机会。** 例如非 agent 引起的主机重启／断电、模型服务故障或响应流断连、运行环境／依赖／仿真器／评分器缺陷。不能仅凭 `invalid`、异常名称或 agent 自述判定免责；原因不明时单列待审，查明后再决定是否消耗有效机会。
- agent 自身的错误动作、违规、控制程序异常或主动放弃导致的失败，以及未成功完成任务时正常的墙钟超时、仿真时间或步数耗尽，仍计为一次有效失败。可恢复的动作拒绝本身不新建一次尝试；若最终因 agent 原因未完成，则按失败计数。
- 每次实际启动都分配独立实验 ID。保留原始日志、终局标志、时间、错误原因、归因依据、任务／条件标识、源码和运行时版本，以及实际 token／图像／耗时用量。剔除记录标明 `attribution=non_agent`、`excluded=true`、`consumes_valid_opportunity=false`，关联原实验和补跑实验；不得删除或覆盖旧记录，也不得把实际用量记为零。
- 补跑使用新的隔离环境和冷启动 agent，保持同一任务、条件、种子、扰动、权限及单次预算，不继承被剔除尝试的记忆、代码产物或轨迹。修复环境时记录变更及其版本；改变组身份字段时仍须另建组并单独报告。实际启动次数可高于有效尝试上限，但有效机会数不得增加；本条不允许绕过另行规定的总资源上限。
- 最终成绩中的每个有效实验结果只有成功或失败，且必须链接实验记录。剔除事件和待补条件是独立审计／调度状态，不是第三种任务结果；补齐后仍按原定条件数统计。标准四回合协议不允许重试有效失败；若单独实验预先声明每条件最多两次有效机会，则非 agent 异常不占这两次，首次成功即停止，否则两次有效失败后才判该条件失败。

<a id="section-4"></a>
## 尝试与模型预算

评测前声明有效尝试上限、token／图像上限、墙钟限制及资源计量口径，不因失败增加预算。任务原生时间和步数限制始终有效。标准协议每个条件一次有效尝试；明确声明的 Pass@2 实验最多两次，首次成功即停止。剔除的基础设施异常不占有效机会。

实验主机汇总 agent 与所有辅助进程的全部输入 token（包括缓存输入）和输出 token，包含准备、工具调用与报告。按唯一请求 ID 记录实际用量，未知用量不等于零。剔除异常消耗的资源仍保留在账本中。

<a id="section-5"></a>
## 图像与观测

实验主机声明并执行图像读取上限。所有辅助进程提交的图像、帧、裁剪和重复视觉读取均需计数。仅渲染或保存图像不等于 agent 读取；缩放观测时保持相机标定一致。图像预算不授权额外传感器字段或隐藏模拟器信息。

<a id="section-6"></a>
## 尝试隔离

每个条件与有效重试均使用新环境和冷启动 agent，不继承其他尝试的记忆、代码产物、解题轨迹或特权诊断。同一次尝试中可以保留自身合法观测与动作。非 agent 异常补跑使用相同条件并独立初始化，具体要求见上文。

<a id="section-7"></a>
## 执行与验证

- 使用声明的动作接口和机器人真实物理接触。禁止瞬移、直接写状态、隐藏抓取约束、绕过碰撞、穿隧，以及利用可见几何与碰撞几何不匹配。
- 固定场景、相机、光照、几何、初态、物理和评测器设置必须保持不变，除非任务明确将相应变化列为合法动作。特权读取永远不等于写入权限。
- 执行模型/规划器输出前，检查有限值、机器人限位、动作速率、碰撞、目标残差和任务合法性。结果无效、超时或未收敛时应拒绝，不得放宽约束。
- 独立评测器在每个物理子步检查任务违规，包括任务规定范围和容差内的穿透。发生硬违规应停止执行并保留首次原因。不得修改或伪造评测器结果。任务成功要求方法合规和独立评测器成功同时成立。
- 对 Level 0，由可信环境执行必要的合法性和违规检查。固定动作解码器与机器人原生伺服属于环境基础设施，不是智能体工具；它们不得推断目标、求解 IK、规划、修补动作或切换到其他控制器。无效动作应被拒绝。
- 在有意义的状态转换或失败处进行事件驱动检查。必要检查通过后继续；只有相关变化或新证据出现时才重复。详细证据存入文件，汇报简洁结论。

<a id="section-8"></a>
## 本地工具政策与文档索引

Level 0 可执行代码并使用基础依赖，但不得调用预置领域工具或外部视觉模型。下方白名单仅按所列最低等级适用于 Levels 1–3；共享预算计入某种工具，不等于授权使用它。被测模型本身以及环境观测/动作传输不属于辅助工具；事先声明并冻结的模型权重和内置视觉编码器属于被测模型自身。当前任何档位都不授权导入额外的预训练或此前微调过的动作策略检查点或控制器。

评测期间，智能体不得通过在线搜索、浏览、GitHub或软件包搜索、下载、远程推理或远程规划器来发现或接入工具。请使用下方在本地固定版本的白名单。工具或检查点缺失是能力缺口，不代表可以替换为其他模型。评测前，维护者批准的安装流程可以准备固定版本的源码、依赖和检查点。新增工具必须先审查其用途、数据访问、许可证、不可变版本及本地烟测，再明确更新白名单/文档。仅提到模型名称不构成工具授权。

| 最低等级 | 工具与文档 |
| --- | --- |
| 1 | [Depth Pro](docs/tools/depth-pro/README.zh-CN.md)、[Depth Anything 3](docs/tools/depth-anything-3/README.zh-CN.md) |
| 1 | [Stream3D](docs/tools/stream3d/README.zh-CN.md)（仅 SAM3D 后端）、[SAM 3D Objects](docs/tools/sam-3d-objects/README.zh-CN.md) |
| 1 | [Pinocchio](docs/tools/pinocchio/README.zh-CN.md)、[SciPy](docs/tools/scipy/README.zh-CN.md)、[Pyroki](docs/tools/pyroki/README.zh-CN.md) |
| 1 | [cuRoboV2](docs/tools/curobo-v2/README.zh-CN.md) v0.8.0、[cuRobo v1](docs/tools/curobo-v1/README.zh-CN.md) v0.7.8（仅旧版兼容）、[OMPL](docs/tools/ompl/README.zh-CN.md) |
| 1 | [RSL-RL](docs/tools/rsl-rl/README.zh-CN.md) v5.0.1、[Optuna](docs/tools/optuna/README.zh-CN.md) v4.9.0 |
| 2 | [GraspNet Baseline](docs/tools/graspnet-baseline/README.zh-CN.md)、[DexGraspNet 2.0](docs/tools/dexgraspnet2/README.zh-CN.md)、[GenDexGrasp](docs/tools/gendexgrasp/README.zh-CN.md)、[CEDex ContactGen](docs/tools/cedex-contactgen/README.zh-CN.md) |
| 2 | [MinkowskiEngine](docs/tools/minkowski-engine/README.zh-CN.md)，仅作为 DexGraspNet 的稀疏卷积依赖 |

Pinocchio/SciPy 是默认重定向方案。JAX 与主运行时冲突时，将 Pyroki 隔离运行。cuRobo v1/v2 使用独立环境；新增集成采用 v2，任何回退到旧 v1 的情况都需记录。OMPL 要求调用方提供限位、碰撞检查和状态转换。精确版本、安装和运行注意事项见[工具索引](rules.zh-CN.md#section-8)。

<a id="section-9"></a>
## 审计与结果

适用证据保存一次，并通过路径引用：尝试/token/读取总账（图像来源、尺寸、用途、数量）、带时间戳的观测和标定、工具/代码/检查点版本与哈希、预处理、输入来源与单位、原始输出、决定/拒绝、规划器配置和残差、轨迹/命令，以及要求的最终图像或视频。评测器日志单独保存，只按所选档位和接口允许的范围公开。保存证据不要求重新读取每张图像。

报告 `capability_level`、`method_profile`、`method_compliance`、独立任务结果、证据路径及首次违规/原因（如有）。保留任务评测器现有输出结构。任何档位都不自动允许人工示范、遥操作、纠正、偏好、DAgger查询或手写专家训练轨迹。任务专属例外需要明确授权并单独报告，不得作为标准能力档位的结果。

<!-- environment-release-permissions -->
本次环境权限版本允许 L0 执行代码、基础图像处理及自行实现动力学／IK／规划，但不提供预置领域工具或外部视觉模型。权限是工具可用性分级，不是算法能力限制。模型 token／图片预算属于另行执行的实验协议，不作为环境包的验收结果。详见 [L0](rules_model_only.zh-CN.md)。
