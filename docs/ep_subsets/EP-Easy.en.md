[English](EP-Easy.en.md) · [简体中文](EP-Easy.zh-CN.md)

# EP-Easy definition

[Overview and sources](README.en.md) · [Machine-readable membership](tasks.json)

EP-Easy contains the lower-workload side of each EP-100 task type: 50 tasks covering all 16 types. It is disjoint from EP-Hard and their union is EP-100. It is not the globally easiest 50 catalog tasks and does not guarantee success for any model. Ten members enter EP-20. Use it to assess lower workload with a comparable task mix.

Definition: `paper-loaded-only-v1`.

## Size and use

| Tasks | Launch | Tower | Lock | Cube | Home | Groups | Conditions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 17 | 11 | 8 | 6 | 8 | 50 | 200 |

Counts fix access, observation, tools, budgets and base seed. Launch uses `loaded` only (first shot preloaded; subsequent shots still require reloading), others `default`; every task has four conditions. For reference, Pass@2 / Pass@5 / Pass@10 use at most 400 / 1000 / 2000 valid attempts respectively. Declare the limit before running, stop each condition at first success and report each requested cutoff separately; actual usage may be lower. Infrastructure exclusions are recorded separately.

Average four conditions per task, tasks within each suite, then the five suites equally (20% each). Do not pool all conditions for the headline score. See the [overview](README.en.md) for workload formulas, within-type split/tie rules, exception accounting and provenance.

## Type coverage

| Type | Tasks | Paper indices |
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

## Complete task list

Task names are preserved from the paper; indices map exactly to environment IDs. `Yes` marks EP-20 membership.

