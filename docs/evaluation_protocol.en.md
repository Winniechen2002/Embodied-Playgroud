<!-- bilingual-navigation:start -->
[English](evaluation_protocol.en.md) | [简体中文](evaluation_protocol.zh-CN.md) | [Original](evaluation_protocol.md) | [All documents](README.en.md)
<!-- bilingual-navigation:end -->

<a id="section-1"></a>
# Evaluation protocol for all 410 environments

<!-- paper-evaluation-scope:start -->
Embodied Playground contains 410 tasks. The paper evaluates Launcher in loaded mode only: 410 groups / 1640 conditions for the full catalog; EP-100, EP-Easy, EP-Hard and EP-20 contain 100/50/50/20 tasks and 400/200/200/80 conditions. Each task has four conditions, with equal weighting across five suites. See [paper subset definitions](ep_subsets/README.en.md). The runtime also supports ground; its general engineering schedule retains 510 groups / 2040 conditions, which is not the paper denominator.
<!-- paper-evaluation-scope:end -->


[English](evaluation_protocol.en.md) · [简体中文](evaluation_protocol.zh-CN.md) · [Per-task conditions](evaluation/index.en.md) · [Environment engineering checks](environment_validation.en.md)

Protocol version: `environment-four-trial-v2`. Permission version: `2026-10-09-environment-l0-l3`. This document specifies future episode evaluation; it contains no model results. Distribution packaging and public release remain deferred.

<a id="section-2"></a>
## Task identity and number of tests

