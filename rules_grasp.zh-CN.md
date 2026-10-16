<!-- bilingual-navigation:start -->
[English](rules_grasp.en.md) | [简体中文](rules_grasp.zh-CN.md) | [原文](rules_grasp.md) | [全部文档](docs/README.zh-CN.md)
<!-- bilingual-navigation:end -->

当前目录任务采用冷启动尝试；禁止跨尝试记忆与轨迹继承。遵循[共同规则](rules.zh-CN.md)及所声明实验的尝试／资源预算。

<a id="section-1"></a>
# Level 2：抓取模型智能体规则

遵循[共享规则](rules.zh-CN.md)和 [Level 1](Vision_rules.zh-CN.md)，包括所声明实验的资源预算与冷启动要求。Level 2 额外允许预训练抓取生成模型。方法档位：`grasp_model`；继承 `vision_geometry_proxy_rl`。

使用所选环境的 `task.md` 及其共享任务要求，索引见[环境文档](docs/evaluation/index.zh-CN.md)。执行同一任务的机器人共用任务合法性、评分和预算；机器人专用接口与评测器支持情况单独说明。

各次尝试遵循共享规则中的冷启动隔离要求。
遵循[共享尝试隔离规则](rules.zh-CN.md#section-6)。

<a id="section-2"></a>
## 新增能力

只有[共享白名单](rules.zh-CN.md#section-8)中固定版本的 Level 2 工具可生成、排序或优化抓取/接触：GraspNet Baseline、DexGraspNet 2.0、GenDexGrasp 和 CEDex ContactGen。MinkowskiEngine 仅可作为 DexGraspNet 的稀疏卷积依赖。这些模型的通用检查点及独立微调是允许的。

使用合法 RGB 或 Level 1 派生的深度、掩码、点云和几何。候选可用于可达性/碰撞/任务过滤、抓取优化、IK、规划、闭环控制，或代理仿真的动作/初始化/奖励。模型建议仍受全部物理与任务约束。AnyGrasp、Contact-GraspNet、远程 API 和其他未列出的模型不在授权范围内。

<a id="section-3"></a>
## 保持不变的边界

不得使用原始仿真器的特权状态、原生标注、接触、奖励、评测器反馈，也不得针对这些输入训练或优化。这里不增加原始仿真器重置或回合次数。不得用过去的场景数据初始化或调整代理仿真；不得继承过去尝试的轨迹。不允许导入额外的预训练或此前微调过的动作策略检查点/控制器；获准运行期间在代理仿真中从零训练仍然允许。被测模型自身可以保留事先声明并冻结的预训练权重。这里不授予使用人工示范/纠正的权限。

<a id="section-4"></a>
## 附加证据

保存抓取模型/检查点/版本、预处理、输入来源、原始候选/分数、选择/拒绝原因、最终下发的抓取，以及微调数据/配置。共享审计覆盖轨迹、代理仿真来源，以及私有评测器逐步穿透记录，包括首次违规碰撞对、深度和轨迹标签。

<!-- environment-release-permissions -->
本次环境权限版本允许 L0 执行代码、基础图像处理及自行实现动力学／IK／规划，但不提供预置领域工具或外部视觉模型。权限是工具可用性分级，不是算法能力限制。模型 token／图片预算属于另行执行的实验协议，不作为环境包的验收结果。详见 [L0](rules_model_only.zh-CN.md)。
