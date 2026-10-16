# GraspNet Baseline

[English](README.en.md) · [简体中文](README.zh-CN.md) · [工具政策](../../../rules.zh-CN.md#section-8)

最低能力等级：**L2**。参考修订：`280c215129f759ed8649cb4e89fc5dfee55f4f80`。[上游源码与安装文档](https://github.com/graspnet/graspnet-baseline)。

根据合法几何生成平行夹爪抓取候选。网关插件要求明确授权、已配置实现及不可替换的采集／标定绑定；生成候选不执行动作或推进物理。Level 2 不允许隐藏的原生深度，除非它被明确声明为允许传感器。

固定版本源码已内嵌于 [`third_party/graspnet-baseline`](../../../third_party/graspnet-baseline)，版本与许可见[源码清单](../../../third_party/README.md)。评测前仍需按上游条款配置运行依赖及另行要求的检查点，明确声明授权。能力等级本身不代表工具已可用；Level 0 不得使用此预置工具。

遵循所选等级的[观测与控制权限](../../../Vision_rules.zh-CN.md)、[抓取规则](../../../rules_grasp.zh-CN.md)及 [L3 读取边界](../../../rules_privileged.zh-CN.md)。更高等级仅授权声明的输入，不授权状态写入、额外重置、新工具或在线下载。候选结果仍需动作、碰撞与任务验证，并保留源码／检查点身份及输入来源。额外的预训练动作策略仍被禁止。
