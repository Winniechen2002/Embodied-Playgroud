# 资产与许可

[English](environment_assets.en.md) · [文档](README.zh-CN.md)

项目授权适用于[许可范围](../LICENSING.md)中的原创内容：原创代码使用 Apache-2.0，原创文档与独立自制非代码资产使用 CC BY 4.0。第三方内容保留其自身条款；文件位置、格式转换或公开可见不证明项目所有权或再分发许可。

保留[第三方通知](../THIRD_PARTY_NOTICES.md)、相邻许可文本与 `UPSTREAM.json`。这些记录标明固定来源修订、文件哈希与许可范围。已确认的 Sharpa 手部组件文件固定到上游修订 `6eea427eb24189519f32b9f21674cd534d3f973c`；该范围不覆盖全部组合机器人、转接件或转换网格。

ManiSkill 打包了 444 个具有完整性记录的文件，必须保留清单与内嵌通知。原生机器人资产、YCB、Google Scanned Objects、RoboCasa/Lightwheel 与转换机器人组件保留各自原有适用许可证。[资产许可清单](../env/runtime/license-decisions.json)记录维护者分发决定与各项许可范围。

维护者于 2026-10-16 确认完整随附资产包可按原有适用许可证分发，包括组合机器人、转接件、转换网格及 ManiSkill 资产。此决定保留上游条款与通知，属于维护者批准，不代表独立法律审计。Isaac Sim 依 NVIDIA 条款单独获取；可选视觉与规划仓库不作为本源码版本的捆绑依赖。

运行以下命令生成包含内容及已有通知的清单：

```bash
python scripts/environment_release.py audit --output /tmp/agentbench-public-content.json
```

审计检查文件身份、LFS 实体文件、静态导入、本地链接和内嵌资产完整性。它不能依据哈希确认权利，也不能证明动态导入、原生资产加载或干净安装已通过。审计分别报告已记录的维护者分发批准与工程验收状态。
