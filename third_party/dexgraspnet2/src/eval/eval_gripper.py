import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.realpath('.'))

import argparse
from tqdm import tqdm
import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import CosineAnnealingLR
from math import sqrt
from graspnetAPI.graspnet_eval import GraspNetEval

from src.network.model import get_model
from src.utils.dataset import GraspNetDataset, Loader, minkowski_collate_fn
from src.utils.logger import Logger
from src.utils.vis_plotly import Vis
from src.utils.config import load_config, add_argparse
from src.utils.util import set_seed
from src.utils.robot_info import GRIPPER_DEPTH_BASE, GRIPPER_NEW_DEPTH

arg_mapping = [
    # (key in console, (key in config, type, default value))
    ('batch_size', ('batch_size', int, 32)),
    ('ckpt', ('ckpt', str, None)),
    ('type', ('model/type', str, None)), # key in config can be hierarchical
    ('split', ('split', str, None)), # key in config can be hierarchical
    ('save', ('save', int, 1)),
    ('eval', ('eval', int, 1)),
    ('proc', ('proc', int, 10)),
]

def save(config, dump_dir):
    set_seed(config.seed)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    test_dataset = GraspNetDataset(config, config.split, is_eval=True)
    test_loader = DataLoader(test_dataset, batch_size=config.batch_size, drop_last=True, num_workers=config.num_workers, shuffle=False, collate_fn=minkowski_collate_fn)

    # model and optimizer
    model = get_model(config.model)
    model.config.voxel_size = config.data.voxel_size

    # load ckpt if exists
    ckpt = torch.load(config.ckpt, map_location='cpu')
    model.load_state_dict(ckpt['model'])
    print(f'loaded ckpt from {config.ckpt}')

    # evaluation
    model.to(device)
    model.eval()

    with torch.no_grad():
        for data in tqdm(test_loader):
            data = {k: v.to(device) for k, v in data.items()}
            rot, trans, joint, log_prob, _ = model.sample(data, k=1024, edge=data['edge'], allow_fail=True, cate=False, ratio=0.1, graspness_scale=1, near=True)
            width = joint[..., 0]
            depth = torch.full_like(width, GRIPPER_NEW_DEPTH)
            b = rot.shape[0]
            for i in range(b):
                grasp = torch.cat([log_prob[i][:, None], width[i][:,None], torch.full_like(width[i][:,None], GRIPPER_DEPTH_BASE), torch.full_like(depth[i][:,None], GRIPPER_NEW_DEPTH), rot[i].reshape(-1, 9), trans[i], torch.full_like(width[i][:,None], -1)], dim=-1)
                save_path = os.path.join(dump_dir, f"scene_{str(data['scene'][i].item()).zfill(4)}", config.data.camera, f"{str(data['view'][i].item()).zfill(4)}.npy")
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                np.save(save_path, grasp.cpu().numpy())

def eval(config, dump_dir):
    ge = GraspNetEval(root='data', camera=config.data.camera, split=config.split)
    proc = config.proc
    if config.split == 'test_seen':
        res, ap = ge.eval_seen(dump_folder=dump_dir, proc=proc)
    elif config.split == 'test_similar':
        res, ap = ge.eval_similar(dump_folder=dump_dir, proc=proc)
    elif config.split == 'test_novel':
        res, ap = ge.eval_novel(dump_folder=dump_dir, proc=proc)
    save_dir = os.path.join(dump_dir, f'ap_{config.split}.npy')
    np.save(save_dir, res)

if __name__ == '__main__':
    # process config, seed, logger, device
    parser = argparse.ArgumentParser()
    add_argparse(parser, arg_mapping)
    args = parser.parse_args()
    config = load_config(os.path.join(os.path.dirname(os.path.dirname(args.ckpt)), 'config.yaml'), arg_mapping, args)
    print(config)
    dump_dir = os.path.join(os.path.dirname(os.path.dirname(config.ckpt)), 'est')
    if config.save:
        save(config, dump_dir)
    if config.eval:
        eval(config, dump_dir)
