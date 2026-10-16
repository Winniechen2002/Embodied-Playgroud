import os
import sys
import torch
import yaml
import argparse
import numpy as np
import xml.etree.ElementTree as ET
import transforms3d
import time
from tqdm import tqdm
from PIL import Image
import scipy.io as scio
import pytorch3d
from graspnetAPI.utils.xmlhandler import xmlReader
from graspnetAPI.utils.utils import parse_posevector

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.realpath('.'))
from src.utils.robot_model import RobotModel
from src.utils.pc import depth_image_to_point_cloud, get_workspace_mask
from src.utils.vis_plotly import Vis
from src.utils.pose_refine import PoseRefine

def get_orig_scene(scene_id):
    idx = int(scene_id)
    if idx >= 1000:
        idx = (idx - 1000) // 75
    return str(idx).zfill(4)

intersect_finder = PoseRefine()

parser = argparse.ArgumentParser()
parser.add_argument('--device', type=str, default='cuda:0')
parser.add_argument('--start', type=int, default=0)
parser.add_argument('--end', type=int, default=1)
parser.add_argument('--fraction', type=int, default=1)

# parser.add_argument('--scene_data_root', type=str, default='data/scene_dexgrasp')
# parser.add_argument('--dataset_path', type=str, default='data/scene_dexgrasp')
parser.add_argument('--save_root', type=str, default='data/dex_graspness_new')
parser.add_argument('--grasp_save_root', type=str, default='data/dex_grasps_new')
parser.add_argument('--urdf_path', type=str,default='robot_models/urdf/leap_hand_simplified.urdf')
parser.add_argument('--robotmodel_meta_path', type=str,default='robot_models/meta/leap_hand/meta.yaml')
parser.add_argument('--widthmapper_meta_path', type=str,default='robot_models/meta/leap_hand/width_mapper_meta.yaml')
parser.add_argument('--scene_id', type=str, default='0001')
parser.add_argument('--view_id', type=str, default='0000')
parser.add_argument('--object_points', type=int, default=1000)
parser.add_argument('--robot_name', type=str,
    default='leap_hand', choices=['leap_hand'])
parser.add_argument('--camera', type=str,
    default='realsense', choices=['kinect', 'realsense'])
parser.add_argument('--gt_depth', type=int, default=1)

parser.add_argument('--object_collision_thr', type=float, default=0.002)
parser.add_argument('--scene_collision_thr', type=float, default=0.0025)
parser.add_argument('--cone_height_diff', type=float, default=0.02)
parser.add_argument('--graspness_assignment_thr', type=float, default=0.015)
# parser.add_argument('--midpoint_height', type=float, default=0.02)
parser.add_argument('--cone_angle', type=float, default=30.0)
args = parser.parse_args()

robot_model = RobotModel(args.urdf_path, args.robotmodel_meta_path)
vis = Vis(args.robot_name, args.urdf_path, args.robotmodel_meta_path)

def get_weight(args, heights, angles, midpoints_local, min_valid_height, positive_mask):
    '''
    implementation of weight-allocation distribution
    inputs of shape [B,n] = [num_grasps, num_points]
    output [n] = [num_points]
    '''
    # reference to /mnt/disk0/danshili/Development/DexGraspNet1B/src/scripts/compute_graspness.py
    # weights = torch.zeros(heights.shape[-1], device=heights.device)
    
    # calculate the distance of grasp midpoint
    # midpoint_distance = midpoints_local.norm(dim=-1)
    # or we can hard-write
    # midpoint_heights = args.midpoint_height
    
    # calculate point probability density
    '''
    Note on units of decay: height is calculated in m and angle calculated in radians.
    height diff truncated at 0.05
    angle diff truncated at (30 degree) 0.52
    We intentionally want the decay to be more strict along the angle dimension so that graspness will 
    focus on palm-facing points and avoid being allocated to side-facing points.
    '''
    
    # coef_angle = -np.sqrt((50 * np.log(10))) / 10
    # coef_height = -np.sqrt((50 * np.log(10))) / 10
    coef_angle = -180 / np.pi * np.log(2) / 10 # decay 50% at 10 degree
    coef_height = -np.log(2) / 0.015 # decay 50% at 1.5 cm
    angle_decay = (coef_angle * angles) # [B,n]
    # decay w.r.t height starting from the point nearest in height. This way to enforce palm-facing points get allocated maximal graspness
    height_decay = (coef_height * (heights - min_valid_height)) # [B,n]
    return ((angle_decay + height_decay).exp() * positive_mask) #.sum(dim=0) #[n]
    

