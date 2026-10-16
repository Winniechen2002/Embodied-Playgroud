"""Initialization-only visual perturbations; no policy or physical randomization."""
import math
LIGHT_SCALES=(.85,.95,1.,1.05,1.15)

def validate_light_scale(value):
    if type(value) not in (int,float) or not math.isfinite(value) or value not in LIGHT_SCALES:
        raise ValueError('Unknown evaluation light scale')
    return float(value)

def lighting_parameters(scale):
    scale=validate_light_scale(scale)
    return dict(ambient=[x*scale for x in (.32,.35,.39)],
        directional=[[x*scale for x in color] for color in ((2.,1.89,1.75),(.43,.49,.58))])
