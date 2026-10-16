"""Explicit public export: never copy a checkout, directory tree, or episode."""
import hashlib
import json
import os
from pathlib import Path
from .profiles import RunProfile
from .tasks import normalize_embodiment, validate_task

SDK_FILES = ('pyproject.toml', 'agentbench_sdk/__init__.py', 'agentbench_sdk/client.py', 'agentbench_sdk/types.py')
VIEWS = ('front_left', 'front_right', 'top')
EXAMPLE = '''import json, os
from pathlib import Path
from agentbench_sdk import Client
session = json.loads(Path('/run/agentbench/session.json').read_text())
client = Client('/run/native.sock', session['native_token'])
print(json.dumps(client.describe(), indent=2))
print(json.dumps(client.observe(camera_ids=['front_left']), indent=2))
# Observe never advances physics. describe()['action_spec'] gives action size and bounds.
# get_resource returns base64 bytes and their public encoding metadata.
# finish ends this attempt; reconnecting never resets it.
'''


def _read(path):
    path = Path(path)
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
        raise ValueError('Public input must be a regular file without symlinks')
    return path.read_bytes()


def export_bundle(destination, *, sdk_root, native_public, goal_directory, mode, profile,
                  task_family='kongming_lock', target_sequence=None, embodiment='franka-panda',case_id=None):
    if profile.experience != 'none':
        raise ValueError('Public coding-agent bundles require cold experience=none')
    embodiment = normalize_embodiment(embodiment)
    target_sequence = validate_task(task_family, mode, target_sequence, embodiment=embodiment)
    destination = Path(destination)
    # Exact names, selected by the maintainer. No globs or recursive copying.
    files = {'sdk/'+name: _read(Path(sdk_root)/name) for name in SDK_FILES}
    for name in ('robot_model.json', 'cameras.json'):
        data = _read(Path(native_public)/name)
        json.loads(data)
        files[name] = data
    for name in VIEWS:
        data = _read(Path(goal_directory)/(name+'.png'))
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Goal image must be PNG')
        files['goals/'+name+'.png'] = data
    task_text = f'''# Kongming lock {mode}
Use the two Franka arms to {mode} the six-piece wooden puzzle. Goal reference
images show only the desired final state. Read client.describe() for action
order, bounds, task limits and the frozen observation profile. Read
robot_model.json for joint frames, units and TCP calibration, and cameras.json
for camera calibration. RGB has no depth; RGB-D depth is a sensor output.

All 16 action entries are required. Invalid actions are rejected. Physics runs
at 120 Hz and controls at 30 Hz; observations do not advance simulation.
Assembly requires one coherent structure inside x=[0.50,0.95], y=[-0.22,0.22] m,
within 0.0075 m position and 0.08 rad angle tolerance. Disassembly requires six
separate pieces in the marked target regions. Release both grippers and retreat
both arms. Stable windows are 60 assembly or 30 disassembly control steps.
Penetration beyond 0.002 m and forbidden contact at or above 0.5 N fail hard audits.

Use only the public SDK. This is one attempt: there is no reset or resume into
another episode. Write your programs in /workspace. example.py demonstrates
legal observation and resource access without supplying a controller.
'''
    if task_family == 'rubiks_cube':
        objective = ('Restore all six faces to uniform colors using the current observations.' if mode == 'solve'
                     else 'Execute these face turns in this exact order: '+ ' '.join(target_sequence)+'.')
        robot_text = ('one Floating Sharpa Wave right hand with 28 absolute native joint targets'
                      if embodiment == 'floating-sharpa' else 'one Franka Panda arm with a parallel gripper')
        action_text = ('All 28 action entries are absolute native joint targets in the order and bounds returned by describe().'
                       if embodiment == 'floating-sharpa' else
                       'All 8 action entries are required: seven arm targets q=default_q+0.5*action and one continuous gripper coordinate. Each finger target is 0.02*(action+1) m, between 0 and 0.04 m.')
        task_text = f'''# Rubik's cube {mode}
Use {robot_text} to manipulate the 3×3 cube.
{objective}
Read client.describe() for the action order, limits, frozen observation profile,
mechanism command preconditions and available tools. The three goal images show
the final state only. robot_model.json and cameras.json contain public calibration.

{action_text} Invalid actions are rejected. Physics runs at 120 Hz,
control at 30 Hz. Observing and tool calls do not advance simulation.

This task uses hybrid_fixture_v1: internal layer constraints, a support anchor,
measured hand attachment during transport, and passive carrier detents assist
the physical mechanism. This is an assisted manipulation benchmark.
client.mechanism.command requests a state transition, never a robot trajectory.
Conditions are checked against measured physical history. All motion and waiting
require step calls; no grasp proof or completion claim is accepted from the agent.

A half turn requires two real quarter turns. Cancelling turns must each execute;
whole-cube reorientation does not count as a face turn. The final cube must return
to its accepted initial pose within 5 mm / 2°, remain stable for 0.5 seconds,
and all fingers must open to at least 0.035 m. Return each arm joint within
0.05 rad of the public home configuration. Quarter-turn tolerance is 3°,
internal alignment tolerance is 1 mm, and the contact force limit is 20 N.

Use only the public SDK. There is one attempt and no reset. Write programs in
/workspace. example.py shows observation access without providing a controller.
'''
    if embodiment == 'dual-floating-sharpa':
        task_text = f'''# Kongming lock {mode}
Use two official Floating Sharpa Wave right hands to {mode} the six-piece wooden puzzle.
The public case id and subtask are visible in client.describe(); trusted reset
poses and reference trajectories are not exposed. The action vector has 56
absolute native joint targets: the first 28 entries are the left hand, followed
by the 28 entries of the right hand. Each hand uses six floating-base joints
followed by its 22 finger joints in the order returned by describe().

Physics runs at 120 Hz and controls at 30 Hz. Observing, camera capture and
read-only contact queries do not advance physics. Invalid action lengths or
out-of-limit targets are rejected. There is one attempt and no reset or
teleport capability. Success is determined from measured piece poses, velocity,
contact audits and the stable goal window; controller supplied completion flags
are ignored.

This first dual-hand release supports complete, key-only and key-plus-bar public
subtasks. Keep both hands clear and open at the terminal state. Use only the
public SDK and write programs in /workspace.
'''
    elif task_family == 'kongming_lock' and case_id is not None:
        from .kongming_cases import public_description
        case = public_description(case_id)
        if case['task'] != mode: raise ValueError('Case mode mismatch')
        task_text = f'''# Kongming lock {case_id}
{case['description']}
Goal reference images show this case's final state. Read client.describe() for
action order, limits, tolerances and the frozen permission profile. Robot and
camera calibration are provided in robot_model.json and cameras.json.
All 16 action entries are required. Physics runs at 120 Hz and controls at 30 Hz.
Observations do not advance time. Use only the public SDK; there is no client
reset, state write or scoring override. Release both grippers and retreat both
arms. Stable windows are 60 assembly or 30 disassembly control steps.
Penetration beyond 0.002 m and forbidden contact at or above 0.5 N fail audits.
'''
    files['TASK.md'] = task_text.encode()
    files['example.py'] = EXAMPLE.encode()
    manifest = dict(version=1, task_family=task_family, embodiment=embodiment, mode=mode, profile=profile.public_record(),
        files={name:dict(sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)) for name,data in files.items()})
    if target_sequence is not None:
        manifest['target_sequence'] = target_sequence
    if case_id is not None:manifest['case_id']=case_id
    destination.mkdir(parents=True, exist_ok=False, mode=0o755)
    for name,data in files.items():
        path = destination/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        os.chmod(path, 0o444)
    (destination/'bundle.json').write_text(json.dumps(manifest, indent=2)+'\n')
    os.chmod(destination/'bundle.json', 0o444)
    return manifest
