import numpy as np
import os
from PIL import Image
import scipy.io as scio
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from pytorch3d.ops import knn_points, ball_query
import torch
from graspnetAPI.utils.xmlhandler import xmlReader
from graspnetAPI.utils.utils import get_obj_pose_list, transform_points
from src.utils.pc import depth_image_to_point_cloud, get_workspace_mask
from src.utils.pose_refine import PoseRefine
import argparse
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--start', default=0, type=int)
parser.add_argument('--end', default=100, type=int)
parser.add_argument('--gt', default=1, type=int)
parser.add_argument('--fraction', default=10, type=int)
parser.add_argument('--camera', default='realsense', help='Camera split [realsense/kinect]')


if __name__ == '__main__':
    cfgs = parser.parse_args()
    camera = cfgs.camera# kinect / realsense
    suffix = '_gt' if cfgs.gt else ''
    save_path_root = os.path.join('data', 'gripper_graspness')
    if cfgs.fraction != 1:
        save_path_root = f'{save_path_root}_{cfgs.fraction}'
    pbar = tqdm(total=(cfgs.end-cfgs.start)*256)

    for scene_id in range(cfgs.start, cfgs.end):
        scene = f'scene_{str(scene_id).zfill(4)}'
        save_path = os.path.join(save_path_root, scene, camera)
        points = torch.from_numpy(np.load(os.path.join('data', 'gripper_grasps', scene, camera, 'points.npy')))[::cfgs.fraction].cuda()
        poses = torch.from_numpy(np.load(os.path.join('data', 'gripper_grasps', scene, camera, 'poses.npy')))[::cfgs.fraction].cuda()

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for ann_id in range(256):
            str_view = str(ann_id).zfill(4)
            if os.path.exists(os.path.join(save_path, str_view + '.npy')):
                pbar.update(1)
                continue
            path = os.path.join('data', 'scenes', scene, camera)
            depth = np.array(Image.open(os.path.join(path, 'depth'+suffix, str_view + '.png')))
            seg = np.array(Image.open(os.path.join(path, 'label'+suffix, str_view + '.png')))
            meta = scio.loadmat(os.path.join(path, 'meta', str_view + '.mat'))
            instrincs = meta['intrinsic_matrix']
            factor_depth = meta['factor_depth']
            camera_poses = np.load(os.path.join(path, 'camera_poses.npy'))
            align_mat = np.load(os.path.join(path, 'cam0_wrt_table.npy'))

            # get pointcloud in workspace in camera frame
            cloud = depth_image_to_point_cloud(depth, instrincs, factor_depth)
            depth_mask = (depth > 0)
            trans = np.dot(align_mat, camera_poses[ann_id])
            workspace_mask = get_workspace_mask(cloud, seg, trans)
            mask = (depth_mask & workspace_mask)
            cloud = cloud[mask]
            seg = seg[mask]
            cloud_masked_graspness = torch.zeros((mask.sum(),)).cuda()

            camera_pose = torch.from_numpy(camera_poses[ann_id])
            view_point = torch.einsum('ba,kb->ka', camera_pose[:3, :3].cuda(), points - camera_pose[:3, 3].cuda())
            cloud = torch.from_numpy(cloud).cuda()
            seg = torch.from_numpy(seg).cuda()

            for i in range(len(view_point)//500+1):
                idxs = slice(i*500, min(i*500+500, len(view_point)))
                v = view_point[idxs]
                dist = torch.cdist(v[None], cloud[None])[0]
                obj_ids = poses[idxs, -1].long() + 1
                # score = 10 ** (-dist*150)
                dist *= -150 * np.log(10)
                score = dist.exp_()
                score = torch.where(obj_ids[:, None] == seg, score, torch.zeros_like(score))
                cloud_masked_graspness += score.sum(dim=0)
            cloud_masked_graspness = cloud_masked_graspness

            np.save(os.path.join(save_path, str(ann_id).zfill(4) + '.npy'), cloud_masked_graspness.cpu().numpy()[:, None])
            pbar.update(1)
    print("!")