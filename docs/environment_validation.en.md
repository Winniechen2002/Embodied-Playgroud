# Environment validation

[简体中文](environment_validation.zh-CN.md) · [Documentation](README.en.md)

Validation checks environment implementation, asset loading, native actions and observations, scoring, permissions and episode lifecycle. It does not establish agent performance or prove that every seed is solvable. Engineering acceptance for this public source release has passed within the scope below.

## Engineering acceptance standard for this source release

On 2026-10-16, the maintainer approved the following executed, passing checks as the acceptance standard for this public source release. Engineering acceptance against this standard is **passed**.

| Check | Passing coverage |
| --- | --- |
| Source regression | 287 tests, zero failures and zero skips |
| Scorer endpoint fixtures | MuJoCo 100, Isaac 280 and ManiSkill 30: 410 tasks |
| Native installation and basic operation | Loading, stepping and finish checks for all 410 tasks; rendering checks for 10 Isaac categories, plus MuJoCo and ManiSkill rendering/gateway smoke checks |
| Default-condition physics | 100 MuJoCo tasks and 30 ManiSkill tasks |
| Documentation and public content | Bilingual protocol generation consistency, permission documentation, 1,438 local link targets and a static audit of 742 public files |
| Export usability | Independent source export, discovery of all 410 tasks and the MuJoCo A001 smoke check |

Native checks used existing isolated runtimes with validated versions on an NVIDIA RTX 4090 with driver 580.173.02. They are not a claim that every simulator was freshly installed on an empty machine. Scorer fixtures exercise constructed states; physics coverage is limited to the default conditions listed above; the exported package smoke check covers MuJoCo. Assets retain their original applicable licenses and attributions.

This standard applies to this public source release and does not require repeating the full condition matrix for release. Generated check reports belong in local output directories outside the repository and are not committed with the public source.

## Local checks

Prepare the three separate environments in the [installation guide](environment_installation.en.md). Run every command from the repository root using the interpreter for its backend. Do not run all backend scoring checks inside the MuJoCo environment.

### Catalog and protocol checks

Use the configured MuJoCo environment. These commands do not start native simulation:

```bash
python scripts/environment_release.py catalog --output /tmp/agentbench-catalog.json
python scripts/export_evaluation_protocol.py --check
```

Expect 410 catalog tasks and a protocol check confirming that generated documents and source hashes match.

### MuJoCo: 100 tasks

Use the MuJoCo environment from the installation guide, keeping `MUJOCO_GL=egl` and any required EGL vendor selection:

```bash
python scripts/validate_environment_contracts.py --backend mujoco --output /tmp/agentbench-mujoco-contracts.json
python scripts/environment_smoke.py --task-id marble/dual-panda/A001 --output /tmp/agentbench-mujoco-smoke.json
```

### Isaac: 280 tasks

Configure `ISAACSIM_PATH`, `ISAACLAB_PATH` and `AGENTBENCH_ISAAC_PYTHON`, then use the installation guide's wrapper for the separate Isaac environment. Bookshelf scoring fixtures require Torch from that environment:

```bash
bash scripts/run_isaac_binary.sh scripts/validate_environment_contracts.py --backend isaac --output /tmp/agentbench-isaac-contracts.json
bash scripts/run_isaac_binary.sh scripts/environment_smoke.py --task-id hanoi_panda/panda/H01 --output /tmp/agentbench-isaac-smoke.json
```

### ManiSkill: 30 tasks

Switch to the ManiSkill environment from the installation guide, extract its assets and set `AGENTBENCH_MANISKILL_ASSETS`:

```bash
python scripts/validate_environment_contracts.py --backend maniskill --output /tmp/agentbench-maniskill-contracts.json
python scripts/environment_smoke.py --task-id maniskill_long_horizon/fetch/L1 --output /tmp/agentbench-maniskill-smoke.json
```

Successful scoring reports have `run_status: completed` and `passed_fixture` for every selected task; successful smoke reports have `passed_probe`. Preserve errors and diagnostic details on failure. Saved ManiSkill initial/goal fixtures no longer store or validate task-definition hashes: scoring checks execute the current evaluator assertions directly. Removing hashes does not make physical or scoring assertions pass automatically.

Smoke checks exercise real observations, time advancement, repeated request IDs, finish behavior and process exit. A short probe is not a full-horizon or full-condition pass. Native Isaac checks require the configured GPU runtime; native ManiSkill checks require its separate dependencies, assets and Vulkan.

Use the backend-specific clean-installation scripts from the installation guide. The validators ignore materialized assets whose contents match their Git LFS index pointers. Real source, asset or staged changes still require a clean checkout before installation validation.

## Release checks and optional diagnostics

`environment_release.py check` and `build --candidate` use the source-release scope. Their required evidence covers the three native installations, assets, licenses, bilingual documentation, source regression, scorer fixtures, default-condition physics and export smoke checks. The full matrix and its local-contact qualification are separate diagnostics.

Pass locally collected evidence with `--evidence`; each required category needs a `passed` entry in `global_checks` and a nonempty measurement in `global_measurements`, bound to the current source identity. Missing, failed, stale or nonfinite evidence is rejected. Approval of this source release does not turn absent evidence into passing measurements.

Matrix generation and per-condition tools remain optional diagnostics. Use `environment_release.py check-matrix` or `environment_status.py` when needed to inspect evidence. Their full-matrix conclusions are not release prerequisites. Use each backend's simulator environment and keep generated results outside the repository.

## Contract changes

Action contracts record dimensions, limits, joint order, mappings and control/physics periods. A changed fingerprint can block discovery. `revalidate_action_contracts.py` accepts measured native captures only after checking coverage and unchanged semantics. Updating a fingerprint alone is insufficient to approve changed action behavior. Regenerate per-task protocol documents with `export_evaluation_protocol.py` after an approved contract change.
