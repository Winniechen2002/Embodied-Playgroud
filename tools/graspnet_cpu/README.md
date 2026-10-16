# CPU GraspNet worker

[Tool guide / 工具总览](../../docs/embedded_tools.en.md)

The CPU worker uses GraspNet revision `280c215129f759ed8649cb4e89fc5dfee55f4f80`.
Its inference-only NumPy PointNet++ operators reject CUDA tensors and training.
Prepare Python 3.11 wheels for `torch==2.5.1+cpu`, `numpy==1.26.4` and exact
transitive dependencies, with a fully hash-locked pip requirements file.

The builder requires the original pinned source ZIP (SHA-256
`177849327fa21c7271df45421186706050e7fda80f02c8689c055a7c2113d1fc`) and RealSense
checkpoint (`60680087c61cba2b6791614fef1519071e294f6dcaf99b3f581bb95f7c51a868`).
Source files are embedded under `third_party/graspnet-baseline`; the exact original
ZIP and checkpoint must be prepared separately. An arbitrary re-zipped directory
will not satisfy the archive identity.

```bash
python scripts/agentbench_build_graspnet_cpu.py --help
python scripts/agentbench_graspnet.py --help
```

Build with an immutable official Python base, the pinned ZIP/checkpoint, offline
wheelhouse, requirements lock and a new output directory. The builder includes
source, runtime and [third-party notices](THIRD_PARTY_NOTICES.txt) in the image
and writes `tool.json`. Pass `--tool graspnet --tool-setup /absolute/setup/tool.json`
to the environment runtime with capability level 2 or 3 and an available RGB-D
profile. Startup verifies the image and checkpoint before creating an episode.

The input is a gateway-bound RGB-D capture and calibration. Output poses are
camera-frame GraspNet +X approach / +Y jaw candidates, not wrist commands or
collision-free guarantees. The runtime uses a non-root, read-only, offline
container; checkpoint mounting is read-only. Local Docker/Podman configuration
must support the selected isolation options. No new container-inference result
is claimed by embedding these build sources.

CPU 工具的构建源码与官方源码已包含；独立依赖环境、原始固定 ZIP、权重和镜像需单独准备。
它只处理授权的 RGB-D 与标定，输出相机坐标系候选抓取，不控制机器人。
