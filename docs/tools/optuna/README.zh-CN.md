# Optuna

[English](README.en.md) · [简体中文](README.zh-CN.md) · [工具政策](../../../rules.zh-CN.md#section-8)

最低能力等级：**L1**。参考修订：`v4.9.0 / 4db42e31c24b200e52595df9d4c00e2cdeefea2b`。[上游源码与安装文档](https://github.com/optuna/optuna)。

优化声明的代理目标。Level 1/2 不得使用原始模拟器奖励、私有评分反馈、额外重置或跨回合 rollout 定义目标。

固定版本源码已内嵌于 [`third_party/optuna`](../../../third_party/optuna)，版本与许可见[源码清单](../../../third_party/README.md)。评测前仍需按上游条款配置运行依赖及另行要求的检查点，明确声明授权。能力等级本身不代表工具已可用；Level 0 不得使用此预置工具。

遵循所选等级的[观测与控制权限](../../../Vision_rules.zh-CN.md)、[抓取规则](../../../rules_grasp.zh-CN.md)及 [L3 读取边界](../../../rules_privileged.zh-CN.md)。更高等级仅授权声明的输入，不授权状态写入、额外重置、新工具或在线下载。候选结果仍需动作、碰撞与任务验证，并保留源码／检查点身份及输入来源。额外的预训练动作策略仍被禁止。
