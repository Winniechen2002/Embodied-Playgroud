# Tested-agent brief template

[简体中文](tested_agent_brief.zh-CN.md) · [Agent instructions](../Agent.en.md) · [Rules](../rules/rules.en.md)

[Agent.md](../Agent.en.md) is written for the **evaluation host**. The **tested agent** should receive only what it needs for one episode. This page gives a brief the host can fill in and send to each fresh tested-agent session, plus the attachments that go with it. It adds no task information beyond the public interface and the rules, so results stay comparable across agents.

## What to send, and what not to send

| Send | Do not send |
| --- | --- |
| The filled-in brief below | `Agent.md` or other host-only sections |
| The shared rules and the rule document for the level (see the table in [Agent.md](../Agent.en.md#fix-the-requested-setting--host-only)) | The repository checkout, `docs/evaluation/tasks.json`, `docs/ep_subsets/tasks.json` or any condition manifest |
| The session file path, or its `socket_path` and `native_token`, and an importable `agentbench_sdk` | The run output directory (it contains host-private records such as `requests.sqlite`) |
| The granted tool list (empty if none) | Records, code, images or results of any other attempt or condition |

## Placeholders

| Placeholder | Example | Source |
| --- | --- | --- |
| `{TASK_ID}` | `marble/dual-panda/A007` | selected schedule row |
| `{CONDITION}` | `1` | trial index, 1–4 |
| `{ATTEMPT}` / `{MAX_ATTEMPTS}` | `1` / `1` | declared Pass@K limit |
| `{LEVEL}` / `{PROFILE}` | `L0` / `rgb` | fixed setting |
| `{TOOLS}` | `none` | explicit tool grants |
| `{SESSION_PATH}` | `/runs/a007-l0-c1-a1/session.json` | written by `environment_runtime.py` |
| `{WALL_SECONDS}` / `{MAX_STEPS}` | `600` / `7500` | task budgets, see [Agent.md](../Agent.en.md#budgets-by-family) |
| `{TOKEN_CAP}` / `{IMAGE_CAP}` | `30,000,000` / `100` | host-declared resource caps, or `none` |

Do not put the condition's parameters (seed, perturbation, spring stiffness, lighting) in the brief; the agent obtains what it may know through `describe()`.

## Brief

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

## Notes for the host

- Start the tested session only after `session.json` exists. The wall clock is already running, so a slow agent start uses episode time.
- Adapt the connection paragraph if your agent cannot run Python directly (for example, a tool that forwards SDK calls). Keep the content of the other paragraphs unchanged across agents so results remain comparable.
- Keep every brief you send in the per-attempt record. If you change the brief during an evaluation, keep the results before and after the change separate.
