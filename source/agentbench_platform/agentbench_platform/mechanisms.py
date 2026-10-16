"""Versioned, finite requests for the declared hybrid cube mechanism.

These are intent schemas, never evidence schemas. The native bridge owns all
contact, frame capture and transition checks; this module owns public filtering.
"""
from copy import deepcopy
from .plugins import validate


VERSION = 'hybrid_fixture_v1'
STATES = frozenset(('idle', 'turning', 'settling', 'transporting', 'attached', 'supported', 'finished'))


def _object(properties):
    return dict(type='object', properties=properties, required=list(properties), additionalProperties=False)


def _array(items, size):
    return dict(type='array', items=items, minItems=size, maxItems=size)


COMMANDS = {
    'turn.begin': _object({'move': dict(type='string', enum=[face+suffix for face in 'UDLRFB' for suffix in ('', "'")])}),
    'turn.end': _object({}),
    'transport.begin': _object({'target_frame': dict(
        **_array(_array(dict(type='number', minimum=-1, maximum=1), 3), 3),
        description='Proper 3x3 world-from-core rotation matrix, including any continuous scene yaw.')}),
    'transport.attach': _object({}),
    'transport.capture_support': _object({}),
    'transport.release': _object({}),
    'transport.end': _object({}),
    'detent.begin': _object({'axis': dict(type='string', enum=['x', 'y', 'z'])}),
    'detent.end': _object({}),
}


def description(raw):
    if not isinstance(raw, dict) or raw.get('version') != VERSION:
        raise ValueError('Unsupported mechanism contract')
    return dict(version=VERSION, commands=deepcopy(COMMANDS), states=sorted(STATES))


def validate_command(name, arguments):
    if not isinstance(name, str) or name not in COMMANDS:
        raise ValueError('Unsupported mechanism command')
    validate(arguments, COMMANDS[name])


def public_state(raw):
    if (not isinstance(raw, dict) or raw.get('state') not in STATES
            or type(raw.get('epoch')) is not int or raw['epoch'] < 0):
        raise ValueError('Invalid mechanism state')
    return dict(state=raw['state'], epoch=raw['epoch'])


def public_reply(raw):
    if not isinstance(raw, dict) or type(raw.get('accepted')) is not bool:
        raise ValueError('Invalid mechanism reply')
    return dict(accepted=raw['accepted'], **public_state(raw))
