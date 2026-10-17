<!-- bilingual-navigation:start -->
[English](Vision_rules.en.md) | [简体中文](Vision_rules.zh-CN.md) | [Original](Vision_rules.md) | [All documents](../docs/README.en.md)
<!-- bilingual-navigation:end -->

<a id="section-1"></a>
# Level 1: Vision, Geometry, and Proxy RL

Apply [shared rules](rules.en.md), including the experiment’s declared budgets, and the selected
environment's task specification. Level 1 explicitly adds prebuilt domain and vision tools to the code-enabled Level 0 baseline; see
[rules_model_only.md](rules_model_only.en.md) for that baseline. Level 1 permits vision-derived geometry,
IK, retargeting, planning, feedback control, and observation-derived proxy
RL/optimization. Method profile: `vision_geometry_proxy_rl`.

Attempts remain isolated under the shared rule.
Apply the [shared attempt-isolation rule](rules.en.md#section-6).

<a id="section-2"></a>
## Allowed Inputs and Trust Boundary

The agent, helpers, and external models may use declared camera RGB,
intrinsics/extrinsics, robot model and joint limits, joint position/velocity,
symbolic task/target and ordinal object sizes, current-episode action history,
permitted current-attempt trajectories, and estimates
derived from these inputs.

The Launcher spring stiffness disclosed by the host for the current episode
is an explicit public task parameter, available to Levels 0–3. It may be used
for reasoning, control, and Level 1/2 proxy initialization without estimating it
from RGB. This narrow exception to hidden-dynamics restrictions does not expose
other simulator parameters or scene geometry; see the [four-trial protocol](../docs/evaluation/marble.en.md).

Native depth, masks, segmentation, IDs, point clouds, flow, normals, boxes,
and contacts are privileged unless explicitly declared as rendered sensor
observations. Both Hanoi Vision interfaces expose one `policy` group:
`rgb`, `joint_pos`, `joint_vel`, `actions`. See the environment IDs in
[Franka](../docs/evaluation/hanoi_panda.en.md) and
[Floating Sharpa](../docs/evaluation/hanoi_floating.en.md).
A bare environment is not the independent scored evaluator.

Do not read simulator object/gripper world poses, hidden dynamics, contacts, physics
tensors beyond allowed proprioception, USD/scene graph, object handles, reset
seeds/origins, task-object assets/generators, or private evaluator state.
Public or memorized task dimensions, nominal coordinates, stack heights,
and seed-specific priors are forbidden substitutes for perception. Current-attempt trajectory reuse does not authorize other-episode data or hidden scene geometry. Passing
forbidden information through files,
images, prompts, caches, or helper processes does not make them allowed.

The evaluator privately monitors every physics substep and determines success.
During execution it may stop a failed run, but must not expose privileged
classifications, reasons, or snapshots. Post-episode disclosure does not
authorize reusing privileged information in later Level 1/2 attempts.

<a id="section-3"></a>
## Perception and Control

Use only Level 1 tools in the [shared allowlist](rules.en.md#section-8).
Depth Pro, Depth Anything 3, Stream3D with SAM3D, and SAM 3D Objects are the
approved perception/reconstruction models. TRELLIS.2 implementations,
TRELLIS.2 checkpoints, and the TRELLIS runner scripts are forbidden, as are
unlisted learned vision models and remote perception services.

Scene geometry for grasping, avoidance and placement must derive from declared
legal observations. The Level 0 basic-computation and self-authored algorithm
permissions remain available. Explicitly granted external perception models are
optional additional tools, not a prerequisite for implementing an algorithm.
Robot kinematics and sensor calibration may transform observation-derived estimates;
hidden simulator state and seed-specific fitted priors remain unavailable.

Ground each manipulation in current observations; generate, reuse, or adapt a
trajectory and apply the required validation. Compatible reused segments do
not require reconstructing their targets from scratch. Execute through the
action interface and observe after each move to verify release/seating before
the next move. Observe during execution
when tracking uncertainty requires it; reuse cached estimates otherwise.
Apply the shared image budget to all agent visual inspections.

<a id="section-4"></a>
## Reconstructed Proxy and Learning

Levels 1/2 may build a new proxy simulation from observations collected in the
current evaluation episode. It may expose complete proxy object state, contacts,
dynamics, and a custom proxy reward to RSL-RL/Optuna for training,
reward/trajectory optimization, and model selection. Policies may start from
scratch within the allowed run; importing an additional pretrained or previously
fine-tuned action-policy checkpoint/controller is not permitted. This restriction
does not prohibit the declared frozen weights of the evaluated model itself.

Every proxy asset/parameter must trace to legal frames, calibration, robot
model, symbolic task, explicitly public current-episode task parameters, or
allowlisted model output. Never initialize or correct
it from original-simulator assets, dimensions, hidden state, contacts, original
reward, evaluator diagnostics, reset seeds, or previous-episode scene data.
Reusable trajectories may be tested as candidate actions in the current proxy;
they do not supply its scene geometry or privileged training labels.
Original-simulator success/failure is not an available optimization objective.

Deploy through an observation adapter that removes all proxy-only state.
Use later legal RGB, proprioception, and the agent's own action history from
the same episode to update the proxy. This grants no additional original-
simulator episodes or resets. Label assets and logs `derived/proxy`; record
source provenance, rewards, training/trial configuration, seeds, results,
checkpoints, and deployment observation schema separately from evaluator logs.

<a id="section-5"></a>
## Hard Hanoi Rules

Apply the canonical [Hanoi task](../docs/evaluation/hanoi_panda.en.md) to both Franka and No-arm
Sharpa. It defines legal moves, shared budgets, seating/penetration tolerances,
substep failure handling, and exact target matching. Robot-specific task files
define interfaces and evaluator availability. These scoring criteria do not
grant privileged measurements to Level 1/2 agents; a visual estimate alone
cannot establish success.

<a id="section-6"></a>
## Evidence and Results

Save shared audit evidence, lossless model geometry outputs, derived masks/
depth/point clouds, pose/grasp estimates and uncertainty, and proxy provenance.
Preserve Hanoi output fields: `status`, `success_tolerance_met`,
`vision_only_compliance`, `hanoi_rule_result` (status/reason/violating_ring/
state_snapshot), and `visual_evidence` (video/observation_log/trajectory_log).

Physical failure may still be vision-compliant but fails the task; record
`HanoiRuleViolation` and its stage. Forbidden privileged access sets
`vision_only_compliance: false` and `PrivilegedObservationViolation`.
Preserve the first violation and disclose private terminal state only after
execution ends. Overall success requires method compliance and task success.

<!-- environment-release-permissions -->
The environment release permits Level 0 code, basic image processing and self-implemented dynamics/IK/planning, but no prebuilt domain or external vision tools. This is a tool-availability distinction, not an algorithm prohibition. Model token/image budgets belong to separately executed experiment protocols, not environment-package certification. See [Level 0](rules_model_only.en.md).
