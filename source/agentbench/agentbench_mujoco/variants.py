"""Reproducible task parameters, independent of cosmetic randomization.

These are authored distributions for evaluation, not calibrated material data.
The default path consumes no additional draws from the legacy scene generator.
"""
import hashlib
import json
import numpy as np

TARGET_PROFILES = ('authored', 'small', 'large', 'mixed')
VARIATIONS = ('nominal', 'train', 'heldout')
TARGET_TYPES = {
    'small': dict(radius=.042, impulse_threshold=.012, code=0),
    'standard': dict(radius=.052, impulse_threshold=.018, code=1),
    'large': dict(radius=.072, impulse_threshold=.030, code=2),
}


def derived_seed(rng, domain):
    """Fork a stream without advancing physics RNG or relying on Python hash()."""
    state=json.dumps(rng.bit_generator.state,sort_keys=True,separators=(',', ':'))
    return int.from_bytes(hashlib.sha256((domain+state).encode()).digest()[:8], 'little')


def validate_variant(target_profile, variation, background, visual_seed):
    from .backgrounds import BACKGROUNDS
    if target_profile not in TARGET_PROFILES:raise ValueError('Unknown target_profile')
    if variation not in VARIATIONS:raise ValueError('Unknown variation')
    if background not in BACKGROUNDS:raise ValueError('Unknown background')
    if visual_seed is not None and (isinstance(visual_seed,bool) or
            not isinstance(visual_seed,(int,np.integer)) or not 0<=int(visual_seed)<2**64):
        raise ValueError('visual_seed must be a nonnegative integer below 2**64 or None')


def sample_variant(rng, target_profile, variation, background, visual_seed, count):
    physical_seed=derived_seed(rng,'campaign-task-v1:')
    sampled_visual_seed=derived_seed(rng,'campaign-visual-v1:') if visual_seed is None else int(visual_seed)
    physical=np.random.default_rng(physical_seed)
    # Size assignment has its own stream, so adding visual or physics factors
    # never silently reassigns which target is large.
    sizes=np.random.default_rng(derived_seed(rng,'campaign-target-sizes-v1:'))
    if target_profile=='mixed':
        offset=int(sizes.integers(2))
        target_types=[('small','large')[(i+offset)%2] for i in range(count)]
    else:target_types=[{'authored':'standard'}.get(target_profile,target_profile)]*count
    realized=dict(layout_offset_m=[0.,0.,0.],structure_mass_scale=1.,
                  structure_friction_scale=1.,strength_scale=1.,target_types=target_types,
                  physical_seed=physical_seed,visual_seed=sampled_visual_seed)
    if variation=='train':
        realized.update(layout_offset_m=[float(physical.uniform(-.025,.025)),
                                        float(physical.uniform(-.006,.006)),0.],
                        structure_mass_scale=float(physical.uniform(.92,1.08)),
                        structure_friction_scale=float(physical.uniform(.90,1.10)),
                        strength_scale=float(physical.uniform(.92,1.08)))
    elif variation=='heldout':
        def outside(low,high):
            magnitude=float(physical.uniform(low,high))
            return magnitude if physical.integers(2) else -magnitude
        realized.update(layout_offset_m=[outside(.05,.08),outside(.012,.020),0.],
                        structure_mass_scale=1+outside(.15,.25),
                        structure_friction_scale=1+outside(.20,.30),
                        strength_scale=1+outside(.15,.25))
    return dict(requested=dict(target_profile=target_profile,variation=variation,
                               background=background,visual_seed=None if visual_seed is None else int(visual_seed)),
                realized=realized,distribution_version=2)


def scale_structure_contacts(world, body_names, scale):
    if scale==1.:return
    for name in body_names:
        body=world.find(f"body[@name='{name}']")
        for geom in body.findall('geom'):
            if geom.get('contype','1')=='0':continue
            friction=np.fromstring(geom.get('friction','1 .005 .0001'),sep=' ')
            geom.set('friction',' '.join(str(float(x*scale)) for x in friction))
