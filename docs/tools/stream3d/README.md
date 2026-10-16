# Stream3D

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Tool policy](../../../rules.en.md#section-8)

Minimum capability level: **L1**. Reference revision: `be551cc756f5710875ec1c6a4c0fa545b56d2c4f`. [Upstream source and installation documentation](https://github.com/kaichen-z/STREAM3D).

Fuse legal posed multi-view RGB into proxy geometry. Only the sam3d backend is allowed; TRELLIS.2 and its runners/checkpoints are excluded. Upstream license status at this revision is unresolved; do not redistribute it as part of this release.

This optional tool's source, dependencies and model weights are not bundled. Provision and verify a pinned local implementation before evaluation, under its upstream terms, and declare explicit grants. A capability level alone does not make a tool available. Level 0 cannot use this prebuilt tool.

Follow the selected [observation and control permissions](../../../Vision_rules.en.md), [grasp rules](../../../rules_grasp.en.md) and [L3 read boundary](../../../rules_privileged.en.md). Higher levels grant only declared inputs, not state writes, extra resets, new tools or online downloads. Candidates require normal action, collision and task validation. Preserve source/checkpoint identity and input provenance. Additional pretrained action policies remain prohibited.
