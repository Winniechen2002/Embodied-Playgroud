# Agent 操作说明

[English](Agent.en.md) · [人类使用入口](README.zh-CN.md) · [规则](rules/rules.zh-CN.md)

收到“以 L0–L3 测试 EP-20、EP-100、EP-Easy 或 EP-Hard”的要求时，按本文组织测试并汇报真实结果。安装成功、烟雾检查通过或生成执行计划都不是 Agent 得分。

## 区分评测组织者与被测 Agent

**评测宿主**负责选择条件、启动环境、创建全新的 Agent 会话、执行预算和收集结果。编码 Agent 可以组织这些工作，但被测策略必须在单独会话中运行，只接收授权输入。

**被测 Agent**通过 `describe()` 获取任务，通过 SDK 获取观测，并遵守对应等级的规则。它只能通过公开接口控制环境，不应获得仓库源码、运行目录、条件清单、评分器内部信息或其他尝试的记录。宿主应向它提供相关规则和交互说明，不应把下文仅供宿主使用的设置与调度内容一起传入。L3 通过网关开放声明的特权字段，不授予任意文件读取权限。

同一个模型同时负责组织评测和参加测试时，组织者的上下文、工作区和私有信息不得进入被测会话。网关本身不能隔离外部 Agent 的文件系统，也不执行模型 token 预算；这些边界由宿主提供。

## 固定测试设置——仅供宿主

从用户 prompt 中读取并记录：

- Benchmark：`EP-20`、`EP-100`、`EP-Easy` 或 `EP-Hard`。
- 能力等级：`L0`、`L1`、`L2` 或 `L3`。
- 尝试策略：默认 `Pass@1`；参考上限为 `Pass@2`、`Pass@5` 和 `Pass@10`。运行前固定最大 K 值和需要报告的档位。
- Agent／模型版本、指令、推理设置及声明的 token／图像预算。
- 观测配置、明确授权的工具及已准备的工具配置清单。
- 仓库修订、运行时版本和仓库外的新输出目录。

Easy／Hard 是任务难度划分，不是能力等级。使用用户指定的 benchmark 和 level；缺少其中一项时，在计分运行前确定。未授权工具时记录空工具清单，不擅自提升等级、在回合中安装新工具，或声称测过该等级允许的所有工具。

阅读[共享规则](rules/rules.zh-CN.md)和对应等级的规则：

| Level | 规则 | 观测选择 |
| --- | --- | --- |
| L0 | [代码直控](rules/rules_model_only.zh-CN.md) | `rgb` |
| L1 | [视觉与规划](rules/Vision_rules.zh-CN.md) | `rgb`，或环境支持且明确选择的 `rgbd` |
| L2 | [抓取／接触工具](rules/rules_grasp.zh-CN.md) | `rgb`，或环境支持且明确选择的 `rgbd` |
| L3 | [特权只读](rules/rules_privileged.zh-CN.md) | `privileged`，或明确声明的受限配置 |

Launcher 提供 RGB，不提供 RGB-D。高等级继承低等级权限，但工具仍需明确授权并完成安装，准备方式见[内嵌工具](docs/embedded_tools.zh-CN.md)。额外预训练动作策略、直接修改仿真状态和评分逻辑仍被禁止。

## 准备运行——仅供宿主

按照[安装说明](docs/environment_installation.zh-CN.md)，分别准备 MuJoCo、Isaac 和 ManiSkill 环境。在计分运行前检查资产和模拟器访问能力。凭据留在宿主，不写入 prompt 或结果文件。

仓库提供单回合启动器和 Python SDK，没有一条现成 CLI 可以自动选择 EP 子集、调用你的模型并生成完整 benchmark 得分。使用宿主的 Agent 适配器和调度器；缺少这些组件时，先接通 SDK，再开始测试。不能用固定保持动作的示例替代被测策略。

从 [docs/ep_subsets/tasks.json](docs/ep_subsets/tasks.json) 读取成员名单：取 `subsets[name].indices`，按各行的 `index` 从 `tasks` 选出对应记录，再使用其中的 `task_id`、`suite` 和 `initial_mode`。不要猜测任务 ID，也不要按名字相似度挑任务。

采用 `paper-loaded-only-v1` 定义、`environment-four-trial-v2` 协议和 `2026-10-09-environment-l0-l3` 权限版本，标准 base seed 为 0。每个任务执行 trial index 1、2、3、4；Launcher 只使用 `loaded`。宿主读取[条件定义](docs/evaluation/tasks.json)和[尝试计次规则](docs/ep_subsets/README.zh-CN.md)，不要把这些清单发给被测 Agent。

| Benchmark | 任务数 | 必须完成的条件数 |
| --- | ---: | ---: |
| EP-20 | 20 | 80 |
| EP-100 | 100 | 400 |
| EP-Easy | 50 | 200 |
| EP-Hard | 50 | 200 |

这些数量对应一套固定的 Agent／level／观测／工具设置。不同设置分别统计。四个条件是四项必测内容，不是四次重试后取最好结果。

## 启动每次尝试——仅供宿主

每个条件、每次获准的尝试都使用全新的环境进程、输出目录和被测 Agent 会话。例如，在配置好的 MuJoCo 环境中，以 L0 启动 EP-20 任务 `marble/dual-panda/A007` 的第一个条件：

```bash
python scripts/environment_runtime.py \
  --task-id marble/dual-panda/A007 \
  --capability-level 0 --profile rgb \
  --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 \
  --initial-mode loaded --headless \
  --output /tmp/ep20-l0-a007-c1-a1
```

