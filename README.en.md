# Embodied Playground

> Follow `Agent.md` to test this agent on **EP-20** at **L0** with **Pass@1**, and report the five suite scores, overall score and completed coverage.

Copy this prompt to the agent that organizes your evaluation. Change **EP-20** and **L0** to choose another benchmark and access level.

[简体中文](README.zh-CN.md) · [Agent instructions](Agent.md) · [Rules](rules/rules.en.md)

Embodied Playground tests whether an agent can observe a simulated scene, choose actions and complete physical tasks. It covers launching, stacking, assembly, cubes and household manipulation.

## How to test your agent

1. **Prepare the playground.** Follow the [installation guide](docs/environment_installation.en.md). The benchmarks use MuJoCo, Isaac Lab and ManiSkill; prepare all required runtimes and assets.
2. **Connect your agent.** Your evaluation host must let the agent receive observations and send actions through the Python SDK. Prepare any approved tools before testing. [Agent.md](Agent.md) explains the connection and run procedure.
3. **Send the prompt above.** Keep the same agent version, instructions and settings throughout the test. Each condition gets a fresh environment and agent session.
4. **Read the results.** Use the environment's final success result. Report scores together with completed coverage; an unfinished test has no final benchmark score.

The prompt directs an evaluation workflow. The repository provides environments and an SDK; your agent host runs the sessions. `environment_client.py` only checks the connection—it does not test an agent's ability to solve tasks.

## Choose a benchmark

| Benchmark | Tasks | Conditions | Use |
| --- | ---: | ---: | --- |
| **EP-20** | 20 | 80 | Start here |
| **EP-100** | 100 | 400 | Full paper benchmark |
| **EP-Easy** | 50 | 200 | Easier half of EP-100 |
| **EP-Hard** | 50 | 200 | Harder half of EP-100 |

Every task has four conditions. These benchmarks use loaded initialization for Launcher. Exact task lists are in the [benchmark definitions](docs/ep_subsets/README.en.md).

## Choose an access level

| Level | What the agent may use |
| --- | --- |
| **L0** | RGB, public robot information, Python, NumPy, Pillow and its own algorithms |
| **L1** | L0 plus approved vision, geometry, IK, planning and proxy tools |
| **L2** | L1 plus approved pretrained grasp/contact tools |
| **L3** | L2 plus declared privileged simulator information, read-only |

A higher level does not automatically install or enable tools. Fix the tool list and observation profile before testing. All levels follow the [rules](rules/rules.en.md); no level permits changing simulator state directly.

## What the score means

With **Pass@1**, each condition gets one valid attempt. Average the four conditions for each task, average tasks within each suite, then give each of the five suites 20% of the overall score. **Pass@2** allows at most two valid attempts per condition and must be reported separately. See [Agent.md](Agent.md#report-results) for failures, incomplete runs and reporting.

[Installation](docs/environment_installation.en.md) · [Tools and solvers](docs/embedded_tools.en.md) · [Validation](docs/environment_validation.en.md) · [All documentation](docs/README.en.md)

Original code: [Apache-2.0](LICENSE). Original documentation and independently authored non-code assets: [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Third-party content retains its own terms; see [licensing](LICENSING.md).
