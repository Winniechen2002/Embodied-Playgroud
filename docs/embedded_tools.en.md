# Embedded tools and solvers

[简体中文](embedded_tools.zh-CN.md) · [Documentation](README.en.md)

The source release includes Agent-Bench's `tools/`, both Rubik solver interfaces,
and [17 third-party source snapshots](../third_party/README.md) with their nested
dependencies. GitHub clones need Git LFS (`git lfs pull`); exported source packages
contain materialized files and need no Git or submodule initialization.

| Entry | Purpose |
| --- | --- |
| [Cube solver](../tools/cube_solver/README.md) | Frozen-table worker, independent replay and isolated image builder |
| [CPU GraspNet](../tools/graspnet_cpu/README.md) | Offline image build and authorized RGB-D inference |
| [Rubik asset generator](../tools/rubiks_cube/generate_asset.py) | Native USD generation; requires the Isaac/USD environment |
| [Joint smoke tool](../tools/rubiks_cube/joint_toggle_smoke.py) | Isaac native joint-toggle diagnostic |
| [Solver client interface](../source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config/rubiks_cube/rubiks_cube_solver.py) | Dependency-light symbolic solver adapter |

Run commands from the repository root. Use each tool's own dependency environment.
The default environment launch grants no tools. Select `--tool cube_solver` with
`--cube-solver-setup`, or `--tool graspnet` with `--tool-setup`, only after preparing
the corresponding frozen setup. Existing capability rules and observation limits
still apply. Tool snapshots do not install dependencies, provide all checkpoints,
or imply successful GPU inference. Additional pretrained action policies remain
prohibited. Container setup is performed before an episode, with offline wheels;
workers cannot fetch new tools during evaluation.

```bash
python scripts/check_embedded_sources.py
python scripts/agentbench_cube_solver.py --help
python scripts/agentbench_build_cube_solver.py --help
python scripts/agentbench_build_graspnet_cpu.py --help
```

All original upstream terms are retained. Three repositories lack a repository-level
license file, and one upstream documentation LFS image is unavailable; see the
[snapshot inventory](../third_party/README.md) for exact scope. The original environment
acceptance does not certify optional tools' independent dependency installations.
