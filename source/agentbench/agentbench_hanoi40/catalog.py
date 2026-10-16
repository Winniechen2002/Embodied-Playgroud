"""Forty five-ring Hanoi tasks. Ring indices 0..4 mean largest..smallest.

The pure symbolic layer is independent of simulators. All tasks preserve the
ordinary top-only / larger-below-smaller rules; start and goal may be split.
"""
from collections import deque
from dataclasses import asdict, dataclass
import hashlib
import json
import math


def successors(state):
    tops = {p: max((i for i, q in enumerate(state) if q == p), default=-1) for p in range(3)}
    for src, ring in tops.items():
        if ring < 0:
            continue
        for dst, below in tops.items():
            if dst != src and (below < 0 or ring > below):
                nxt = list(state); nxt[ring] = dst
                yield tuple(nxt), (ring, src, dst)


def shortest_distance(start, goal):
    """Measure task difficulty without constructing or returning solution moves."""
    start, goal = tuple(start), tuple(goal)
    for state in (start, goal):
        if len(state) != 5 or any(type(p) is not int or p not in range(3) for p in state):
            raise ValueError('A state must assign exactly five rings to pegs 0,1,2')
    q = deque([(start, 0)]); seen = {start}
    while q:
        state, distance = q.popleft()
        if state == goal:
            return distance
        for nxt, _ in successors(state):
            if nxt not in seen:
                seen.add(nxt); q.append((nxt, distance + 1))
    raise ValueError('Unreachable goal')


def state_at_distance(start, distance, index):
    q = deque([(tuple(start), 0)]); seen = {tuple(start)}; choices = []
    while q:
        s, d = q.popleft()
        if d == distance:
            choices.append(s); continue
        for nxt, _ in successors(s):
            if nxt not in seen:
                seen.add(nxt); q.append((nxt, d + 1))
    if not choices:
        raise ValueError((start, distance))
    return sorted(choices)[index % len(choices)]


@dataclass(frozen=True)
class Task:
    id: str
    name: str
    family: str
    level: int
    start: tuple
    goal: tuple
    pegs: tuple
    bases: tuple = (0., 0., 0.)
    peg_heights: tuple = (.22, .22, .22)
    peg_radius: float = .016
    inner_radius: float = .038
    masses: tuple = (.03, .03, .03, .03, .03)
    friction: float = 1.2
    handle_angles: tuple = (0., -math.pi/3, 0., math.pi/3, 0.)
    handle_width: float = .030
    gripper_closed_half_width: float = .014
    obstacles: tuple = ()  # boxes: x,y,z,hx,hy,hz
    tags: tuple = ()
    inference: str = ''
    control: str = ''
    distinction: str = ''

    @property
    def shortest_moves(self):
        return shortest_distance(self.start, self.goal)

    def record(self):
        d = asdict(self); d['shortest_moves'] = self.shortest_moves
        d['environment_id'] = f'Agentbench-Hanoi40-{self.id}-FrankaPanda-v0'
        d['verify_command'] = f'python scripts/validate_hanoi40.py --cases env/hanoi40/cases/{self.id}.json --images --headless --enable_cameras --device cuda:0 --output outputs/hanoi40/verify_{self.id}'
        d['static_command'] = d['verify_command'].replace(' --images','')
        d['control_verify_command'] = d['verify_command'].replace(' --images',' --execute')
        physical_grade=1 if self.family in ('状态分解','平面布局') else 3 if self.family=='组合约束' else 2
        precision_flags=[]
        if self.inner_radius-self.peg_radius<=.012: precision_flags.append('small_clearance')
        if max(self.bases)>=.08: precision_flags.append('raised_support')
        if max(self.peg_heights)>=.30: precision_flags.append('long_peg')
        if self.obstacles: precision_flags.append('obstacle')
        if self.family in ('把手方向','组合约束'): precision_flags.append('noncanonical_grasp_frame')
        if max(self.masses)>=.08: precision_flags.append('high_mass')
        if self.friction<=.8: precision_flags.append('low_friction')
        control_grade=3 if self.inner_radius-self.peg_radius<=.008 or len(precision_flags)>=3 else 2 if precision_flags else 1
        d['difficulty_axes']={'planning_depth':self.level,'physical_reasoning':physical_grade,'control':control_grade,'control_flags':precision_flags}
        d['control_schema']={'arm_joints':7,'arm_action_scale':.5,'gripper_action':'binary_symmetric_position',
            'gripper_open_half_width_m':.04,'gripper_closed_half_width_m':self.gripper_closed_half_width}
        d['control_sha256']=hashlib.sha256(json.dumps(d['control_schema'],sort_keys=True).encode()).hexdigest()
        physical = {k: v for k, v in d.items() if k in {'pegs','bases','peg_heights','peg_radius','inner_radius','masses','friction','handle_angles','handle_width','obstacles'}}
        d['physical_sha256'] = hashlib.sha256(json.dumps(physical, sort_keys=True).encode()).hexdigest()
        return d


