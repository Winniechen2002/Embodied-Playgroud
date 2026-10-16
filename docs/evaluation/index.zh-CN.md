# 逐任务评测条件

`environment-four-trial-v2` · base seed `0` · 410 tasks · 510 groups · 2040 planned episodes

[English](index.en.md) · [简体中文](index.zh-CN.md)

根据源码生成；不含执行成绩。[Protocol](../evaluation_protocol.zh-CN.md) · [JSON](tasks.json)

Embodied Playground 论文仅评测发射器 loaded 初态：完整 410 项为 410 组／1640 条件，EP-100 为 100 组／400 条件。本运行时清单另保留 ground，共 510 组／2040 条件。[EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.zh-CN.md)

| Family / 系列 | Tasks / 任务 | Episodes / 回合 |
| --- | ---: | ---: |
| [发射器](marble.zh-CN.md) | 100 | 800 |
| [Panda 汉诺塔](hanoi_panda.zh-CN.md) | 40 | 160 |
| [FR3 Sharpa 汉诺塔](hanoi_sharpa.zh-CN.md) | 40 | 160 |
| [Floating Sharpa 汉诺塔](hanoi_floating.zh-CN.md) | 40 | 160 |
| [二阶魔方](pocket_cube.zh-CN.md) | 20 | 80 |
| [Panda 三阶魔方](rubiks_panda.zh-CN.md) | 30 | 120 |
| [Floating Sharpa 三阶魔方](rubiks_sharpa.zh-CN.md) | 30 | 120 |
| [孔明锁](kongming_lock.zh-CN.md) | 60 | 240 |
| [书架](bookshelf.zh-CN.md) | 20 | 80 |
| [ManiSkill 长程任务](maniskill_long_horizon.zh-CN.md) | 10 | 40 |
| [ManiSkill 几何任务](maniskill_geometry.zh-CN.md) | 10 | 40 |
| [ManiSkill 动力学任务](maniskill_dynamics.zh-CN.md) | 10 | 40 |
