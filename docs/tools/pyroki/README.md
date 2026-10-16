# Pyroki

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Tool policy](../../../rules.en.md#section-8)

Minimum capability level: **L1**. Reference revision: `388e43e1`. [Upstream source and installation documentation](https://github.com/chungmin99/pyroki).

JAX-based IK and retargeting. Isolate dependencies from Isaac/PyTorch and pin transitive source dependencies before evaluation.

The pinned source is embedded at [`third_party/pyroki`](../../../third_party/pyroki). See the [snapshot inventory](../../../third_party/README.md). Prepare runtime dependencies and any separately required checkpoints before evaluation, under upstream terms, and declare explicit grants. A capability level alone does not make a tool available. Level 0 cannot use this prebuilt tool.

Follow the selected [observation and control permissions](../../../Vision_rules.en.md), [grasp rules](../../../rules_grasp.en.md) and [L3 read boundary](../../../rules_privileged.en.md). Higher levels grant only declared inputs, not state writes, extra resets, new tools or online downloads. Candidates require normal action, collision and task validation. Preserve source/checkpoint identity and input provenance. Additional pretrained action policies remain prohibited.
