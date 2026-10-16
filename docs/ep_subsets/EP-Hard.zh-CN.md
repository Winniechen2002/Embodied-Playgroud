[English](EP-Hard.en.md) · [简体中文](EP-Hard.zh-CN.md)

# EP-Hard 说明

[集合总览与来源](README.zh-CN.md) · [机器可读成员索引](tasks.json)

EP-Hard 是 EP-100 在各任务类型内部按工作量排序后较高分的一侧，共 50 项，覆盖全部 16 类型。它与 EP-Easy 互斥且并集为 EP-100；Hard 是相对类型内工作量，不等于尚未被任何模型解决，也不等同于权限 L3。其 10 项进入 EP-20。适合分析更高工作量下的规划、物理控制和灵巧操作能力。

定义版本：`paper-loaded-only-v1`。

## 规模与使用

| 任务 | Launch | Tower | Lock | Cube | Home | 组 | 条件 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 17 | 10 | 8 | 6 | 9 | 50 | 200 |

上述为固定权限、观测、工具、预算和 base seed 下的数量。Launch 仅 `loaded`（第一发预装，后续仍须装填），其余 `default`；每任务四条件。Pass@2 最多使用 400 个有效尝试，首次成功即停止，实际数可更少；基础设施排除记录另列。

总分先计算每任务四条件均值，再计算套件内任务均值，最后对五个套件等权平均（各 20%）。不要直接混合全部条件求总成功率。Easy／Hard 的类型内划分、工作量公式、并列规则、异常口径和来源见[总览](README.zh-CN.md)。

## 类型覆盖

| 类型 | 任务数 | 论文编号 |
| --- | --- | --- |
| Launch-Aim | 3 | Launch-01, Launch-06, Launch-07 |
| Launch-Causal | 7 | Launch-13, Launch-14, Launch-16, Launch-17, Launch-18, Launch-19, Launch-20 |
| Launch-Glass | 2 | Launch-24, Launch-25 |
| Launch-Rules | 5 | Launch-29, Launch-30, Launch-31, Launch-33, Launch-34 |
| Tower-Plan | 2 | Tower-04, Tower-05 |
| Tower-Physics | 4 | Tower-08, Tower-10, Tower-12, Tower-13 |
| Tower-Dex | 4 | Tower-15, Tower-16, Tower-17, Tower-19 |
| Lock-Assemble | 3 | Lock-01, Lock-04, Lock-06 |
| Lock-Disassemble | 3 | Lock-07, Lock-10, Lock-12 |
| Lock-Dex | 2 | Lock-13, Lock-15 |
| Cube-Rubik | 4 | Cube-05, Cube-06, Cube-07, Cube-08 |
| Cube-Pocket | 2 | Cube-10, Cube-12 |
| Home-Tidy | 3 | Home-03, Home-04, Home-05 |
| Home-Long | 2 | Home-08, Home-09 |
| Home-Precise | 2 | Home-10, Home-12 |
| Home-Dynamic | 2 | Home-15, Home-16 |

## 完整任务清单

任务名称保留论文英文，编号与环境 ID 精确对应；`是` 表示同时属于 EP-20。

