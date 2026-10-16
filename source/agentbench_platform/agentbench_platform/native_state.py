"""Read-only physical extraction from the one existing Kongming environment."""
import numpy as np
from scipy.spatial.transform import Rotation


def plain(tensor):return tensor.detach().cpu().numpy().tolist()


def rigid_parameters(view, *, body_names):
    """Effective PhysX values; inertia is in each body's local COM frame.

    First dimension is the single environment. Remaining body/shape order is
    the native view order; material columns are static/dynamic/restitution.
    """
    return dict(body_names=list(body_names),shape_indices=list(range(len(plain(view.get_material_properties()[0])))),
        mass_kg=plain(view.get_masses()[0]),inertia_kg_m2=plain(view.get_inertias()[0]),
        material_static_dynamic_restitution=plain(view.get_material_properties()[0]),
        contact_offset_m=plain(view.get_contact_offsets()[0]),rest_offset_m=plain(view.get_rest_offsets()[0]))


def rotation(q):return Rotation.from_quat(np.asarray(q)[[1,2,3,0]]).as_matrix()


def scorer_spec(spec, collision_boxes, table_z, *, case_spec=None):
    pieces = {}
    for p in spec.pieces:
        row = dict(centers=collision_boxes(p)[0].tolist(),
            half_extents=collision_boxes(p)[1].tolist(),assembly_position=list(p.assembly_position),
            assembly_quaternion=list(p.assembly_quat_wxyz),target_position=list(p.target_position),
            target_quaternion=list(p.target_quat_wxyz),
            initial_position=list(p.assembly_position), initial_quaternion=list(p.assembly_quat_wxyz),
            parking_position=list(p.target_position), parking_quaternion=list(p.target_quat_wxyz))
        if case_spec is not None:
            row['initial_position'], row['initial_quaternion'] = case_spec['initial'][p.name]
            row['target_position'], row['target_quaternion'] = case_spec['goal_state'][p.name]
            row['parking_position'], row['parking_quaternion'] = (
                case_spec['pieces'][p.name]['parking_position'], case_spec['pieces'][p.name]['parking_quaternion'])
        pieces[p.name] = row
    return dict(table_top_z=table_z, pieces=pieces,
        case_id=case_spec.get('case_id') if case_spec else None,
        subtask=case_spec.get('subtask') if case_spec else 'complete',
        target_pieces=list(case_spec.get('target_pieces', ())) if case_spec else [])


def action_bounds(defaults, limits):
    """Bounds whose actual float32 q=default+.5*a stays within hard limits."""
    defaults=np.asarray(defaults,dtype=np.float32);limits=np.asarray(limits,dtype=np.float32)
    bounds=[]
    for column,direction in ((0,np.inf),(1,-np.inf)):
        values=((limits[:,column].astype(float)-defaults.astype(float))/.5).astype(np.float32)
        for index in range(len(values)):
            while ((defaults[index]+np.float32(.5)*values[index] < limits[index,column]) if column==0
                   else (defaults[index]+np.float32(.5)*values[index] > limits[index,column])):
                values[index]=np.nextafter(values[index],np.float32(direction))
        bounds.append(values.astype(float).tolist())
    return bounds


