# 被测 Agent 任务书模板

[English](tested_agent_brief.en.md) · [Agent 操作说明](../Agent.zh-CN.md) · [规则](../rules/rules.zh-CN.md)

[Agent.md](../Agent.zh-CN.md) 面向**评测宿主**。**被测 Agent** 只应拿到完成一个回合所需的内容。本页给出一份宿主可以直接填写的任务书，以及随附材料清单；每个全新的被测 Agent 会话发送一份。任务书不提供公开接口和规则之外的任何任务信息，因此不同 Agent 的结果可以相互比较。

## 发送什么，不发送什么

| 发送 | 不发送 |
| --- | --- |
| 下面填好的任务书 | `Agent.md` 或其他仅供宿主的内容 |
| 共享规则以及对应等级的规则文档（见 [Agent.md](../Agent.zh-CN.md) 中的等级表） | 仓库源码、`docs/evaluation/tasks.json`、`docs/ep_subsets/tasks.json` 或任何条件清单 |
| 会话文件路径（或其中的 `socket_path` 与 `native_token`），以及可导入的 `agentbench_sdk` | 运行输出目录（其中有 `requests.sqlite` 等宿主私有记录） |
| 授权工具列表（没有则写“无”） | 其他尝试或其他条件的记录、代码、图像或结果 |

## 占位符

| 占位符 | 示例 | 来源 |
| --- | --- | --- |
| `{TASK_ID}` | `marble/dual-panda/A007` | 选中的调度行 |
| `{CONDITION}` | `1` | 条件编号 1–4 |
| `{ATTEMPT}` / `{MAX_ATTEMPTS}` | `1` / `1` | 事先声明的 Pass@K 上限 |
| `{LEVEL}` / `{PROFILE}` | `L0` / `rgb` | 固定的测试设置 |
| `{TOOLS}` | `none` | 明确授权的工具 |
| `{SESSION_PATH}` | `/runs/a007-l0-c1-a1/session.json` | `environment_runtime.py` 写出 |
| `{WALL_SECONDS}` / `{MAX_STEPS}` | `600` / `7500` | 任务预算，见 [Agent.md](../Agent.zh-CN.md#各任务族预算) |
| `{TOKEN_CAP}` / `{IMAGE_CAP}` | `30,000,000` / `100` | 宿主声明的资源上限，没有则写 `none` |

不要把条件参数（种子、扰动、弹簧刚度、光照）写进任务书；Agent 可以知道的内容都通过 `describe()` 获取。

## 任务书

任务书保持英文原文发送，以便不同 Agent 收到完全相同的文字：

```text
You are the agent under evaluation in Embodied Playground. Control one robot task
episode from a cold start and try to complete the task.

Task: {TASK_ID}. Registered condition {CONDITION} of 4.
Capability level {LEVEL}, observation profile {PROFILE}. Granted tools: {TOOLS}.
This is attempt {ATTEMPT} of at most {MAX_ATTEMPTS} for this condition. You have no
information from any other attempt and must not look for any.

Rules: read the attached shared rules and the {LEVEL} rule document before acting.
They define what you may observe and use. Nothing in this brief overrides them.

Connection: the episode is already running. Connect with the Python SDK:

    import json
    from agentbench_sdk import Client
    session = json.load(open("{SESSION_PATH}"))
    client = Client(session["socket_path"], session["native_token"])

Then:
1. Call client.describe() for the goal, action layout, units, limits and declared
   interfaces of THIS task. Do not assume another task's action format.
2. Call client.observe(). Fetch images or other declared resources with
   client.get_resource(resource_id). Use only observations allowed at your level.
3. Act through client.step(action) or client.step_sequence(actions). Use
   client.mechanism.command() only for mechanisms the task declares, and
   client.tools.list() / client.tools.call() only for granted tools.
4. When you are done or give up, or an observation reports terminated or truncated,
   call client.finish() and keep its result. Then call client.close().

Budgets: the episode wall clock is {WALL_SECONDS} s and started when the environment
was launched, including simulator startup; it keeps running while you think. The
episode allows at most {MAX_STEPS} control steps. Your own budget for this attempt is
{TOKEN_CAP} tokens and {IMAGE_CAP} image reads. The episode ends by itself on success,
on a rule or physical violation, at a limit, or when the wall clock expires.

Errors: if a request fails with a transport error and its outcome is unknown, retry it
with the same request ID and identical content (TransportError.request_id). A new
request ID may repeat an action. Never try to reset, relaunch or bypass the episode.

When you finish, report what you did and whether you believe the task succeeded.
The benchmark scores the episode from the environment's own records, not from your
report.
```

## 给宿主的说明

- 等 `session.json` 出现后再启动被测会话。墙钟已经在走，Agent 启动慢也会占用回合时间。
- 如果你的 Agent 不能直接运行 Python（例如通过工具转发 SDK 调用），可以改写“Connection”一段；其余段落在不同 Agent 之间保持不变，结果才可比较。
- 把每次发送的任务书存进该次尝试的记录。评测中途若修改任务书，修改前后的结果要分开报告。
