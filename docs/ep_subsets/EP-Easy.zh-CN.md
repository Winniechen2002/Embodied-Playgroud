[English](EP-Easy.en.md) · [简体中文](EP-Easy.zh-CN.md)

# EP-Easy 说明

[集合总览与来源](README.zh-CN.md) · [机器可读成员索引](tasks.json)

EP-Easy 是 EP-100 在各任务类型内部按工作量排序后较低分的一侧，共 50 项，覆盖全部 16 类型。它与 EP-Hard 互斥且并集为 EP-100；不是全库中绝对最简单的 50 项，也不保证某个模型一定成功。其 10 项进入 EP-20。适合观察相近任务构成下较低工作量部分的表现。

定义版本：`paper-loaded-only-v1`。

## 规模与使用

| 任务 | Launch | Tower | Lock | Cube | Home | 组 | 条件 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 17 | 11 | 8 | 6 | 8 | 50 | 200 |

上述为固定权限、观测、工具、预算和 base seed 下的数量。Launch 仅 `loaded`（第一发预装，后续仍须装填），其余 `default`；每任务四条件。Pass@2 最多使用 400 个有效尝试，首次成功即停止，实际数可更少；基础设施排除记录另列。

总分先计算每任务四条件均值，再计算套件内任务均值，最后对五个套件等权平均（各 20%）。不要直接混合全部条件求总成功率。Easy／Hard 的类型内划分、工作量公式、并列规则、异常口径和来源见[总览](README.zh-CN.md)。

## 类型覆盖

| 类型 | 任务数 | 论文编号 |
| --- | --- | --- |
| Launch-Aim | 4 | Launch-02, Launch-03, Launch-04, Launch-05 |
| Launch-Causal | 6 | Launch-08, Launch-09, Launch-10, Launch-11, Launch-12, Launch-15 |
| Launch-Glass | 3 | Launch-21, Launch-22, Launch-23 |
| Launch-Rules | 4 | Launch-26, Launch-27, Launch-28, Launch-32 |
| Tower-Plan | 3 | Tower-01, Tower-02, Tower-03 |
| Tower-Physics | 4 | Tower-06, Tower-07, Tower-09, Tower-11 |
| Tower-Dex | 4 | Tower-14, Tower-18, Tower-20, Tower-21 |
| Lock-Assemble | 3 | Lock-02, Lock-03, Lock-05 |
| Lock-Disassemble | 3 | Lock-08, Lock-09, Lock-11 |
| Lock-Dex | 2 | Lock-14, Lock-16 |
| Cube-Rubik | 4 | Cube-01, Cube-02, Cube-03, Cube-04 |
| Cube-Pocket | 2 | Cube-09, Cube-11 |
| Home-Tidy | 2 | Home-01, Home-02 |
| Home-Long | 2 | Home-06, Home-07 |
| Home-Precise | 2 | Home-11, Home-13 |
| Home-Dynamic | 2 | Home-14, Home-17 |

## 完整任务清单

任务名称保留论文英文，编号与环境 ID 精确对应；`是` 表示同时属于 EP-20。