FAMILIES = (
 ('状态分解', ('顶环换柱','双环局部迁移','分散态重组','五环长程重排'), '识别可移动顶环，推导中间状态和子目标依赖', '确认放置完成再开始下一步，避免移动非顶环', ('state_graph','subgoal','legal_order')),
 ('平面布局', ('斜列换位','三角转运','弧线重组','不对称长程'), '将符号柱位映射到不同平面坐标，比较路径与可达空间', '跨方向搬运，保持环孔对准目标柱', ('spatial_mapping','noncollinear','travel')),
 ('支撑高差', ('低台到高台','阶梯往返','高低交错','三台长程重排'), '区分柱顶高度与支撑面高度，计算抓放的世界坐标', '按各柱台高调整提升与下降终点', ('height','support','clearance')),
 ('插入净空', ('宽孔定位','中孔复位','窄孔重组','小净空长程'), '推断环孔和柱体允许的横向偏差及倾斜风险', '减小插入横向误差，低速接近接触面', ('insertion','tolerance','alignment')),
 ('质量分布', ('轻环抬升','重顶双环','逆质量重组','混合惯量长程'), '环尺寸不等于质量，判断夹持与加减速需求', '限制搬运加速度，维持摩擦夹持和静置稳定', ('mass','inertia','grip')),
 ('摩擦条件', ('高摩擦抓取','普通摩擦迁移','低摩擦重组','光滑环长程'), '推断法向夹持力与滑落、黏滞的关系', '闭夹后检验抬升，平滑搬运并等待释放', ('friction','slip','contact')),
 ('把手方向', ('斜柄单步','交错双柄','多向柄重组','异向长程'), '辨别抓取面朝向并将夹爪坐标变换到把手坐标', '绕竖轴定向，从对应方向对称夹持', ('grasp_frame','yaw','orientation')),
 ('路径障碍', ('低墙越障','中墙往返','偏置立障','高墙长程'), '将环的扫掠体积与墙顶净空一起规划', '先竖直拔离再越障，避免环和夹爪碰墙', ('obstacle','swept_volume','lift')),
 ('柱长差异', ('短柱换位','长短双柱','高柱重组','交错长柱'), '根据源柱和目标柱长度选择最低安全飞越高度', '先完全脱柱，再平移，插入时减速', ('peg_length','extraction','vertical_path')),
 ('组合约束', ('高台斜柄','窄孔三角','重环越障','综合长程'), '联合状态计划、接触稳定性、把手姿态和净空约束', '协调抓取朝向、提升高度与稳定放置', ('composition','multiconstraint','long_horizon')),
)


def build_catalog():
    tasks = []
    for row, (family, names, infer, control, tags) in enumerate(FAMILIES):
        for col in range(4):
            level = col + 1; ident = f'H{row * 4 + col + 1:02d}'
            # State graph distance, not a renamed initial-state seed.
            start = ((0,0,0,0,0), (0,0,0,1,0), (0,1,2,0,1), (0,0,0,0,0))[col]
            distance = (1, 3, 9, 31)[col]
            goal = state_at_distance(start, distance, row)
            span = .29 + col * .012 + row * .001
            pegs = ((-span,0.),(0.,0.),(span,0.))
            kw = {}
            if row == 1:
                pegs = (((-.30,-.08),(0.,0.),(.30,.08)), ((-.30,-.13),(0.,.16),(.30,-.13)), ((-.32,-.10),(-.03,.10),(.28,-.02)), ((-.38,-.14),(-.04,.09),(.32,-.05)))[col]
            elif row == 2:
                kw['bases'] = ((0.,.025,.05),(0.,.04,.08),(.065,0.,.035),(.04,.10,0.))[col]
            elif row == 3:
                kw['inner_radius'] = (.038,.032,.027,.023)[col]
            elif row == 4:
                kw['masses'] = ((.02,)*5,(.03,.03,.03,.055,.07),(.02,.07,.035,.08,.045),(.10,.065,.09,.04,.075))[col]
            elif row == 5:
                kw['friction'] = (1.8,1.2,.8,.55)[col]
            elif row == 6:
                kw['handle_angles'] = tuple(math.radians(x) for x in ((15,-45,15,45,15),(0,30,-30,30,-30),(45,-35,20,-45,35),(60,-50,30,-60,45))[col])
            elif row == 7:
                height = (.08,.15,.22,.30)[col]
                kw['obstacles'] = ((-span/2, .01, height/2, .018,.14,height/2),)
            elif row == 8:
                kw['peg_heights'] = ((.19,.21,.23),(.20,.29,.22),(.32,.20,.26),(.25,.34,.30))[col]
            elif row == 9:
                pegs = ((-span,-.06),(0.,.13),(span,-.06))
                kw.update(bases=(0., .02 + col*.01,.01), inner_radius=(.038,.030,.028,.025)[col],
                          handle_angles=tuple(math.radians(a) for a in (20,-25,35,-20,25)),
                          masses=tuple(.03*(1+col*.3) for _ in range(5)))
                if col >= 2:
                    kw['obstacles'] = ((-span/2,-.04,.12,.015,.10,.12),)
            distinction = f'{names[col]}；最短{distance}步；柱距/布局、接触参数按该任务固定，随机种子不计作新环境'
            tasks.append(Task(ident,names[col],family,level,start,goal,pegs,tags=tags,
                              inference=infer,control=control,distinction=distinction,**kw))
    return tuple(tasks)


TASKS = build_catalog()
BY_ID = {task.id: task for task in TASKS}
