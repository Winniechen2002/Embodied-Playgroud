"""Trusted construction of the forty native Isaac Lab / Franka scenes."""
import importlib.util
import math
from pathlib import Path
import random

from .catalog import BY_ID

ROOT = Path(__file__).resolve().parents[3]
NAMES = ('xlarge','large','medium','small','xsmall')
USD_NAMES = ('RingXLarge','RingLarge','RingMedium','RingSmall','RingXSmall')
OUTER = (.102,.091,.080,.069,.058)


def sample(task_id, seed=0, split='nominal'):
    if split not in ('nominal','train','heldout') or type(seed) is not int or seed < 0:
        raise ValueError('Invalid seed/split')
    task = BY_ID[task_id]
    r = random.Random(f'hanoi40-v1:{task_id}:{split}:{seed}')
    def delta(lo,hi):
        return r.choice((-1.,1.))*r.uniform(lo,hi)
    shift = [0.,0.] if split == 'nominal' else [delta(0,.004) if split=='train' else delta(.008,.012) for _ in range(2)]
    mf = 1. if split=='nominal' else 1.+(delta(0,.10) if split=='train' else delta(.15,.25))
    ff = 1. if split=='nominal' else 1.+(delta(0,.08) if split=='train' else delta(.12,.20))
    yaw = 0. if split=='nominal' else delta(0,2) if split=='train' else delta(3,5)
    theta = math.radians(yaw)
    pegs = []
    for x,y in task.pegs:
        # Local long axis maps to the original board's world Y axis.
        xx = x*math.cos(theta)-y*math.sin(theta)
        yy = x*math.sin(theta)+y*math.cos(theta)
        pegs.append((.67+yy+shift[0],xx+shift[1]))
    angles = [a+theta for a in task.handle_angles]
    return dict(task_id=task_id, seed=seed, split=split, pegs=pegs, bases=list(task.bases),
                masses=[m*mf for m in task.masses], friction=task.friction*ff,
                handle_angles=angles, board_shift=shift, board_yaw_deg=yaw,
                mass_factor=mf, friction_factor=ff, light_intensity=900 if split=='nominal' else r.uniform(700,1100))


def generate_assets(task_id, directory):
    task = BY_ID[task_id]
    spec = importlib.util.spec_from_file_location('_hanoi40_mesh_generator',ROOT/'scripts/generate_hanoi_ring_assets.py')
    gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
    directory = Path(directory); directory.mkdir(parents=True,exist_ok=True)
    gen.ASSET_DIR = directory; gen.RING_INNER_RADIUS = task.inner_radius
    gen.HANDLE_STEM_WIDTH = task.handle_width; gen.HANDLE_FLANGE_WIDTH = task.handle_width
    for (name, radius, color, _), angle in zip(gen.RINGS, task.handle_angles):
        gen._write_ring(name,radius,color,(math.cos(angle),math.sin(angle)))
    return directory


def spawn_ring(prim_path,cfg,*args,**kwargs):
    import copy
    from isaaclab.sim.spawners.from_files import spawn_from_usd
    from isaaclab.sim import schemas
    import isaaclab.sim as sim
    from isaaclab.sim.utils import bind_physics_material
    from agentbench.tasks.manager_based.table_top_manipulation.config.hanoi.hanoi_cfg import _iter_mesh_prims
    spawn = copy.copy(cfg); spawn.rigid_props=None; spawn.collision_props=None; spawn.mass_props=None
    prim = spawn_from_usd(prim_path,spawn,*args,**kwargs)
    path=str(prim.GetPath())
    schemas.define_rigid_body_properties(path,cfg.rigid_props)
    schemas.define_mass_properties(path,cfg.mass_props)
    for child in _iter_mesh_prims(prim):
        schemas.define_collision_properties(str(child.GetPath()),cfg.collision_props,stage=prim.GetStage())
        schemas.define_mesh_collision_properties(str(child.GetPath()),sim.ConvexHullPropertiesCfg(hull_vertex_limit=16),stage=prim.GetStage())
    # Friction is encoded in the per-case authored USD material by build_cfg.
    material = cfg.physics_material
    material.func(path+'/PhysicsMaterial',material)
    bind_physics_material(path,path+'/PhysicsMaterial',stage=prim.GetStage())
    return prim