保持该进程运行。等待 `session.json` 出现，只向被测客户端提供授权会话凭据与 SDK。输出目录还含宿主私有记录，不要共享整个目录。其他等级将 `--capability-level` 改为 1、2 或 3，观测配置与工具授权使用前面固定的设置。

Isaac 任务使用已配置的包装脚本：

```bash
bash scripts/run_isaac_binary.sh scripts/environment_runtime.py \
  --task-id hanoi_panda/panda/H04 \
  --capability-level 0 --profile rgb \
  --seed 0 --evaluation-protocol environment-four-trial-v2 --trial-index 1 \
  --headless --output /tmp/ep20-l0-h04-c1-a1
```

ManiSkill 任务仍使用 `environment_runtime.py`，但必须切换到安装说明中的 ManiSkill 解释器、资产和环境变量，并使用所选成员记录的任务 ID。不要在同一个 Python 环境中运行三个后端。

对全部任务及 trial index 重复执行。由协议选择每个条件的参数和预算，不覆盖已注册条件的 split、弹簧刚度、控制步数或墙钟限制。墙钟预算包含启动时间。不要更换条件、重置进行中的回合或在尝试之间复用 Agent 记忆。已批准的冻结工具安装可以复用，之前的观测、计划和轨迹不能复用。

## 与单个回合交互——被测 Agent

阅读宿主提供的规则，然后：

1. 调用 `describe()` 获取目标、动作维度、单位、范围、机器人信息与公开接口，不套用其他任务的动作格式。
2. 调用 `observe()`，通过 `get_resource(resource_id)` 读取图像等已声明资源，只使用当前等级允许的观测。
3. 根据这些输入选择动作，通过 `step()` 或 `step_sequence()` 提交，读取返回的观测并在预算内循环。仅对任务声明的机构使用 `mechanism.command()`。
4. 通过 `tools.list()` 查看已授予的网关工具，通过 `tools.call()` 调用。存在源码目录或已安装库不代表获得使用授权。
5. 完成操作，或观测显示终止／截断时，调用 `finish()` 并保存返回结果，随后关闭客户端。主动提前结束时，除非环境确认成功，否则按失败处理。

宿主可按以下方式接入 SDK。`choose_action` 是宿主实际提供的 Agent 适配器，返回合法动作，或返回 `None` 表示结束。此代码展示接口连接方式，不是求解器：

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

被测客户端只需能导入 `agentbench_sdk`，无需导入原生模拟器。宿主应在会话仍存活时保存返回结果。`environment_client.py` 只发送一次中性动作然后结束，单独运行它只算连接检查。

读取不会推进仿真时间。传输错误导致结果不确定时，使用**相同请求 ID 和相同内容**重试；`TransportError.request_id` 提供该 ID。使用新 ID 可能重复执行动作。回合结束后，不继续步进，也不能重启回合来修补有效失败。不要公开会话 token。

## 报告结果

以 `finish()` 返回的可信终态为准，其中包含 `success`、`score`、`step_count`、`terminated`、`truncated`。进程退出码为 0、画面看起来正确、符号魔方已解或动作被接受，都不能证明物理任务成功。客户端无法取得结果时，由宿主检查私有终态证据，被测 Agent 不得读取。

**Pass@K**（K = 1、2、5 或 10）使用同一条件按时间顺序最早 K 次有效尝试，首次成功即停止。默认使用 Pass@1，Pass@2、Pass@5 和 Pass@10 为参考上限。每次保持条件、种子、设置和单次预算一致，使用全新的环境与 Agent 会话；不得看到失败后临时增加 K。

从同一组有序尝试记录中分别报告各个要求的档位，不从 Pass@1 推算，也不挑选有利尝试。对于档位 k，前 k 次有效尝试中任一次成功即判该条件成功；只有累计 k 次有效失败才判失败，否则该档位仍待完成。例如，第 4 次首次成功，则 Pass@1、Pass@2 失败，Pass@5、Pass@10 成功，无需继续尝试。如果只完成了两次失败，Pass@5、Pass@10 仍待完成。各档位分别计算覆盖率和得分。

普通 Agent 失败、违规、预算耗尽（含正常墙钟超时）均消耗尝试机会。只有证据确认由非 Agent 原因造成的基础设施故障可排除，并在同一条件下补测；保留原始记录及补测关联。原因未明确的事件保持待处理，不记为成功，也不静默删除。

对每套完成的设置，按以下顺序计算：

```text
任务得分 = 四个条件成功值的平均
套件得分 = 该套件内任务得分的平均
总分 = Launch、Tower、Lock、Cube、Home 五个套件得分的平均
```

五个套件各占 20%。不要将所有成功回合直接汇总成一个比例，也不要只取最好条件。任何必测条件尚未确定结果时，标为 `partial`，最终 benchmark 得分设为 `null`，报告完成覆盖率；如报告已观测成功率下界，须明确标注并保留原计划分母。

报告 benchmark、level、实际观测／工具设置、尝试策略、Agent 版本、仓库修订、各档位计划／已完成条件数、实际有效尝试次数、各任务结果、五个套件分数、总分、失败及排除／待处理事件。只有实际测量时才报告 token／图像消耗，缺失值不是 0。逐次记录保存在仓库外，不向源码发布仓库提交 token、私有状态或生成的评测报告。准确说明完成范围，不把安装检查或部分覆盖包装成完整 benchmark 结果。
