<!-- bilingual-navigation:start -->
[English](rules_grasp.en.md) | [简体中文](rules_grasp.zh-CN.md) | [Original](rules_grasp.md) | [All documents](docs/README.en.md)
<!-- bilingual-navigation:end -->

Current catalog tasks use cold-start attempts with no cross-attempt memory or trajectory reuse. Follow the [shared rules](rules.en.md) and the declared experiment’s attempt and resource budgets.

<a id="section-1"></a>
# Level 2: Grasp-Model Agent Rules

Apply [shared rules](rules.en.md) and [Level 1](Vision_rules.en.md), including the experiment’s declared budgets and cold-start requirement.
Level 2 additionally grants pretrained grasp-generation models.
Method profile: `grasp_model`; inherits `vision_geometry_proxy_rl`.

Use the selected environment's `task.md` and its shared task contract, indexed
in [environment documentation](docs/evaluation/index.en.md). Task legality,
scoring, and budgets are shared across robots performing the same task;
robot-specific interfaces and evaluator support are documented separately.

Attempts remain isolated under the shared rule.
Apply the [shared attempt-isolation rule](rules.en.md#section-6).

<a id="section-2"></a>
## Added Capability

Only the pinned Level 2 tools in the [shared allowlist](rules.en.md#section-8)
may generate/rank/refine grasps or contacts: GraspNet Baseline, DexGraspNet 2.0,
GenDexGrasp, and CEDex ContactGen. MinkowskiEngine is allowed only as the
DexGraspNet sparse-convolution dependency. Generic checkpoints for these
models and independent fine-tuning are allowed.

Use legal RGB or Level 1 derived depth, masks, point clouds, and geometry.
Candidates may feed reachability/collision/task filters, grasp optimization,
IK, planning, closed-loop control, or proxy actions/initializations/rewards.
Model proposals remain subject to all physical and task constraints.
AnyGrasp, Contact-GraspNet, remote APIs, and other unlisted models are not granted.

<a id="section-3"></a>
## Unchanged Boundaries

No privileged original-simulator state, native annotations, contacts, reward,
evaluator feedback, or training/optimization against those inputs is allowed.
Extra original-simulator resets or additional episodes are not granted.
Prior scene data or trajectories may not initialize or tune the proxy across attempts. Importing an additional pretrained or
previously fine-tuned action-policy checkpoint/controller is not permitted;
from-scratch proxy training within the allowed run remains allowed. The evaluated
model itself may retain its declared frozen pretrained weights. Human demonstrations/corrections are not granted.

<a id="section-4"></a>
## Additional Evidence

Save grasp model/checkpoint/revision, preprocessing, input provenance, raw
candidates/scores, selection/rejection reasons, final commanded grasp, and
fine-tuning data/configuration. Shared audits cover trajectories, proxy
provenance, and the private evaluator's per-step penetration records, including
the first violating pair, depth, and trajectory label.

<!-- environment-release-permissions -->
The environment release permits Level 0 code, basic image processing and self-implemented dynamics/IK/planning, but no prebuilt domain or external vision tools. This is a tool-availability distinction, not an algorithm prohibition. Model token/image budgets belong to separately executed experiment protocols, not environment-package certification. See [Level 0](rules_model_only.en.md).
