"""Full-scale matched Hanoi40 scenes with the native standalone Sharpa hand.

The pre-existing half-scale sharpa_hanoi_no_arm environment remains unchanged.
"""
from dataclasses import asdict
import hashlib
import json
from .sharpa import SharpaTask, TASKS as ARMED_TASKS, HAND_JOINT_NAMES

TRANSLATION_JOINT_NAMES=('right_x_joint','right_y_joint','right_z_joint')
ROTATION_JOINT_NAMES=('right_roll_joint','right_pitch_joint','right_yaw_joint')
VIRTUAL_BODY_NAMES=('base_root',)+tuple(f'right_root_{i}' for i in range(1,6))
CONTROL={
    '状态分解':'自由手多指抓放，确认落座后切换子目标',
    '平面布局':'直接协调手掌平移、旋转和抓型，跨柱对准',
    '支撑高差':'推断掌指最低点，按台高调整自由手的升降与释放',
    '插入净空':'用手掌姿态和多指约束保持环孔对准，逐步松指',
    '质量分布':'协调掌部加速度与多指接触，避免重环滑移',
    '摩擦条件':'调整指间接触和闭合量，平滑搬运并控制释放',
    '把手方向':'直接定向手掌，协调拇指对掌和各指抓型',
    '路径障碍':'规划整只手与环的扫掠体积，抬升后越障',
    '柱长差异':'控制手掌拔出高度和横移时机，避免伸展手指碰柱',
    '组合约束':'联合六维掌位姿、多指抓型、净空和稳定释放',
}

class SharpaNoArmTask(SharpaTask):
    def record(self):
        d=super().record()
        d['embodiment']='floating_sharpa_right'
        d['environment_id']=f'Agentbench-Hanoi40-{self.id}-SharpaNoArm-v0'
        d['scene_scale']=1.0
        d['original_no_arm_default_scene_scale']=0.5
        d['verify_command']=f'python scripts/validate_hanoi40.py --robot sharpa_no_arm --cases env/sharpa_hanoi_no_arm40/cases/{self.id}.json --images --headless --enable_cameras --device cuda:0 --output outputs/sharpa_hanoi_no_arm40/verify_{self.id}'
        d['static_command']=d['verify_command'].replace(' --images','')
        d['control_schema']={'arm_joints':0,'pose_joints':6,'hand_joints':22,
            'action_dimension':28,'translation_action_scale_m':.03,
            'rotation_action_scale_rad':.1,'hand_action_scale_rad':.1,
            'action_type':'relative_joint_position_current_state',
            'translation_joint_names':list(TRANSLATION_JOINT_NAMES),
            'rotation_joint_names':list(ROTATION_JOINT_NAMES),
            'hand_joint_names':list(HAND_JOINT_NAMES),'robot_self_collisions':False,
            'external_contact_collisions':True,'support':'fixed_geometry_free_root_plus_6dof_virtual_chain',
            'root_position_m':[.67,-.40,1.32]}
        d['control_sha256']=hashlib.sha256(json.dumps(d['control_schema'],sort_keys=True).encode()).hexdigest()
        d['difficulty_axes']['embodiment_note']='C 为场景约束分级；无臂版考察六维手掌位姿与多指协调，不考察机械臂逆解或臂部避障'
        return d

TASKS=tuple(SharpaNoArmTask(**{**asdict(t),'control':CONTROL[t.family],
    'inference':t.inference.replace('腕部与手指坐标','手掌与手指坐标').replace('可达空间','手部通行空间'),
    'tags':t.tags+('free_palm_pose',)}) for t in ARMED_TASKS)
BY_ID={t.id:t for t in TASKS}
