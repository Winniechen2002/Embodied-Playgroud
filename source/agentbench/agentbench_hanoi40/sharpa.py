"""Sharpa embodiments of the same forty Hanoi state/physics tasks.

Pure catalog metadata is importable without starting Isaac Sim.
"""
from dataclasses import asdict
import hashlib
import json
from .catalog import Task, TASKS as FRANKA_TASKS

HAND_JOINT_NAMES = (
    'right_index_MCP_FE','right_index_MCP_AA','right_index_PIP','right_index_DIP',
    'right_middle_MCP_FE','right_middle_MCP_AA','right_middle_PIP','right_middle_DIP',
    'right_ring_MCP_FE','right_ring_MCP_AA','right_ring_PIP','right_ring_DIP',
    'right_pinky_CMC','right_pinky_MCP_FE','right_pinky_MCP_AA','right_pinky_PIP','right_pinky_DIP',
    'right_thumb_CMC_FE','right_thumb_CMC_AA','right_thumb_MCP_FE','right_thumb_MCP_AA','right_thumb_IP',
)
CONTROL = {
    '状态分解':'多指抓放后确认落座，避免邻指扰动非顶环',
    '平面布局':'协调腕姿与多指抓型，跨方向搬运并保持孔柱对准',
    '支撑高差':'按台高调整腕部和手指的抓放高度，留足掌指净空',
    '插入净空':'保持多指夹持姿态，精确对孔并逐步松指落座',
    '质量分布':'协调多指接触与搬运加速度，避免重环滑落',
    '摩擦条件':'调整多指接触和闭合量，控制滑移与释放时机',
    '把手方向':'联合腕姿、拇指对掌与其余手指抓型匹配把手方向',
    '路径障碍':'规划掌部、所有手指与环的扫掠体积，先拔离再越障',
    '柱长差异':'按柱长提升手腕和环，避免伸展手指碰柱',
    '组合约束':'同时协调多指抓型、腕姿、提升高度与稳定释放',
}

class SharpaTask(Task):
    def record(self):
        d=super().record()
        d.pop('gripper_closed_half_width')
        d['embodiment']='fr3_sharpa_right'
        d['environment_id']=f'Agentbench-Hanoi40-{self.id}-Sharpa-v0'
        d['verify_command']=f'python scripts/validate_hanoi40.py --robot sharpa --cases env/sharpa_hanoi40/cases/{self.id}.json --images --headless --enable_cameras --device cuda:0 --output outputs/sharpa_hanoi40/verify_{self.id}'
        d['static_command']=d['verify_command'].replace(' --images','')
        d.pop('control_verify_command')
        d['control_schema']={'arm_joints':7,'arm_action_scale':.5,'hand_joints':22,
            'hand_action_scale':.1,'hand_action':'joint_position_default_offset',
            'hand_joint_names':list(HAND_JOINT_NAMES),'action_dimension':29,
            'robot_self_collisions':False,'external_contact_collisions':True}
        d['control_sha256']=hashlib.sha256(json.dumps(d['control_schema'],sort_keys=True).encode()).hexdigest()
        d['difficulty_axes']['embodiment_note']='C 为任务约束分级；Sharpa 所有任务还需多指协调，不是跨机器人成功率排名'
        return d

TASKS=tuple(SharpaTask(**{**asdict(t),'control':CONTROL[t.family],'inference':t.inference.replace('夹爪坐标','腕部与手指坐标'),
    'tags':t.tags+('dexterous_hand','finger_coordination')}) for t in FRANKA_TASKS)
BY_ID={t.id:t for t in TASKS}
