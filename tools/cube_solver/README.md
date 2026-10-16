# Submitted-facelet cube solver

[工具总览 / Tool guide](../../docs/embedded_tools.en.md)

The embedded worker accepts only `{"arguments":{"facelets_urfdlb":"...54 URFDLB labels..."}}`
on stdin. It returns symbolic moves; the gateway independently replays the answer.
It receives no environment state, image recognizer or robot actuator.

Use Python 3.11, `cube-solver==1.1.4`, `typing_extensions==4.12.2` and its pinned
transitive dependencies in a separate environment. Prepare tables before evaluation:

```bash
python scripts/agentbench_cube_solver.py --cache /absolute/new/solver-cache --prepare
python -I -B scripts/agentbench_cube_solver.py --cache /absolute/new/solver-cache < request.json
```

Preparation creates a frozen setup manifest. Evaluation refuses missing or changed
tables and cannot generate/download them. The process command is a local worker
diagnostic. To enable the gateway tool, build an isolated image with
`scripts/agentbench_build_cube_solver.py --help`, using an immutable official
`python@sha256:...` base, offline wheelhouse, hash-locked requirements, prepared
cache and a new output directory. Docker and Podman options are supported.
The builder emits `tool.json`; launch with `--tool cube_solver --cube-solver-setup
/absolute/setup/tool.json` and capability level 1 or higher. Startup checks the
actual isolated worker. Missing setup fails; there is no host-process fallback.
The cache is mounted read-only and no model credentials or simulator handles are
mounted. Source inclusion does not bundle third-party Python wheels or generated
tables. Preserve each dependency's own license in the environment and image.

求解器只接收明确提交的 54 个面片标签，返回符号动作并独立回放验证。
先在独立环境准备冻结表，再构建离线隔离镜像；使用工具需显式授权。
源码内嵌不代表依赖、求解表或容器已经安装，也不代表机器人任务完成。
