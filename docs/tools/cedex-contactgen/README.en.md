# CEDex ContactGen

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Tool policy](../../../rules/rules.en.md#section-8)

Minimum capability level: **L2**. Reference revision: `ef59a9fb`. [Upstream source and installation documentation](https://github.com/GeorgeWuzy/CEDex-Grasp).

Generate five-finger semantic contact candidates. Retarget to the target hand and validate IK, joint limits, collisions and task rules.

The pinned source is embedded at [`third_party/CEDex-Grasp`](../../../third_party/CEDex-Grasp). See the [snapshot inventory](../../../third_party/README.md). Prepare runtime dependencies and any separately required checkpoints before evaluation, under upstream terms, and declare explicit grants. A capability level alone does not make a tool available. Level 0 cannot use this prebuilt tool.

Follow the selected [observation and control permissions](../../../rules/Vision_rules.en.md), [grasp rules](../../../rules/rules_grasp.en.md) and [L3 read boundary](../../../rules/rules_privileged.en.md). Higher levels grant only declared inputs, not state writes, extra resets, new tools or online downloads. Candidates require normal action, collision and task validation. Preserve source/checkpoint identity and input provenance. Additional pretrained action policies remain prohibited.
