# Agent instructions

[简体中文](Agent.zh-CN.md) · [Human quick start](README.md) · [Rules](rules/rules.en.md)

Use this guide when asked to test an agent on EP-20, EP-100, EP-Easy, EP-Hard, Full test or one exact environment task ID at L0–L3. Run the requested evaluation and report measured results. A successful installation, smoke check or generated plan is not an agent score.

## Separate the evaluator from the tested agent

The **evaluation host** selects conditions, starts environments, creates fresh agent sessions, enforces limits and collects results. A coding agent may organize this work, but it must run the tested policy in separate sessions with only the authorized inputs.

The **tested agent** receives its task through `describe()`, observations through the SDK, and the rules for its level. It controls the environment only through the public interface. Do not give it the repository checkout, private run directory, condition manifests, scorer internals or past attempts. The host should supply the relevant rules and interaction instructions, rather than the host-only setup and scheduling sections below. L3 exposes declared privileged fields through the gateway; it does not grant arbitrary filesystem access.

If the same model organizes and takes the test, keep the organizer's conversation, workspace and private information out of the tested sessions. The gateway alone does not isolate an external agent's filesystem or enforce model token limits; the host must provide those boundaries.

## Fix the requested setting — host only

Read the user's prompt and record:

- Scope: `EP-20`, `EP-100`, `EP-Easy`, `EP-Hard`, `Full test` or one exact `task_id`.
- Capability level: `L0`, `L1`, `L2` or `L3`.
- Attempt policy: default `Pass@1`; reference limits are `Pass@2`, `Pass@5` and `Pass@10`. Fix the maximum K and the requested reporting cutoffs before running.
- Agent/model version, instructions, inference settings and any token/image budgets.
- Observation profile, explicit tool grants and prepared tool setup manifests.
- Repository revision, runtime versions and a new output directory outside the repository.

Do not confuse an Easy/Hard split with an access level. Use the user's chosen scope and level; if either is missing, resolve it before starting scored runs. When no tools are granted, record an empty tool list. Do not silently change the level, install new tools during an episode, or claim that all tools permitted by a level were tested.

Read the [shared rules](rules/rules.en.md) and the level-specific document:

| Level | Rule document | Observation choice |
| --- | --- | --- |
| L0 | [Code-only rules](rules/rules_model_only.en.md) | `rgb` |
| L1 | [Vision and planning](rules/Vision_rules.en.md) | `rgb`, or supported and explicitly selected `rgbd` |
| L2 | [Grasp/contact tools](rules/rules_grasp.en.md) | `rgb`, or supported and explicitly selected `rgbd` |
| L3 | [Privileged read access](rules/rules_privileged.en.md) | `privileged`, or a declared restricted profile |

Launcher exposes RGB, not RGB-D. Higher levels inherit earlier permissions, but tools still require explicit grants and a working installation. See [embedded tools](docs/embedded_tools.en.md) for setup. Extra pretrained action policies, direct simulator writes and scoring changes remain prohibited.

## Prepare the run — host only

Follow the [installation guide](docs/environment_installation.en.md) using separate MuJoCo, Isaac and ManiSkill environments. Check the required assets and simulator access before launching scored episodes. Keep credentials in the host, never in prompts or result files.

The repository provides a single-episode launcher and a Python SDK. There is no bundled CLI that selects an evaluation scope, calls your model and produces a complete benchmark score. Use your host's agent adapter and scheduler; if these are missing, implement the SDK connection before testing. Do not substitute the fixed hold-action example for the tested policy.

Select tasks on the host:

- **EP subsets:** read [docs/ep_subsets/tasks.json](docs/ep_subsets/tasks.json). Take `subsets[name].indices`, then select matching rows from `tasks` using each row's `index`. Use their `task_id`, `suite` and `initial_mode`.
- **Full test:** select all 410 rows in `tasks` from [docs/evaluation/tasks.json](docs/evaluation/tasks.json). For each row, take its `groups` entry with `variant="loaded"` for the `marble` family or `variant="default"` for other families, then run all four entries in `trials`. This gives 410 groups and 1,640 conditions. Do not include the separate Launcher `ground` groups in this score.
- **One environment:** find exactly one matching `task_id` in that same full schedule and select its group and four trials as above. For example, `marble/dual-panda/A007` selects one loaded group and four conditions. An unknown or ambiguous ID must be resolved before running; do not substitute a similar task. A separately requested Launcher ground run must be labeled with its initialization and reported separately.