def allocate_sample_weights(args, obj_point_palm, midpoints_local):
    '''
    given object points in graspness cone frame, get sample weights    
    Input:  obj_point_palm[B,n,3] points in cone frame
    Output:
    '''
    # get angle and height(x-value)
    heights = obj_point_palm[:,:,0]

    angles = torch.arccos(torch.abs(heights) / torch.norm(obj_point_palm,dim=-1))
    # print(angles.min(dim=-1).values / torch.pi * 180)
    # print(angles.min(dim=-1).values.max() / torch.pi * 180)
    # mask = (heights > 0) * (angles < 5 / 180 * torch.pi)
    # heights_masked = heights.clone()
    # heights_masked[~mask] = 1000
    # best_point = heights_masked.argmin(dim=-1)
    # dist = (obj_point_palm - obj_point_palm[torch.arange(obj_point_palm.shape[0]), best_point][:,None]).norm(dim=-1)
    # weights = 10 ** (-dist * 150)
    # assign weights
    # (heights < args.cone_height)
    positive_mask = (heights > 0) * (angles < args.cone_angle / 180 * torch.pi)
    assert (positive_mask.sum(dim=-1) > 0).all()

    min_valid_height = heights.clone()
    min_valid_height[~positive_mask] = 100.0
    best_point = min_valid_height.argmin(dim=-1)
    min_valid_height = min_valid_height.min(dim=-1,keepdim=True)[0]

    positive_mask = (torch.abs(heights - min_valid_height) < args.cone_height_diff) * positive_mask
    raw_weights = get_weight(args, heights, angles, midpoints_local, min_valid_height, positive_mask)
    best_point = raw_weights.argmax(dim=-1)
    dist = (obj_point_palm - obj_point_palm[torch.arange(obj_point_palm.shape[0]), best_point][:,None]).norm(dim=-1)
    weights = (10 ** (-dist * 150)).sum(dim=0)
    return weights, best_point

def cal_palm_tip_transform(midpoints_local):
    '''
    obtain palm-tip rotation
    '''
    B = midpoints_local.shape[0]
    midpoints_local_norm = midpoints_local / midpoints_local.norm(dim=-1, keepdim=True)
    y_axis = torch.zeros((B, 3), device=midpoints_local.device, dtype=torch.float)
    arange = torch.arange(B, device=midpoints_local.device)
    y_axis[arange, midpoints_local_norm.abs().argmin(dim=-1)] = 1
    y_axis = y_axis - (y_axis * midpoints_local_norm).sum(dim=-1, keepdim=True) * midpoints_local_norm
    y_axis = y_axis / y_axis.norm(dim=-1, keepdim=True)
    z_axis = torch.cross(midpoints_local_norm, y_axis, dim=-1)
    T = torch.stack([midpoints_local_norm, y_axis, z_axis], dim=-1)
    return T