| Index | Type | Paper task name | Split | EP-20 | Environment ID |
| --- | --- | --- | --- | --- | --- |
| Launch-02 | Launch-Aim | Single-target warm-up | Easy | Yes | `marble/dual-panda/A007` |
| Launch-03 | Launch-Aim | Long-range energy budget | Easy | — | `marble/dual-panda/A008` |
| Launch-04 | Launch-Aim | Elevated-platform shot | Easy | — | `marble/dual-panda/A009` |
| Launch-05 | Launch-Aim | Toppling timber gate | Easy | — | `marble/dual-panda/A010` |
| Launch-08 | Launch-Causal | Orchard rolling bodies | Easy | Yes | `marble/dual-panda/A017` |
| Launch-09 | Launch-Causal | One beam, two targets | Easy | — | `marble/dual-panda/A004` |
| Launch-10 | Launch-Causal | Light roof on three supports | Easy | — | `marble/dual-panda/A039` |
| Launch-11 | Launch-Causal | Gravity-driven stone at a low fort | Easy | — | `marble/dual-panda/A044` |
| Launch-12 | Launch-Causal | Whole arch and separate crown stone | Easy | — | `marble/dual-panda/A071` |
| Launch-15 | Launch-Causal | Breakable window in a fixed frame | Easy | — | `marble/dual-panda/A029` |
| Launch-21 | Launch-Glass | Rigid glass village | Easy | — | `marble/dual-panda/A018` |
| Launch-22 | Launch-Glass | Two glass layers | Easy | Yes | `marble/dual-panda/A025` |
| Launch-23 | Launch-Glass | Low lintel, high target | Easy | — | `marble/dual-panda/A064` |
| Launch-26 | Launch-Rules | Far target before near target | Easy | — | `marble/dual-panda/A026` |
| Launch-27 | Launch-Rules | Protect the garden neighbor | Easy | — | `marble/dual-panda/A028` |
| Launch-28 | Launch-Rules | Fire again with damage retained | Easy | — | `marble/dual-panda/A030` |
| Launch-32 | Launch-Rules | Numbered fan courtyard | Easy | — | `marble/dual-panda/A091` |
| Tower-01 | Tower-Plan | Top-ring transfer | Easy | — | `hanoi_panda/panda/H01` |
| Tower-02 | Tower-Plan | Local two-ring transfer | Easy | — | `hanoi_panda/panda/H02` |
| Tower-03 | Tower-Plan | Reassemble a distributed state | Easy | — | `hanoi_panda/panda/H03` |
| Tower-06 | Tower-Physics | Triangular transfer | Easy | Yes | `hanoi_panda/panda/H06` |
| Tower-07 | Tower-Physics | Low-to-high platform | Easy | — | `hanoi_panda/panda/H09` |
| Tower-09 | Tower-Physics | Light-ring lift | Easy | — | `hanoi_panda/panda/H17` |
| Tower-11 | Tower-Physics | Single tilted handle | Easy | — | `hanoi_panda/panda/H25` |
| Tower-14 | Tower-Dex | Top-ring transfer | Easy | — | `hanoi_floating/floating-sharpa/H01` |
| Tower-18 | Tower-Dex | Top-ring transfer | Easy | Yes | `hanoi_sharpa/fr3-sharpa/H01` |
| Tower-20 | Tower-Dex | Low-to-high platform | Easy | — | `hanoi_sharpa/fr3-sharpa/H09` |
| Tower-21 | Tower-Dex | Single tilted handle | Easy | — | `hanoi_sharpa/fr3-sharpa/H25` |
| Lock-02 | Lock-Assemble | Assemble key | Easy | — | `kongming_lock/dual-panda/A06` |
| Lock-03 | Lock-Assemble | Assemble key + bar | Easy | Yes | `kongming_lock/dual-panda/A11` |
| Lock-05 | Lock-Assemble | Assemble key | Easy | — | `kongming_lock/dual-panda/A09` |
| Lock-08 | Lock-Disassemble | Disassemble key | Easy | — | `kongming_lock/dual-panda/D06` |
| Lock-09 | Lock-Disassemble | Disassemble key + bar | Easy | — | `kongming_lock/dual-panda/D11` |
| Lock-11 | Lock-Disassemble | Disassemble key | Easy | — | `kongming_lock/dual-panda/D09` |
| Lock-14 | Lock-Dex | Assemble key | Easy | Yes | `kongming_lock/dual-floating-sharpa/A06` |
| Lock-16 | Lock-Dex | Disassemble key | Easy | — | `kongming_lock/dual-floating-sharpa/D06` |
| Cube-01 | Cube-Rubik | Solve scramble C01 | Easy | — | `rubiks_panda/panda/C01` |
| Cube-02 | Cube-Rubik | Solve scramble C02 | Easy | — | `rubiks_panda/panda/C02` |
| Cube-03 | Cube-Rubik | Solve scramble C03 | Easy | — | `rubiks_panda/panda/C03` |
| Cube-04 | Cube-Rubik | Solve scramble C01 | Easy | — | `rubiks_sharpa/floating-sharpa/C01` |
| Cube-09 | Cube-Pocket | Clockwise top turn | Easy | Yes | `pocket_cube/aloha/C01` |
| Cube-11 | Cube-Pocket | Half-turn in two stages | Easy | — | `pocket_cube/aloha/C08` |
| Home-01 | Home-Tidy | Three upright books onto the middle shelf | Easy | — | `bookshelf/dual-panda/BooksTableD1` |
| Home-02 | Home-Tidy | Unpack a neatly packed crate | Easy | — | `bookshelf/dual-panda/ShelfCrateD1` |
| Home-06 | Home-Long | Prepare a shared writing desk | Easy | Yes | `maniskill_long_horizon/fetch/L1` |
| Home-07 | Home-Long | Prepare a tea station for two | Easy | — | `maniskill_long_horizon/fetch/L3` |
| Home-11 | Home-Precise | Seat a keyed electronics connector | Easy | — | `maniskill_geometry/panda/P3` |
| Home-13 | Home-Precise | Insert a book into a narrow shelf gap | Easy | — | `maniskill_geometry/panda/P7` |
| Home-14 | Home-Dynamic | Stop a rolling orange | Easy | Yes | `maniskill_dynamics/panda/D1` |
| Home-17 | Home-Dynamic | Slide a puck into a scoring zone | Easy | — | `maniskill_dynamics/panda/D3` |
