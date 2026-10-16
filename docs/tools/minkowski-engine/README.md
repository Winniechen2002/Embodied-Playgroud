# MinkowskiEngine

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Tool policy](../../../rules.en.md#section-8)

Minimum capability level: **L2**. Reference revision: `v0.5.4 / 9f81ae66`. [Upstream source and installation documentation](https://github.com/NVIDIA/MinkowskiEngine).

Sparse-convolution dependency for DexGraspNet 2.0 only; not a standalone grasp generator or broader input permission.

This optional tool's source, dependencies and model weights are not bundled. Provision and verify a pinned local implementation before evaluation, under its upstream terms, and declare explicit grants. A capability level alone does not make a tool available. Level 0 cannot use this prebuilt tool.

Follow the selected [observation and control permissions](../../../Vision_rules.en.md), [grasp rules](../../../rules_grasp.en.md) and [L3 read boundary](../../../rules_privileged.en.md). Higher levels grant only declared inputs, not state writes, extra resets, new tools or online downloads. Candidates require normal action, collision and task validation. Preserve source/checkpoint identity and input provenance. Additional pretrained action policies remain prohibited.