Full test is a scope name in these instructions, not a key in the EP subset membership file or a new CLI flag. Use the family prefix before the first `/` in `task_id` to assign the full catalog to suites:

| Suite | Task ID family prefixes | Full test tasks |
| --- | --- | ---: |
| Launch | `marble` | 100 |
| Tower | `hanoi_panda`, `hanoi_sharpa`, `hanoi_floating` | 120 |
| Lock | `kongming_lock` | 60 |
| Cube | `rubiks_panda`, `rubiks_sharpa`, `pocket_cube` | 80 |
| Home | `bookshelf`, `maniskill_long_horizon`, `maniskill_geometry`, `maniskill_dynamics` | 50 |

Use `paper-loaded-only-v1`, protocol `environment-four-trial-v2` and permission version `2026-10-09-environment-l0-l3`. The standard base seed is 0. Every task has trial indices 1, 2, 3 and 4; benchmark runs and default single-environment tests use Launcher `loaded` only. Read the [condition definitions](docs/evaluation/tasks.json) and [attempt accounting](docs/ep_subsets/README.en.md) on the host. Do not send these manifests to the tested agent.

| Benchmark | Tasks | Required conditions |
| --- | ---: | ---: |
| EP-20 | 20 | 80 |
| EP-100 | 100 | 400 |
| EP-Easy | 50 | 200 |
| EP-Hard | 50 | 200 |
| Full test | 410 | 1,640 |
| One environment | 1 | 4 |

These counts are for one fixed agent/level/observation/tool setting. Keep results from different settings separate. Four conditions are four required tests, not four retries from which to choose the best.

## Launch each attempt — host only

Start a new environment process, output directory and tested-agent session for every condition and every permitted attempt. For a single-environment test of `marble/dual-panda/A007` at L0, start its first condition in the configured MuJoCo environment (the same command also applies when this task belongs to an EP-20 or Full test run):

```bash
python scripts/environment_runtime.py \
  --task-id marble/dual-panda/A007 \
  --capability-level 0 --profile rgb \
  --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 \
  --initial-mode loaded --headless \
  --output /tmp/a007-l0-c1-a1
```

Keep this process running. Wait for its `session.json`, and give the tested client only the authorized session credentials and SDK. The output directory also contains host-private records: do not share the whole directory. Use `--capability-level 1`, `2` or `3` for other levels, with the observation profile and tool grants fixed above.

For Isaac tasks, use the configured wrapper:

```bash
bash scripts/run_isaac_binary.sh scripts/environment_runtime.py \
  --task-id hanoi_panda/panda/H04 \
  --capability-level 0 --profile rgb \
  --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 \
  --headless --output /tmp/ep20-l0-h04-c1-a1
```

For ManiSkill tasks, run the same `environment_runtime.py` entry point using the ManiSkill interpreter, assets and environment variables from the installation guide. Replace the task ID with the selected membership row. Do not run all three backends in the same Python environment.

For another environment, pass its exact ID to `--task-id` and use the interpreter for its backend. Set `--initial-mode loaded` for Launcher; omit this option for other families (`default` is a schedule label, not a CLI value). For a single-environment test, run trial indices 1, 2, 3 and 4 with a new output directory and agent session each time.

Repeat for all selected tasks and trial indices. Let the protocol choose each condition's parameters and budgets. Do not override split, spring stiffness, control-step limits or wall limits for registered trials. The wall limit includes startup. Do not change conditions, reset a live episode or reuse agent memory between attempts. Approved frozen tool installations may be reused; prior observations, plans and trajectories may not.

## Interact with one episode — tested agent

Read the supplied rules and then:

