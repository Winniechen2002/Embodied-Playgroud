# 安装

[English](environment_installation.en.md) · [文档](README.zh-CN.md)

使用 Linux x86_64、Python 3.11，并分别为三个模拟器配置独立环境。所有命令从仓库根目录运行。使用 Git 检出时，安装 Git LFS 并执行 `git lfs pull` 获取所需资产。可选视觉、抓取与规划模型不属于环境依赖。运行需要保留源码目录结构；仅安装顶层项目不会配置模拟器。

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

无窗口渲染需要可用的 EGL 实现。系统存在多个 EGL vendor 时，可用 `export __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/50_mesa.json` 选择 Mesa，并按本机实际安装位置调整路径。不同驱动可能产生不同渲染结果；复现时记录 GL vendor、renderer 与版本。

## Isaac Lab

使用官方 **Isaac Sim 5.1.0 独立二进制版本**及 Isaac Lab 修订 `b4c321024792976150ca55fddb26fa34480d974e`。从 [NVIDIA](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/download.html) 获取模拟器，记录归档哈希并遵循供应商许可与安装要求。运行需要 NVIDIA GPU 与驱动访问权限。模拟器作为外部依赖获取。先安装下列命令使用的 `uv`，并将三个 `/path/to/` 路径替换为实际目录。

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

通过 `bash scripts/run_isaac_binary.sh <script> <arguments>` 运行 Isaac 脚本。包装器使用独立二进制版本与隔离解释器，不自动接受供应商条款。使用上面的 binary 约束文件；旧 Isaac Sim 5.1 pip 组合的 FastAPI/Starlette 依赖不兼容。安装验证器加载原生配置，检查渲染、动作与正常退出，不求解任务；这是源码发布工程验收中的安装与基本运行检查。

### Isaac 资产的网络访问

Isaac Lab 在环境启动时会从 NVIDIA 的 Omniverse 内容服务器解析部分机器人资产。例如基于 Panda 的任务（`hanoi_panda`、`kongming_lock/dual-panda`、`rubiks_panda`、`bookshelf`）会从 `https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/` 加载 `Isaac/IsaacLab/Robots/FrankaEmika/panda_instanceable.usd`。因此宿主需要可用的 DNS 和到该服务器的出站 HTTPS，或者把 Isaac 5.1 资产的本地镜像配置为 Isaac Lab 的资产根目录。正式运行前先检查：

```bash
getent hosts omniverse-content-production.s3-us-west-2.amazonaws.com
curl -sSI --max-time 20 https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/IsaacLab/Robots/FrankaEmika/panda_instanceable.usd | head -1
```

服务器不可达时，启动日志会出现 `Waiting for server response...`，等满 300 秒后放弃（`Timed out after 300s while checking for USD`），进程退出且不会写出 `session.json`。这段时间计入回合墙钟，该次启动应判为非 Agent 事故。MuJoCo 与 ManiSkill 任务不访问该服务器。

### 选择 GPU

多 GPU 主机上，用 `CUDA_VISIBLE_DEVICES=<编号>` 把每个环境进程固定到一张卡，并保持默认的 `--device cuda:0`，例如 `CUDA_VISIBLE_DEVICES=1 bash scripts/run_isaac_binary.sh scripts/environment_runtime.py ...`。

## ManiSkill

此运行时需要 NumPy 2.x，而 MuJoCo 固定 NumPy 1.x，因此必须使用独立环境。原生渲染需要 Vulkan，资产解压需要预留足够磁盘空间。

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

运行时使用单个 SAPIEN CPU 场景，物理频率为 240 Hz、控制频率为 20 Hz。资产完整性校验只检查文件内容，不证明再分发权利，详见[资产来源](environment_assets.zh-CN.md)。

## 复现记录

记录源码修订、本地改动、包版本、模拟器与驱动版本、资产哈希、任务与条件及命令行。单独的目录查询或烟雾检查不代表完成全部源码发布检查；源码发布验收标准见[验证说明](environment_validation.zh-CN.md)。本项目不声明跨硬件逐位一致。
