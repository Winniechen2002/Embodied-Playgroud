[English](README.en.md) · [简体中文](README.zh-CN.md)

# EP evaluation subsets: paper definitions

This guide and four companion documents map EP-100, EP-20, EP-Easy and EP-Hard to Agent-bench environment IDs. They follow `paper-loaded-only-v1` They document definitions and membership, not model results.

## Paper names and implementation names

Use Embodied Playground as the display name; Agent-bench remains the repository name. This documentation mapping preserves directories, Python packages, Gym IDs, environment IDs and CLI names. Suite membership applies only to selected tasks.

| Paper family | EP suite | Runtime family | Full catalog | EP-100 |
| --- | --- | --- | ---: | ---: |
| Launcher | Launch | `marble` | 100 | 34 |
| Tower of Hanoi | Tower | `hanoi_panda`, `hanoi_sharpa`, `hanoi_floating` | 120 | 21 |
| Kongming lock | Lock | `kongming_lock` | 60 | 16 |
| Rubik’s cube / Pocket cube | Cube | `rubiks_panda`, `rubiks_sharpa`, `pocket_cube` | 80 | 12 |
| Bookshelf / ManiSkill | Home | `bookshelf`, `maniskill_long_horizon`, `maniskill_geometry`, `maniskill_dynamics` | 50 | 17 |

## Relationships

EP-100 selects 100 of the full 410 environments, covering five suites and 16 task types. EP-Easy and EP-Hard are disjoint 50-task partitions whose union is EP-100. EP-20 is a fixed subset with ten tasks from each split, not 20 additional environments or a train/test split.

A configuration paired with a different robot may be a different task. Paper indices such as `Tower-18` identify appendix entries; environment IDs such as `hanoi_sharpa/fr3-sharpa/H01` identify runtime tasks. Seeds, conditions and initialization modes do not add catalog tasks.

| Subset | Tasks | Launch | Tower | Lock | Cube | Home | Conditions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [EP-100](EP-100.en.md) | 100 | 34 | 21 | 16 | 12 | 17 | 400 |
| [EP-Easy](EP-Easy.en.md) | 50 | 17 | 11 | 8 | 6 | 8 | 200 |
| [EP-Hard](EP-Hard.en.md) | 50 | 17 | 10 | 8 | 6 | 9 | 200 |
| [EP-20](EP-20.en.md) | 20 | 6 | 4 | 3 | 3 | 4 | 80 |

Counts apply to one fixed evaluation setting: one group per task and four conditions per group. Pass@1 uses one valid attempt per condition; Pass@2, Pass@5 and Pass@10 allow at most 2, 5 and 10 respectively, stopping at first success. These reference limits must be declared before running. Condition counts are not actual execution counts.

## Selection and difficulty

EP-100 favors tasks accessible through the shared runtime, allocating most slots to parallel grippers and smaller samples from easier native configurations to each dexterous family, while retaining family-specific difficulty variation. Its 34 Launch tasks are selected from 80 atlas scenes with recorded full-task success. This does not establish success under every perturbation.

Easy/Hard assignments derive from task workload, independently of a particular model result. Rank tasks **within each type**: lower scores enter Easy and higher scores enter Hard. For odd-sized types, assign the median to the side with the closer neighboring score; resolve remaining allocation ties so each split has 50 tasks and suite counts differ by at most one. Equal workload scores are ordered by embodiment (parallel grippers first), then task ID. Scores rank tasks within types and are not a universal cross-suite scale.

| Suite | Workload score |
| --- | --- |
| Launch | 10 × native tier + loaded difficulty level D1–D5 + required target count |
| Tower | 2 × depth index + 1 for a physical theme + 2 for FR3–Sharpa / 3 for floating Sharpa (0 for Panda) |
| Lock | 0/2/4 for key/key-and-bar/full lock + 1 for hard pose + 0.5 for assembly + 2 for dual floating Sharpa |
| Cube | Scramble/transition length in quarter turns + 3 for a Sharpa embodiment |
| Home | Object count for Bookshelf; ordered milestone and final predicate count for ManiSkill |

The depth index maps 1, 3, 9 and 31 moves to 0, 1, 2 and 3. Cube quarter-turn length differs from scramble-token length: EP-20's Cube-06 (C11) has 14 quarter turns. Native difficulty (tier, D1, Hanoi L1), EP splits and access levels L0–L3 are separate dimensions; L1 in a ManiSkill task ID is also a task code.

