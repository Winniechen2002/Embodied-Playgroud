"""Notice-invalidated USD serialization for the trusted evaluator.

Unchanged USD serialization and its complete digest are cached. Configuration,
shell coverage, and live fixed-body transforms are still checked every substep.
The digest is byte-for-byte compatible with the uncached implementation.
"""
from __future__ import annotations

import hashlib
import json

from pxr import Tf, Usd


class SceneFingerprintCache:
    def __init__(self, stage, iter_prims, include_attribute):
        self._stage = stage
        self._iter_prims = iter_prims
        self._include_attribute = include_attribute
        self._stage_json = None
        self._paths = set()
        self._revision = 0
        self._last_prefix = None
        self._last_digest = None
        # Retain the registration: releasing it unregisters the callback.
        self._listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged,
                                            self._changed, stage)

    def _changed(self, notice, sender):
        # Resync covers additions/removals, references, variants, activation,
        # and instance/prototype changes, including newly added physics scenes.
        dirty = bool(notice.GetResyncedPaths())
        if not dirty:
            for path in notice.GetChangedInfoOnlyPaths():
                if not path.IsPropertyPath():
                    dirty = True  # Prim/stage metadata: conservatively rebuild.
                    break
                prim_path = str(path.GetPrimPath())
                if prim_path in self._paths and (self._include_attribute(prim_path, path.name)
                        or self._stage.GetRelationshipAtPath(path)):
                    dirty = True
                    break
        if dirty:
            self._revision += 1
            self._stage_json = None
            self._last_digest = None

    def _serialize_stage(self):
        self._last_digest = None
        revision = self._revision
        records, paths = [], set()
        for prim in self._iter_prims():
            path = str(prim.GetPath())
            paths.add(path)
            # Referenced instance geometry can report changes through its
            # prototype; watch both the visible proxy and its prototype path.
            if prim.IsInstanceProxy():
                paths.add(str(prim.GetPrimInPrototype().GetPath()))
            attrs = [(attr.GetName(), repr(attr.Get())) for attr in prim.GetAttributes()
                     if self._include_attribute(path, attr.GetName())]
            rels = [(rel.GetName(), list(map(str, rel.GetTargets())))
                    for rel in prim.GetRelationships()]
            records.append((path, prim.GetTypeName(), sorted(attrs), sorted(rels)))
        encoded = json.dumps(records, sort_keys=True).encode()
        if revision != self._revision:
            raise RuntimeError('USD scene changed while computing evaluation fingerprint')
        self._paths = paths
        self._stage_json = encoded

    def fingerprint(self, cfg_repr, shell_manifest, live_fixed_transforms):
        if self._stage_json is None:
            self._serialize_stage()
        # These keys precede "stage" in the original sort_keys=True encoding.
        prefix = json.dumps({'cfg': cfg_repr, 'shell_manifest': shell_manifest,
                             'live_fixed_transforms': live_fixed_transforms}, sort_keys=True)
        # Equality compares the freshly read live inputs, not a cached pose.
        # Hashing the same tens of MB of static USD text again cannot reveal
        # any additional change; notices above invalidate both cached results.
        if self._last_digest is not None and prefix == self._last_prefix:
            return self._last_digest
        digest = hashlib.sha256((prefix[:-1] + ', "stage": ').encode())
        digest.update(self._stage_json)
        digest.update(b'}')
        self._last_prefix = prefix
        self._last_digest = digest.hexdigest()
        return self._last_digest

    def close(self):
        self._listener.Revoke()