def build_cfg(task_id, seed=0, split='nominal', asset_dir=None, vision=False, robot='franka'):
    from isaaclab.assets import AssetBaseCfg
    import isaaclab.sim as sim
    from agentbench.tasks.manager_based.table_top_manipulation.config.hanoi.hanoi_cfg import HanoiEnvFrankaPandaCfg_PLAY, HanoiEnvFrankaPandaVisionCfg_PLAY
    task=BY_ID[task_id]; params=sample(task_id,seed,split)
    if robot=='sharpa_no_arm':
        import copy
        from agentbench.tasks.manager_based.table_top_manipulation.config.sharpa_hanoi_no_arm.sharpa_hanoi_no_arm_cfg import SharpaHanoiNoArmEnvCfg_PLAY, SharpaHanoiNoArmVisionEnvCfg_PLAY
        from agentbench.tasks.manager_based.table_top_manipulation.config.hanoi.hanoi_cfg import HanoiSceneCfg
        cfg=(SharpaHanoiNoArmVisionEnvCfg_PLAY if vision else SharpaHanoiNoArmEnvCfg_PLAY)()
        cfg.scene.table=copy.deepcopy(HanoiSceneCfg(num_envs=1,env_spacing=2.5,replicate_physics=False).table)
        cfg.scene.robot.init_state.pos=(.67,-.40,1.32)
        cfg.hanoi40_fixed_robot_body='base_root'
    elif robot=='sharpa':
        from agentbench.tasks.manager_based.table_top_manipulation.config.sharpa_hanoi.sharpa_hanoi_cfg import SharpaHanoiEnvCfg_PLAY, SharpaHanoiVisionEnvCfg_PLAY
        cfg=(SharpaHanoiVisionEnvCfg_PLAY if vision else SharpaHanoiEnvCfg_PLAY)()
    elif robot=='franka':
        cfg=(HanoiEnvFrankaPandaVisionCfg_PLAY if vision else HanoiEnvFrankaPandaCfg_PLAY)()
    else:
        raise ValueError('Unknown robot: '+robot)
    cfg.seed=seed; cfg.scene.num_envs=1
    if robot=='franka':
        cfg.actions.gripper_action.close_command_expr={'panda_finger_.*':task.gripper_closed_half_width}
    asset_dir=generate_assets(task_id,asset_dir or ROOT/'outputs'/({'franka':'hanoi40','sharpa':'sharpa_hanoi40','sharpa_no_arm':'sharpa_hanoi_no_arm40'}[robot])/'assets'/task_id)
    cfg.scene.sky_light.spawn.texture_file=None
    cfg.scene.sky_light.spawn.intensity=params['light_intensity']
    # Broad support board; per-column pads account for deliberately raised supports.
    cfg.scene.hanoi_base.spawn.size=(.72,1.12,.025)
    cfg.scene.hanoi_base.init_state.pos=(.69,0.,.6125)
    for p, name in enumerate(('left','middle','right')):
        peg=getattr(cfg.scene,'peg_'+name); x,y=params['pegs'][p]; height=task.peg_heights[p]
        peg.spawn.height=height; peg.spawn.radius=task.peg_radius
        peg.init_state.pos=(x,y,.625+task.bases[p]+height/2)
        if task.bases[p]>0:
            pad=AssetBaseCfg(prim_path=f'{{ENV_REGEX_NS}}/Support{p}',
                spawn=sim.CuboidCfg(size=(.26,.26,task.bases[p]),collision_props=sim.CollisionPropertiesCfg(),
                    visual_material=sim.PreviewSurfaceCfg(diffuse_color=(.28,.38,.44))),
                init_state=AssetBaseCfg.InitialStateCfg(pos=(x,y,.625+task.bases[p]/2)))
            setattr(cfg.scene,'support_'+str(p),pad)
    for i,name in enumerate(NAMES):
        ring=getattr(cfg.scene,'ring_'+name); p=task.start[i]; level=sum(q==p for q in task.start[:i])
        x,y=params['pegs'][p]
        ring.spawn.usd_path=str(asset_dir/USD_NAMES[i])+'.usda'; ring.spawn.func=spawn_ring
        if robot=='sharpa_no_arm': ring.spawn.scale=(1.,1.,1.)
        ring.spawn.mass_props.mass=params['masses'][i]
        ring.spawn.physics_material=sim.RigidBodyMaterialCfg(static_friction=params['friction']*4/3,
            dynamic_friction=params['friction'],restitution=0.,friction_combine_mode='average',restitution_combine_mode='min')
        ring.init_state.pos=(x,y,.625+task.bases[p]+.0175+level*.035)
        yaw=math.radians(params['board_yaw_deg'])
        ring.init_state.rot=(math.cos(yaw/2),0.,0.,math.sin(yaw/2))
    for j,(x,y,z,hx,hy,hz) in enumerate(task.obstacles):
        theta=math.radians(params['board_yaw_deg']); xx=x*math.cos(theta)-y*math.sin(theta); yy=x*math.sin(theta)+y*math.cos(theta)
        obstacle=AssetBaseCfg(prim_path=f'{{ENV_REGEX_NS}}/Obstacle{j}',
            spawn=sim.CuboidCfg(size=(2*hy,2*hx,2*hz),collision_props=sim.CollisionPropertiesCfg(),
                visual_material=sim.PreviewSurfaceCfg(diffuse_color=(.34,.36,.39))),
            init_state=AssetBaseCfg.InitialStateCfg(pos=(.67+yy+params['board_shift'][0],xx+params['board_shift'][1],.625+z),
                rot=(math.cos(theta/2),0.,0.,math.sin(theta/2))))
        setattr(cfg.scene,'obstacle_'+str(j),obstacle)
    cfg.hanoi40_robot=robot
    cfg.hanoi40_task_id=task_id; cfg.hanoi40_parameters=params
    return cfg
