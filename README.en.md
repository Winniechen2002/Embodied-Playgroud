# Embodied Playground

[English](README.en.md) · [简体中文](README.zh-CN.md) · [Documentation](docs/README.en.md)

Embodied Playground is a robotics benchmark for closed-loop physical, strategic and spatial reasoning. This repository provides 410 task environments, robot and scene assets, a Python SDK, native scoring, and a shared permission gateway. The implementation retains the Agent-bench package and command names.

The release also embeds [tools, solvers and third-party sources](docs/embedded_tools.en.md), preserving pinned versions and original terms. Prepare separate dependencies and explicit grants before use.

| Environment family | Tasks | Runtime |
| --- | ---: | --- |
| Launcher, dual Panda | 100 | MuJoCo |
| Tower of Hanoi, Panda / FR3 + Sharpa / floating Sharpa | 120 | Isaac Lab |
| Kongming lock, dual Panda / dual floating Sharpa | 60 | Isaac Lab |
| Rubik’s cube, Panda / floating Sharpa | 60 | Isaac Lab |
| Pocket cube, ALOHA / dual Sharpa | 20 | Isaac Lab |
| Bookshelf, dual Panda | 20 | Isaac Lab |
| Household, precise manipulation and dynamics | 30 | ManiSkill |
| **Total** | **410** | |

## Get started

Use Python 3.11 and separate environments for MuJoCo, Isaac Lab and ManiSkill. Follow the [installation guide](docs/environment_installation.en.md) for pinned dependencies, native simulators and asset setup. From the repository root, in the configured MuJoCo environment:

```bash
python scripts/environment_release.py catalog --output /tmp/agentbench-catalog.json
python scripts/environment_runtime.py --task-id marble/dual-panda/A001 --capability-level 0 --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 --initial-mode loaded --headless --output /tmp/agentbench-session
```

In a second terminal with the same environment, connect using:

```bash
python scripts/environment_client.py /tmp/agentbench-session/session.json
```

The example client reads observations, performs a short hold, and finishes. Agents interact through `describe`, `observe`, `step` and `finish`. Initialization and reset belong to the evaluator. Read requests do not advance physics; repeated action request IDs do not repeat actions; completed episodes reject further stepping.

## Evaluation

The [EP subsets](docs/ep_subsets/README.en.md) define EP-100, EP-20, EP-Easy and EP-Hard. They contain 100, 20, 50 and 50 tasks, respectively, grouped into Launch, Tower, Lock, Cube and Home.

Each task has four conditions. The paper setting uses Launcher **loaded only**: 1,640 conditions for all 410 tasks and 400 for EP-100. EP-20 has 80; EP-Easy and EP-Hard each have 200. The general runtime also supports ground initialization, giving 510 groups and 2,040 conditions; that is a separate schedule.

Task rates average their four conditions; suite rates average task rates; the reported subset rate gives each of the five suites equal weight. Pass@1 uses the first valid attempt. Pass@2 permits at most two valid attempts per condition, stopping at success. Ordinary agent failures and budget exhaustion consume an opportunity. Confirmed non-agent infrastructure incidents are retained with evidence, excluded from valid attempts, and replaced under the same condition. See the [protocol](docs/evaluation_protocol.en.md), [exact conditions](docs/evaluation/index.en.md) and [rules](rules.en.md).

## Access levels

Permission version: `2026-10-09-environment-l0-l3`.

- **L0:** Python standard library, NumPy, Pillow and self-authored algorithms.
- **L1:** Additionally, explicitly granted and installed vision, geometry, IK, planning and proxy tools.
- **L2:** Additionally, explicitly granted and installed pretrained grasp/contact tools.
- **L3:** Additionally, declared privileged read-only simulator fields.

Levels do not authorize state writes or automatically install tools. The gateway enforces its exposed interfaces; it does not audit every library used by an external client process. Rubik tasks explicitly use the `hybrid_fixture_v1` auxiliary mechanism and its physical prerequisites.

## Scope and validation

This source distribution contains environments, the SDK, rules and supporting validation tools. It includes no model results, solution trajectories or leaderboard. See [validation](docs/environment_validation.en.md) for the engineering checks and their limits.

Engineering acceptance for this public source release has passed against the maintainer-approved scope: source regression tests, all 410 scorer fixtures and native installation checks, 130 default-condition physics probes, documentation checks and a MuJoCo export smoke test.

The maintainer has approved distribution of the included asset bundle under its original applicable licenses; see the asset license inventory.

## License

Original code is licensed under [Apache-2.0](LICENSE). Original documentation and independently authored non-code assets use [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Copyright holder: Chen Feng. Third-party terms and notices remain in effect; see [licensing scope](LICENSING.md), [third-party notices](THIRD_PARTY_NOTICES.md) and [asset provenance](docs/environment_assets.en.md).
