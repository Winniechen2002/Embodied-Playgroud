# Stream3D

[English](README.en.md) · [简体中文](README.zh-CN.md) · [工具政策](../../../rules/rules.zh-CN.md#section-8)

最低能力等级：**L1**。参考修订：`be551cc756f5710875ec1c6a4c0fa545b56d2c4f`。[上游源码与安装文档](https://github.com/kaichen-z/STREAM3D)。

将合法多视角 RGB 融合为代理几何。仅允许 sam3d 后端，排除 TRELLIS.2 及其运行器和检查点。此修订没有仓库级许可证；内嵌不授予第三方再分发权。

固定版本源码已内嵌于 [`third_party/STREAM3D`](../../../third_party/STREAM3D)，版本与许可见[源码清单](../../../third_party/README.md)。评测前仍需按上游条款配置运行依赖及另行要求的检查点，明确声明授权。能力等级本身不代表工具已可用；Level 0 不得使用此预置工具。

遵循所选等级的[观测与控制权限](../../../rules/Vision_rules.zh-CN.md)、[抓取规则](../../../rules/rules_grasp.zh-CN.md)及 [L3 读取边界](../../../rules/rules_privileged.zh-CN.md)。更高等级仅授权声明的输入，不授权状态写入、额外重置、新工具或在线下载。候选结果仍需动作、碰撞与任务验证，并保留源码／检查点身份及输入来源。额外的预训练动作策略仍被禁止。