1. Call `describe()` to obtain the task goal, action dimensions, units, limits, robot information and declared interfaces. Never assume another task's action format.
2. Call `observe()`. Fetch images or other declared resources with `get_resource(resource_id)`; use only the observations allowed at your level.
3. Choose an action from those inputs and submit it through `step()` or `step_sequence()`. Read the returned observation and repeat within the budget. Use `mechanism.command()` only for mechanisms declared by the task.
4. Use `tools.list()` to discover granted gateway tools and `tools.call()` to invoke them. A source directory or installed library does not itself authorize a tool.
5. When done, or when observations report termination/truncation, call `finish()` and retain its returned result. A voluntary early finish is a failure unless the environment confirms success. Close the client afterwards.

The host can integrate its policy callback with the SDK as follows. `choose_action` is the actual agent adapter supplied by your host; it returns a valid action, or `None` to finish. This is an integration sketch, not a solver:

```python
import json
from pathlib import Path
from agentbench_sdk import Client


def run_episode(session_path, choose_action):
    session = json.loads(Path(session_path).read_text())
    client = Client(session["socket_path"], session["native_token"])
    try:
        description = client.describe()
        observation = client.observe()
        while not (observation["terminated"] or observation["truncated"]):
            action = choose_action(description, observation, client)
            if action is None:
                break
            observation = client.step(action)["observation"]
        return client.finish()
    finally:
        client.close()
```

Make the `agentbench_sdk` package available to the tested client; it does not need native simulator imports. The host must persist the returned result while the episode is alive. `environment_client.py` sends one neutral action and finishes, so running it alone is only a connection check.

Reads do not advance simulation time. If a request's outcome is uncertain after a transport error, retry with the **same request ID and identical content**; `TransportError.request_id` exposes the ID. A new ID may repeat an action. After the episode closes, do not keep stepping or restart it to repair a valid failure. Keep session tokens out of published logs.

## Report results

Use the trusted final result returned by `finish()` (`success`, `score`, `step_count`, `terminated`, `truncated`). Process exit code 0, a convincing image, a solved symbolic cube or an accepted action is not proof of task success. If the client cannot obtain a result, the host must inspect its private terminal evidence; the tested agent must not read it.

For **Pass@K** (K = 1, 2, 5 or 10), use the first K valid attempts in chronological order on the same condition, stopping at the first success. Pass@1 is the default; Pass@2, Pass@5 and Pass@10 are reference limits. Keep the condition, seed, settings and per-attempt budgets fixed, with a fresh environment and agent session each time. Do not increase K after seeing failures.

Report each requested cutoff separately from the same ordered attempt records, never by extrapolating Pass@1 or selecting favorable attempts. At cutoff k, a condition succeeds if any of its first k valid attempts succeeds; it fails only after k valid failures. Otherwise it is pending for that cutoff. For example, first success on attempt 4 means Pass@1 and Pass@2 fail, while Pass@5 and Pass@10 succeed without further attempts. If only two failures have run, Pass@5 and Pass@10 remain pending. Apply coverage and scoring separately for each cutoff.

Ordinary agent failures, rule violations and exhausted budgets—including normal wall timeout—consume an attempt. Only evidence-confirmed non-agent infrastructure incidents may be excluded and replaced under the same condition. Preserve the original record and replacement link. Unresolved incidents remain pending; do not label them success or silently drop them.

For a single-environment test, report the task ID, initialization, four condition outcomes, task score and completed coverage separately for each requested Pass@K cutoff. The task score is the mean of its four condition success values; it remains `null` while any required condition is pending at that cutoff. Do not calculate five-suite or overall benchmark scores from one task.

For each fully evaluated EP subset or Full test setting:

```text
Task score = mean success over its four conditions
Suite score = mean task score within that suite
Overall score = mean of Launch, Tower, Lock, Cube and Home scores
```

Each suite has 20% weight. Do not pool all successful episodes into a single percentage or select the best condition. If any required condition remains unresolved, report the run as `partial`, set its final benchmark score to `null`, and show completed coverage and any clearly labeled observed-success lower bound using the original denominators.

Report the evaluation scope, level, actual observation/tool setting, attempt policy, agent version, repository revision, planned/completed conditions per cutoff, actual valid-attempt counts, per-task outcomes, suite and overall scores where applicable, failures and excluded/pending incidents. Report token/image usage only when measured; missing usage is not zero. Retain per-attempt records locally outside the repository. Never commit session tokens, private state or generated evaluation reports to the source release. State exactly what completed; do not present setup checks or partial coverage as a completed benchmark.
