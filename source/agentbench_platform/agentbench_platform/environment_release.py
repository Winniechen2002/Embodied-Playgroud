"""Allowlisted environment distribution and fail-closed release gates."""
from collections import Counter
import ast
import hashlib
import json
import re
from pathlib import Path
from .environment_catalog import ROOT,catalog,digest
from .profiles import CAPABILITY_VERSION

CHECKS=('contract','necessary_geometry','physics','action_observation','scorer','gateway_l0',
        'gateway_l1','gateway_l2','gateway_l3','lifecycle','repeat_initialization')
GLOBAL_CHECKS=('clean_install_mujoco','clean_install_isaac','clean_install_maniskill','assets','licenses','bilingual_docs','local_contact')
SOURCE_ROOTS=('source/agentbench','source/agentbench_platform','source/agentbench_sdk','env/maniskill_lgd')
SCRIPT_NAMES=('environment_runtime.py','environment_release.py','environment_smoke.py',
    'environment_client.py','franka_marble_test_protocol.py','check_tool_policy_docs.py','validate_environment_physics.py','agentbench_platform_runtime.py','generate_hanoi_ring_assets.py','validate_isaac_environments.py','export_evaluation_protocol.py','validate_environment_contracts.py','environment_status.py','validate_source_installation.py','revalidate_action_contracts.py','validate_maniskill_environments.py','validate_maniskill_fixtures.py','check_maniskill_dynamics.py','validate_isaac_installation.py','run_isaac_binary.sh','isaac_binary_bootstrap/sitecustomize.py')
EXCLUDED_NAMES={'__pycache__','.pytest_cache','.git','.codex-local','outputs','output','baselines','tests','build','dist'}
EXCLUDED_MODULES={'model_proxy.py','controller.py','baseline.py','campaign_baseline.py','dual_baseline.py','joint_planner.py','panda_kinematics.py'}
PLATFORM_EXCLUDES={'runner.py','adapters.py','image_build.py','sandbox.py','rubiks_suite.py','cube_solver.py','native_video.py','dual_native_video.py','sampled_video.py'}
BASELINE_WRAPPERS={'kongming_lock/assembly_oracle.py','kongming_lock/oracle.py',
                   'kongming_lock/key_slot.py','kongming_lock/geometry.py','rubiks_cube/rubiks_cube_arm_plan.py',
                   'rubiks_cube/rubiks_cube_route.py','rubiks_cube/rubiks_cube_solver.py',
                   'rubiks_cube/rubiks_cube_continuous_plan.py','rubiks_cube/rubiks_cube_planner.py',
                   'rubiks_cube/rubiks_cube_session.py','rubiks_cube/rubiks_cube_reconcile.py',
                   'rubiks_cube/rubiks_cube_reorientation.py','rubiks_cube/rubiks_cube_continuous_pose.py'}
ALLOWED_SUFFIXES={'.py','.toml','.cfg','.json','.usd','.usda','.usdc','.stl','.obj','.mtl',
    '.dae','.png','.jpg','.jpeg','.hdr','.exr','.urdf','.xacro','.ply','.pts','.xml','.txt','.yaml','.yml','.mesh','.glb','.gltf','.bin'}
SCENE_MODULES={'campaign_scene.py','redesigned_levels.py','benchmark_levels.py',
               'multilevel_levels.py','defense_levels.py','atlas_levels_a.py','atlas_levels_b.py'}
MUJOCO_REQUIREMENTS='mujoco==3.3.7\ngymnasium==1.2.1\nnumpy==1.26.4\nPillow==11.3.0\nscipy==1.15.3\n'


