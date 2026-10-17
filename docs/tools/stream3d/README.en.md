# Stream3D

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Tool policy](../../../rules/rules.en.md#section-8)

Minimum capability level: **L1**. Reference revision: `be551cc756f5710875ec1c6a4c0fa545b56d2c4f`. [Upstream source and installation documentation](https://github.com/kaichen-z/STREAM3D).

Fuse legal posed multi-view RGB into proxy geometry. Only the sam3d backend is allowed; TRELLIS.2 and its runners/checkpoints are excluded. This revision has no repository-level license; embedding does not grant third-party redistribution rights.

The pinned source is embedded at [`third_party/STREAM3D`](../../../third_party/STREAM3D). See the [snapshot inventory](../../../third_party/README.md). Prepare runtime dependencies and any separately required checkpoints before evaluation, under upstream terms, and declare explicit grants. A capability level alone does not make a tool available. Level 0 cannot use this prebuilt tool.

Follow the selected [observation and control permissions](../../../rules/Vision_rules.en.md), [grasp rules](../../../rules/rules_grasp.en.md) and [L3 read boundary](../../../rules/rules_privileged.en.md). Higher levels grant only declared inputs, not state writes, extra resets, new tools or online downloads. Candidates require normal action, collision and task validation. Preserve source/checkpoint identity and input provenance. Additional pretrained action policies remain prohibited.
