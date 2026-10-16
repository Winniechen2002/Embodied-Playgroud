"""Ten representative directed transitions on two embodiments, with explicit design (not empirical) difficulty."""
from dataclasses import asdict, dataclass
import hashlib
import importlib.util
from pathlib import Path
import sys

RULE_PATH = Path(__file__).resolve().parents[1] / 'agentbench/tasks/manager_based/table_top_manipulation/config/pocket_cube/pocket_cube_rules.py'
spec = importlib.util.spec_from_file_location('_cube20_base_rules', RULE_PATH)
rules = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = rules
spec.loader.exec_module(rules)
State = rules.PocketCubeState

def moves(text):
    result = []
    for token in text.split():
        if token[0] not in rules.FACE_NAMES or token[1:] not in ('', "'", '2'):
            raise ValueError(token)
        result.extend([(token[0], -1 if token.endswith("'") else 1)] * (2 if token.endswith('2') else 1))
    return tuple(result)

@dataclass(frozen=True)
class Task:
    id: str
    name: str
    category: str
    start_moves: str
    transition: str
    physics: str
    control: str
    ability: str
    tags: tuple[str, ...]
    difficulty: int
    physics_level: int
    control_level: int
    mass_scale: float = 1.
    friction_scale: float = 1.
    yaw_deg: float = 0.
    x_offset: float = 0.
    y_offset: float = 0.

    @property
    def start(self): return State().apply(moves(self.start_moves))
    @property
    def goal(self): return self.start.apply(moves(self.transition))
    def record(self):
        r = asdict(self)
        r.update(start_state=list(self.start.as_vector()), goal_state=list(self.goal.as_vector()),
                 quarter_turns=len(moves(self.transition)),
                 verify_commands={r:f'python scripts/validate_cube20_batch.py --robot {r} --tasks {self.id} --output outputs/cube20/{r}_{self.id}_new --headless --enable_cameras --device cuda:0' for r in ('aloha','sharpa')},
                 success='精确目标态；全部面落入1度定位区；无活动层；角速度<0.05 rad/s；连续保持1秒；无历史规则失败；场景指纹不变')
        return r

