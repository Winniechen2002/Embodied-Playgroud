import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.realpath('.'))

from graspnetAPI import GraspNet, Grasp, GraspGroup
import open3d as o3d
import cv2
import numpy as np
from tqdm import trange


import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--start', default=None, required=True, type=int)
parser.add_argument('--end', default=None, required=True, type=int)
parser.add_argument('--camera', default='realsense', type=str)
parser.add_argument('--thresh', default=0.2, type=float)
cfgs = parser.parse_args()

graspnet_root = 'data'
g = GraspNet(graspnet_root, camera=cfgs.camera, split='train')

for sceneId in trange(cfgs.start, cfgs.end):
    path = os.path.join('data', 'poses_gn', 'scene_' + str(sceneId).zfill(4), cfgs.camera, 'poses.npy')
    if os.path.exists(path):
        continue
    _6d_grasp = g.loadGrasp(sceneId = sceneId, annId = 0, format = '6d', camera = cfgs.camera, fric_coef_thresh = cfgs.thresh)
    array = _6d_grasp.grasp_group_array

    camera_poses = np.load(os.path.join(g.root,'scenes','scene_%04d' %(sceneId,), cfgs.camera, 'camera_poses.npy'))
    camera_pose = camera_poses[0]

    rot = array[:, -13:-4].reshape(-1, 3, 3)
    new_rot = np.einsum('ij,njk->nik', camera_pose[:3, :3], rot)
    trans = array[:, -4:-1]
    new_trans = np.einsum('ij,nj->ni', camera_pose[:3, :3], trans) + camera_pose[:3, 3]
    array = np.concatenate([array[:, :-13], new_rot.reshape(-1, 9), new_trans, array[:, -1:]], axis=1)
 
    print(len(array))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.save(path, array)