def export_content(relative, content):
    """Omit stored shot suggestions while retaining the physical scene definitions.

    Only the independent distribution is transformed. The development source and
    experiment provenance remain untouched. Runtime case identities hash physical
    configuration rather than these authoring hints.
    """
    path=Path(relative)
    if path.name.upper().startswith('UPSTREAM') and path.suffix=='.md':
        # Repository-added navigation is not part of the upstream attribution.
        return re.sub(rb'<!-- bilingual-navigation:start -->.*?<!-- bilingual-navigation:end -->\s*',
            b'',content,flags=re.S)
    if 'agentbench_mujoco' not in path.parts or path.name not in SCENE_MODULES:
        return content
    class PhysicalOnly(ast.NodeTransformer):
        def visit_Call(self,node):
            self.generic_visit(node)
            if isinstance(node.func,ast.Name) and node.func.id=='dict':
                node.keywords=[kw for kw in node.keywords if kw.arg not in {'plan','yaw_plan','reference'}]
            return node
        def visit_Dict(self,node):
            self.generic_visit(node)
            pairs=[(k,v) for k,v in zip(node.keys,node.values)
                   if not isinstance(k,ast.Constant) or k.value not in {'plan','yaw_plan','reference'}]
            node.keys=[k for k,v in pairs];node.values=[v for k,v in pairs]
            return node
    source=content.decode();tree=PhysicalOnly().visit(ast.parse(source))
    if tree.body and isinstance(tree.body[0],ast.Expr) and isinstance(tree.body[0].value,ast.Constant) and isinstance(tree.body[0].value.value,str):
        tree.body[0].value.value='Physical environment definitions for the independent distribution.'
    notices=[line for line in source.splitlines() if line.lstrip().startswith('#') and
             ('copyright' in line.lower() or 'SPDX' in line)]
    return ('\n'.join(notices+[ast.unparse(ast.fix_missing_locations(tree))])+'\n').encode()


def source_files(root=ROOT):
    """Enumerate individual files; no directory copy can include experiment artifacts."""
    root=Path(root)
    files=[]
    for prefix in SOURCE_ROOTS:
        for path in (root/prefix).rglob('*'):
            rel=path.relative_to(root)
            if any(part in EXCLUDED_NAMES or part.endswith('.egg-info') for part in rel.parts):continue
            if prefix=='env/maniskill_lgd' and any(part in ('verification','previews') for part in rel.parts):continue
            if 'evidence' in rel.parts and path.name not in {'initial_state.json','goal_fixture_state.json'}:continue
            if path.is_symlink():raise ValueError(f'Symlink in release input: {rel}')
            if not path.is_file() or path.name in EXCLUDED_MODULES:continue
            if prefix.endswith('agentbench_platform') and path.name in PLATFORM_EXCLUDES:continue
            if '/'.join(rel.parts[-2:]) in BASELINE_WRAPPERS:continue
            # These are reference-controller/calibration modules, not the native
            # Sharpa environment. Keep the native configuration and SDK adapter.
            if path.name.startswith('rubiks_cube_sharpa_') and path.name not in {
                    'rubiks_cube_sharpa_cfg.py','rubiks_cube_sharpa_benchmark.py'}:continue
            if path.name!='assets.tar.gz' and path.suffix.lower() not in ALLOWED_SUFFIXES and not path.name.upper().startswith(('LICENSE','NOTICE','COPYING','UPSTREAM','ATTRIBUTION','AUTHORS')):continue
            if path.name.upper().startswith(('README','CHANGELOG')):continue
            files.append(rel)
    files.extend(Path('scripts')/name for name in SCRIPT_NAMES if (root/'scripts'/name).is_file())
    for folder in ('tests/environment_release','tests/benchmark_platform'):
        files.extend(p.relative_to(root) for p in (root/folder).glob('test_*.py'))
    policy_test=root/'tests/test_tool_policy_docs.py'
    if policy_test.is_file():files.append(policy_test.relative_to(root))
    files.extend(p.relative_to(root) for p in (root/'env/runtime').glob('*') if p.suffix in ('.json','.txt'))
    files.extend(Path(name) for name in ('LICENSE','NOTICE','LICENSING.md','THIRD_PARTY_NOTICES.md',
                                       '.gitignore','.gitattributes','pyproject.toml','pytest.ini')
                 if (root/name).is_file())
    files.extend(p.relative_to(root) for p in (root/'LICENSES').glob('*.txt'))
    files.extend(p.relative_to(root) for p in (root/'.github/workflows').glob('*.yml'))
    # Upstream pins may require dotfiles or original README attribution that the
    # general source suffix filter excludes. Preserve exactly those declarations.
    for relative in tuple(files):
        if relative.name!='UPSTREAM.json':continue
        declaration=json.loads((root/relative).read_text())
        for name in declaration.get('files',{}):
            target=root/relative.parent/name
            if not target.resolve().is_relative_to(root.resolve()) or target.is_symlink():
                raise ValueError(f'Unsafe upstream dependency: {relative}: {name}')
            if not target.is_file():raise ValueError(f'Missing upstream dependency: {relative}: {name}')
            files.append(target.relative_to(root))
    return sorted(set(files))


