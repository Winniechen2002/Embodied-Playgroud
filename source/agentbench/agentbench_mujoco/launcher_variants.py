"""Explicit reset-only launcher parameters for reproducible evaluation trials.

The spring is a real passive slide-joint spring in N/m. Placement offsets are
added to independently sampled launcher/ammunition offsets before compilation;
targets, structures, robot bases and latch-relative poses are unchanged.
"""
from numbers import Real
import numpy as np


DEFAULT_SPRING_STIFFNESS = 25.0


def validate_launcher_configuration(spring_stiffness=DEFAULT_SPRING_STIFFNESS,
                                    launcher_offset_m=(0., 0., 0.),
                                    ammunition_offset_m=(0., 0., 0.)):
    if (isinstance(spring_stiffness, (bool, np.bool_)) or
            not isinstance(spring_stiffness, Real) or
            not np.isfinite(spring_stiffness) or spring_stiffness <= 0):
        raise ValueError('spring_stiffness must be a positive finite number in N/m')
    offsets = []
    for name, value in (('launcher_offset_m', launcher_offset_m),
                        ('ammunition_offset_m', ammunition_offset_m)):
        try:
            array = np.asarray(value, dtype=float)
        except (TypeError, ValueError):
            raise ValueError(f'{name} must be a finite planar three-vector') from None
        if (array.shape != (3,) or not np.all(np.isfinite(array)) or
                array[2] != 0 or np.any(np.abs(array[:2]) > .05)):
            raise ValueError(f'{name} must have three finite values, z=0 and |x|,|y| <= 0.05 m')
        offsets.append(array.copy())
    return float(spring_stiffness), *offsets


def configure_launcher(root, positions, *, spring_stiffness=DEFAULT_SPRING_STIFFNESS,
                       launcher_offset_m=(0., 0., 0.),
                       ammunition_offset_m=(0., 0., 0.)):
    """Configure the passive spring and position plan, without stepping physics."""
    stiffness, launcher, ammunition = validate_launcher_configuration(
        spring_stiffness, launcher_offset_m, ammunition_offset_m)
    joint = root.find(".//joint[@name='draw']")
    if joint is None:
        raise ValueError('Launcher configuration requires the passive draw joint')
    # Preserve legacy XML bytes for the default configuration.
    if float(joint.get('stiffness', '0')) != stiffness:
        joint.set('stiffness', format(stiffness, '.15g'))
    values = positions['realized']
    for field, delta in (('launcher_offset_m', launcher),
                         ('ammunition_offset_m', ammunition)):
        if np.any(delta):
            values[field] = (np.asarray(values[field]) + delta).tolist()
    request = dict(spring_stiffness=stiffness, launcher_offset_m=launcher.tolist(),
                   ammunition_offset_m=ammunition.tolist())
    return dict(configuration_version=1, requested=request,
                realized=dict(spring_stiffness_n_per_m=stiffness))
