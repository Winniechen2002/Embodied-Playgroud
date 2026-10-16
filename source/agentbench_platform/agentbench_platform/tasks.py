"""Public task identities; no simulator, reference controller, or private initial state."""
import re

FAMILIES = {'kongming_lock': ('assemble', 'disassemble'),
            'rubiks_cube': ('solve', 'execute_sequence')}
EMBODIMENTS = ('franka-panda', 'floating-sharpa', 'dual-floating-sharpa')


def normalize_embodiment(value):
    """Return the stable public embodiment identity used by the gateway."""
    aliases = {
        'floating-sharpa-right': 'floating-sharpa',
        'floating_sharpa': 'floating-sharpa',
        'floating-sharpa-dual': 'dual-floating-sharpa',
        'dual_floating_sharpa': 'dual-floating-sharpa',
    }
    value = aliases.get(value, value)
    if value not in EMBODIMENTS:
        raise ValueError('Unknown benchmark embodiment')
    return value


def validate_task(family, mode, target_sequence=None, *, embodiment='franka-panda'):
    if family not in FAMILIES or mode not in FAMILIES[family]:
        raise ValueError('Unknown task family or mode')
    embodiment = normalize_embodiment(embodiment)
    if family == 'kongming_lock' and embodiment not in ('franka-panda', 'dual-floating-sharpa'):
        raise ValueError('Kongming lock supports Franka or dual Floating Sharpa')
    if family != 'kongming_lock' and embodiment == 'dual-floating-sharpa':
        raise ValueError('Dual Floating Sharpa is only registered for kongming_lock')
    if family == 'rubiks_cube' and mode == 'execute_sequence':
        if (not isinstance(target_sequence, (list, tuple)) or not target_sequence
                or any(not isinstance(move, str) or not re.fullmatch(r"[URFDLB](?:'|2)?", move)
                       for move in target_sequence)):
            raise ValueError('Execution task requires a nonempty legal target sequence')
        return list(target_sequence)
    if target_sequence is not None:
        raise ValueError('Only execute_sequence publishes a target sequence')
    return None


def add_task_arguments(parser):
    parser.add_argument('--task-family', choices=tuple(FAMILIES), default='kongming_lock')
    parser.add_argument('--mode', choices=tuple(m for modes in FAMILIES.values() for m in modes), required=True)
    parser.add_argument('--embodiment', choices=EMBODIMENTS, default='franka-panda')
