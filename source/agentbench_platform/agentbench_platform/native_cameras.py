"""Explicit, non-advancing calibrated camera capture; no segmentation annotators."""
import numpy as np
from scipy.spatial.transform import Rotation

VIEWS = {
    'front_left': ((1.75,-2.05,1.55),(.70,0,.72),(0,0,1)),
    'front_right': ((1.75,2.05,1.55),(.70,0,.72),(0,0,1)),
    'top': ((.70,0,2.20),(.70,0,.60),(0,1,0)),
}
CONVENTION = 'opencv_x_right_y_down_z_forward'


def world_from_view(eye, target, up):
    eye,target,up = map(lambda v: np.asarray(v,dtype=float),(eye,target,up))
    forward = target-eye; forward /= np.linalg.norm(forward)
    right = np.cross(forward,up); right /= np.linalg.norm(right)
    down = np.cross(forward,right)
    matrix = np.eye(4); matrix[:3,:3] = np.column_stack((right,down,forward)); matrix[:3,3] = eye
    return matrix


def valid_depth(values, near, far):
    values = np.asarray(values,dtype='<f4')
    mask = np.isfinite(values) & (values >= near) & (values < far)
    return np.where(mask,values,0).astype('<f4'), mask.astype(np.uint8)


def add_cameras(cfg, *, views=None):
    """Configure before environment construction. Legacy cfg is untouched."""
    import isaaclab.sim as sim_utils
    from isaaclab.sensors import CameraCfg
    for name,args in (VIEWS if views is None else views).items():
        matrix = world_from_view(*args)
        q = Rotation.from_matrix(matrix[:3,:3]).as_quat()[[3,0,1,2]]
        setattr(cfg.scene,'benchmark_'+name,CameraCfg(
            prim_path='{ENV_REGEX_NS}/BenchmarkCamera_'+name,update_period=0.,
            width=640,height=480,data_types=['rgb','distance_to_image_plane'],
            depth_clipping_behavior='none',update_latest_camera_pose=True,
            spawn=sim_utils.PinholeCameraCfg(focal_length=20. if name=='top' else 24.,horizontal_aperture=32.,clipping_range=(.01,10.)),
            offset=CameraCfg.OffsetCfg(pos=tuple(matrix[:3,3]),rot=tuple(q),convention='ros')))


class NativeCameras:
    def __init__(self, env, resources, *, views=None, physical_arrays=None):
        self.env,self.resources = env,resources
        self.views = dict(VIEWS if views is None else views)
        self._task_physical_arrays = physical_arrays

    def description(self):
        return {name:dict(width=640,height=480,model='pinhole',calibration=self.calibration(name)) for name in self.views}

    def calibration(self,name):
        data = self.env.scene['benchmark_'+name].data
        q = data.quat_w_ros[0].cpu().numpy()
        matrix = np.eye(4)
        matrix[:3,:3] = Rotation.from_quat(q[[1,2,3,0]]).as_matrix()
        matrix[:3,3] = data.pos_w[0].cpu().numpy()
        return dict(intrinsics=data.intrinsic_matrices[0].cpu().numpy().tolist(),
                    world_from_camera=matrix.tolist(),convention=CONVENTION,near_m=.01,far_m=10.,
                    pixel_center_offset=[.5,.5])

    def capture(self,names,step):
        if not names:return {}
        if len(set(names)) != len(names) or not set(names)<=set(self.views):raise ValueError('Invalid cameras')
        before = (self.env._sim_step_counter, float(self.env.sim.current_time))
        def physical_arrays():
            if self._task_physical_arrays is not None:
                return [np.asarray(a).copy() for a in self._task_physical_arrays()]
            arrays=[self.env.scene['piece_'+n].data.root_state_w for n in self.env.lock_piece_names]
            for side in ('left','right'):
                data=self.env.scene[side+'_robot'].data
                arrays.extend((data.joint_pos,data.joint_vel,data.body_state_w))
            return [a.detach().cpu().numpy().copy() for a in arrays]
        state_before=physical_arrays()
        # Render twice to flush RTX's one-frame pipeline, without sim.step/app.update.
        for _ in range(2): self.env.sim.render()
        result = {}
        for name in names:
            sensor = self.env.scene['benchmark_'+name]
            sensor.update(0.,force_recompute=True)
            data = sensor.data
            rgb = data.output['rgb'][0].cpu().numpy().astype(np.uint8)
            depth,mask = valid_depth(data.output['distance_to_image_plane'][0].cpu().numpy().reshape(480,640),.01,10.)
            result[name] = self.resources.register_capture(camera_id=name,capture_step=step,
                rgb=rgb.tobytes(),depth=depth.tobytes(),validity=mask.tobytes(),calibration=self.calibration(name))
        if (self.env._sim_step_counter, float(self.env.sim.current_time)) != before:raise RuntimeError('Render advanced physics')
        state_after=physical_arrays()
        if len(state_before)!=len(state_after) or not all(np.array_equal(a,b) for a,b in zip(state_before,state_after)):
            raise RuntimeError('Render changed measured piece or robot state')
        return result


def add_target_outlines(env, spec, *, mode=None):
    """Thin visual curves only, never collision geometry or control overlays."""
    from pxr import UsdGeom, UsdShade, Sdf, Gf
    stage = env.sim.stage
    material=UsdShade.Material.Define(stage,'/World/BenchmarkTargetMaterial')
    shader=UsdShade.Shader.Define(stage,'/World/BenchmarkTargetMaterial/Shader')
    shader.CreateIdAttr('UsdPreviewSurface')
    shader.CreateInput('diffuseColor',Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(.005,.12,.008))
    shader.CreateInput('roughness',Sdf.ValueTypeNames.Float).Set(1.)
    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(),'surface')
    rectangles = [(.50,.95,-.22,.22)] if (mode or env.task_mode.value)=='assemble' else [
        (p.target_position[0]-.04,p.target_position[0]+.04,p.target_position[1]-.04,p.target_position[1]+.04)
        for p in spec.pieces]
    if (mode or env.task_mode.value)=='disassemble' and getattr(env,'case_spec',None):
        case=env.case_spec
        targets=case['target_pieces'] or list(case['pieces'])
        rectangles=[(case['goal_state'][name][0][0]-.04,case['goal_state'][name][0][0]+.04,
                     case['goal_state'][name][0][1]-.04,case['goal_state'][name][0][1]+.04) for name in targets]
    for index,(x0,x1,y0,y1) in enumerate(rectangles):
        curve = UsdGeom.BasisCurves.Define(stage,f'/World/BenchmarkTarget{index}')
        curve.CreateTypeAttr('linear'); curve.CreateWrapAttr('nonperiodic')
        curve.CreateCurveVertexCountsAttr([5])
        curve.CreatePointsAttr([Gf.Vec3f(x,y,.602) for x,y in ((x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0))])
        curve.CreateWidthsAttr([.006]);curve.SetWidthsInterpolation('constant')
        curve.CreateDisplayColorAttr([Gf.Vec3f(.005,.12,.008)])
        UsdShade.MaterialBindingAPI.Apply(curve.GetPrim()).Bind(material)
