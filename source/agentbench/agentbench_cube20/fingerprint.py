"""Immutable USD physics projection, excluding declared live mechanism state."""
import hashlib
import json

# These values describe live joint state or the documented constraint switches.
# Joint limits, local frames and enable flags are mutable only for cube joints;
# robot joint limits, actuator gains, collision geometry and materials stay fixed.
CUBE_SWITCH_ATTRIBUTES = frozenset((
    'physics:jointEnabled', 'physics:localPos0', 'physics:localPos1',
    'physics:localRot0', 'physics:localRot1', 'physics:lowerLimit', 'physics:upperLimit',
))
GEOMETRY_ATTRIBUTES = frozenset((
    'points', 'faceVertexCounts', 'faceVertexIndices', 'holeIndices', 'subdivisionScheme',
    'size', 'radius', 'height', 'axis', 'xformOp:scale',
))


def immutable_attribute(path, name):
    if name in ('physics:velocity', 'physics:angularVelocity') or name.startswith('state:') or name.endswith((':targetPosition', ':targetVelocity')):
        return False
    if '/PocketCube/Joints/' in path and name in CUBE_SWITCH_ATTRIBUTES:
        return False
    return name in GEOMETRY_ATTRIBUTES or name.startswith((
        'physics:', 'physx', 'drive:', 'collision:'))


def fingerprint(stage, *, physics_dt, decimation, gravity):
    from pxr import Usd, UsdPhysics
    records = {}
    for prim in Usd.PrimRange.Stage(stage, Usd.TraverseInstanceProxies()):
        path = str(prim.GetPath())
        if (not path.startswith('/World/envs/env_0') and prim.GetTypeName() != 'PhysicsScene'
                and not any(prim.HasAPI(api) for api in
                    (UsdPhysics.MaterialAPI, UsdPhysics.CollisionAPI, UsdPhysics.RigidBodyAPI))):
            continue
        values = {a.GetName(): str(a.Get()) for a in prim.GetAttributes()
                  if immutable_attribute(path, a.GetName())}
        relationships = {r.GetName(): [str(p) for p in r.GetTargets()] for r in prim.GetRelationships()
                         if r.GetName().startswith(('material:binding', 'physics:'))}
        records[path] = dict(type=str(prim.GetTypeName()), schemas=list(prim.GetAppliedSchemas()),
                             attributes=values, relationships=relationships)
    records['simulation'] = dict(dt=physics_dt, decimation=decimation, gravity=list(gravity))
    return hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest()


class FixedPhysicsFingerprintCache:
    """USD notices invalidate immutable geometry; live poses are audited separately."""
    def __init__(self, stage):
        from pxr import Tf, Usd
        self.stage=stage
        self.dirty=True
        self.parameters=None
        self.value=None
        self.listener=Tf.Notice.Register(Usd.Notice.ObjectsChanged,self._changed,stage)

    def _changed(self, notice, sender):
        if notice.GetResyncedPaths():self.dirty=True
        for path in notice.GetChangedInfoOnlyPaths():
            if (not path.IsPropertyPath() or immutable_attribute(str(path.GetPrimPath()),path.name)
                    or self.stage.GetRelationshipAtPath(path)):
                self.dirty=True
                break

    def fingerprint(self, **parameters):
        if self.dirty or self.parameters!=parameters:
            self.value=fingerprint(self.stage,**parameters)
            self.parameters=parameters
            self.dirty=False
        return self.value

    def close(self):self.listener.Revoke()
