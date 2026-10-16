"""Apply the three authored physical parameter sets. No Category 4 label tasks."""
import copy

def resolve(base, physics_variant=0):
    t=copy.deepcopy(base)
    variants=t.get('physics_variants',[])
    if int(physics_variant) not in range(max(1,len(variants))):
        raise ValueError('physics_variant out of range for this task')
    if variants:
        v=variants[int(physics_variant)];t['active_physics']=v
        for o in t['objects']:
            if o['name'] in v.get('objects',{}):o.update(v['objects'][o['name']])
    # Preserve the original audited specification hash; label tasks are excluded.
    t['label_variant']=0;t['physics_variant']=int(physics_variant)
    return t
