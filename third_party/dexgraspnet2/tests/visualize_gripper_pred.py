import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.realpath('.'))

import argparse
import numpy as np
import torch
from pytorch3d import transforms as pttf
from pytorch3d.ops import sample_farthest_points

from src.utils.vis_plotly import Vis
from src.utils.config import ckpt_to_config
from src.network.model import get_model
from src.utils.dataset import get_sparse_tensor
from src.utils.eval_grasp import eval_grasp
from src.utils.util import pack_17dgrasp, unpack_17dgrasp, set_seed
from src.utils.robot_info import GRIPPER_NEW_DEPTH

parser = argparse.ArgumentParser()
parser.add_argument('--ckpt_path', type=str, required=True)
parser.add_argument('--robot_name', type=str, default='gripper', choices=['gripper'])
parser.add_argument('--urdf_path', type=str, default='robot_models/urdf/leap_hand.urdf')
parser.add_argument('--meta_path', type=str, default='robot_models/meta/leap_hand/meta.yaml')
parser.add_argument('--camera', type=str, default='realsense')
parser.add_argument('--scene', type=str, default='scene_0000')
parser.add_argument('--view', type=str, default='0000')
parser.add_argument('--grasp_num', type=int, default=1024)
parser.add_argument('--output_path', type=str, default=None)
parser.add_argument('--gpu', type=int, default=0)
parser.add_argument('--ratio', type=float, default=0.05)
parser.add_argument('--display', type=str, default='all')
parser.add_argument('--display_thresh', type=float, default=0.0)
parser.add_argument('--seed', type=int, default=0)
args = parser.parse_args()

set_seed(args.seed)

if __name__ == '__main__':
    vis = Vis(
        robot_name=args.robot_name,
        urdf_path=args.urdf_path,
        meta_path=args.meta_path,
    )

    pc_plotly, pc = vis.scene_plotly(args.scene, args.view, args.camera, with_pc=True, mode='pc')
    edge = pc[:, -1]
    seg = pc[:, 3]
    pc = pc[:, :3]

    device = torch.device(args.gpu if torch.cuda.is_available() else 'cpu')
    config = ckpt_to_config(args.ckpt_path)
    model = get_model(config.model)
    model.config.voxel_size = config.data.voxel_size
    ckpt = torch.load(args.ckpt_path, map_location='cpu')
    model.load_state_dict(ckpt['model'])
    model.to(device)
    model.eval()

    with torch.no_grad():
        data = get_sparse_tensor(pc[None].float(), config.data.voxel_size)
        data['seg'] = seg[None].long()
        data = {k: v.to(device) for k, v in data.items()}
        rot, trans, joints, score, _ = (t.cpu() for t in model.sample(data, args.grasp_num, edge=edge.to(device)[None], ratio=0.1, cate=False, graspness_scale=1, near=True, allow_fail=True))
        width = joints[..., 0]
        depth = torch.full_like(width, GRIPPER_NEW_DEPTH)
    
    grasp_17d = pack_17dgrasp(rot[0], trans[0], width[0], depth[0], score[0])
    nms_grasp, nms_score, nms_collision, nms_accuracy = eval_grasp(int(args.scene.split('_')[-1]), int(args.view), grasp_17d)
    if args.display != 'all':
        rot, trans, width, depth, score = (t[None] for t in unpack_17dgrasp(nms_grasp))

    pose_plotly = []
    for i in range(len(rot[0])):
        if args.display == "all":
            condition = True
        else:
            score_i = nms_score[i]
            if args.display == "lower":
                condition = score_i < args.display_thresh
            elif args.display == "higher":
                condition = score_i >= args.display_thresh
            elif args.display == "collision":
                condition = nms_collision[i]
            else:
                condition = True

        if condition:
            pose_plotly += vis.robot_plotly(trans[:, i].cpu(), rot[:, i].cpu(), torch.stack((width[:, i], depth[:, i]), dim=-1).cpu())

    view_plotly, _ = vis.scene_plotly(args.scene, args.view, args.camera, mode='model')
    plotly = view_plotly + pose_plotly + pc_plotly
    vis.show(plotly, args.output_path, scene=args.scene, view=args.view, camera=args.camera)
