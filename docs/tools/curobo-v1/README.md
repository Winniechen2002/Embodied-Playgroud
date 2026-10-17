# cuRobo v1

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Tool policy](../../../rules/rules.en.md#section-8)

Minimum capability level: **L1**. Reference revision: `v0.7.8 / d64c4b00`. [Upstream source and installation documentation](https://github.com/NVlabs/curobo).

Legacy compatibility only. New integrations use v2. Do not silently fall back from v2 or install both packages in one environment.

The pinned source is embedded at [`third_party/curobo-v1`](../../../third_party/curobo-v1). See the [snapshot inventory](../../../third_party/README.md). Prepare runtime dependencies and any separately required checkpoints before evaluation, under upstream terms, and declare explicit grants. A capability level alone does not make a tool available. Level 0 cannot use this prebuilt tool.

Follow the selected [observation and control permissions](../../../rules/Vision_rules.en.md), [grasp rules](../../../rules/rules_grasp.en.md) and [L3 read boundary](../../../rules/rules_privileged.en.md). Higher levels grant only declared inputs, not state writes, extra resets, new tools or online downloads. Candidates require normal action, collision and task validation. Preserve source/checkpoint identity and input provenance. Additional pretrained action policies remain prohibited.
