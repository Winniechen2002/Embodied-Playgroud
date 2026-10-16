# 环境验证

[English](environment_validation.en.md) · [文档](README.zh-CN.md)

验证检查环境实现、资产加载、原生动作与观测、评分、权限及回合生命周期，不代表 agent 表现，也不证明每个种子均可求解。本次公开源码发布的工程验收已通过，验收范围如下。

## 本次源码发布的工程验收标准

维护者于 2026-10-16 确认采用以下已执行且通过的检查作为本次源码发布标准，工程验收结论为**通过**。

| 检查 | 已通过范围 |
| --- | --- |
| 源码回归 | 280 项测试，0 失败、0 跳过 |
| 评分端点夹具 | MuJoCo 100、Isaac 280、ManiSkill 30，共 410 项 |
| 原生安装与基本运行 | 三后端全部 410 项加载、步进和结束检查；Isaac 10 类渲染检查，以及 MuJoCo、ManiSkill 渲染与网关烟雾检查 |
| 默认条件物理检查 | MuJoCo 100 项、ManiSkill 30 项 |
| 文档与公开内容 | 双语协议生成一致性、权限文档、1,438 个本地链接目标、740 个公开文件的静态审计 |
| 导出可用性 | 独立源码导出、410 项目录加载及 MuJoCo A001 烟雾检查 |

原生检查使用隔离且版本受校验的现有运行时，测试硬件为 NVIDIA RTX 4090、驱动 580.173.02；不将其描述为在空机器上重新安装全部模拟器。评分夹具检查人工构造的状态，物理检查覆盖上表所列默认条件，导出包烟雾检查覆盖 MuJoCo。资产按原有适用许可证分发，许可与署名保持不变。

本标准适用于此次公开源码发布。生成的检查报告放在仓库外的本地输出目录，不随公开源码提交。

## 本地检查

先按[安装指南](environment_installation.zh-CN.md)准备三个独立环境。以下命令均从仓库根目录运行；每个小节使用对应模拟器的解释器，不在 MuJoCo 环境中执行全部后端的评分检查。

### 目录与协议检查

在已配置的 MuJoCo 环境中执行；这些命令不启动原生仿真：

```bash
python scripts/environment_release.py catalog --output /tmp/agentbench-catalog.json
python scripts/export_evaluation_protocol.py --check
```

预期目录含 410 个任务，协议生成检查报告源码哈希与文档一致。

### MuJoCo：100 个任务

使用安装指南中的 MuJoCo 环境，并保留 `MUJOCO_GL=egl` 及所需的 EGL vendor 设置：

```bash
python scripts/validate_environment_contracts.py --backend mujoco --output /tmp/agentbench-mujoco-contracts.json
python scripts/environment_smoke.py --task-id marble/dual-panda/A001 --output /tmp/agentbench-mujoco-smoke.json
```

### Isaac：280 个任务

配置 `ISAACSIM_PATH`、`ISAACLAB_PATH` 和 `AGENTBENCH_ISAAC_PYTHON`，通过安装指南的包装器使用 Isaac 独立环境。书架评分夹具需要该环境中的 Torch：

```bash
bash scripts/run_isaac_binary.sh scripts/validate_environment_contracts.py --backend isaac --output /tmp/agentbench-isaac-contracts.json
bash scripts/run_isaac_binary.sh scripts/environment_smoke.py --task-id hanoi_panda/panda/H01 --output /tmp/agentbench-isaac-smoke.json
```

### ManiSkill：30 个任务

切换到安装指南中的 ManiSkill 环境，完成资产解压，并设置 `AGENTBENCH_MANISKILL_ASSETS`：

```bash
python scripts/validate_environment_contracts.py --backend maniskill --output /tmp/agentbench-maniskill-contracts.json
python scripts/environment_smoke.py --task-id maniskill_long_horizon/fetch/L1 --output /tmp/agentbench-maniskill-smoke.json
```

评分检查成功时，报告中的 `run_status` 为 `completed`，对应任务均为 `passed_fixture`；烟雾检查成功时为 `passed_probe`。失败时保留报告中的 `error` 和诊断信息。ManiSkill 保存的初始／目标夹具不再包含或校验任务定义哈希，评分检查直接执行当前评分器的断言；删除哈希不代表物理或评分断言自动通过。

烟雾检查覆盖实际观测、时间推进、重复请求 ID、结束行为与进程退出。短探针不等于完整时长或全条件通过。Isaac 原生检查需要配置好的 GPU 运行时，ManiSkill 原生检查需要其独立依赖、资产与 Vulkan。

干净安装验证使用安装指南中的对应脚本。验证器忽略内容与 Git LFS 索引指针匹配的实体资产，避免误报本地修改；真实源码、资产或暂存区修改仍须在干净检出中解决后再验证。

## 发布检查

`environment_release.py check` 和 `build --candidate` 使用源码发布标准，要求的证据覆盖三个后端的原生安装、资产、许可、双语文档、源码回归、评分夹具、默认条件物理检查和导出烟雾检查。

通过 `--evidence` 提供本地收集的证据；每个必需检查项都需要 `global_checks` 中的 `passed` 状态，以及 `global_measurements` 中绑定当前源码身份的非空测量。缺失、失败、过期或包含非有限数值的证据不能通过。源码发布批准不会把缺失证据自动变为通过的测量。

运行工具时使用对应模拟器环境，结果保存在仓库外。

## 契约变更

动作契约记录维度、限制、关节顺序、映射及控制／物理周期。指纹变化可能阻止任务发现；`revalidate_action_contracts.py` 仅接受测得的原生记录，并检查覆盖范围与语义是否保持。仅更新指纹不足以批准动作行为变化。批准契约变更后，用 `export_evaluation_protocol.py` 重新生成各任务的协议文档。
