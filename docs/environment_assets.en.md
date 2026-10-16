# Assets and licensing

[简体中文](environment_assets.zh-CN.md) · [Documentation](README.en.md)

The project grant covers original material as described in [LICENSING.md](../LICENSING.md). Original code uses Apache-2.0; original documentation and independently authored non-code assets use CC BY 4.0. Third-party material retains its own terms. File location, conversion or public availability does not establish project ownership or redistribution permission.

Retain [third-party notices](../THIRD_PARTY_NOTICES.md), adjacent license texts and `UPSTREAM.json` records. These records identify pinned source revisions, file hashes and license scope. The known Sharpa hand component files are pinned to upstream revision `6eea427eb24189519f32b9f21674cd534d3f973c`; this does not cover every combined robot, adapter or converted mesh.

ManiSkill bundles 444 integrity-recorded files. Its manifest and embedded notices must remain intact. Native robot assets, YCB, Google Scanned Objects, RoboCasa/Lightwheel and converted robot components retain their original applicable licenses. The [asset license inventory](../env/runtime/license-decisions.json) records the maintainer distribution decision and these individual scopes.

On 2026-10-16, the maintainer approved distribution of the complete included asset bundle, including combined robots, adapters, converted meshes and ManiSkill assets, under their original applicable licenses. This decision preserves upstream terms and notices and is not an independent legal audit. Isaac Sim is obtained separately under NVIDIA terms. Optional perception and planning repositories are not bundled dependencies of this source distribution.

For an inventory of included content and available notices, run:

```bash
python scripts/environment_release.py audit --output /tmp/agentbench-public-content.json
```

The audit checks file identities, LFS materialization, static imports, local links and embedded asset integrity. It cannot establish rights from file hashes or certify dynamic imports, native asset loading or clean installation. The audit reports the recorded maintainer approval separately from engineering qualification.
