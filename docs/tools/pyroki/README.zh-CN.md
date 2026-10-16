# Pyroki

[English](README.en.md) · [简体中文](README.zh-CN.md) · [工具政策](../../../rules.zh-CN.md#section-8)

最低能力等级：**L1**。参考修订：`388e43e1`。[上游源码与安装文档](https://github.com/chungmin99/pyroki)。

基于 JAX 的 IK 与重定向。依赖与 Isaac/PyTorch 隔离，评测前固定传递源码依赖。

本版本不捆绑此可选工具的源码、依赖或模型权重。评测前按上游条款配置并验证固定版本的本地实现，明确声明授权。能力等级本身不代表工具已可用；Level 0 不得使用此预置工具。

遵循所选等级的[观测与控制权限](../../../Vision_rules.zh-CN.md)、[抓取规则](../../../rules_grasp.zh-CN.md)及 [L3 读取边界](../../../rules_privileged.zh-CN.md)。更高等级仅授权声明的输入，不授权状态写入、额外重置、新工具或在线下载。候选结果仍需动作、碰撞与任务验证，并保留源码／检查点身份及输入来源。额外的预训练动作策略仍被禁止。