def inventory(root=ROOT):
    rows={}
    from .public_content import public_files
    for relative in public_files(root):
        path=Path(root)/relative
        content=path.read_bytes()
        if content.startswith(b'version https://git-lfs.github.com/spec/v1'):
            raise ValueError(f'Unresolved LFS asset: {relative}')
        rows[str(relative)]={'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)}
    return rows


def license_inventory(files,root=ROOT):
    """Record actual notices and unresolved author declarations without relicensing."""
    notices={name:record for name,record in files.items()
             if Path(name).name.upper().startswith(('LICENSE','NOTICE','COPYING'))
             or name.startswith('LICENSES/') or name=='THIRD_PARTY_NOTICES.md'}
    source=(Path(root)/'source/agentbench/setup.py').read_text()
    issues=[]
    decision_path=Path(root)/'env/runtime/license-decisions.json'
    project=json.loads(decision_path.read_text()).get('project',{}) if decision_path.is_file() else {}
    scope_path=Path(root)/'LICENSING.md'
    scope=scope_path.read_text() if scope_path.is_file() else ''
    scoped=(project.get('status')=='confirmed' and project.get('copyright_holder')
            and project.get('selected_license')=='Apache-2.0'
            and project.get('non_code_license')=='CC-BY-4.0'
            and 'source/agentbench/setup.py' in scope and 'BSD-3-Clause' in scope
            and (Path(root)/'LICENSES/IsaacLab-BSD-3-Clause.txt').is_file()
            and (Path(root)/'LICENSES/CC-BY-4.0.txt').is_file())
    if 'SPDX-License-Identifier: BSD-3-Clause' in source and 'license="Apache-2.0"' in source and not scoped:
        issues.append('Inherited BSD-3-Clause file and Apache-2.0 package scope require an explicit project license declaration')
    if not any((Path(root)/name).is_file() for name in ('LICENSE','LICENSE.txt','LICENSE.md','COPYING')):
        issues.append('No repository-level license text found; project redistribution grant requires maintainer confirmation')
    return dict(status='unqualified',notices=notices,issues=issues,
        project_license='confirmed' if scoped else 'unconfirmed',
        copyright_holder=project.get('copyright_holder'),
        third_party_redistribution='requires_individual_review',
        scope='Notice inventory only; every redistributed asset still requires provenance verification')


def bilingual_checks():
    numbers=lambda s:Counter(re.findall(r'\d+(?:\.\d+)*',s))
    commands=lambda s:re.findall(r'`(python [^`]+)`',s)
    checks=dict(numeric_tokens=numbers(EN)==numbers(ZH),commands=commands(EN)==commands(ZH),
        capability_version=CAPABILITY_VERSION in EN and CAPABILITY_VERSION in ZH,
        script_paths=all((ROOT/command.split()[1]).is_file() for command in commands(EN)))
    if not all(checks.values()):raise ValueError('Bilingual release README mismatch')
    return dict(scope='release_readme_pair',checks=checks,
        bodies={name:hashlib.sha256(body.encode()).hexdigest() for name,body in [('en',EN),('zh-CN',ZH)]},
        limitation='Numeric, command and version checks do not replace a complete per-task semantic review')


def matrix(manifest, selection='union'):
    from .environment_matrix import matrix as generate
    return generate(manifest, selection)


def evidence_identity(manifest, files):
    from .environment_matrix import VERSION
    from .public_content import public_files
    documentation={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        for name in public_files() if name.endswith('.md') or name.startswith('docs/')}
    assets = {k:v for k,v in files.items() if Path(k).suffix.lower() not in ('.py','.md','.toml','.cfg','.txt')}
    scorers = {k:v for k,v in files.items() if Path(k).suffix == '.py'}
    return dict(source_digest=digest(files), catalog_digest=digest(manifest), documentation_digest=digest(documentation),
        asset_digest=digest(assets), scorer_digest=digest(scorers),
        matrix_version=VERSION, matrix_digest=digest(matrix(manifest)),
        capability_profile_version=CAPABILITY_VERSION)


def gate(manifest,files,evidence):
    """Fail closed on stale, unknown, duplicate or incomplete maintainer evidence.

    Labels alone never qualify an environment. Evidence remains trusted owner
    input; this validator is not a signature or a hostile-report attestation.
    """
    import math
    missing=[]; expected=matrix(manifest); identity=evidence_identity(manifest,files)
    for name,value in identity.items():
        if evidence.get(name)!=value:missing.append(name)
    observed={}; expected_keys={r['key'] for r in expected}
    for row in evidence.get('cases',[]):
        key=row.get('key')
        if key in observed:missing.append('duplicate:'+str(key))
        observed[key]=row
    if set(observed)-expected_keys:missing.append('unknown_case')
    def finite(value):
        return type(value) in (int,float) and math.isfinite(value)
    def valid_measurement(value):
        if type(value) is float:return math.isfinite(value)
        if isinstance(value,dict):return all(isinstance(k,str) and valid_measurement(v) for k,v in value.items())
        if isinstance(value,list):return all(valid_measurement(v) for v in value)
        return value is None or type(value) in (str,int,bool)
    per_task={t['id']:dict(required=0,qualified=0,failed=0,missing=0) for t in manifest['tasks']}
    for wanted in expected:
        count=per_task[wanted['task_id']];count['required']+=1
        row=observed.get(wanted['key'],{}); before=len(missing)
        failures=[check for check in CHECKS if row.get('checks',{}).get(check)!='passed']
        if failures:missing.append(dict(task_id=wanted['task_id'],condition=wanted['condition'],checks=failures))
        if row:
            for field in ('task_id','condition','configuration_sha256'):
                if row.get(field)!=wanted[field]:missing.append('mismatched_'+field+':'+wanted['key'])
            if row.get('actual_initialization')!=wanted['condition']:
                missing.append('initialization_mismatch:'+wanted['key'])
            if row.get('versions')!=identity:missing.append('stale_case_versions:'+wanted['key'])
            if row.get('status')!='passed':missing.append('case_not_qualified:'+wanted['key'])
            for check in CHECKS:
                measure=row.get('measurements',{}).get(check)
                if not isinstance(measure,dict) or not measure or not valid_measurement(measure):
                    missing.append('missing_measurement:'+wanted['key']+':'+check)
        if not failures:
            steps=row.get('physics_steps'); settle=row.get('settle_seconds'); hold=row.get('hold_seconds')
            seconds=row.get('no_operation_seconds'); hz=wanted['condition']['budgets']['physics_hz']
            minimum=wanted['episode_time_limit_seconds'] if wanted['full_horizon_stability'] else 5.
            dynamic=wanted.get('physics_acceptance')=='expected_dynamics'
            duration_invalid=(not finite(settle) or settle<2 or not finite(hold) or hold<3) if not dynamic else False
            if dynamic:
                physics=row.get('measurements',{}).get('physics',{})
                for audit in ('trigger_audit','contact_audit','terminal_audit'):
                    if not isinstance(physics.get(audit),dict) or not physics[audit] or physics[audit].get('passed') is not True:
                        missing.append('incomplete_dynamic_'+audit+':'+wanted['key'])
            if (type(steps) is not int or steps < round(minimum*hz) or duration_invalid
                    or not finite(seconds) or seconds<minimum-1e-6
                    or not isinstance(row.get('runtime'),dict) or not row['runtime']):
                missing.append('incomplete_native_measurement:'+wanted['key'])
            if wanted['full_horizon_stability'] and (not finite(seconds) or seconds<minimum-1e-6):
                missing.append('missing_full_horizon_stability:'+wanted['key'])
        if len(missing)==before:count['qualified']+=1
        elif not row:count['missing']+=1
        else:count['failed']+=1
    environmental_missing=list(missing)
    for check in GLOBAL_CHECKS:
        before=len(missing)
        if evidence.get('global_checks',{}).get(check)!='passed':missing.append(check)
        proof=evidence.get('global_measurements',{}).get(check,{})
        if (not isinstance(proof,dict) or proof.get('versions')!=identity
                or not set(proof)-{'versions'} or not valid_measurement(proof)):
            missing.append('missing_global_measurement:'+check)
        if check=='local_contact':environmental_missing.extend(missing[before:])
    return dict(schema_version=2,release_ready=not missing,
        environment_qualified=not environmental_missing,
        source_release_ready=not missing,distribution_validation='not_executed',
        task_count=manifest['count'],required_case_count=len(expected),missing=missing,
        tasks=per_task,scope='environment_quality_only',**identity)


EN='''# Embodied Playground environment distribution

Embodied Playground is the paper-facing benchmark name; Agent-bench repository,
package, environment and command identifiers retain their existing spelling.
The paper uses loaded-only Launcher initialization: 410 tasks / 1640 conditions
for the full catalog. EP-100, EP-Easy, EP-Hard and EP-20 contain 100/50/50/20
tasks and 400/200/200/80 conditions. Each task has four conditions and the five
suites (Launch, Tower, Lock, Cube, Home) receive equal score weight. The runtime
also supports ground; its general schedule retains 510 groups / 2040 conditions.

This distribution contains 410 task/robot entries, their assets, physical task
interfaces, scoring functions and a Level 0–3 permission gateway. It contains no
model evaluations, completion tables, controller trajectories or leaderboards.
Engineering checks concern environment operation and necessary feasibility
conditions; they are not demonstrations of solving every task or seed.

## Installation

Keep the source tree layout. For the CPU MuJoCo backend, use Python 3.11 and
install `mujoco==3.3.7`, `gymnasium==1.2.1`, `numpy==1.26.4`, `Pillow==11.3.0`,
`scipy==1.15.3`, then add `source/agentbench`, `source/agentbench_platform` and
`source/agentbench_sdk` to PYTHONPATH. No model weights or planning stack are
required. Isaac environments require a separately installed Isaac Sim / Isaac Lab
runtime; consult runtime-qualification.json for the exact qualified versions.
An unqualified runtime must not be represented as supported.

## Discover and launch

`python scripts/environment_release.py catalog --output catalog.json`

`python scripts/environment_runtime.py --task-id marble/dual-panda/A001 --capability-level 0 --headless --output /tmp/agentbench-episode`

In another terminal: `python scripts/environment_client.py /tmp/agentbench-episode/session.json`

The owner keeps the environment source and assets. Give a client only its SDK,
session and public description; an open-source distribution is not itself an
isolated evaluation sandbox. Keep the printed session file private. The SDK uses
`describe`, `observe`, `step`, `finish` and resource IDs, never server paths.
Descriptions declare native action dimensions, bounds, units, target and camera
metadata. Observe does not advance simulation. Only the owner may initialize or
reset; no client reset or state-write endpoint exists. Physics success and
violations are environment outputs, not published model results.

## Capability profiles

Version: `2026-10-09-environment-l0-l3`. Difficulty is independent of permissions.
L0 permits Python, standard library, NumPy, Pillow and self-authored dynamics,
IK and planning algorithms. No prebuilt dynamics/IK/planning domain tools or
external vision/grasp models are granted. L1 additionally permits explicitly
authorized perception, geometry, IK/planning and observation-derived proxy tools.
L2 adds explicitly authorized pretrained grasp/contact tools. L3 adds the
interface's privileged read-only fields, never direct writes or extra resets.
Higher levels do not install or grant tools automatically. This distribution's
minimal launcher grants no optional tools; installed tool workers are configured
and granted by the owner through the platform interface.
The gateway enforces its own access boundary, not all libraries in an arbitrary
external client. Model token/image accounting is outside this environment release.

## Physical contracts

Hanoi uses legal top-ring moves, 22 mm XY / 16 mm Z seating tolerances, 5 mm
visible-shell penetration and a continuous 1-second final hold. Pocket Cube
requires the configured target state and committed turns, <=1 degree detent
error, speed <0.05 rad/s, a continuous 1-second hold, unchanged fixed physics,
and <=0.25 mm visible-shell penetration. Panda Rubik uses explicitly assisted
hybrid_fixture_v1 mechanics. Sharpa Rubik uses the same declared constraint
mechanism with 28 native joints and five fingertip contact sensors. Both task
scorers require native physical evidence; full-case qualification remains pending.
Neither is described as unassisted free manipulation. Kongming
subtasks select the pieces to move; all other pieces retain their assembled
configuration. Bookshelf instructions define category, placement and release
rules; physical checks run each substep. Marble exposes configured spring
stiffness in N/m before actions and retains ordered/protected target constraints.
Consult catalog.json and runtime describe for each selected task's contract.

## Engineering verification

`python scripts/environment_release.py check --output environment-check.json`

`python scripts/environment_smoke.py --task-id marble/dual-panda/A001 --seed 0 --output /tmp/agentbench-check.json`

These checks do not solve tasks. Only a package with release_ready=true has
passed every required release gate. A staging package is not a release candidate.
'''
ZH='''# Embodied Playground 环境发行包

Embodied Playground 是论文展示名；Agent-bench 仓库、包、环境和命令标识保留原拼写。
论文发射器仅采用 loaded 初态：完整目录为 410 项／1640 条件；EP-100、EP-Easy、EP-Hard、EP-20
分别为 100／50／50／20 项、400／200／200／80 条件。每项四条件，Launch、Tower、Lock、Cube、Home
五个套件等权评分。运行时另支持 ground，通用清单保留 510 组／2040 条件。

本包包含 410 个任务／机器人条目、资产、环境接口、评分器和 Level 0–3 权限网关。不包含模型测试、任务完成统计、控制器解题轨迹或排行榜。环境验收检查运行质量与必要可行条件，不代表所有任务或种子已证明可解。

## 安装与使用

保留源码目录结构。CPU MuJoCo 使用 Python 3.11，依赖固定为 mujoco==3.3.7、gymnasium==1.2.1、numpy==1.26.4、Pillow==11.3.0、scipy==1.15.3。将 source/agentbench、source/agentbench_platform、source/agentbench_sdk 加入 PYTHONPATH，无须安装模型权重或规划工具。Isaac 环境需另装 Isaac Sim／Isaac Lab；实际通过验证的版本以 runtime-qualification.json 为准，未经验证的平台不声明支持。

目录：`python scripts/environment_release.py catalog --output catalog.json`

启动：`python scripts/environment_runtime.py --task-id marble/dual-panda/A001 --capability-level 0 --headless --output /tmp/agentbench-episode`

另一个终端：`python scripts/environment_client.py /tmp/agentbench-episode/session.json`

维护者持有环境源码与资产，只将 SDK、会话和公开描述交给受控客户端；开源发行包本身不是隔离沙箱。会话文件应保密。SDK 提供 describe、observe、step、finish 和资源 ID 读取。describe 声明动作维度、边界、单位、目标和相机信息；读取观测不推进物理。只有维护者可初始化和 reset，客户端没有 reset、状态写入或评分修改入口。评分结果是环境功能，不是本包发布的模型成绩。

## 权限

版本：2026-10-09-environment-l0-l3，区别于任务难度。
L0 允许 Python、标准库、NumPy、Pillow 和自行实现的动力学／IK／规划，不提供预置领域工具或外部视觉／抓取模型。L1 增加明确授权的视觉、几何、IK、规划和观测重建代理工具。L2 增加明确授权的预训练抓取／接触模型。L3 增加接口声明的特权只读字段，不增加写入或 reset 权限。提升级别不会自动安装或授权工具；最小启动器不授予可选工具，由维护者通过平台配置已安装的工具进程。
网关保证自身访问边界，不认证任意外部客户端使用的所有库。模型 token／图片计费不属于本版环境范围。

## 物理合同

汉诺塔只移动顶环，遵守小环在上；落座容差为 XY 22 mm、Z 16 mm，可见壳体穿透不超过 5 mm，终态连续保持 1 秒。二阶魔方要求目标态、提交次数、定位误差不超过 1 度、速度低于 0.05 rad/s、连续保持 1 秒、固定物理指纹不变、可见壳体穿透不超过 0.25 mm。Panda 三阶魔方明确采用 hybrid_fixture_v1 辅助机构；Sharpa 三阶魔方使用相同的声明约束机构，包含 28 个原生关节和五个指尖接触传感器。两种任务评分器均要求原生物理证据；全案例验收仍待完成，两者均不描述成无辅助操作。孔明锁只移动子任务指定零件，其余保持组装态。书架按任务说明执行类别、放置和释放规则，并逐物理子步检查违规。小鸟在动作前公开弹簧刚度及 N/m 单位，保留目标顺序和保护对象约束。各项具体条件见 catalog.json 与运行时 describe。

## 工程检查

`python scripts/environment_release.py check --output environment-check.json`

`python scripts/environment_smoke.py --task-id marble/dual-panda/A001 --seed 0 --output /tmp/agentbench-check.json`

上述检查不进行解题。只有 release_ready=true 才表示所有发布门槛通过，staging 包不是发布候选。
'''


def build(destination,*,evidence=None,candidate=False,root=ROOT):
    destination=Path(destination)
    if Path(root).resolve()!=ROOT.resolve():
        raise ValueError('Build must run from the source tree being exported')
    manifest=catalog();files=inventory(root);evidence=evidence or {}
    status=gate(manifest,files,evidence)
    if candidate and not status['release_ready']:raise ValueError('Release gates incomplete; candidate build refused')
    if destination.exists():raise ValueError('Destination already exists')
    destination.mkdir(parents=True)
    try:
        for name in files:
            target=destination/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(export_content(name,(Path(root)/name).read_bytes()))
        # contract_source is a document URI with an anchor, never a filename.
        # The generated per-task protocol document is already in public_files.
        for name,value in [('catalog.json',manifest),('acceptance-matrix.json',matrix(manifest)),
            ('source-manifest.json',files),
            ('release-gates.json',status),('license-inventory.json',license_inventory(files,root)),
            ('bilingual-checks.json',bilingual_checks()),
            ('runtime-qualification.json',evidence.get('qualified_runtimes',{}))]:
            (destination/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
        # Preserve the repository's maintained bilingual entry points.
        (destination/'requirements-mujoco.txt').write_text(MUJOCO_REQUIREMENTS)
        if evidence.get('engineering_report') is not None:
            (destination/'environment-quality-report.json').write_text(json.dumps(evidence['engineering_report'],ensure_ascii=False,indent=2,allow_nan=False)+'\n')
        for name,measurement in evidence.get('environment_measurements',{}).items():
            if not re.fullmatch('[a-z0-9][a-z0-9_-]*',name):
                raise ValueError('Invalid environment measurement name')
            target=destination/'environment-checks'/(name+'.json')
            target.parent.mkdir(exist_ok=True)
            target.write_text(json.dumps(measurement,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
        (destination/'DISTRIBUTION_STATUS').write_text('release-candidate\n' if status['release_ready'] else 'staging-not-qualified\n')
        bundle={str(p.relative_to(destination)):dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
                for p in sorted(destination.rglob('*')) if p.is_file()}
        # Public source packages preserve executable launchers.
        for name in files:
            (destination/name).chmod((Path(root)/name).stat().st_mode & 0o777)
        (destination/'distribution-manifest.json').write_text(json.dumps(bundle,indent=2)+'\n')
    except BaseException:
        # Keep an incomplete staging tree for diagnosis; never promote it.
        (destination/'DISTRIBUTION_STATUS').write_text('build-failed\n')
        raise
    return status
