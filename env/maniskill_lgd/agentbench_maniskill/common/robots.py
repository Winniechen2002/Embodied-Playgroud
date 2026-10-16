"""Register only the three converted arm/hand combinations used by this suite."""
import json
import xml.etree.ElementTree as ET
import numpy as np
from mani_skill.agents.base_agent import BaseAgent
from mani_skill.agents.controllers import PDJointPosControllerConfig
from mani_skill.agents.registration import register_agent
from .paths import LEGACY, NATIVE_ROOT
SUPPORTED_ROBOTS=['fetch','panda','everyday_robot_01','everyday_robot_03','everyday_robot_09']
_REGISTERED=False

class EverydayAgent(BaseAgent):
    fix_root_link=True
    disable_self_collisions=True
    load_multiple_collisions=False
    def _after_loading_articulation(self):
        for joint in self.robot.get_active_joints():
            for native in joint._objs:
                native.set_max_velocity(3.0)
                native.set_armature(np.full(native.dof,1e-4 if joint.name.startswith('hand_') else .02))
    @property
    def _controller_configs(self):
        return {'pd_joint_pos':dict(
            arm=PDJointPosControllerConfig(self.arm_joint_names,None,None,stiffness=1200,damping=100,force_limit=140,normalize_action=False,drive_mode='force'),
            hand=PDJointPosControllerConfig(self.hand_joint_names,None,None,stiffness=15,damping=.5,force_limit=1.2,normalize_action=False,drive_mode='force'))}

def register_robots():
    global _REGISTERED
    if _REGISTERED:return
    from .preflight import check_robot
    for uid in SUPPORTED_ROBOTS:check_robot(uid)
    from mani_skill.agents.robots.fetch.fetch import Fetch
    from mani_skill.agents.robots.panda.panda import Panda
    Fetch.urdf_path=str(NATIVE_ROOT/'fetch/fetch.urdf')
    Panda.urdf_path=str(NATIVE_ROOT/'panda/panda_v2.urdf')
    for i in [1,3,9]:
        folder=next((LEGACY/'robots').glob(f'{i:02d}_*'))
        meta=json.loads((folder/'physical_model.json').read_text())
        cls=type(f'EverydayRobot{i:02d}',(EverydayAgent,),dict(
            uid=f'everyday_robot_{i:02d}',urdf_path=str(folder/'robot.urdf'),
            urdf_config=dict(_materials=dict(fingertip=dict(static_friction=2.0,dynamic_friction=1.5,restitution=0.0)),link={l.get('name'):dict(material='fingertip',patch_radius=.01,min_patch_radius=.005) for l in ET.parse(folder/'robot.urdf').findall('link') if l.get('name').startswith('hand_')}),
            arm_joint_names=meta['arm_joint_names'],hand_joint_names=meta['hand_joint_names']))
        register_agent()(cls)
    _REGISTERED=True
