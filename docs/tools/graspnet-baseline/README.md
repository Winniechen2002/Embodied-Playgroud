# GraspNet Baseline

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Tool policy](../../../rules.en.md#section-8)

Minimum capability level: **L2**. Reference revision: `280c215129f759ed8649cb4e89fc5dfee55f4f80`. [Upstream source and installation documentation](https://github.com/graspnet/graspnet-baseline).

Generate parallel-gripper grasp candidates from permitted geometry. The gateway plugin requires an explicit grant, configured implementation and immutable capture/calibration binding; candidate generation neither executes actions nor advances physics. Level 2 excludes native hidden depth unless declared as a permitted sensor.

This optional tool's source, dependencies and model weights are not bundled. Provision and verify a pinned local implementation before evaluation, under its upstream terms, and declare explicit grants. A capability level alone does not make a tool available. Level 0 cannot use this prebuilt tool.

Follow the selected [observation and control permissions](../../../Vision_rules.en.md), [grasp rules](../../../rules_grasp.en.md) and [L3 read boundary](../../../rules_privileged.en.md). Higher levels grant only declared inputs, not state writes, extra resets, new tools or online downloads. Candidates require normal action, collision and task validation. Preserve source/checkpoint identity and input provenance. Additional pretrained action policies remain prohibited.
