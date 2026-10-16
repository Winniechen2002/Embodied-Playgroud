# 内嵌工具与求解器

[English](embedded_tools.en.md) · [文档索引](README.zh-CN.md)

发布版包含 Agent-Bench 的 `tools/`、两套魔方求解器接口，以及带嵌套依赖的
[17 个第三方源码快照](../third_party/README.md)。从 GitHub 克隆后执行 `git lfs pull`；
导出的源码包已包含真实文件，无需 Git 或子模块初始化。

| 入口 | 用途 |
| --- | --- |
| [魔方求解器](../tools/cube_solver/README.md) | 冻结表工作进程、独立回放与隔离镜像构建 |
| [CPU GraspNet](../tools/graspnet_cpu/README.md) | 离线镜像构建与授权 RGB-D 推理 |
| [魔方资产生成器](../tools/rubiks_cube/generate_asset.py) | 原生 USD 生成，需要 Isaac/USD 环境 |
| [关节烟雾工具](../tools/rubiks_cube/joint_toggle_smoke.py) | Isaac 原生关节开关诊断 |
| [求解器客户端接口](../source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config/rubiks_cube/rubiks_cube_solver.py) | 轻量符号求解适配器 |

从仓库根目录执行命令，各工具使用独立依赖环境。环境启动默认不授予工具；
完成冻结配置后，明确指定 `--tool cube_solver` 与 `--cube-solver-setup`，
或 `--tool graspnet` 与 `--tool-setup`。能力等级与观测边界仍适用。
源码快照不代表依赖已经安装、所有检查点已经包含或 GPU 推理已通过；额外预训练动作策略仍被禁止。
容器在回合前使用离线依赖构建，评测工作进程不得在线获取新工具。

```bash
python scripts/check_embedded_sources.py
python scripts/agentbench_cube_solver.py --help
python scripts/agentbench_build_cube_solver.py --help
python scripts/agentbench_build_graspnet_cpu.py --help
```

保留上游原条款。三个仓库缺少仓库级许可证，一个上游文档 LFS 图片无法获取；
具体范围见[快照清单](../third_party/README.md)。原环境验收不包含这些可选工具的独立依赖安装验收。