def get_graspness_weighted(args, obj_points, grasp_poses_global, keypoints):
    '''
    given hand pose and object to grasp, get object points with graspness annotation
    
    Input:  obj_points: dict of object point clouds in scene frame
            grasp_poses_global: dict of grasp poses in scene frame
    Output:
    '''
    # those aligns midpoint between thumb-midfinger with grasp point
    graspness_dict = {}
    batch = 10000
    for object_code in list(obj_points.keys()):
        # print('*****' + object_code + '*****')
        B = grasp_poses_global[object_code]['translation'].shape[0]
        graspness_weight_all = []
        best_point_all = []
        for b in range(B // batch + 1):
            batch_size = min(batch, B - b * batch)
            slices = slice(b*batch, b*batch+batch_size)
            # make +x direction point to thumb-middlefinger midpoint
            R_palm_tip = cal_palm_tip_transform(keypoints[object_code][1][slices]-keypoints[object_code][0][slices])   # midpoint - centerpoint
            T_palm_tip = keypoints[object_code][0][slices]
            obj_point_palm = torch.einsum('nba,nkb->nka', R_palm_tip, obj_points[object_code] - T_palm_tip[:,None,:])
            midpoints_palm = torch.einsum('nba,nb->na', R_palm_tip, keypoints[object_code][1][slices] - T_palm_tip)

            # idx = 0
            # trans = grasp_poses_global[object_code]['translation'][slices][[idx]]
            # rot = grasp_poses_global[object_code]['rotation'][slices][[idx]]
            # rot = torch.einsum('ba,nbc->nac', R_palm_tip[idx], rot).cpu()
            # trans = torch.einsum('ba,nb->na', R_palm_tip[idx], trans - T_palm_tip[idx]).cpu()
            # qpos = {k:v[slices][[idx]].cpu() for k, v in grasp_poses_global[object_code].items()}
            # robot_plotly = vis.robot_plotly(trans, rot, qpos)
            # kp_plotly = vis.pc_plotly(midpoints_palm[idx][None].cpu(), size=5, color='red')
            # kp_plotly += vis.pc_plotly(torch.zeros((1,3)), size=5, color='red')
            # weight = allocate_sample_weights(args, obj_point_palm[[idx]], midpoints_palm[[idx]])
            # pc_plotly = vis.pc_plotly(obj_point_palm[idx].cpu(), value=weight.cpu(), size=1)
            # vis.show(pc_plotly + kp_plotly + robot_plotly)

            # alocate weights w.r.t graspness cone
            graspness_weight, best_point = allocate_sample_weights(args, obj_point_palm, midpoints_palm)
            graspness_weight_all.append(graspness_weight)
            best_point_all.append(best_point)
        graspness_weight = torch.stack(graspness_weight_all).sum(dim=0)
        best_point = torch.cat(best_point_all)
        grasp_poses_global[object_code]['point'] = obj_points[object_code][best_point]
        # pc_plotly = vis.pc_plotly(obj_points[object_code].cpu(), value=graspness_weight.cpu(), size=1)
        # vis.show(pc_plotly)
        graspness_dict[object_code] = graspness_weight
        
    return graspness_dict

def get_keypoints(args, grasps_positive):
    # calculate midpoints over hand frame
    link_translations, link_rotations = robot_model.forward_kinematics(grasps_positive)    

    thumb_link = 'thumb_fingertip'
    boxes = robot_model.get_link_mesh(thumb_link, 'collision')[0].reshape(2, -1, 3).mean(1).to(args.device).float()
    thumb = torch.einsum('nab,b->na', link_rotations[thumb_link], boxes[boxes[:,1].argmin()]) + link_translations[thumb_link]

    midfinger_link = 'fingertip_2'
    boxes = robot_model.get_link_mesh(midfinger_link, 'collision')[0].reshape(2, -1, 3).mean(1).to(args.device).float()
    midfinger = torch.einsum('nab,b->na', link_rotations[midfinger_link], boxes[boxes[:,1].argmin()]) + link_translations[midfinger_link]

    midpoint = (thumb + midfinger) / 2

    box = robot_model.get_link_mesh('hand_base_link', 'collision')[0].mean(0).to(args.device).float()
    centerpoint = torch.einsum('nab,b->na', link_rotations['hand_base_link'], box) + link_translations['hand_base_link']
    return [torch.einsum('nab,nb->na', grasps_positive['rotation'], t) + grasps_positive['translation'] for t in (centerpoint, midpoint)]

current_scene = None
current_filter = dict()

def get_collision_free_grasps(args, object_poses, object_codes):
    '''
    load collision-free grasp poses in scene
    
    Note: ***optimized_grasp_data.npz*** loaded grasps are all pre-filter grasps in obj frame, need to transform into scene global frame 
    
    rules for success are:
    1. object collision < 2mm 
    2. scene collision < 0 & scene pregrasp collision < 0
    3. table penetration < 0 
    4. sim success ***evaluation_results.npy***
    
    Input:
    Output:
    '''
    global current_scene, current_filter
    grasp_dict = {}
    keypoints_dict = {}
    object_codes_non_empty = []
    for object_code in object_codes:

        if current_scene != args.scene_id:
            current_scene = args.scene_id
            current_filter = dict()

        if object_code not in current_filter:
            # load pre-filter grasps
            data_root = 'data'
            graspdata_path = os.path.join('data', 'graspdata', args.robot_name, object_code, 'pregrasps.npz')
            grasps = dict(np.load(graspdata_path, allow_pickle=True))
            grasps = {k:torch.tensor(v, device=args.device, dtype=torch.float) for k,v in grasps.items()}
            
            # load success indicators
            sim_success_path = os.path.join(data_root, 'graspdata', args.robot_name, object_code, 'sim_success_0.2.npy')
            obj_collision_path = os.path.join(data_root, 'graspdata', args.robot_name, object_code, 'object_pen.npy')
            sim_success = torch.tensor(np.load(sim_success_path),device=args.device,dtype=torch.float)
            obj_collision = torch.tensor(np.load(obj_collision_path),device=args.device,dtype=torch.float)

            scene_collision_dir = os.path.join('data', 'collision_label', args.robot_name, get_orig_scene(args.scene_id), object_code, 'object_scene_pen_pregrasp')
            table_pregrasp_collision_path = os.path.join('data', 'collision_label', args.robot_name, get_orig_scene(args.scene_id), object_code, 'table_pen_pregrasp.npy')
            scene_pregrasp_collisions = [np.load(os.path.join(scene_collision_dir, p)) for p in os.listdir(scene_collision_dir) if p.split('.')[0]  in object_codes]
            scene_pregrasp_collisions.append(np.full(sim_success.shape[0], -np.inf))
            scene_pregrasp_collision = torch.tensor(np.stack(scene_pregrasp_collisions).max(0),device=args.device,dtype=torch.float)
            table_pregrasp_collision = torch.tensor(np.load(table_pregrasp_collision_path),device=args.device,dtype=torch.float)
            
            filter_positive = (sim_success > 0) * (obj_collision < args.object_collision_thr) * (scene_pregrasp_collision < -args.scene_collision_thr) * (table_pregrasp_collision < -args.scene_collision_thr)
            grasps = {k: v[::args.fraction] for k, v in grasps.items()}
            filter_positive = filter_positive[::args.fraction]
            if filter_positive.sum() == 0:
                current_filter[object_code] = None
            else:
                grasps_positive = grasps.copy()
                grasps_positive = {k: v[filter_positive] for k, v in grasps_positive.items()}
                current_filter[object_code] = grasps_positive
        
        if current_filter[object_code] is None:
            continue
        object_codes_non_empty.append(object_code)
        grasps_positive = {k: v.clone() for k, v in current_filter[object_code].items()}
        
        # transform from object frame into global frame
        object_pose = object_poses[object_code]
        grasps_positive['translation'] = torch.einsum('ab,nb->na', object_pose[:3, :3], grasps_positive['translation']) + object_pose[:3, 3]
        grasps_positive['rotation'] = torch.einsum('ab,nbc->nac', object_pose[:3, :3], grasps_positive['rotation'])
        grasp_dict[object_code] = grasps_positive
        
        keypoints = get_keypoints(args, grasps_positive)
        keypoints_dict[object_code] = keypoints
        # idx = 0
        # scene_plotly, _ = vis.scene_plotly('scene_'+args.scene_id, args.view_id, args.camera)
        # robot_plotly = vis.robot_plotly(grasps_positive['translation'][[idx]].cpu(), grasps_positive['rotation'][[idx]].cpu(), {k:v[[idx]].cpu() for k, v in grasps_positive.items()})
        # pc_plotly = vis.pc_plotly(keypoints[0][idx][None].cpu(), size=10, color='blue')
        # pc_plotly += vis.pc_plotly(keypoints[1][idx][None].cpu(), size=10, color='red')
        # vis.show(scene_plotly + robot_plotly + pc_plotly)
        
    return grasp_dict, keypoints_dict, object_codes_non_empty
        
def load_collision_free_grasps(args, object_poses, object_codes):
    load_dir = os.path.join(args.grasp_save_root, f'scene_{args.scene_id}', args.robot_name)
    object_codes_non_empty = []
    grasp_dict = dict()
    keypoints_dict = dict()

    camera_pose = np.load(os.path.join('data/scenes', f'scene_{args.scene_id}', args.camera, 'camera_poses.npy'))[int(args.view_id)]

    for p in os.listdir(load_dir):
        if not p.endswith('.npz'):
            continue
        object_code = p.split('.')[0]
        object_codes_non_empty.append(object_code)
        grasps_positive = {k: v[::args.fraction] for k, v in np.load(os.path.join(load_dir, p)).items()}
        grasps_positive['rotation'] = np.einsum('ba,nbc->nac', camera_pose[:3, :3], grasps_positive['rotation'])
        grasps_positive['translation'] = np.einsum('ba,nb->na', camera_pose[:3, :3], grasps_positive['translation'] - camera_pose[:3, 3])
        grasps_positive['point'] = np.einsum('ba,nb->na', camera_pose[:3, :3], grasps_positive['point'] - camera_pose[:3, 3])
        grasps_positive = {k: torch.tensor(v, device=args.device, dtype=torch.float) for k, v in grasps_positive.items()}
        grasp_dict[object_code] = grasps_positive
        keypoints_dict[object_code] = get_keypoints(args, grasps_positive)
    
    return grasp_dict, keypoints_dict, object_codes_non_empty

def load_scene(args):
    '''
    construct scenes
    Note: reference to src/scripts/compose_scenes.py
    
    Input:
    Output:
    '''
    # load scene annotation
    scene_path = os.path.join('data/scenes', f'scene_{str(args.scene_id).zfill(4)}')
    annotation_path = os.path.join(scene_path, args.camera, 'annotations', f'{args.view_id}.xml')
    scene_reader = xmlReader(annotation_path)
    posevectors = scene_reader.getposevectorlist()
    
    # parse scene annotation
    object_poses_dict = {}
    object_surface_points_dict = {}
    object_codes_list = []
    for posevector in posevectors:
        object_idx, object_pose = parse_posevector(posevector)
        object_code = str(object_idx).zfill(3)
        object_pose = torch.from_numpy(object_pose).to(args.device).float()
        object_codes_list.append(object_code)
        object_poses_dict[object_code] = object_pose

        object_surface_points_path = os.path.join(f"data/meshdata", object_code, f'surface_points_{args.object_points}.npy')
        object_surface_points = torch.from_numpy(np.load(object_surface_points_path)).to(args.device).float()
        object_surface_points_dict[object_code] = torch.einsum('ab,kb->ka', object_pose[:3, :3], object_surface_points) + object_pose[:3, 3]
    object_poses = object_poses_dict
    object_surface_points = object_surface_points_dict
    return object_poses, object_surface_points, object_codes_list

def generate_graspness(args):
    '''
    The entry function to generate graspness data for one scene.
    
    Input: args
    Output: save generated grasp data
    '''
    object_poses, object_surface_points_all, object_codes = load_scene(args)
    t = time.time()
    grasp_poses_global, keypoints, object_codes = load_collision_free_grasps(args, object_poses, object_codes)
    tt = time.time()
    # ignore object codes for which no valid grasp is detected
    object_surface_points = {}
    for k in object_codes:
        object_surface_points[k] = object_surface_points_all[k]

    graspness = get_graspness_weighted(args, object_surface_points, grasp_poses_global, keypoints)

    if int(args.scene_id) < 1000 or np.random.rand() < 0.1:
        # combine graspness labels to a scene-file
        # below loaded in camera frame
        suffix = '_gt' if args.gt_depth else ''
        path = os.path.join('data/scenes', f'scene_{str(args.scene_id).zfill(4)}', args.camera)
        depth = np.array(Image.open(os.path.join(path, 'depth'+suffix, str(args.view_id).zfill(4) + '.png')))
        seg = np.array(Image.open(os.path.join(path, 'label'+suffix, str(args.view_id).zfill(4) + '.png')))
        meta = scio.loadmat(os.path.join(path, 'meta', str(args.view_id).zfill(4) + '.mat'))
        camera_poses = np.load(os.path.join(path, 'camera_poses.npy'))
        align_mat = np.load(os.path.join(path, 'cam0_wrt_table.npy'))
        instrincs = meta['intrinsic_matrix']
        factor_depth = meta['factor_depth']
        
        cloud = depth_image_to_point_cloud(depth, instrincs, factor_depth)
        depth_mask = (depth > 0)
        trans = np.dot(align_mat, camera_poses[int(args.view_id)])
        workspace_mask = get_workspace_mask(cloud, seg, trans)
        mask = (depth_mask & workspace_mask)
        cloud = cloud[mask]
        cloud = torch.tensor(cloud,dtype=torch.float,device=args.device)
        seg = torch.from_numpy(seg[mask]).to(args.device)
        
        # scene_path = os.path.join('data/scenes', f'scene_{str(args.scene_id).zfill(4)}')
        # extrinsics_path = os.path.join(scene_path, args.camera, 'cam0_wrt_table.npy')
        # extrinsics = torch.tensor(np.load(extrinsics_path), device=args.device, dtype=torch.float)
        # cloud = extrinsics[None, :3, :3] @ cloud[:,:,None] + extrinsics[:3, 3].reshape(3,1) # [n, 3]
        # cloud = cloud.reshape(-1,3)
        
        # assign graspness to cloud via nearest neighbour with dist thresholding (graspness_assignment_thr = 1.5cm)
        graspness_perfect = torch.cat([g for g in graspness.values()])  # [m]
        label = torch.cat([torch.full_like(v, int(k)) for k, v in graspness.items()])
        cloud_perfect = torch.cat([p for p in object_surface_points.values()])  # [m, 3]
        
        # # knn 
        graspness_single_view = torch.zeros_like(cloud[:, 0])
        dists, inds, _ = pytorch3d.ops.knn_points(cloud[None,:,:], cloud_perfect[None,:,:])
        dists, inds = dists[0,:,0], inds[0,:,0]
        mask = (dists < args.graspness_assignment_thr) & (seg - 1 == label[inds])
        graspness_single_view[mask] = graspness_perfect[inds[mask]]
        
        save_root = args.save_root
        if args.fraction != 1:
            save_root = f'{save_root}_{args.fraction}'
        save_path = os.path.join(save_root, f'scene_{args.scene_id}', args.camera, f'{args.view_id}.npy')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        np.save(save_path, graspness_single_view.cpu().numpy()[:, None])

    # if args.view_id == '0000':
    #     grasp_save_root = args.grasp_save_root
    #     if args.fraction != 1:
    #         grasp_save_root = f'{grasp_save_root}_{args.fraction}'
    #     path = os.path.join('data/scenes', f'scene_0000', args.camera)
    #     camera_poses = np.load(os.path.join(path, 'camera_poses.npy'))
    #     path = os.path.join(grasp_save_root, f'scene_{args.scene_id}', args.robot_name)
    #     os.makedirs(path, exist_ok=True)
    #     for k, v in grasp_poses_global.items():
    #         cam_pos = torch.from_numpy(camera_poses[0]).to(args.device).float()
    #         v['rotation'] = torch.einsum('ab,nbc->nac', cam_pos[:3, :3], v['rotation'])
    #         v['translation'] = torch.einsum('ab,nb->na', cam_pos[:3, :3], v['translation']) + cam_pos[:3, 3]
    #         v['point'] = torch.einsum('ab,nb->na', cam_pos[:3, :3], v['point']) + cam_pos[:3, 3]
    #         np.savez(os.path.join(path, k + '.npz'), **{kk: vv.cpu().numpy() for kk, vv in v.items()})
    print(time.time()-t)
    print(time.time()-tt)
    print("**********")

if __name__ == '__main__':
    pbar = tqdm(total=(args.end-args.start) * 256)
    for scene in range(args.start, args.end):
        for view in range(256):
            args.scene_id = str(scene).zfill(4)
            args.view_id = str(view).zfill(4)
            generate_graspness(args)
            pbar.update(1)