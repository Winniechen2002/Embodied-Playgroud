"""Small convex projectiles with their visible shape used for collision.

The flat lower face and parallel gripping faces are intentional: these are
irregular objects that the two-finger Panda can manipulate without a grasp
constraint.  MuJoCo integrates the closed mesh volume to obtain its centre of
mass and inertia.  No sphere/box collision proxy is substituted for the mesh.
"""
import xml.etree.ElementTree as ET


def _prism(outline, half_width):
    """Extrude a counter-clockwise (x, z) outline and triangulate its hull."""
    count = len(outline)
    vertices = [(x, -half_width, z) for x, z in outline]
    vertices += [(x, half_width, z) for x, z in outline]
    faces = []
    for i in range(1, count - 1):
        faces.extend([(0, i, i + 1), (count, count + i + 1, count + i)])
    for i in range(count):
        nxt = (i + 1) % count
        faces.extend([(i, count + i, count + nxt), (i, count + nxt, nxt)])
    return vertices, faces


_WEDGE = _prism([(-.020, -.017), (.020, -.017), (.020, .005), (-.020, .017)], .016)
_SHARD = _prism([(-.018, -.017), (.012, -.017), (.019, -.003),
                 (.016, .018), (-.006, .020), (-.020, .007)], .015)

NEW_AMMO = {
    'wedge': dict(type='mesh', size=[1, 1, 1], mass=.032, z=.0175,
                  color=[.98, .47, .11, 1], label='Amber wedge',
                  vertices=_WEDGE[0], faces=_WEDGE[1]),
    'shard': dict(type='mesh', size=[1, 1, 1], mass=.030, z=.0175,
                  color=[.43, .29, .82, 1], label='Violet shard',
                  vertices=_SHARD[0], faces=_SHARD[1]),
}


def build_projectile_geometry(root, body, geom, kind, name):
    """Replace an existing primary geom with an irregular convex mesh.

    Call after setting the usual mass, friction and colour.  The primary geom
    keeps ``name`` so existing contact attribution and physical seating logic
    still identify exactly one collision geom per projectile.  Returns False
    for primitive types, allowing the caller to invoke it for every piece.
    """
    if kind not in NEW_AMMO:
        return False
    if geom not in list(body):
        raise ValueError('The projectile geom must belong to its body')
    spec = NEW_AMMO[kind]
    assets = root.find('asset')
    if assets is None:
        assets = ET.SubElement(root, 'asset')
    mesh_name = f'projectile_{kind}_mesh'
    if assets.find(f"mesh[@name='{mesh_name}']") is None:
        ET.SubElement(assets, 'mesh', name=mesh_name,
                      vertex=' '.join(str(v) for vertex in spec['vertices'] for v in vertex),
                      face=' '.join(str(v) for face in spec['faces'] for v in face))
    # Primitive size/fromto attributes must not leak into the mesh definition.
    for attribute in ('size', 'fromto'):
        geom.attrib.pop(attribute, None)
    geom.attrib.update(name=name, type='mesh', mesh=mesh_name,
                      mass=str(spec['mass']), condim='6', friction='1.2 .005 .002')
    return True
