"""Lossless numeric-array fingerprints for the large Sharpa USD meshes."""
import hashlib
import json
import numpy as np


def value_record(value):
    """Keep scalar repr; encode every numeric array byte, shape and type."""
    if isinstance(value,np.ndarray) or type(value).__module__=='pxr.Vt':
        try:
            array=np.asarray(value)
            if array.dtype.kind in 'biufc':
                return {'type':type(value).__module__+'.'+type(value).__name__,
                        'dtype':array.dtype.str,'shape':list(array.shape),
                        'sha256':hashlib.sha256(array.tobytes(order='C')).hexdigest()}
        except (TypeError,ValueError):
            pass
    return repr(value)


def cache_class():
    from agentbench.tasks.manager_based.table_top_manipulation.config.hanoi.scene_fingerprint import SceneFingerprintCache

    class NumericArrayFingerprintCache(SceneFingerprintCache):
        def _serialize_stage(self):
            self._last_digest=None
            revision=self._revision
            records,paths=[],set()
            for prim in self._iter_prims():
                path=str(prim.GetPath());paths.add(path)
                if prim.IsInstanceProxy():paths.add(str(prim.GetPrimInPrototype().GetPath()))
                attrs=[(attr.GetName(),value_record(attr.Get())) for attr in prim.GetAttributes()
                       if self._include_attribute(path,attr.GetName())]
                rels=[(rel.GetName(),list(map(str,rel.GetTargets()))) for rel in prim.GetRelationships()]
                records.append((path,prim.GetTypeName(),sorted(attrs),sorted(rels)))
            encoded=json.dumps(records,sort_keys=True).encode()
            if revision!=self._revision:raise RuntimeError('USD scene changed during fingerprint')
            self._paths=paths;self._stage_json=encoded
    return NumericArrayFingerprintCache
