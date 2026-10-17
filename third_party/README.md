# Embedded third-party sources / 内嵌第三方源码

These are regular source snapshots from Agent-Bench's 17 pinned repositories,
including 16 nested dependencies. No submodule initialization is needed. See
[manifest.json](manifest.json) for exact revisions, source URLs, file identities
and retained license files. Check the snapshot offline with:

```bash
python scripts/check_embedded_sources.py
```

Run this command from the repository root. Install each tool's declared build and
runtime dependencies in its own environment; inclusion does not install a tool
or grant it evaluation access. Tool use follows the [capability rules](../rules/rules.en.md).

Git metadata, local caches and untracked files were not copied. Tracked upstream
examples and data are retained. Two upstream symbolic links are materialized as
ordinary files/directories. Upstream `.gitattributes` files are retained as
`.gitattributes.upstream`; the release controls its own LFS handling. Six Boost
Math HTML documents bundled by SciPy have unused Mapbox access tokens removed
from Plotly chart configuration. Their manifest entries record `modification`,
`upstream_sha256` and `upstream_bytes`, alongside the sanitized file identities.
All other included upstream regular files retain their original bytes.

One documentation image, `Depth-Anything-3/assets/images/da3_teaser.png`, is absent:
the pinned LFS object returns HTTP 404 upstream. Its identity is recorded in
`unavailable_lfs`; no pointer or replacement image is shipped. Runtime source is
present. This inventory does not claim that every optional tool has passed GPU
inference or that separately downloaded checkpoints are bundled.

Each component retains its original terms; the project Apache-2.0 / CC BY 4.0
licenses do not cover third-party material. GenDexGrasp, DexGraspNet2 and STREAM3D
have no repository-level license file at these revisions. Their inclusion records
a source snapshot and does not grant redistribution or commercial-use rights.
Check the upstream terms before using or redistributing a component. See also
[third-party notices](../THIRD_PARTY_NOTICES.md).

这里是 Agent-Bench 固定的 17 个项目及 16 个嵌套依赖的实际源码，无需初始化子模块。
版本、来源、文件校验值及许可路径见清单。各工具仍需独立安装依赖，并按能力等级明确授权。
未复制 Git 元数据、本地缓存或未跟踪文件；保留上游已跟踪示例与数据。
两个符号链接已展开为普通文件／目录；上游 Git 属性保存为 `.gitattributes.upstream`。
SciPy 附带的六份 Boost Math HTML 文档已移除 Plotly 配置中未使用的 Mapbox 访问 token。
对应清单条目保留 `modification`、`upstream_sha256`、`upstream_bytes`，并记录清理后的文件校验值。
其余随附上游普通文件字节保持不变。

唯一缺失项为 Depth-Anything-3 的文档展示图片 `assets/images/da3_teaser.png`，
上游固定 LFS 对象返回 HTTP 404；清单保留其身份，不发布失效指针。运行源码已包含。
内嵌不代表所有工具已通过 GPU 推理验证，也不代表需要另行下载的检查点已经包含。
GenDexGrasp、DexGraspNet2 与 STREAM3D 在这些修订中没有仓库级许可文件；
内嵌不授予再分发或商业使用权。所有第三方条款保持原样，不适用本项目的原创内容许可。

| Project / 项目 | Revision / 修订 | Original terms / 原条款 |
| --- | --- | --- |
| [CEDex-Grasp](CEDex-Grasp) | `ef59a9fbec062b5aeedf3b7ee7e3f535718bc5a6` | [LICENSE](CEDex-Grasp/LICENSE) |
| [Depth-Anything-3](Depth-Anything-3) | `3d835ec1a5802d64a8b8b15f817a1ab54809bfe4` | [LICENSE](Depth-Anything-3/LICENSE) |
| [GenDexGrasp](GenDexGrasp) | `29fe7efc558b8cc3ce2d8e67c9c22b014adc21c7` | No repository-level license file / 无仓库级许可文件 |
| [MinkowskiEngine](MinkowskiEngine) | `9f81ae66b33b883cd08ee4f64d08cf633608b118` | [LICENSE](MinkowskiEngine/LICENSE) |
| [STREAM3D](STREAM3D) | `be551cc756f5710875ec1c6a4c0fa545b56d2c4f` | No repository-level license file / 无仓库级许可文件 |
| [curobo](curobo) | `4ea77366ca48ee453e7df139e39fa6532af49f3b` | [LICENSE](curobo/LICENSE), [LICENSE_ASSETS](curobo/LICENSE_ASSETS), [LICENSE](curobo/curobo/content/assets/robot/franka_description/LICENSE), [LICENSE](curobo/curobo/content/assets/robot/g1/LICENSE), [LICENSE](curobo/curobo/content/assets/robot/ur_description/LICENSE) |
| [curobo-v1](curobo-v1) | `d64c4b005459db10c5dd867d8b30a87d5bda9bdb` | [LICENSE](curobo-v1/LICENSE), [LICENSE_ASSETS](curobo-v1/LICENSE_ASSETS), [LICENSE](curobo-v1/src/curobo/content/assets/robot/kinova/kortex_description/grippers/robotiq_2f_140/LICENSE), [LICENSE](curobo-v1/src/curobo/content/assets/robot/kinova/kortex_description/grippers/robotiq_2f_85/LICENSE) |
| [dexgraspnet2](dexgraspnet2) | `26ecd76121e3c8218ad53db9840cf34f6b81b076` | No repository-level license file / 无仓库级许可文件 |
| [graspnet-baseline](graspnet-baseline) | `280c215129f759ed8649cb4e89fc5dfee55f4f80` | [LICENSE](graspnet-baseline/LICENSE) |
| [ml-depth-pro](ml-depth-pro) | `9efe5c1def37a26c5367a71df664b18e1306c708` | [LICENSE](ml-depth-pro/LICENSE) |
| [ompl](ompl) | `96b7b9c2c62f80570b5b93e03a95d56dea8410d9` | [LICENSE](ompl/LICENSE), [license.md](ompl/doc/markdown/license.md) |
| [optuna](optuna) | `4db42e31c24b200e52595df9d4c00e2cdeefea2b` | [LICENSE](optuna/LICENSE), [LICENSE_THIRD_PARTY](optuna/LICENSE_THIRD_PARTY), [license_thirdparty.rst](optuna/docs/source/license_thirdparty.rst) |
| [pinocchio](pinocchio) | `0caf0ca4d07e63834cdc420c703993662c59e01b` | [COPYING.LESSER](pinocchio/COPYING.LESSER) |
| [pyroki](pyroki) | `388e43e1fc0d0ee382968d3dd72970fd62a0450c` | [LICENSE](pyroki/LICENSE) |
| [rsl_rl](rsl_rl) | `3ac56acd3376f2952eb636a133f4b5aa30142552` | [LICENSE_HEADER.txt](rsl_rl/.github/LICENSE_HEADER.txt), [LICENSE](rsl_rl/LICENSE) |
| [sam-3d-objects](sam-3d-objects) | `f91db411c50efee93d8db7aeb323885650f6f722` | [LICENSE](sam-3d-objects/LICENSE) |
| [scipy](scipy) | `e29dcb65a2040f04819b426a04b60d44a8f69c04` | [LICENSE.txt](scipy/LICENSE.txt), [LICENSES_bundled.txt](scipy/LICENSES_bundled.txt), [LICENSE.txt](scipy/scipy/_build_utils/tempita/LICENSE.txt), [LICENSE](scipy/scipy/_lib/_uarray/LICENSE), [LICENSE.md](scipy/scipy/fft/_pocketfft/LICENSE.md) |