# Keep original candidates and IDs for provenance; only selected tasks are active.
CANDIDATES = (
 Task('C01','顶层顺转','竖轴基准','','U','分离上层转矩与底层支撑反力','一手固定下层，一手水平转动','识别活动层及反作用力',('竖轴','支撑','基准'),1,1,1),
 Task('C02','顶层逆转','方向辨识','R',"U'",'同一竖轴上的转矩反向','反向轨迹与终点减速','根据目标判断旋向，避免镜像错误',('逆转','目标辨识'),1,1,1),
 Task('C03','左层离台','侧轴净空','','L','侧层扫掠体积与台座碰撞','抬升、固定右层、左层转动','推断离台高度与支撑位置',('侧轴','离台','左手'),1,2,2),
 Task('C04','右层离台','双手角色','F','R','左右支撑的力矩平衡','左手承重，右手操作','迁移左右手角色及坐标映射',('侧轴','换角色','右手'),1,2,2),
 Task('C05','前层进深','前后轴可达','U','F','前向扫掠与手臂可达范围','进深接近与夹持避碰','三维轴向判断和可达性',('前轴','三维几何'),2,2,2),
 Task('C06','后层遮挡','背面操作','L',"B'",'背侧接触面与支撑反力','绕到背面建立接触','遮挡下状态保持与背面旋向',('后轴','遮挡','逆转'),2,2,3),
 Task('C07','底层脱座','下层接触','F R','D','台座承重与底层运动相冲突','从上层承重后抬升转下层','识别需要改变支撑的动作',('底轴','重抓','离台'),2,2,3),
 Task('C08','半周分段','定位连续性','B','U2','两次90度定位，禁止一次超行程','到位、重新建立接触、再转','连续动作分段与定位检查',('半周','定位','重复'),2,1,2),
 Task('C09','重载侧转','惯性变化','U F','L','总质量与转动惯量同步增大','提高支撑能力并降低加速度','区分尺寸与惯性，调整动作速度',('质量','惯性','侧轴'),3,2,3,mass_scale=1.5),
 Task('C10','低摩擦逆转','抗滑夹持','R U',"R'",'接触摩擦降低导致滑移风险','分配法向力并监测层间滑移','摩擦锥和夹持稳定性推断',('低摩擦','逆转','抗滑'),3,2,3,friction_scale=.65),
 Task('C11','斜置双轴','坐标变换','F B','U F','局部转轴与世界坐标不一致','在偏航25度姿态下切换轴','物体坐标到机器人坐标转换',('偏航','跨轴','换手'),3,2,3,yaw_deg=25),
 Task('C12','偏置对层','对面层串联','U R','L R','对面层虽可交换，支撑不能丢失','偏离中心处交换承重手','交换性与执行约束分离',('偏置','对面层','双手'),3,2,3,y_offset=.035),
 Task('C13','双轴顺序','非交换操作','L D','R U','不同转轴的先后次序影响终态','两次定位后换轴','预测R U与U R的不同结果',('非交换','双轴','顺序'),4,2,3),
 Task('C14','三轴接力','连续换手','B D','U F R','每次换轴重新分配支撑和扭矩','三轴转动与两次接触重建','子目标衔接及中间状态跟踪',('三轴','换手','接力'),4,3,3),
 Task('C15','回退修复','逆过程恢复','R U F',"F' U' R'",'逆过程需要逆序且反向','多次逆转并恢复统一面色','逆向规划与错误状态恢复',('复原','逆序','恢复'),4,2,3),
 Task('C16','双侧重载','耦合物性','F D','L2 B','重载和低摩擦同时限制加速度','半周分段后换到背轴','联合推断摩擦、惯性与换手风险',('质量','摩擦','半周'),4,3,3,mass_scale=1.3,friction_scale=.8),
 Task('C17','交换子环路','局部状态编辑','D F',"R U R' U'",'回到原转轴不等于回到原状态','四段正反转及重复换手','非交换性与中间状态记忆',('交换子','长序列','正反转'),5,3,3),
 Task('C18','共轭换位','临时重排','B R',"F U2 F'",'暂时扰动、局部操作、逆向恢复','半周两定位，回到原轴反转','共轭子目标与保留结构',('共轭','半周','恢复'),5,3,3),
 Task('C19','四轴复原','长程逆解','R U F L',"L' F' U' R'",'四个轴向支撑依赖与逆序关系','四轴逆转、偏航下持续追踪','长程逆向规划与坐标一致性',('四轴','复原','偏航'),5,3,3,yaw_deg=-20,x_offset=.02),
 Task('C20','复合扰动恢复','综合约束','F R U B',"B' U' R' F'",'偏置、质量、摩擦共同改变稳定余量','偏置处重抓与四段反向恢复','联合物理推断、闭环纠偏与长程控制',('综合','质量','摩擦','偏置'),5,3,3,mass_scale=1.25,friction_scale=.75,yaw_deg=15,y_offset=-.025),
)
SELECTED_IDS = ('C01','C03','C07','C08','C09','C10','C14','C15','C17','C20')
TASKS = tuple(t for t in CANDIDATES if t.id in SELECTED_IDS)
ROBOTS = ('aloha','sharpa')
ENTRIES = tuple((t,robot) for t in TASKS for robot in ROBOTS)
BY_ID = {t.id: t for t in TASKS}

def sample(task_id, seed, split):
    """Disjoint magnitude bands, sampled before scene construction only."""
    import random
    if split not in ('nominal', 'train', 'heldout') or type(seed) is not int or seed < 0:
        raise ValueError('Invalid split/seed')
    t = BY_ID[task_id]
    rng = random.Random(int.from_bytes(hashlib.sha256(f'cube20-v1/{task_id}/{split}/{seed}'.encode()).digest()[:8], 'big'))
    def perturb(lo, hi):
        if split == 'nominal': return 0.
        if split == 'train': return rng.uniform(-lo, lo)
        return rng.choice((-1, 1)) * rng.uniform(lo * 1.5, hi)
    return dict(task_id=task_id,seed=seed,split=split,
                x=.56+t.x_offset+perturb(.003,.008), y=t.y_offset+perturb(.003,.008),
                yaw_deg=t.yaw_deg+perturb(2.,5.),
                mass_scale=t.mass_scale*(1+perturb(.06,.15)),
                friction_scale=t.friction_scale*(1+perturb(.05,.12)),
                light=900. if split=='nominal' else rng.uniform(750,1050))