| 论文编号 | 类型 | 论文任务名称 | 分割 | EP-20 | 环境 ID |
| --- | --- | --- | --- | --- | --- |
| Launch-02 | Launch-Aim | Single-target warm-up | Easy | 是 | `marble/dual-panda/A007` |
| Launch-03 | Launch-Aim | Long-range energy budget | Easy | — | `marble/dual-panda/A008` |
| Launch-04 | Launch-Aim | Elevated-platform shot | Easy | — | `marble/dual-panda/A009` |
| Launch-05 | Launch-Aim | Toppling timber gate | Easy | — | `marble/dual-panda/A010` |
| Launch-08 | Launch-Causal | Orchard rolling bodies | Easy | 是 | `marble/dual-panda/A017` |
| Launch-09 | Launch-Causal | One beam, two targets | Easy | — | `marble/dual-panda/A004` |
| Launch-10 | Launch-Causal | Light roof on three supports | Easy | — | `marble/dual-panda/A039` |
| Launch-11 | Launch-Causal | Gravity-driven stone at a low fort | Easy | — | `marble/dual-panda/A044` |
| Launch-12 | Launch-Causal | Whole arch and separate crown stone | Easy | — | `marble/dual-panda/A071` |
| Launch-15 | Launch-Causal | Breakable window in a fixed frame | Easy | — | `marble/dual-panda/A029` |
| Launch-21 | Launch-Glass | Rigid glass village | Easy | — | `marble/dual-panda/A018` |
| Launch-22 | Launch-Glass | Two glass layers | Easy | 是 | `marble/dual-panda/A025` |
| Launch-23 | Launch-Glass | Low lintel, high target | Easy | — | `marble/dual-panda/A064` |
| Launch-26 | Launch-Rules | Far target before near target | Easy | — | `marble/dual-panda/A026` |
| Launch-27 | Launch-Rules | Protect the garden neighbor | Easy | — | `marble/dual-panda/A028` |
| Launch-28 | Launch-Rules | Fire again with damage retained | Easy | — | `marble/dual-panda/A030` |
| Launch-32 | Launch-Rules | Numbered fan courtyard | Easy | — | `marble/dual-panda/A091` |
| Tower-01 | Tower-Plan | Top-ring transfer | Easy | — | `hanoi_panda/panda/H01` |
| Tower-02 | Tower-Plan | Local two-ring transfer | Easy | — | `hanoi_panda/panda/H02` |
| Tower-03 | Tower-Plan | Reassemble a distributed state | Easy | — | `hanoi_panda/panda/H03` |
| Tower-06 | Tower-Physics | Triangular transfer | Easy | 是 | `hanoi_panda/panda/H06` |
| Tower-07 | Tower-Physics | Low-to-high platform | Easy | — | `hanoi_panda/panda/H09` |
| Tower-09 | Tower-Physics | Light-ring lift | Easy | — | `hanoi_panda/panda/H17` |
| Tower-11 | Tower-Physics | Single tilted handle | Easy | — | `hanoi_panda/panda/H25` |
| Tower-14 | Tower-Dex | Top-ring transfer | Easy | — | `hanoi_floating/floating-sharpa/H01` |
| Tower-18 | Tower-Dex | Top-ring transfer | Easy | 是 | `hanoi_sharpa/fr3-sharpa/H01` |
| Tower-20 | Tower-Dex | Low-to-high platform | Easy | — | `hanoi_sharpa/fr3-sharpa/H09` |
| Tower-21 | Tower-Dex | Single tilted handle | Easy | — | `hanoi_sharpa/fr3-sharpa/H25` |
| Lock-02 | Lock-Assemble | Assemble key | Easy | — | `kongming_lock/dual-panda/A06` |
| Lock-03 | Lock-Assemble | Assemble key + bar | Easy | 是 | `kongming_lock/dual-panda/A11` |
| Lock-05 | Lock-Assemble | Assemble key | Easy | — | `kongming_lock/dual-panda/A09` |
| Lock-08 | Lock-Disassemble | Disassemble key | Easy | — | `kongming_lock/dual-panda/D06` |
| Lock-09 | Lock-Disassemble | Disassemble key + bar | Easy | — | `kongming_lock/dual-panda/D11` |
| Lock-11 | Lock-Disassemble | Disassemble key | Easy | — | `kongming_lock/dual-panda/D09` |
| Lock-14 | Lock-Dex | Assemble key | Easy | 是 | `kongming_lock/dual-floating-sharpa/A06` |
| Lock-16 | Lock-Dex | Disassemble key | Easy | — | `kongming_lock/dual-floating-sharpa/D06` |
| Cube-01 | Cube-Rubik | Solve scramble C01 | Easy | — | `rubiks_panda/panda/C01` |
| Cube-02 | Cube-Rubik | Solve scramble C02 | Easy | — | `rubiks_panda/panda/C02` |
| Cube-03 | Cube-Rubik | Solve scramble C03 | Easy | — | `rubiks_panda/panda/C03` |
| Cube-04 | Cube-Rubik | Solve scramble C01 | Easy | — | `rubiks_sharpa/floating-sharpa/C01` |
| Cube-09 | Cube-Pocket | Clockwise top turn | Easy | 是 | `pocket_cube/aloha/C01` |
| Cube-11 | Cube-Pocket | Half-turn in two stages | Easy | — | `pocket_cube/aloha/C08` |
| Home-01 | Home-Tidy | Three upright books onto the middle shelf | Easy | — | `bookshelf/dual-panda/BooksTableD1` |
| Home-02 | Home-Tidy | Unpack a neatly packed crate | Easy | — | `bookshelf/dual-panda/ShelfCrateD1` |
| Home-06 | Home-Long | Prepare a shared writing desk | Easy | 是 | `maniskill_long_horizon/fetch/L1` |
| Home-07 | Home-Long | Prepare a tea station for two | Easy | — | `maniskill_long_horizon/fetch/L3` |
| Home-11 | Home-Precise | Seat a keyed electronics connector | Easy | — | `maniskill_geometry/panda/P3` |
| Home-13 | Home-Precise | Insert a book into a narrow shelf gap | Easy | — | `maniskill_geometry/panda/P7` |
| Home-14 | Home-Dynamic | Stop a rolling orange | Easy | 是 | `maniskill_dynamics/panda/D1` |
| Home-17 | Home-Dynamic | Slide a puck into a scoring zone | Easy | — | `maniskill_dynamics/panda/D3` |
