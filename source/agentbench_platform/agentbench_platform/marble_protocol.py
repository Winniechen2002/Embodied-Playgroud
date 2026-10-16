"""Canonical bird trial parameters; independent of historical experiment runners."""
import hashlib

PROTOCOL_VERSION = 'four-trial-v1'
PUBLIC_TASK_METADATA_VERSION = 'public-spring-v1'
PROTOCOLS = ('legacy', PROTOCOL_VERSION)
PUBLIC_VARIATION_NOTICE = ('The current launcher spring stiffness is supplied in variation_request in N/m. '
                           'Relative launcher and ammunition positions and visual backgrounds may vary. '
                           'Use the supplied stiffness, observation and physical interaction to adapt your control.')
THEMES = ('park', 'desert', 'snow', 'studio', 'dusk')
SPRINGS = (22., 24., 26., 28.)
LAUNCHER_X = (-.012, -.004, .004, .012)
AMMUNITION_OFFSETS = ((-.012, -.008, 0.), (-.004, .008, 0.),
                      (.004, -.008, 0.), (.012, .008, 0.))
MOTIONS = ('static', 'static', 'drift', 'pulse')
ENV_DEFAULTS = dict(background_motion='static', spring_stiffness=25.,
                    launcher_offset_m=(0., 0., 0.), ammunition_offset_m=(0., 0., 0.))
PUBLIC_VARIANT_KEYS = ('target_profile', 'variation', 'background', 'visual_seed',
                       'position_randomization', 'yaw_enabled')


def protocol_trials(scenario, base_seed=0):
    """Four JSON-safe PRIVATE records, ordered 1..4, all with the same reset seed.

    Theme start = big-endian integer of SHA256(UTF-8 scenario)'s first 8 bytes
    modulo 5; successive trials take successive themes modulo 5.
    """
    if not isinstance(scenario, str) or not scenario:
        raise ValueError('Expected a nonempty scenario name')
    if isinstance(base_seed, bool) or not isinstance(base_seed, int) or base_seed < 0:
        raise ValueError('Base seed must be a nonnegative integer')
    start = int.from_bytes(hashlib.sha256(scenario.encode('utf-8')).digest()[:8], 'big') % len(THEMES)
    return [dict(version=PROTOCOL_VERSION, trial_index=i+1, expected_trials=4,
                 base_seed=base_seed, reset_seed=base_seed,
                 environment_parameters=dict(spring_stiffness=SPRINGS[i],
                     launcher_offset_m=[LAUNCHER_X[i], 0., 0.],
                     ammunition_offset_m=list(AMMUNITION_OFFSETS[i]),
                     background=THEMES[(start+i) % len(THEMES)], background_motion=MOTIONS[i]))
            for i in range(4)]

