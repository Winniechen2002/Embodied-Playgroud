"""Restore native robot SRDF semantics omitted from the relocated asset bundle."""
from pathlib import Path
import xml.etree.ElementTree as ET


def restore_native_self_collision_filters(agent):
    """Apply the same Default pairs and parent exclusions as SAPIEN's loader.

    The converted URDFs live outside ManiSkill's asset directory, so SAPIEN
    cannot discover their original sibling SRDF files automatically. Read the
    pinned dependency's original SRDF; keep all other self/object collisions.
    """
    from mani_skill import PACKAGE_ASSET_DIR
    files = {'fetch': 'fetch/fetch.srdf', 'panda': 'panda/panda_v2.srdf'}
    if agent.uid not in files:
        return
    srdf = Path(PACKAGE_ASSET_DIR) / 'robots' / files[agent.uid]
    loader = agent.scene.create_urdf_loader()
    pairs = loader.parse_srdf(srdf.read_text())
    root = ET.parse(agent.urdf_path).getroot()
    parents = {j.find('child').get('link'): j.find('parent').get('link')
               for j in root.findall('joint')}
    bit = 0
    for pair in pairs:
        left, right = sorted(pair)
        if parents.get(left) == right or parents.get(right) == left:
            continue
        if bit >= 30:
            raise ValueError('Robot SRDF overlaps reserved Fetch collision bits')
        for name in (left, right):
            agent.robot.links_map[name].set_collision_group_bit(group=2, bit_idx=bit, bit=1)
        bit += 1


def configure_fetch_floor(env):
    """Filter the ground against Fetch's planar base and non-rolling wheels."""
    if env.task['robot']['uid'] == 'fetch':
        from mani_skill.agents.robots.fetch.fetch import (
            FETCH_WHEELS_COLLISION_BIT, FETCH_BASE_COLLISION_BIT)
        # Neither wheels nor the base have vertical freedom. Ground contact
        # creates unsatisfiable penetration constraints; walls/objects still collide.
        env.supports['floor'].set_collision_group_bit(
            group=2, bit_idx=FETCH_WHEELS_COLLISION_BIT, bit=1)

        env.supports['floor'].set_collision_group_bit(
            group=2, bit_idx=FETCH_BASE_COLLISION_BIT, bit=1)
