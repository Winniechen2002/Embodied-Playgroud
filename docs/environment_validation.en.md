# Environment validation

[简体中文](environment_validation.zh-CN.md) · [Documentation](README.en.md)

Validation checks environment implementation, asset loading, native actions and observations, scoring, permissions and episode lifecycle. It does not establish agent performance or prove that every seed is solvable. Complete engineering qualification remains incomplete.

## Local checks

Use the simulator-specific environment from the [installation guide](environment_installation.en.md). Run CPU-only contract checks before native checks:

```bash
python scripts/environment_release.py catalog --output /tmp/agentbench-catalog.json
python scripts/validate_environment_contracts.py --output /tmp/agentbench-contracts.json
python scripts/environment_release.py matrix --matrix union --output /tmp/agentbench-conditions.json
python scripts/environment_smoke.py --task-id marble/dual-panda/A001 --output /tmp/agentbench-smoke.json
```

The catalog contains 410 tasks. Smoke checks exercise real observations, time advancement, repeated request IDs, finish behavior and process exit. A short probe is not a full-horizon or full-condition pass. Native Isaac checks require the configured GPU runtime; ManiSkill checks require its separate dependencies and assets.

## Engineering condition matrix

The matrix version is `environment-conditions-v3`:

| Selection | Unique conditions | Memberships |
| --- | ---: | ---: |
| legacy | 4,970 | 4,970 |
| protocol, base seeds 0/1/2 | 5,160 | 6,120 |
| union | 9,390 | 11,090 |

Memberships retain overlaps between groups. These engineering counts are distinct from the paper evaluation denominators. The general base-seed-0 schedule includes loaded and ground initialization: 510 groups and 2,040 conditions. The paper's loaded-only setting has 410 groups and 1,640 conditions; EP-100 has 400 conditions. See [EP definitions](ep_subsets/README.en.md).

Matrix tools include `validate_environment_physics.py`, `validate_isaac_environments.py` and `validate_maniskill_environments.py`. Use each tool's `--help` and its correct simulator runtime. Preserve exact selected conditions, source identity and budgets when resuming. A changed source requires new evidence.

## Acceptance and limitations

Required checks cover contracts, necessary geometry, physics, native actions/observations, scoring, four permission levels, lifecycle and repeat initialization. Static scenes require at least 2 seconds settling and 3 seconds holding; specified support scenes retain full-horizon checks. Dynamic checks cover triggers, contacts, finite state and termination. An expected no-action task failure is not by itself an environment defect.

Records bind actual initialization, source/catalog/assets/scorer versions, physical steps, measured quantities and failure causes. Unknown conditions, duplicates, stale sources, skips, missing measurements or insufficient duration cannot pass the gate. `passed_probe` is partial evidence. Full qualification also requires clean-installation checks, asset provenance and licensing review.

The source tree is prepared for review; it does not assert `environment_qualified`, `source_release_ready` or completed distribution validation. Runtime compatibility, native installation probes, complete engineering qualification and redistribution rights are separate claims. Preserve these distinctions when reporting checks.

## Contract changes

Action contracts record dimensions, limits, joint order, mappings and control/physics periods. A changed fingerprint can block discovery. `revalidate_action_contracts.py` accepts measured native captures only after checking coverage and unchanged semantics. Updating a fingerprint alone is insufficient to approve changed action behavior. Regenerate per-task protocol documents with `export_evaluation_protocol.py` after an approved contract change.
