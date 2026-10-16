import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.realpath('.'))

import argparse
import numpy as np
import torch
import cv2 as cv
from PIL import Image
from src.utils.edge import detect_edge
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--camera', type=str, default='realsense')
parser.add_argument('--dataset', type=str, choices=['graspnet','acronym'], default='graspnet')
parser.add_argument('--start', type=int, default=0)
parser.add_argument('--end', type=int, default=190)
args = parser.parse_args()

if args.dataset == 'graspnet':
    pbar = tqdm(total=(args.end - args.start) * 256)

    for scene_id in range(args.start, args.end):
        if scene_id > 8500 and scene_id % 5 > 0:
            pbar.update(256)
            continue
        for view_id in range(256):
            scene = f'scene_{str(scene_id).zfill(4)}'
            view = str(view_id).zfill(4)
            path = os.path.join('data', 'scenes', scene, args.camera, 'depth_gt', f'{view}.png')

            img = Image.open(path)
            img = np.array(img)
            img = (img / img.max() * 200).astype(np.uint8)

            edges = detect_edge(img)
            edges_img = Image.fromarray(edges)
            path = os.path.join('data', 'scenes', scene, args.camera, 'edge_gt', f'{view}.png')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            edges_img.save(path)
            pbar.update(1)
elif args.dataset == 'acronym':
    # process test split
    scene_id_list_random = [f.split('.')[0] for f in os.listdir('data/acronym_test_scenes/test_acronym_random')]
    scene_id_list_loose = [f.split('.')[0] for f in os.listdir('data/acronym_test_scenes/test_acronym_loose')]
    scene_id_list_dense = [f.split('.')[0] for f in os.listdir('data/acronym_test_scenes/test_acronym_dense')]
    pbar = tqdm(total=(len(scene_id_list_random)+len(scene_id_list_loose)+len(scene_id_list_dense)) * 256)
    
    # process random split
    for scene_id in scene_id_list_random:
        for view_id in range(256):
            scene = scene_id
            view = str(view_id).zfill(4)
            path = os.path.join('data/acronym_test_scenes/test_acronym_random_depth_gt', args.camera, scene, f'{view}.png')
            
            img = Image.open(path)
            img = np.array(img)
            img = (img / img.max() * 200).astype(np.uint8)

            edges = detect_edge(img)
            edges_img = Image.fromarray(edges)
            path = os.path.join('data/acronym_test_scenes', f'network_input_random', scene, args.camera, 'edge_gt', f'{view}.png')
            os.makedirs(os.path.dirname(path),exist_ok=True)
            edges_img.save(path)
            pbar.update(1)
            
    # process loose split
    for scene_id in scene_id_list_loose:
        for view_id in range(256):
            scene = scene_id
            view = str(view_id).zfill(4)
            path = os.path.join('data/acronym_test_scenes/test_acronym_loose_depth_gt', args.camera, scene, f'{view}.png')
            
            img = Image.open(path)
            img = np.array(img)
            img = (img / img.max() * 200).astype(np.uint8)

            edges = detect_edge(img)
            edges_img = Image.fromarray(edges)
            path = os.path.join('data/acronym_test_scenes', f'network_input_loose', scene, args.camera, 'edge_gt', f'{view}.png')
            os.makedirs(os.path.dirname(path),exist_ok=True)
            edges_img.save(path)
            pbar.update(1)
            
    # process dense split
    for scene_id in scene_id_list_dense:
        for view_id in range(256):
            scene = scene_id
            view = str(view_id).zfill(4)
            path = os.path.join('data/acronym_test_scenes/test_acronym_dense_depth_gt', args.camera, scene, f'{view}.png')
            
            img = Image.open(path)
            img = np.array(img)
            img = (img / img.max() * 200).astype(np.uint8)

            edges = detect_edge(img)
            edges_img = Image.fromarray(edges)
            path = os.path.join('data/acronym_test_scenes', f'network_input_dense', scene, args.camera, 'edge_gt', f'{view}.png')
            os.makedirs(os.path.dirname(path),exist_ok=True)
            edges_img.save(path)
            pbar.update(1)