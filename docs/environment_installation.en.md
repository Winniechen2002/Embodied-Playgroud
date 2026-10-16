# Installation

[简体中文](environment_installation.zh-CN.md) · [Documentation](README.en.md)

Use Linux x86_64, Python 3.11, and independent environments for the three simulators. Run commands from the repository root. Install Git LFS and retrieve required assets with `git lfs pull` when using a Git checkout. Optional perception, grasp and planning models are not environment dependencies. The source layout is required; installing the top-level project alone does not provision simulators.

## MuJoCo

```bash
python3.11 -m venv /tmp/agentbench-mujoco
source /tmp/agentbench-mujoco/bin/activate
python -m pip install -r env/runtime/mujoco-constraints.txt
export PYTHONPATH="$PWD/source/agentbench:$PWD/source/agentbench_platform:$PWD/source/agentbench_sdk"
export MUJOCO_GL=egl
python scripts/environment_release.py catalog --output /tmp/agentbench-catalog.json
python scripts/environment_smoke.py --task-id marble/dual-panda/A001 --output /tmp/agentbench-mujoco-smoke.json
```

Headless rendering requires a working EGL implementation. For Mesa EGL on systems with multiple vendors, select the installed Mesa configuration with `export __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/50_mesa.json`. Use the path present on your system. Rendering behavior can differ across drivers; record the GL vendor, renderer and version for reproducibility.

## Isaac Lab

Use the official **Isaac Sim 5.1.0 standalone binary** with Isaac Lab revision `b4c321024792976150ca55fddb26fa34480d974e`. Obtain the simulator from [NVIDIA](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/download.html), record the archive hash, and follow the vendor's license and installation requirements. NVIDIA GPU and driver access are required. The simulator is an external dependency. Install `uv` for the commands below and replace the three `/path/to/` values with your installation directories.

```bash
export ISAACSIM_PATH=/path/to/isaac-sim-5.1.0
export ISAACLAB_PATH=/path/to/IsaacLab
export AGENTBENCH_ISAAC_VENV=/path/to/isaac-venv
export AGENTBENCH_ISAAC_PYTHON="$AGENTBENCH_ISAAC_VENV/bin/python"
python3.11 -m venv "$AGENTBENCH_ISAAC_VENV"
git clone https://github.com/isaac-sim/IsaacLab.git "$ISAACLAB_PATH"
git -C "$ISAACLAB_PATH" checkout b4c321024792976150ca55fddb26fa34480d974e
ln -s "$ISAACSIM_PATH" "$ISAACLAB_PATH/_isaac_sim"
uv pip install --python "$AGENTBENCH_ISAAC_PYTHON" \
  --constraint env/runtime/isaac-binary-constraints.txt \
  --requirement env/runtime/isaac-binary-lock.txt \
  torch torchvision scipy fastapi toml wheel setuptools pip \
  --editable "$ISAACLAB_PATH/source/isaaclab" \
  --editable "$ISAACLAB_PATH/source/isaaclab_assets" \
  --editable "$ISAACLAB_PATH/source/isaaclab_tasks"
"$AGENTBENCH_ISAAC_PYTHON" -m pip check
bash scripts/run_isaac_binary.sh scripts/validate_isaac_installation.py \
  --isaac-root "$ISAACSIM_PATH" --isaac-lab-root "$ISAACLAB_PATH" \
  --output /tmp/agentbench-isaac-installation.json
```

Run Isaac scripts through `bash scripts/run_isaac_binary.sh <script> <arguments>`. The wrapper uses the standalone binary and isolated interpreter; it does not accept vendor terms automatically. Use the binary constraints above: the older Isaac Sim 5.1 pip dependency combination has incompatible FastAPI/Starlette pins. The installation validator loads native configurations and checks rendering, actions and clean exit; it does not solve tasks or establish complete engineering qualification.

## ManiSkill

Use its own environment because this runtime requires NumPy 2.x while the MuJoCo environment pins NumPy 1.x. Native rendering requires Vulkan. Asset extraction requires sufficient disk space for the packaged archive.

```bash
python3.11 -m venv /tmp/agentbench-maniskill
source /tmp/agentbench-maniskill/bin/activate
python -m pip install -c env/maniskill_lgd/requirements-simulator.txt -e 'env/maniskill_lgd[sim]'
export AGENTBENCH_MANISKILL_ASSETS=/tmp/agentbench-maniskill-assets
python -m agentbench_maniskill assets
python -m agentbench_maniskill assets --verify
export PYTHONPATH="$PWD/source/agentbench:$PWD/source/agentbench_platform:$PWD/source/agentbench_sdk"
python scripts/validate_source_installation.py --backend maniskill --output /tmp/agentbench-maniskill-installation.json
```

The runtime uses one SAPIEN CPU scene, 240 Hz physics and 20 Hz control. Asset integrity verification checks bytes; it does not establish redistribution rights. See [asset provenance](environment_assets.en.md).

## Reproducibility

Record source revision, local changes, package versions, simulator and driver versions, asset hashes, selected task/condition and command line. A successful catalog or smoke check is narrower than complete environment qualification. See [validation](environment_validation.en.md) for the remaining checks. Cross-hardware bitwise reproducibility is not asserted.
