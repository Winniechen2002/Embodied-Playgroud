# Agent instructions

[简体中文](Agent.zh-CN.md) · [Human quick start](README.md) · [Rules](rules/rules.en.md)

Use this guide when asked to test an agent on EP-20, EP-100, EP-Easy or EP-Hard at L0–L3. Run the requested evaluation and report measured results. A successful installation, smoke check or generated plan is not an agent score.

## Separate the evaluator from the tested agent

The **evaluation host** selects conditions, starts environments, creates fresh agent sessions, enforces limits and collects results. A coding agent may organize this work, but it must run the tested policy in separate sessions with only the authorized inputs.

The **tested agent** receives its task through `describe()`, observations through the SDK, and the rules for its level. It controls the environment only through the public interface. Do not give it the repository checkout, private run directory, condition manifests, scorer internals or past attempts. The host should supply the relevant rules and interaction instructions, rather than the host-only setup and scheduling sections below. L3 exposes declared privileged fields through the gateway; it does not grant arbitrary filesystem access.

If the same model organizes and takes the test, keep the organizer's conversation, workspace and private information out of the tested sessions. The gateway alone does not isolate an external agent's filesystem or enforce model token limits; the host must provide those boundaries.

## Fix the requested setting — host only

Read the user's prompt and record:

- Benchmark: `EP-20`, `EP-100`, `EP-Easy` or `EP-Hard`.
- Capability level: `L0`, `L1`, `L2` or `L3`.
- Attempt policy: `Pass@1` unless the user requests `Pass@2`.
- Agent/model version, instructions, inference settings and any token/image budgets.
- Observation profile, explicit tool grants and prepared tool setup manifests.
- Repository revision, runtime versions and a new output directory outside the repository.

Do not confuse an Easy/Hard split with an access level. Use the user's chosen benchmark and level; if either is missing, resolve it before starting scored runs. When no tools are granted, record an empty tool list. Do not silently change the level, install new tools during an episode, or claim that all tools permitted by a level were tested.

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

The repository provides a single-episode launcher and a Python SDK. There is no bundled CLI that selects an EP subset, calls your model and produces a complete benchmark score. Use your host's agent adapter and scheduler; if these are missing, implement the SDK connection before testing. Do not substitute the fixed hold-action example for the tested policy.

Read membership from [docs/ep_subsets/tasks.json](docs/ep_subsets/tasks.json). For the selected benchmark, take `subsets[name].indices`, then select matching rows from `tasks` using each row's `index`. Use their `task_id`, `suite` and `initial_mode`; do not invent task IDs or select tasks by name similarity.

Use `paper-loaded-only-v1`, protocol `environment-four-trial-v2` and permission version `2026-10-09-environment-l0-l3`. The standard base seed is 0. Every task has trial indices 1, 2, 3 and 4; Launcher uses `loaded` only. Read the [condition definitions](docs/evaluation/tasks.json) and [attempt accounting](docs/ep_subsets/README.en.md) on the host. Do not send these manifests to the tested agent.

| Benchmark | Tasks | Required conditions |
| --- | ---: | ---: |
| EP-20 | 20 | 80 |
| EP-100 | 100 | 400 |
| EP-Easy | 50 | 200 |
| EP-Hard | 50 | 200 |

These counts are for one fixed agent/level/observation/tool setting. Keep results from different settings separate. Four conditions are four required tests, not four retries from which to choose the best.

## Launch each attempt — host only

Start a new environment process, output directory and tested-agent session for every condition and every permitted attempt. For example, in the configured MuJoCo environment, start the first condition of the EP-20 task `marble/dual-panda/A007` at L0:

```bash
python scripts/environment_runtime.py \
  --task-id marble/dual-panda/A007 \
  --capability-level 0 --profile rgb \
  --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 \
  --initial-mode loaded --headless \
  --output /tmp/ep20-l0-a007-c1-a1
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

For **Pass@1**, score the first valid attempt on each condition. For **Pass@2**, allow at most two valid attempts on the same condition, stop after success, and count condition success if either valid attempt succeeds. Report Pass@1 and Pass@2 separately. Ordinary agent failures, rule violations and exhausted budgets—including normal wall timeout—consume an attempt. Only evidence-confirmed non-agent infrastructure incidents may be excluded and replaced under the same condition. Preserve the original record and replacement link. Unresolved incidents remain pending; do not label them success or silently drop them.

For each fully evaluated setting:

```text
Task score = mean success over its four conditions
Suite score = mean task score within that suite
Overall score = mean of Launch, Tower, Lock, Cube and Home scores
```

Each suite has 20% weight. Do not pool all successful episodes into a single percentage or select the best condition. If any required condition remains unresolved, report the run as `partial`, set its final benchmark score to `null`, and show completed coverage and any clearly labeled observed-success lower bound using the original denominators.

Report the benchmark, level, actual observation/tool setting, attempt policy, agent version, repository revision, planned/completed conditions, per-task outcomes, five suite scores, overall score, failures and excluded/pending incidents. Report token/image usage only when measured; missing usage is not zero. Retain per-attempt records locally outside the repository. Never commit session tokens, private state or generated evaluation reports to the source release. State exactly what completed; do not present setup checks or partial coverage as a completed benchmark.
