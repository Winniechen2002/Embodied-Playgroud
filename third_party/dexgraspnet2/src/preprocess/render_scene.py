import os
import sys 

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import argparse
from tqdm import tqdm
import numpy as np
import scipy.io as scio
from PIL import Image
from graspnetAPI.utils.xmlhandler import xmlReader
from graspnetAPI.utils.utils import parse_posevector

from src.utils.render import Renderer

parser = argparse.ArgumentParser()
parser.add_argument('--start', default=0, type=int)
parser.add_argument('--end', default=190, type=int)
parser.add_argument('--stride', default=1, type=int)
parser.add_argument('--camera', default='realsense', help='Camera split [realsense/kinect]')

if __name__ == '__main__':
    args = parser.parse_args()
    depth = np.array(Image.open(os.path.join('data', 'scenes', 'scene_0000', args.camera, 'depth', '0000.png')))
    width, height = depth.shape[1], depth.shape[0]
    meta = scio.loadmat(os.path.join('data', 'scenes', 'scene_0000', args.camera, 'meta', '0000.mat'))
    instrincs = meta['intrinsic_matrix']
    factor_depth = meta['factor_depth']

    renderer = Renderer(width, height, instrincs, 2)
    pbar = tqdm(total=(args.end-args.start)*256)

    for bias in range(args.stride):
        for scene_id in range(args.start + bias, args.end, args.stride):
            scene = f'scene_{str(scene_id).zfill(4)}'
            print(f'Processing {scene}...', flush=True)
            path = os.path.join('data', 'scenes', scene, args.camera)
            camera_poses = np.load(os.path.join(path, 'camera_poses.npy'))

            for view_id in range(256):
                view = f'{str(view_id).zfill(4)}'
                depth_path = os.path.join(path, 'depth_gt', view + '.png')
                if os.path.exists(depth_path):
                    try:
                        Image.open(depth_path)
                        success = True
                    except:
                        success = False
                    if success:
                        pbar.update(1)
                        continue
                meta = scio.loadmat(os.path.join(path, 'meta', view + '.mat'))
                align_mat = np.load(os.path.join(path, 'cam0_wrt_table.npy'))
                scene_reader = xmlReader(os.path.join(path, 'annotations', str(view).zfill(4) + '.xml'))
                posevectors = scene_reader.getposevectorlist()
                poses = [parse_posevector(posevector) for posevector in posevectors]
                table_mat = np.linalg.inv(np.matmul(align_mat, camera_poses[view_id]))

                image = renderer.render([str(obj_id).zfill(3) for obj_id, pose in poses], [pose for obj_id, pose in poses], table_mat).cpu().numpy()
                image = image[::-1]

                seg = image[..., 3]
                seg_img = Image.fromarray((seg).astype(np.uint8))
                seg_path = os.path.join(path, 'label_gt', view + '.png')
                os.makedirs(os.path.dirname(seg_path), exist_ok=True)
                seg_img.save(seg_path)

                depth = (image[..., 2] * -factor_depth).astype(np.int32)
                depth_img = Image.fromarray(depth)
                os.makedirs(os.path.dirname(depth_path), exist_ok=True)
                depth_img.save(depth_path)

                pbar.update(1)
