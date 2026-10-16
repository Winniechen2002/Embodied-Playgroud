#!/usr/bin/env python3
"""Generate/check bilingual per-task four-trial specifications, never run agents."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/agentbench_platform'))
from agentbench_platform.evaluation_protocol import manifest,VERSION

NAMES={
 'marble':('Launcher','发射器'),
 'hanoi_panda':('Panda Hanoi','Panda 汉诺塔'),
 'hanoi_sharpa':('FR3 Sharpa Hanoi','FR3 Sharpa 汉诺塔'),
 'hanoi_floating':('Floating Sharpa Hanoi','Floating Sharpa 汉诺塔'),
 'pocket_cube':('Pocket cube','二阶魔方'),
 'rubiks_panda':("Panda Rubik's cube",'Panda 三阶魔方'),
 'rubiks_sharpa':("Floating Sharpa Rubik's cube",'Floating Sharpa 三阶魔方'),
 'kongming_lock':('Kongming lock','孔明锁'),
 'bookshelf':('Bookshelf','书架'),
 'maniskill_long_horizon':('ManiSkill long horizon','ManiSkill 长程任务'),
 'maniskill_geometry':('ManiSkill geometry','ManiSkill 几何任务'),
 'maniskill_dynamics':('ManiSkill dynamics','ManiSkill 动力学任务')}
SOURCES=[
 'scripts/export_evaluation_protocol.py','source/agentbench_platform/agentbench_platform/marble_protocol.py','scripts/environment_runtime.py',
 'scripts/agentbench_platform_runtime.py',
 'source/agentbench_platform/agentbench_platform/evaluation_protocol.py',
 'source/agentbench_platform/agentbench_platform/environment_contracts.py',
 'source/agentbench_platform/agentbench_platform/action_contracts.json',
 'source/agentbench_platform/agentbench_platform/environment_catalog.py',
 'source/agentbench_platform/agentbench_platform/environment_backend.py',
 'source/agentbench_platform/agentbench_platform/native_environment.py',
 'source/agentbench_platform/agentbench_platform/bookshelf_catalog.json',
 'source/agentbench_platform/agentbench_platform/kongming_cases.py',
 'source/agentbench_platform/agentbench_platform/rubiks_cases.py']
SOURCES+= [str(p.relative_to(ROOT)) for folder in (
 'source/agentbench/agentbench_hanoi40','source/agentbench/agentbench_cube20','source/agentbench/agentbench_mujoco',
 'source/agentbench/agentbench/tasks/manager_based/table_top_manipulation/config/organize_bookshelf')
 for p in (ROOT/folder).glob('*.py')]

SOURCES += [str(p.relative_to(ROOT)) for p in (ROOT/'env/maniskill_lgd/agentbench_maniskill').rglob('*') if p.suffix=='.py' or p.name=='tasks.json']

def artifacts(base_seed=0):
    data=manifest(base_seed)
    data['sources']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(SOURCES))}
    files={'tasks.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n'}
    for lang,ix in [('en',0),('zh-CN',1)]:
        scope = (
            'Embodied Playground paper scope: Launcher uses loaded initialization only. '
            'The full 410-task paper setting has 410 groups / 1640 conditions; EP-100 has 100 / 400. '
            'This runtime schedule also includes ground and retains 510 groups / 2040 conditions. '
            if ix == 0 else
            'Embodied Playground 论文仅评测发射器 loaded 初态：完整 410 项为 410 组／1640 条件，EP-100 为 100 组／400 条件。'
            '本运行时清单另保留 ground，共 510 组／2040 条件。'
        ) + f'[EP-100 / EP-20 / EP-Easy / EP-Hard](../ep_subsets/README.{lang}.md)'
        title='Per-task evaluation conditions' if ix==0 else '逐任务评测条件'
        index=[f'# {title}', '',f'`{VERSION}` · base seed `{base_seed}` · {data["task_count"]} tasks · {data["group_count"]} groups · {data["planned_episodes"]} planned episodes','',
            '[English](index.en.md) · [简体中文](index.zh-CN.md)', '',
            ('Generated from source; no execution results. ' if ix==0 else '根据源码生成；不含执行成绩。')+
            f'[Protocol](../evaluation_protocol.{lang}.md) · [JSON](tasks.json)', '', scope, '',
            '| Family / 系列 | Tasks / 任务 | Episodes / 回合 |','| --- | ---: | ---: |']
        for family,names in NAMES.items():
            rows=[r for r in data['tasks'] if r['task_id'].startswith(family+'/')]
            index.append(f'| [{names[ix]}]({family}.{lang}.md) | {len(rows)} | {sum(len(r["groups"])*4 for r in rows)} |')
            lines=[f'# {names[ix]}', '',f'[Protocol](../evaluation_protocol.{lang}.md) · [Index](index.{lang}.md) · [JSON](tasks.json)','', scope, '',
                (f'Each task below has four trials per group at base seed {base_seed}. Parameters are private maintainer inputs. '
                 'Goal strings and field names below are verbatim authoring data, not translated protocol prose.' if ix==0 else
                 f'下列每项每组四次，base seed 为 {base_seed}。参数为维护者私有输入。目标字符串与字段名保留作者配置原文，不作为翻译后的协议正文。'),'']
            for row in rows:
                anchor=row['task_id'].replace('/','-')
                budget=row['budgets']
                lines.extend([f'<a id="{anchor}"></a>',f'## `{row["task_id"]}`','',
                    (f'Authoring source: [{row["authoring_source"]}](../../{row["authoring_source"]}). ' if ix==0 else f'作者来源：[{row["authoring_source"]}](../../{row["authoring_source"]})。')+
                    f'Action size: {row["action_size"]}; {budget["max_steps"]} controls / {budget["simulation_seconds"]} s; wall: {budget["wall_seconds"]} s.',
                    '',('Goal (source data):' if ix==0 else '目标（源数据）：'),'```json',
                    json.dumps(row['goal'],ensure_ascii=False,sort_keys=True),'```','',
                    ('Native action and scoring contract:' if ix==0 else '原生动作与评分合同：'),'```json',
                    json.dumps({k:row['contract'][k] for k in ('action_spec','observation_spec','scoring','termination','sha256')},ensure_ascii=False,sort_keys=True,indent=2),'```',''])
                for group in row['groups']:
                    lines.extend([f'### {group["variant"]} — 4 trials','',
                        '| Trial | Reset seed | Split | Parameters / 参数 |', '| ---: | ---: | --- | --- |'])
                    for trial in group['trials']:
                        params=json.dumps(trial['environment_parameters'],ensure_ascii=False,sort_keys=True,separators=(',',':')).replace('|','&#124;')
                        lines.append(f'| {trial["trial_index"]} | {trial["reset_seed"]} | {trial["split"]} | `{params}` |')
                    mode=f' --initial-mode {group["variant"]}' if family=='marble' else ''
                    lines.extend(['','```bash',f'python scripts/environment_runtime.py --task-id {row["task_id"]} --capability-level 0 --seed {base_seed} --evaluation-protocol {VERSION} --trial-index 1{mode} --headless --output /tmp/{anchor}-{group["variant"]}-trial1','```','',
                        ('Repeat with indices 2, 3, 4 and fresh output paths; same group settings. See protocol for isolation and outcome accounting.' if ix==0 else '以编号 2、3、4 和新输出路径分别执行；组内其他设置固定。隔离与终局统计见统一协议。'),''])
            files[f'{family}.{lang}.md']='\n'.join(lines)+'\n'
        files[f'index.{lang}.md']='\n'.join(index)+'\n'
    return files


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base-seed',type=int,default=0)
    p.add_argument('--output',type=Path,default=ROOT/'docs/evaluation')
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    expected=artifacts(args.base_seed)
    if args.check:
        stale=[name for name,body in expected.items() if not (args.output/name).is_file() or (args.output/name).read_text()!=body]
        if stale:p.exit(1,'Stale evaluation documents: '+', '.join(stale)+'\n')
        print('410 tasks; 510 groups; 2040 planned episodes; generated documents and source hashes match.')
    else:
        if args.output.resolve()!=(ROOT/'docs/evaluation').resolve() and args.output.exists():
            p.error('External output must be a new directory')
        args.output.mkdir(parents=True,exist_ok=True)
        for name,body in expected.items():(args.output/name).write_text(body)
        print(f'Wrote {len(expected)} specification files to {args.output}; no episodes executed.')

if __name__=='__main__':main()
