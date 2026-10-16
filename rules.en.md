<!-- bilingual-navigation:start -->
[English](rules.en.md) | [简体中文](rules.zh-CN.md) | [Original](rules.md) | [All documents](docs/README.en.md)
<!-- bilingual-navigation:end -->

Current catalog tasks use the [four-trial protocol](docs/evaluation_protocol.en.md) and cold-start attempts. Pass@2 applies only when explicitly declared for the experiment. Confirmed non-agent incidents are replaced under the [shared accounting rule](#non-agent-failures). The environment gateway does not meter model tokens or image reads.

<a id="section-1"></a>
# Shared Agent Rules

These rules apply to all evaluation profiles and agent models, including all evaluated models. Read this file, the selected level and its inherited profiles,
and the selected environment's task specification once; reread only changes.
`task.md` means the environment task specification, not a required root file.
[Environment documentation](docs/evaluation/index.en.md) indexes canonical
task contracts shared across robots. Robot-specific task files define the
control interface, declared mounting exceptions, and evaluator integration.

<a id="section-2"></a>
## Capability Level Profiles

The capability profiles are Level 0, Level 1, Level 2, and Level 3. Level 0
allows code and self-implemented algorithms; Level 1 explicitly adds prebuilt tools, and Levels 2/3
add the permissions listed below. Only an explicit higher-level grant overrides
a lower-level restriction. Common budgets and physical constraints always apply.
Capability profile version: `2026-10-09-environment-l0-l3`; record it as
`capability_profile_version`, separately from the unchanged budget version.

| Level | Added capability | Profile |
| --- | --- | --- |
| Level 0 | Code-enabled control; own algorithms allowed; no prebuilt domain or external vision tools | [rules_model_only.md](rules_model_only.en.md) |
| Level 1 | Vision, geometry, IK/planning, observation-derived proxy RL | [Vision_rules.md](Vision_rules.en.md) |
| Level 2 | Pretrained grasp/contact models | [rules_grasp.md](rules_grasp.en.md) |
| Level 3 | Privileged original-simulator read access and training | [rules_privileged.md](rules_privileged.en.md) |

Public task conditions are available at every capability level, including Level 0.
For Launcher, before the first action in each episode, the host must supply
that episode's configured spring stiffness as `variation_request.spring_stiffness`
with `variation_request.spring_stiffness_unit` set to `N/m`, and record
`task_metadata_version: public-spring-v1`. Standard four-trial values are
22, 24, 26, and 28 N/m; legacy uses its actual configured value (default 25 N/m).
This is declared task information, not a tool result or privileged-state access.
See the [four-trial protocol](docs/evaluation/marble.en.md). The model need
not infer stiffness from appearance or trial interactions. It must still choose
and execute robot actions under its selected profile; disclosure grants no
access to other hidden dynamics, object poses, or evaluator state.

<a id="non-agent-failures"></a>
<a id="section-3"></a>
## Non-agent failures and valid attempt accounting

Attempt-accounting addendum: `non-agent-exclusion-v1` (2026-10-15), recorded as `attempt_accounting_version` in evaluation metadata. It applies to every capability level and predeclared attempt limit, overriding older blanket statements that all errors consume attempts or that infrastructure incidents cannot be rerun. It does not change task conditions, native success criteria, permission versions or budget versions.

- **A failure or interruption confirmed by evidence not to have been caused by agent operations does not consume a valid attempt and is not scored as a task failure. Rerun the same condition without consuming the next valid opportunity.** Examples include host reboot/power loss, model-service failures or stream disconnections, and environment/dependency/simulator/evaluator defects not caused by the agent. An `invalid` label, error name or agent claim alone is insufficient. Keep unresolved causes under separate review until attribution determines whether the opportunity is consumed.
- Failures caused by the agent's actions, rule violations, control-code exceptions or voluntary abandonment still consume a valid attempt. Normal wall-clock expiration, simulation-time expiration or step-budget exhaustion without success also count as failures. A recoverable rejected action does not itself start another attempt; an attempt ultimately unsuccessful for an agent-caused reason counts as a failure.
- Give every physical launch a unique experiment ID. Preserve original logs, terminal flags, timestamps, error causes, attribution evidence, task/condition identities, source/runtime versions, and actual token/image/time usage. Mark excluded incidents with `attribution=non_agent`, `excluded=true` and `consumes_valid_opportunity=false`, linking the original and replacement experiments. Never delete or overwrite the original records or report consumed resources as zero.
- Use a new isolated environment and cold-start agent for the replacement, retaining the same task, condition, seed, perturbation, permissions and per-attempt budgets. Do not inherit memory, code artifacts or trajectories from the excluded attempt. Record repairs and their versions; changes to group-identity fields still require a separate group and report. Physical launches may exceed the valid-attempt limit, but valid opportunities may not increase; this does not bypass separately imposed total resource limits.
- Every scored experiment has only success or failure and links to its experiment record. Excluded incidents and pending replacements are separate audit/scheduling states, not a third task outcome. Keep the original condition denominator after replacements. The standard four-trial protocol does not retry valid failures; in a separately declared experiment allowing two valid opportunities per condition, non-agent incidents consume neither, the first success stops the condition, and two valid failures establish its failure.

<a id="section-4"></a>
## Attempt and model budgets

Declare the experiment's valid-attempt limit, token/image caps, wall-clock limit and resource accounting before evaluation. Do not increase them in response to failure. The task's native time and step limits remain binding. The standard protocol has one valid attempt per condition; a declared Pass@2 experiment permits at most two, stopping at the first success. Excluded infrastructure incidents consume no valid opportunity.

The experiment host meters all input tokens (including cached input) and output tokens across the agent and helpers. Preparation, tool calls and reporting are included. Record actual usage by unique request ID; missing usage is not zero. Resource usage from excluded incidents remains in the ledger.

<a id="section-5"></a>
## Images and observations

The experiment host declares and enforces image-read limits. Count each submitted image, frame, crop and repeated visual read across all helpers. Rendering or saving a frame alone is not an agent image read. Preserve camera calibration when resizing observations. An image budget never authorizes additional sensor fields or hidden simulator access.

<a id="section-6"></a>
## Attempt isolation

Each condition and valid retry starts a fresh environment and cold-start agent. Do not carry memory, code artifacts, solution trajectories or privileged diagnostics from other attempts. Within one attempt, the agent may retain its own permitted observations and actions. Non-agent incident replacements use the same condition and independent initialization, as specified above.

<a id="section-7"></a>
## Execution and Verification

- Use the declared action interface and physical robot contact. No teleporting,
  direct state writes, hidden grasp constraints, collision bypass, tunnelling,
  or exploitation of visible/collision geometry mismatch.
- Keep fixed scene, camera, lighting, geometry, initial state, physics, and
  evaluator settings unchanged unless the task explicitly declares a change
  as a legal action. Privileged read access never grants write access.
- Check finite values, robot limits, action rate, collision, goal residuals,
  and task legality before executing model/planner output. Reject invalid,
  timed-out, or non-converged results without relaxing constraints.
- The independent evaluator checks task violations, including penetration
  within the task's declared scope and tolerance, at each physics substep.
  A hard violation stops execution; preserve the first reason. Never modify
  or forge evaluator results. Task success requires both method compliance
  and independent evaluator success.
- For Level 0, the trusted environment performs mandatory validation and
  violation checks. Its fixed action decoder and native robot servos are
  infrastructure, not agent tools: they may not infer goals, solve IK, plan,
  repair actions, or switch to another controller. Invalid actions are rejected.
- Use event-driven checks at meaningful transitions or failures. Once the
  required checks pass, proceed; repeat only after a relevant change or new
  evidence. Store detailed evidence in files and report concise findings.

<a id="section-8"></a>
## Local Tool Policy and Documentation Index

Level 0 may execute code with its basic dependencies, but cannot call prebuilt domain or external vision tools. The allowlist below applies only to
Levels 1–3 at each listed minimum level; accounting for a tool in the shared
budgets does not authorize it. The evaluated model itself and the environment
observation/action transport are not auxiliary tools. Its declared frozen
weights and built-in vision encoder are part of the evaluated model.
Importing an additional pretrained or previously fine-tuned action-policy
checkpoint or controller is not authorized by any current profile.

During evaluation the agent must not use online search, browsing, GitHub or
package searches, downloads, remote inference, or remote planners to discover
or integrate tools. Use the locally pinned allowlist below. Missing tools or
checkpoints are capability gaps, not permission to substitute another model.
Before evaluation, maintainer-approved setup may prepare pinned source,
dependencies, and checkpoints. New tools require review of their role, data
access, license, immutable revision, and local smoke check, then an explicit
allowlist/documentation update. A model name alone grants no tool permission.

| Minimum level | Tools and documentation |
| --- | --- |
| 1 | [Depth Pro](docs/tools/depth-pro/README.en.md), [Depth Anything 3](docs/tools/depth-anything-3/README.en.md) |
| 1 | [Stream3D](docs/tools/stream3d/README.en.md) (SAM3D backend only), [SAM 3D Objects](docs/tools/sam-3d-objects/README.en.md) |
| 1 | [Pinocchio](docs/tools/pinocchio/README.en.md), [SciPy](docs/tools/scipy/README.en.md), [Pyroki](docs/tools/pyroki/README.en.md) |
| 1 | [cuRoboV2](docs/tools/curobo-v2/README.en.md) v0.8.0, [cuRobo v1](docs/tools/curobo-v1/README.en.md) v0.7.8 (legacy only), [OMPL](docs/tools/ompl/README.en.md) |
| 1 | [RSL-RL](docs/tools/rsl-rl/README.en.md) v5.0.1, [Optuna](docs/tools/optuna/README.en.md) v4.9.0 |
| 2 | [GraspNet Baseline](docs/tools/graspnet-baseline/README.en.md), [DexGraspNet 2.0](docs/tools/dexgraspnet2/README.en.md), [GenDexGrasp](docs/tools/gendexgrasp/README.en.md), [CEDex ContactGen](docs/tools/cedex-contactgen/README.en.md) |
| 2 | [MinkowskiEngine](docs/tools/minkowski-engine/README.en.md), only as the DexGraspNet sparse-convolution dependency |

Pinocchio/SciPy are the default retargeting path. Isolate Pyroki when JAX
conflicts with the main runtime. Keep cuRobo v1/v2 in separate environments;
use v2 for new integrations and log any legacy v1 fallback. OMPL requires
caller-provided limits, collision checking, and state conversion. Exact pins,
setup, and runtime caveats are in [the tool index](rules.en.md#section-8).

<a id="section-9"></a>
## Audit and Result

Save applicable evidence once and reference it by path: attempt/token/read ledger
(image source, dimensions, purpose, count), timestamped observations and
calibration, tool/code/checkpoint versions and hashes, preprocessing, input
provenance and units, raw outputs, decisions/rejections, planner configuration
and residuals, trajectories/commands, and required final image or video.
Keep evaluator logs separate and expose them only as the selected profile
and interface permit. Saving evidence does not require rereading every image.

Report `capability_level`, `method_profile`, `method_compliance`, independent
task result, evidence paths, and the first violation/reason, if any. Preserve
the task evaluator's existing output schema. No profile grants human
demonstrations, teleoperation, corrections, preferences, DAgger queries, or
handwritten expert training trajectories. A task-specific exception requires
explicit authorization and separate reporting; it must not be presented as
a standard capability-profile result.

<!-- environment-release-permissions -->
The environment release permits Level 0 code, basic image processing and self-implemented dynamics/IK/planning, but no prebuilt domain or external vision tools. This is a tool-availability distinction, not an algorithm prohibition. Model token/image budgets belong to separately executed experiment protocols, not environment-package certification. See [Level 0](rules_model_only.en.md).
