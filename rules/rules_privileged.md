<!-- bilingual-navigation:start -->
[English](rules_privileged.en.md) | [简体中文](rules_privileged.zh-CN.md) | [Original](rules_privileged.md) | [All documents](../docs/README.en.md)
<!-- bilingual-navigation:end -->

Current catalog tasks use cold-start attempts with no cross-attempt memory or trajectory reuse. Follow the [shared rules](rules.en.md) and the declared experiment’s attempt and resource budgets.

<a id="section-1"></a>
# Level 3: Privileged Original-Simulator Agent Rules

Apply [shared rules](rules.en.md) and [Level 2](rules_grasp.en.md), including the experiment’s declared budgets and cold-start requirement.
Level 3 adds read access to privileged fields explicitly exposed by the selected interface.
Method profile: `privileged_original_simulator`; inherits Level 1/2 capabilities.

Attempts remain isolated under the shared rule.
Apply the [shared attempt-isolation rule](rules.en.md#section-6).

<a id="section-2"></a>
## Added Read and Training Capability

Allowed information includes object/robot poses and dynamics; native sensor
buffers and annotations; contacts, penetration, constraints, physics tensors;
USD/scene graph, geometry/materials, task dimensions, reset/randomization state;
reward/termination fields; evaluator classifications/metrics/diagnostics; and
simulator-generated rollouts/labels within the declared task budget.

These inputs may guide estimation, grasping, planning, control, reward design,
training/optimization, validation, domain randomization, selection, and recovery.
A separate reconstructed proxy is optional. This permission supersedes the
Level 1/2 data restrictions only; it grants no extra episodes, resets, task
instances, compute, or time. Use only data exposed by the selected interface;
do not bypass an interface that keeps evaluator state private.

Any privileged input used in a model, reward, plan, filter, training example,
or selection decision requires the run to be labelled Level 3.

<a id="section-3"></a>
## Read Access Is Not Write Access

All shared physical/action constraints remain binding. No direct simulator,
robot/object, scene, reward/termination, or evaluator edits are allowed unless
the task explicitly declares them as legal actions. Never suppress violations,
forge results, or bypass the independent evaluator.

Level 3 may train a policy from scratch and adapt it during the allowed run.
Importing an additional pretrained or previously fine-tuned action-policy
checkpoint/controller is not permitted. The evaluated model itself may retain
its declared frozen pretrained weights. Perception/grasp priors still use the Level 1/2 allowlists;
privileged access does not authorize new tools or network access.

<a id="section-4"></a>
## Additional Evidence

Record each privileged field, source/API, timestamp, frame/units, downstream
consumer, and decisions that used it. Include exposed reward/termination and
evaluator fields, training/optimization configuration and results, and original-
simulator rollout/reset counts against the task budget. Keep executed commands
and private evaluator results separate. Report `privileged_access: "read"`.

<!-- environment-release-permissions -->
The environment release permits Level 0 code, basic image processing and self-implemented dynamics/IK/planning, but no prebuilt domain or external vision tools. This is a tool-availability distinction, not an algorithm prohibition. Model token/image budgets belong to separately executed experiment protocols, not environment-package certification. See [Level 0](rules_model_only.en.md).