Every task requires **4 independent valid condition outcomes per group**, registered before execution. All four conditions count; never select the best trial or replace a valid failure. Under the [shared incident-accounting rule](#non-agent-failures), evidence-confirmed non-agent incidents are unscored, consume no valid attempt, and are replaced for the same condition; physical launches may therefore exceed four. The stable catalog has 410 tasks. Initial modes, seeds, observation profiles and permission levels do not create additional catalog tasks.

A group fixes `(task_id, protocol_version, base_seed, initial_mode, operation_profile, observation_profile, capability_level, permission_version, tool_grants, budgets, implementation_revision)`. Fix any evaluated agent's code/version and instructions too. A changed field creates a separate group; do not pool groups or reuse private state across them. Use base seed 0 for the standard schedule; other base seeds are additional, separately named groups. The accepted base-seed range is 0..2147483644.

Launcher has a loaded group and a ground group, each with four episodes. The other 310 tasks each have one default group. Thus one base seed and one fixed access/observation combination produce **510 groups and 2040 planned episodes**: 800 Launcher episodes and 1240 other episodes. The paper explicitly evaluates the loaded-only subset; 510 groups here describes the runtime engineering schedule across both modes. Testing all four permission levels separately would plan 8160 episodes. These counts are plans, not completed runs.

<a id="section-3"></a>
## Randomization and fixed perturbations

The consistency requirement is the four-episode accounting and isolation contract, not copying launcher parameters to unrelated robots. Every entry in the [machine-readable schedule](evaluation/tasks.json) lists four exact reset seeds, configuration parameters and budgets. Its values are maintainer configuration; do not attach the whole manifest to a client prompt.

| Family | Four-trial mapping | Preserved conditions |
| --- | --- | --- |
| Launcher, 100 | Original `four-trial-v1`: same base reset seed in all four episodes; spring 22/24/26/28 N/m, registered launcher/ammunition offsets, deterministic scene-name SHA-256 theme cycle, static/static/drift/pulse backgrounds | Authored targets, structures, order, protected objects, yaw configuration; loaded and ground are separate groups |
| Hanoi, 120 | Existing `train` sampler with reset seeds `base_seed + 0/1/2/3`; signed uniform board XY displacement up to 0.004 m, yaw up to 2 degrees, mass factor 0.90–1.10, friction factor 0.92–1.08, light intensity 700–1100 | Same ring start/goal assignments, dimensions, robot, obstacles and legal-move rules |
| Pocket cube, 20 | Existing `train` sampler with seeds `base_seed + 0/1/2/3`; XY displacement up to 0.003 m, yaw up to 2 degrees, relative mass factor 0.94–1.06, relative friction factor 0.95–1.05, light intensity 750–1050 | Authored mass/friction multipliers, start/goal corner state, required quarter-turn count and embodiment |
| Rubik cube, 60 | Same base seed and fixed public case; authored sky-light intensity multiplied by 0.85/0.95/1.05/1.15 | Scramble, logical orientation, initial pose, physical parameters, fixture and target |
| Kongming lock, 60 | Same base seed and fixed public case; authored sky-light intensity multiplied by 0.85/0.95/1.05/1.15 | Piece identities, initial/goal poses, task subset, support relationships and physics |
| Bookshelf, 20 | Native reset sampler with seeds `base_seed + 0/1/2/3`; variant-specific object positions, orientations, crate contents and permitted misplaced-object assignments | Variant object set, required destination, wall requirement, geometry, score tolerances and time limit |

Hanoi uses `random.Random("hanoi40-v1:{task_id}:{split}:{seed}")`; pocket cube seeds `random.Random` with the big-endian first 8 SHA-256 bytes of `cube20-v1/{task_id}/{split}/{seed}`. Their actual sampled parameters are exported, not just a range description. Bookshelf uses its native tensor sampler and collision/rejection constraints; record the realized post-settling state privately. Different seeds do not guarantee every object's pose differs.

Rubik and Kongming use **four fixed visual perturbations**, not randomized puzzles or physical-layout robustness tests. Changing the seed alone would not change their fixed case layouts. Lighting factors are applied before scene construction, not as client tools or mid-episode changes. The four light factors and bird perturbations are prescribed design values, not samples from a real-world distribution. Do not claim broad generalization from these four conditions. Nominal and heldout engineering matrices remain separate from this registered evaluation; this protocol's use of the existing `train` range does not make it a heldout benchmark.

<a id="non-agent-failures"></a>
<a id="section-4"></a>
## Episode budgets and scoring

| Family | Physics / control Hz | Maximum controls | Simulated time | External wall-clock limit |
| --- | --- | --- | --- | --- |
| Launcher | 1000 / 50 | 7500 | 150 s | 600 s |
| Hanoi | 120 / 30 | 18000 | 600 s | 3600 s |
| Pocket cube | 240 / 60 | 18000 | 300 s | 3600 s |
| Rubik cube | 120 / 30 | 109800 | 3660 s | 19800 s |
| Kongming lock | 120 / 30 | 36000 | 1200 s | 3600 s |
| Bookshelf | 120 / 30 | 30 × variant seconds | 50–410 s, exact value per task | 3600 s |

The gateway CLI fixes these budgets for registered trials. Wall time includes startup and initialization; the unified entry point enforces it with an external process supervisor. Normal expiration counts as a valid failure; retain raw runtime labels separately rather than treating them as automatic exclusions. Runtime polling is only cooperative and cannot interrupt a stuck simulator call. A protocol manifest or a launched gateway is not a batch evaluator or proof that a hard wall deadline was enforced. Tokens/images are not environment certification gates; any future agent comparison must additionally freeze and disclose its own identical resource budgets.

Use each task's trusted scorer and full task contract. Launcher requires all necessary targets, configured fracture/toppling/order/damage-path requirements and protection; protection scenes wait at least 3 s after the last necessary target hit. Hanoi requires the exact goal, legal moves, seating/physics validity and 1 s continuous stability. Pocket cube requires the exact goal, exact committed quarter-turn count, detents within 1 degree, no active layer, angular speed below 0.05 rad/s, unchanged scene fingerprint and 1 s stability. Rubik requires a solved native cube, legal fixture actions, release/return/support and a fresh 0.5 s stable window. Kongming requires the case-specific goal and release, 2 s assembly or 1 s disassembly stability, with complete substep audit coverage. Bookshelf requires every layout rule and 0.5 s continuous valid placement. Family documents link the numeric scoring implementation and geometry-specific constraints.

A previously latched physical violation denies success even if the final layout looks correct. Stability must be earned before the time budget is exhausted; merely reaching a target at the last instant is insufficient. Normal wall-clock expiration, simulation-time or step-budget exhaustion, object loss, physical violations, agent-caused exceptions and voluntary finish without success are valid failures. Audit initialization/environment/evaluator/model-service incidents by cause: only evidence-confirmed failures or interruptions not caused by agent operations are excluded without consuming an opportunity and replaced. A recoverable action rejection does not automatically end an episode. Unstarted conditions, pending replacements and unresolved attribution are scheduling/audit states, not fabricated success or failure. Record `attempt_accounting_version: non-agent-exclusion-v1`, retaining original terminal flags, first failure and incident evidence. Neither a raw `invalid` label nor an image or action acknowledgment establishes exclusion or success.

<a id="section-5"></a>
## Isolation, permissions and reporting

Create a fresh environment and fresh client/agent session for every trial. Only the maintainer initializes and resets. Within an episode preserve all damage, spent ammunition, state and memory; no reset or reseed is exposed. Between episodes clear agent memory, workspace and caches; constrain and document any external persistent services. Fix code and parameters before all four trials. Do not tune from earlier private outcomes. Resume unstarted conditions and conditions with audited non-agent exclusions; this does not authorize retrying completed valid failures. Each replacement gets a new experiment record linked to the original, with identical conditions and per-attempt budgets. Record repair versions; group-identity changes still require a separate group, never overwriting historical records.

L0 permits standard Python, NumPy, Pillow and self-written algorithms, but no prebuilt domain tools or external vision/grasp models. L1/L2 tools require both explicit authorization and actual installation; L3 only adds declared privileged read access. Observation profiles and native action units remain family-specific. Reads do not advance physical time; duplicate request IDs replay the original operation; termination prevents further stepping. The gateway does not prove arbitrary external Python-library compliance.

Retain private per-episode records: task/group identity, trial index, requested parameters, actual initial state and runtime configuration, source/asset hashes, runtime versions, budgets, permission profile, terminal reason, first violation, elapsed simulated/wall time and actual step counts. Detailed scorer diagnostics and hidden-state snapshots stay private. Only declared public observations, task conditions (including bird spring stiffness) and filtered final results reach clients. Predictable trial mappings are not a secure blind test.

A complete group has a valid terminal outcome for each of four conditions. Its metric is `successful episodes / 4`; `all_four_success` is true only for four successes. While any condition lacks a valid outcome, group status is `partial`, final `success_rate = null` and `all_four_success = null`; this is completion metadata, not a third experiment outcome. Keep `observed_successes`, pending condition indices and the labeled lower bound `observed_successes / 4`. List excluded non-agent incidents separately, outside failures and scored-attempt denominators; after replacement, historical exclusions do not keep a completed group partial. Never shrink the four-condition denominator or select only the best trial. Separately declared multiple-opportunity experiments report their own condition aggregation, not the standard single-attempt four-trial score. Environment QA reports remain separate and contain no model success-rate fields.

<a id="section-6"></a>
## Generate and run

From the repository root, with the appropriate MuJoCo or Isaac interpreter and dependencies:

```bash
python scripts/export_evaluation_protocol.py --check
python scripts/export_evaluation_protocol.py --base-seed 7 --output /tmp/evaluation-seed7
python scripts/environment_runtime.py --task-id hanoi_panda/panda/H01 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --headless --output /tmp/hanoi-trial1
python scripts/environment_client.py /tmp/hanoi-trial1/session.json
```

The example client performs a finite safe interaction and finishes; it is not a solver. Run trial indices 1, 2, 3, 4 in independent processes and new output directories. Select `--initial-mode loaded` and `--initial-mode ground` separately for birds. Registered trials reject custom split, spring, control-budget or wall-budget overrides. Omitting `--evaluation-protocol` retains the engineering single-instance interface and must not be labeled a registered four-trial result.

The checked-in schedule is generated from task authoring sources and the versioned sampler. `--check` detects stale generated content and source hashes. No generated configuration, documentation check or smoke test is evidence of a completed four-trial task evaluation. Full physics qualification of the new condition schedule is still a separate engineering requirement.


<a id="section-7"></a>
## Exact protocol for the added families

Dual Floating Sharpa Kongming uses the same 30 cases, four light scales and 1200 s / 36000 control steps / 3600 s wall budget as dual Panda, retaining 56 native actions and measured finger release/palm retreat conditions.

Each ManiSkill task uses the same base seed in four episodes, fixed authored layout and `physics_variant=0`. Ambient light and both directional lights are multiplied by 0.85, 0.95, 1.05, 1.15 without changing color ratios. Task codes L1–L10 are not access Level 1. Five robot embodiments retain their native controllers, 240 Hz physics, 20 Hz control and 1 s successful dwell. Long-horizon budgets are 6000 steps / 300 s; geometry and dynamics budgets are 2400 steps / 120 s; all have a 3600 s wall budget. Authored dynamics deadlines of 5–20 s remain separate; the one-second dwell must finish before the task deadline.

Each base seed and fixed access/observation combination has 510 groups and 2040 episodes: 800 birds and 1240 other episodes. Four levels separately imply 8160 planned episodes. Engineering base seeds 0, 1, 2 include 6120 formal protocol memberships. Extra physics variants never enter formal statistics.

The unified entry point uses an external process supervisor for the hard wall deadline, including simulator initialization. Normal wall timeout is a valid failure and grants no extra opportunity; only audited non-agent faults are excluded and replaced under the shared rule. Native Gym development access is not the controlled benchmark interface. Legacy v1 invocations are limited to the original 350 tasks; historical evidence retains its version.
