# SAM 3D Objects

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Tool policy](../../../rules.en.md#section-8)

Minimum capability level: **L1**. Reference revision: `f91db411c50efee93d8db7aeb323885650f6f722`. [Upstream source and installation documentation](https://github.com/facebookresearch/sam-3d-objects).

Reconstruct objects from legal RGB and inferred masks. Outputs are derived/proxy assets, never native ground truth. The upstream SAM License applies.

The pinned source is embedded at [`third_party/sam-3d-objects`](../../../third_party/sam-3d-objects). See the [snapshot inventory](../../../third_party/README.md). Prepare runtime dependencies and any separately required checkpoints before evaluation, under upstream terms, and declare explicit grants. A capability level alone does not make a tool available. Level 0 cannot use this prebuilt tool.

Follow the selected [observation and control permissions](../../../Vision_rules.en.md), [grasp rules](../../../rules_grasp.en.md) and [L3 read boundary](../../../rules_privileged.en.md). Higher levels grant only declared inputs, not state writes, extra resets, new tools or online downloads. Candidates require normal action, collision and task validation. Preserve source/checkpoint identity and input provenance. Additional pretrained action policies remain prohibited.