| 论文编号 | 类型 | 论文任务名称 | 分割 | EP-20 | 环境 ID |
| --- | --- | --- | --- | --- | --- |
| Launch-01 | Launch-Aim | Two-range ammunition planning | Hard | — | `marble/dual-panda/A001` |
| Launch-06 | Launch-Aim | Three-target fan | Hard | — | `marble/dual-panda/A075` |
| Launch-07 | Launch-Aim | Left-low and right-high fork | Hard | — | `marble/dual-panda/A031` |
| Launch-13 | Launch-Causal | Branching dominoes | Hard | — | `marble/dual-panda/A006` |
| Launch-14 | Launch-Causal | Indirect clearance with two bridges | Hard | — | `marble/dual-panda/A015` |
| Launch-16 | Launch-Causal | Staggered twin towers | Hard | — | `marble/dual-panda/A034` |
| Launch-17 | Launch-Causal | Two-ball relay | Hard | — | `marble/dual-panda/A055` |
| Launch-18 | Launch-Causal | Upper-to-lower beam transfer | Hard | — | `marble/dual-panda/A063` |
| Launch-19 | Launch-Causal | Movable flap at a narrow throat | Hard | 是 | `marble/dual-panda/A072` |
| Launch-20 | Launch-Causal | Near target before collapse | Hard | — | `marble/dual-panda/A073` |
| Launch-24 | Launch-Glass | One-shot glass breach | Hard | — | `marble/dual-panda/A027` |
| Launch-25 | Launch-Glass | Glass-supported lower story | Hard | — | `marble/dual-panda/A035` |
| Launch-29 | Launch-Rules | Attic target above a protected floor | Hard | — | `marble/dual-panda/A036` |
| Launch-30 | Launch-Rules | Keep the lower chamber safe | Hard | — | `marble/dual-panda/A047` |
| Launch-31 | Launch-Rules | Fragment-risk well | Hard | 是 | `marble/dual-panda/A068` |
| Launch-33 | Launch-Rules | Upper floor before lower floor | Hard | — | `marble/dual-panda/A092` |
| Launch-34 | Launch-Rules | Material-ordered courtyard | Hard | 是 | `marble/dual-panda/A093` |
| Tower-04 | Tower-Plan | Long five-ring rearrangement | Hard | 是 | `hanoi_panda/panda/H04` |
| Tower-05 | Tower-Plan | Long combined challenge | Hard | — | `hanoi_panda/panda/H40` |
| Tower-08 | Tower-Physics | Medium-hole replacement | Hard | — | `hanoi_panda/panda/H14` |
| Tower-10 | Tower-Physics | Standard-friction transfer | Hard | — | `hanoi_panda/panda/H22` |
| Tower-12 | Tower-Physics | Long and short peg pair | Hard | — | `hanoi_panda/panda/H34` |
| Tower-13 | Tower-Physics | Offset vertical barrier | Hard | — | `hanoi_panda/panda/H31` |
| Tower-15 | Tower-Dex | Local two-ring transfer | Hard | 是 | `hanoi_floating/floating-sharpa/H02` |
| Tower-16 | Tower-Dex | Low-to-high platform | Hard | — | `hanoi_floating/floating-sharpa/H09` |
| Tower-17 | Tower-Dex | Single tilted handle | Hard | — | `hanoi_floating/floating-sharpa/H25` |
| Tower-19 | Tower-Dex | Local two-ring transfer | Hard | — | `hanoi_sharpa/fr3-sharpa/H02` |
| Lock-01 | Lock-Assemble | Assemble full lock | Hard | — | `kongming_lock/dual-panda/A01` |
| Lock-04 | Lock-Assemble | Assemble full lock | Hard | — | `kongming_lock/dual-panda/A04` |
| Lock-06 | Lock-Assemble | Assemble key + bar | Hard | — | `kongming_lock/dual-panda/A14` |
| Lock-07 | Lock-Disassemble | Disassemble full lock | Hard | 是 | `kongming_lock/dual-panda/D01` |
| Lock-10 | Lock-Disassemble | Disassemble full lock | Hard | — | `kongming_lock/dual-panda/D04` |
| Lock-12 | Lock-Disassemble | Disassemble key + bar | Hard | — | `kongming_lock/dual-panda/D14` |
| Lock-13 | Lock-Dex | Assemble full lock | Hard | — | `kongming_lock/dual-floating-sharpa/A01` |
| Lock-15 | Lock-Dex | Disassemble full lock | Hard | — | `kongming_lock/dual-floating-sharpa/D01` |
| Cube-05 | Cube-Rubik | Solve scramble C02 | Hard | — | `rubiks_sharpa/floating-sharpa/C02` |
| Cube-06 | Cube-Rubik | Solve scramble C11 | Hard | 是 | `rubiks_panda/panda/C11` |
| Cube-07 | Cube-Rubik | Solve scramble C12 | Hard | — | `rubiks_panda/panda/C12` |
| Cube-08 | Cube-Rubik | Solve scramble C21 | Hard | — | `rubiks_panda/panda/C21` |
| Cube-10 | Cube-Pocket | Clockwise top turn | Hard | — | `pocket_cube/dual-sharpa/C01` |
| Cube-12 | Cube-Pocket | Half-turn in two stages | Hard | 是 | `pocket_cube/dual-sharpa/C08` |
| Home-03 | Home-Tidy | One book on the wrong layer of a tidy shelf | Hard | 是 | `bookshelf/dual-panda/ShelfCrateFixD1` |
| Home-04 | Home-Tidy | Books, a trophy and one box | Hard | — | `bookshelf/dual-panda/ShelfTableD1` |
| Home-05 | Home-Tidy | Three books and two pieces of trash | Hard | — | `bookshelf/dual-panda/TableCleanD1` |
| Home-08 | Home-Long | Unload cups and cutlery from the dishwasher | Hard | — | `maniskill_long_horizon/fetch/L5` |
| Home-09 | Home-Long | Pack a picnic basket | Hard | — | `maniskill_long_horizon/fetch/L6` |
| Home-10 | Home-Precise | Insert three matching pegs | Hard | — | `maniskill_geometry/panda/P1` |
| Home-12 | Home-Precise | Hang a mug by its handle | Hard | 是 | `maniskill_geometry/panda/P5` |
| Home-15 | Home-Dynamic | Push a tall bottle without tipping | Hard | — | `maniskill_dynamics/panda/D5` |
| Home-16 | Home-Dynamic | Close a loaded drawer gently | Hard | — | `maniskill_dynamics/panda/D6` |