class IsaacState:
    def __init__(self, env, spec):
        if str(env.device)!='cpu' or env.cfg.decimation!=4 or abs(env.physics_dt-1/120)>1e-10:
            raise ValueError('Benchmark requires single-env CPU PhysX at 120/30 Hz')
        self.env,self.spec=env,spec
        self.reset_done=False
        self._parameters=None

    def reset(self):
        if self.reset_done:raise RuntimeError('Reset already used')
        self.env.reset();self.reset_done=True
        # Only robot joint targets are legal after reset. Instrument every
        # public rigid-object state setter, including velocity-only mutation.
        for name in self.spec['pieces']:
            piece=self.env.scene['piece_'+name]
            for method in dir(piece):
                if method.startswith('write_root_') and method.endswith('_to_sim'):
                    setattr(piece,method,self._deny_object_write)

    @staticmethod
    def _deny_object_write(*args,**kwargs):raise RuntimeError('Post-reset object state write prohibited')

    def install_hook(self,hook):self.env.benchmark_substep_hook=hook

    def reset_acceptance(self):
        """Check the trusted initial pose without advancing physics."""
        import math
        measured = self.pieces()
        rows = {}
        passed = True
        for name, expected in self.spec['pieces'].items():
            position = np.asarray(measured[name]['position'], dtype=float)
            quaternion = np.asarray(measured[name]['quaternion'], dtype=float)
            # Canonical legacy environments use parking poses for assembly
            # and assembled poses for disassembly.  Public cases carry an
            # explicit trusted initial pose, so keep that projection intact.
            if self.spec.get('case_id') is None:
                if self.env.task_mode.value == 'assemble':
                    target = np.asarray(expected['parking_position'], dtype=float)
                    target_q = np.asarray(expected['parking_quaternion'], dtype=float)
                else:
                    target = np.asarray(expected['assembly_position'], dtype=float)
                    target_q = np.asarray(expected['assembly_quaternion'], dtype=float)
            else:
                target = np.asarray(expected['initial_position'], dtype=float)
                target_q = np.asarray(expected['initial_quaternion'], dtype=float)
            position_error = float(np.linalg.norm(position-target))
            dot = abs(float(np.dot(quaternion/np.linalg.norm(quaternion), target_q/np.linalg.norm(target_q))))
            angle_error = float(2*math.acos(np.clip(dot, 0., 1.)))
            speed = float(np.linalg.norm(measured[name]['linear_velocity']))
            spin = float(np.linalg.norm(measured[name]['angular_velocity']))
            row = dict(position_error_m=position_error, angle_error_rad=angle_error,
                       speed_m_s=speed, spin_rad_s=spin)
            rows[name] = row
            passed = passed and position_error <= .003 and angle_error <= .05 and speed < .01 and spin < .10
        return dict(passed=bool(passed), case_id=self.spec.get('case_id'), pieces=rows,
                    state_hash=self.env.case_spec.get('state_hash') if getattr(self.env, 'case_spec', None) else None)

    def describe(self):
        robots={};low=[];high=[];names=[]
        for side in ('left','right'):
            r=self.env.scene[side+'_robot'];d=r.data
            ids=r.find_joints('panda_joint[1-7]')[0]
            limits=plain(d.joint_pos_limits[0]);defaults=plain(d.default_joint_pos[0])
            arm_low,arm_high=action_bounds([defaults[i] for i in ids],[limits[i] for i in ids])
            for j,i in enumerate(ids):
                low.append(arm_low[j]);high.append(arm_high[j])
                names.append(side+'.'+r.joint_names[i])
            low.append(-1.);high.append(1.);names.append(side+'.gripper')
            robots[side]=dict(model='Franka Panda',joint_names=list(r.joint_names),default_joint_positions=defaults,
                joint_limits=limits,soft_joint_limits=plain(d.soft_joint_pos_limits[0]),joint_action_scale=.5,
                base_position=plain(d.root_pos_w[0]),base_quaternion=plain(d.root_quat_w[0]))
        description = ('Assemble the six wooden pieces inside the green region.'
                       if self.env.task_mode.value == 'assemble'
                       else 'Disassemble the wooden structure and park each piece in a green region.')
        task=dict(task_id='kongming-v1', id='kongming-v1', family='kongming_lock', name='Kongming lock',mode=self.env.task_mode.value,
            case_id=getattr(self.env, 'case_id', None), subtask=getattr(self.env, 'case_subtask', 'complete'),
            description=description)
        if getattr(self.env, 'case_spec', None):
            from .kongming_cases import describe_case_spec
            case = describe_case_spec(self.env.case_spec)
            task.update(description=case['description'], target_pieces=case['target_pieces'])
        return dict(task=task, action_spec=dict(size=16,low=low,high=high,names=names,
                neutral_action=([0.]*7+[1.])*2,
                semantics=['Seven arm targets per side: q=default_q+0.5*action.',
                    'Eighth coordinate is continuous: each finger target is 0.02*(action+1) m.' if self.env.task_mode.value=='assemble'
                    else 'Eighth coordinate is binary: action < 0 closes each finger to 0 m; action >= 0 opens to 0.04 m.']),
            robots=robots,cameras={},goal=dict(mode=self.env.task_mode.value,position_tolerance_m=.0075 if self.env.task_mode.value=='assemble' else .025,
                angular_tolerance_rad=.08 if self.env.task_mode.value=='assemble' else .25,penetration_ceiling_m=.002,stable_controls=60 if self.env.task_mode.value=='assemble' else 30))

    def pieces(self):
        rows={}
        for name in self.spec['pieces']:
            d=self.env.scene['piece_'+name].data
            rows[name]=dict(position=plain(d.root_pos_w[0]),quaternion=plain(d.root_quat_w[0]),
                linear_velocity=plain(d.root_lin_vel_w[0]),angular_velocity=plain(d.root_ang_vel_w[0]))
        return rows

    def physical(self,control,physics):
        robots={}
        for side in ('left','right'):
            r=self.env.scene[side+'_robot'];d=r.data;i=r.find_bodies('panda_hand')[0][0]
            fingers=r.find_joints('panda_finger_joint.*')[0]
            hand=np.array(plain(d.body_pos_w[0,i]));q=plain(d.body_quat_w[0,i])
            contacts=[]
            for suffix in ('finger_piece_contact','other_finger_piece_contact'):
                sensor=self.env.scene[side+'_'+suffix]
                # scene.update marks sensors outdated every physics_dt;
                # reading .data now acquires current PhysX force buffers.
                data=sensor.data;filtered=data.force_matrix_w[0].sum(0)
                if tuple(filtered.shape)!=(29,3):raise RuntimeError('Incomplete finger sensor coverage')
                contacts.append(dict(net_w=plain(data.net_forces_w[0].sum(0)),
                    allowed_piece_sum_w=plain(filtered[:6].sum(0)),forbidden_forces_w=plain(filtered[6:])))
            arm=plain(self.env.scene[side+'_arm_contacts'].data.net_forces_w[0])
            if len(arm)!=8:raise RuntimeError('Incomplete arm sensor coverage')
            robots[side]=dict(fingers=plain(d.joint_pos[0,fingers]),tcp=(hand+rotation(q)@np.array([0,0,.1034])).tolist(),
                arm_forces_w=arm,finger_contacts=contacts)
        return dict(control_step=control,physics_step=physics,pieces=self.pieces(),robots=robots)

    def snapshot(self,control,previous_action):
        robots={};bodies={};jacobians={};contacts=[]
        for side in ('left','right'):
            r=self.env.scene[side+'_robot'];d=r.data
            ids=r.find_joints('panda_joint[1-7]')[0];fingers=r.find_joints('panda_finger_joint.*')[0]
            jac=r.root_physx_view.get_jacobians()[0]
            for index,name in enumerate(r.body_names):
                bodies[side+'.'+name]=dict(position=plain(d.body_pos_w[0,index]),quaternion=plain(d.body_quat_w[0,index]),
                    com_position=plain(d.body_com_pos_w[0,index]),
                    linear_velocity=plain(d.body_link_lin_vel_w[0,index]),angular_velocity=plain(d.body_link_ang_vel_w[0,index]))
                if index:jacobians[side+'.'+name]=plain(jac[index-1][:,ids])
            robots[side]=dict(joint_names=list(r.joint_names),joint_positions=plain(d.joint_pos[0]),
                joint_velocities=plain(d.joint_vel[0]),measured_finger_positions=plain(d.joint_pos[0,fingers]),
                previous_action=list(previous_action))
            sensor=self.env.scene[side+'_arm_contacts']
            for name,force in zip(sensor.body_names,plain(sensor.data.net_forces_w[0])):
                contacts.append(dict(body_a=side+'.'+name,body_b='unresolved_contact',force_vector_n=force))
            for finger,suffix in (('left','finger_piece_contact'),('right','other_finger_piece_contact')):
                data=self.env.scene[side+'_'+suffix].data;matrix=data.force_matrix_w[0].sum(0)
                for name,force in zip(self.spec['pieces'],plain(matrix[:6])):
                    contacts.append(dict(body_a=side+'.panda_'+finger+'finger',body_b='piece_'+name,force_vector_n=force))
                residual=data.net_forces_w[0].sum(0)-matrix[:6].sum(0)
                contacts.append(dict(body_a=side+'.panda_'+finger+'finger',body_b='unresolved_contact',force_vector_n=plain(residual)))
        if self._parameters is None:
            self._parameters={name:rigid_parameters(self.env.scene[name].root_physx_view, body_names=self.env.scene[name].body_names)
                for name in ['left_robot','right_robot','table']+['piece_'+n for n in self.spec['pieces']]}
        return dict(robots=robots,privileged=dict(pieces=self.pieces(),robot_bodies=bodies,jacobians=jacobians,contacts=contacts if control else [],
            geometry={n:dict(collision_boxes=[[c,h] for c,h in zip(p['centers'],p['half_extents'])]) for n,p in self.spec['pieces'].items()},
            physics=dict(physics_hz=120,control_hz=30,timestep_s=1/120,gravity=list(self.env.cfg.sim.gravity),rigid_bodies=self._parameters),
            diagnostics={}))

    def apply(self,action):
        import torch
        value=torch.tensor(action,dtype=torch.float32,device='cpu').view(1,16)
        self.env.step(value)
        return plain(value[0])
