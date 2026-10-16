import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.realpath('.'))

import argparse
import numpy as np
import transforms3d
import trimesh as tm
import xml.etree.ElementTree as ET
import plotly.graph_objects as go


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scene_id', type=str, default='0001')
    args = parser.parse_args()
    
    # load scene annotation
    scene_path = os.path.join(
        'data/scenes', f'scene_{args.scene_id}')
    extrinsics_path = os.path.join(scene_path, 'kinect/cam0_wrt_table.npy')
    extrinsics = np.load(extrinsics_path)
    annotation_path = os.path.join(scene_path, 'kinect/annotations/0000.xml')
    annotation = ET.parse(annotation_path)
    
    # parse annotation
    object_pose_dict = {}
    for obj in annotation.findall('obj'):
        object_code = str(int(obj.find('obj_id').text)).zfill(3)
        translation = np.array([float(x) for x in obj.find('pos_in_world').text.split()])
        rotation = np.array([float(x) for x in obj.find('ori_in_world').text.split()])
        rotation = transforms3d.quaternions.quat2mat(rotation)
        object_pose_dict[object_code] = dict(
            translation=extrinsics[:3, :3] @ translation + extrinsics[:3, 3],
            rotation=extrinsics[:3, :3] @ rotation, 
        )
    object_pose_dict = dict(sorted(object_pose_dict.items()))

    # load object meshes
    object_meshes = {}
    for object_code in object_pose_dict.keys():
        object_path = os.path.join('data/meshdata', object_code, 'simplified.obj')
        object_meshes[object_code] = tm.load(object_path)
    
    # plotly data
    plotly_data = []
    title = f'Scene_{args.scene_id}'
    
    for object_code in object_meshes:
        object_mesh = object_meshes[object_code]
        object_translation = object_pose_dict[object_code]['translation']
        object_rotation = object_pose_dict[object_code]['rotation']
        vertices = object_mesh.vertices @ object_rotation.T + object_translation
        faces = object_mesh.faces
        mesh = go.Mesh3d(
            x=vertices[:, 0], 
            y=vertices[:, 1], 
            z=vertices[:, 2],
            i=faces[:, 0], 
            j=faces[:, 1], 
            k=faces[:, 2],
            color='lightgreen', 
            opacity=1, 
            hoverinfo='text',
            text=[object_code] * len(faces),
        )
        plotly_data.append(mesh)
    
    # plotly layout
    fig = go.Figure(data=plotly_data)
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data',
        ),
    )
    fig.show()
