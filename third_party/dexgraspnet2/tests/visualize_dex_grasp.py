import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.realpath('.'))

import argparse
import random
import numpy as np
import torch

from src.utils.vis_plotly import Vis
from src.utils.util import set_seed
import plotly.express as px

parser = argparse.ArgumentParser()
parser.add_argument('--robot_name', type=str, default='leap_hand', choices=['leap_hand'])
parser.add_argument('--urdf_path', type=str, default='robot_models/urdf/leap_hand_simplified.urdf')
parser.add_argument('--meta_path', type=str, default='robot_models/meta/leap_hand/meta.yaml')
parser.add_argument('--camera', type=str, default='realsense')
parser.add_argument('--scene', type=str, default='scene_0001')
parser.add_argument('--view', type=str, default='0000')
parser.add_argument('--grasp_num', type=int, default=1)
parser.add_argument('--output_path', type=str, default=None)
parser.add_argument('--frame', type=str, default='camera', choices=['world', 'camera'])
parser.add_argument('--with_graspness', type=bool, default=True)
args = parser.parse_args()
set_seed(2)

if __name__ == '__main__':
    vis = Vis(
        robot_name=args.robot_name,
        urdf_path=args.urdf_path,
        meta_path=args.meta_path,
    )

    view_plotly, pc, extrinsics = vis.scene_plotly(args.scene, args.view, args.camera, with_pc=True, mode='pc', graspness_path='dex_graspness_new' if args.with_graspness else None, with_extrinsics=True)
    raw_graspness = (pc[:, 4] + 1e-3).log()
    objectness = (pc[:, 3] != 0)
    graspness = torch.where(objectness, raw_graspness, raw_graspness * 0 + np.log(1e-3))
    idxs = torch.randperm(len(pc))[:10000]
    cam0_wrt_table = np.load(os.path.join('data', 'scenes', args.scene, args.camera, 'cam0_wrt_table.npy'))
    camera_pose_wrt_cam0 = np.load(os.path.join('data', 'scenes', args.scene, args.camera, 'camera_poses.npy'))[int(args.view)]
    camera_pose = torch.from_numpy(np.einsum('ab,bc->ac', cam0_wrt_table, camera_pose_wrt_cam0))
    if args.frame == 'world':
        pc = pc.float()
        camera_pose = camera_pose.float()
        pc[:, :3] = torch.einsum('ab,nb->na', camera_pose[:3, :3], pc[:, :3]) + camera_pose[:3, 3]
    view_plotly = vis.pc_plotly(pc[idxs, :3], size=1, value=graspness[idxs])

    robot_plotly = []
    pc_plotly = []
    path = os.path.join('data', 'dex_grasps_new', args.scene, args.robot_name)
    for p in os.listdir(path):
        if not p.endswith('.npz'):
            continue
        if not '000' in p:
            continue
        data = np.load(os.path.join(path, p))
        idxs = np.random.randint(0, len(data['point']), args.grasp_num)
        data = {k: data[k][idxs] for k in data.files}
        for i in range(args.grasp_num):
            trans = torch.from_numpy(np.einsum('ba,b->a', camera_pose_wrt_cam0[:3, :3], data['translation'][i] - camera_pose_wrt_cam0[:3, 3]))
            rot = torch.from_numpy(np.einsum('ba,bc->ac', camera_pose_wrt_cam0[:3, :3], data['rotation'][i]))
            point = torch.from_numpy(np.einsum('ba,b->a', camera_pose_wrt_cam0[:3, :3], data['point'][i] - camera_pose_wrt_cam0[:3, 3]))
            if args.frame == 'world':
                trans = torch.einsum('ab,b->a', camera_pose[:3, :3], trans.float()) + camera_pose[:3, 3]
                rot = torch.einsum('ab,bc->ac', camera_pose[:3, :3], rot.float())
                point = torch.einsum('ab,b->a', camera_pose[:3, :3], point.float()) + camera_pose[:3, 3]
            qpos = {k: torch.from_numpy(data[k][[i]]).float() for k in data.keys()}
            robot_plotly += vis.robot_plotly(trans[None].float(), rot[None].float(), qpos, opacity=0.5, color=random.choice(px.colors.sequential.Plasma))
            pc_plotly += vis.pc_plotly(point[None].float(), size=5, color='red')
    plotly = view_plotly + robot_plotly + pc_plotly

    vis.show(plotly, args.output_path)