The current loaded-only revision places **Launch-15 (A029) in Easy and Launch-17 (A055) in Hard**. Use the companion lists and `tasks.json` for exact membership.

## Shared evaluation setting

The protocol is `environment-four-trial-v2`; permission version is `2026-10-09-environment-l0-l3`. Standard base seed is 0. A group fixes the task, initialization, operation/observation profiles, access level, grants, budgets, protocol/implementation versions and agent version/code/instructions. Changes define a separate setting.

- **Launch is loaded-only**: the first projectile is preloaded; subsequent reloading remains part of multi-shot tasks. Ground initialization is excluded from all EP scores and Launch workload scores.
- Other families use default initialization. Each condition starts a fresh environment and agent session. Damage, ammunition consumption and state persist within an episode; initialization and reset belong to the evaluator.
- Launch uses spring stiffnesses 22/24/26/28 N/m and prescribed offsets/backgrounds. Hanoi and Pocket use consecutive seeds with bounded pose/physics/lighting changes; Bookshelf uses native layout sampling.
- Rubik, Lock and ManiSkill preserve authored physical layouts and use lighting multipliers 0.85/0.95/1.05/1.15. ManiSkill fixes `physics_variant=0`. These are not four different puzzles or four retries.
- Independent evaluators check goals, trajectory rules, physical validity and release/stability requirements within budget. Higher access levels preserve task rules.

See the [per-task protocol](../evaluation/index.en.md) and [condition schedule](../evaluation/tasks.json) for exact conditions and environment budgets. Filter their groups by the membership and initial modes here before computing EP results.

## Scoring

For a complete group, let z1…z4 indicate condition success:

```text
Task success rate S_task = (z1 + z2 + z3 + z4) / 4
All-four-success indicator A_task = z1 × z2 × z3 × z4
Suite rate S_suite = mean task rate within that subset's suite
Subset rate S = (S_Launch + S_Tower + S_Lock + S_Cube + S_Home) / 5
```

Each suite has **20%** weight. Pooled successful conditions divided by all conditions do not give the paper's headline score. Aggregate all-four indicators through the same task/suite/subset hierarchy; they differ from mean condition success.

Pass@K (K = 1, 2, 5 or 10) uses any success among the first K valid attempts in chronological order on the same condition. Pass@5 and Pass@10 are additional playground reference limits. Report each requested cutoff separately from the same ordered records; never infer it from Pass@1 probability. A condition is complete at cutoff K only after success within its first K valid attempts or K valid failures; otherwise that cutoff remains partial. Stop after first success and keep all attempts isolated with identical conditions and per-attempt budgets. Every condition retains one quarter of its task's denominator. In the paper's experimental extension, ordinary agent failures and budget exhaustion (including wall-clock timeout) consume an opportunity; confirmed infrastructure incidents do not. Preserve all records and exclusion evidence.

Groups with invalid or missing conditions remain partial. Retain the planned denominator, observed-success lower bound, completed coverage and invalid/missing counts; final metrics remain undefined. Report access settings, grants and attempt budgets separately. Time@S averages wall time to success over successful attempts; Tok@S averages their input (including cached input) plus output tokens. Missing usage is not zero.

## Scope relative to existing repository protocols

The [general protocol](../evaluation_protocol.en.md) includes loaded and ground: all 410 tasks yield 510 groups and 2040 conditions. The paper's loaded-only full collection yields 410 groups and 1640 conditions. EP-100 yields 100 groups and 400 conditions. These counts have different scopes.

The paper's base protocol lists wall-clock expiration, rejected actions and agent exceptions as invalid and disallows replacing completed failures or invalid attempts. Its experiments separately define a cause-audited Pass@1/Pass@2 extension. The repository's existing protocol also uses cause-audited exception accounting. Declare the selected interpretation when reproducing results; a raw termination label alone cannot determine opportunity consumption. These documents do not modify the existing protocol or runtime.

## Definition index

[tasks.json](tasks.json) records exact task IDs, subset membership and the `paper-loaded-only-v1` definition. The selection derives from `agentbench-curated-v2`, original index `1.4`, at environment revision `a58a288`.

The index contains 100 EP-100 tasks and disjoint 50-task Easy/Hard partitions. EP-20 contains ten tasks from each partition. It is a documentation membership index, not a campaign runner configuration. Keep both languages and the index synchronized when changing definitions.
