import numpy as np
from graspnetAPI.graspnet_eval import GraspNetEval
from graspnetAPI.grasp import GraspGroup
from graspnetAPI.utils.config import get_config
from graspnetAPI.utils.eval_utils import create_table_points, voxel_sample_points, transform_points
from graspnetAPI.utils.eval_utils import eval_grasp as eval_grasp_api

ge = None

def eval_grasp(scene_id, ann_id, grasp: np.ndarray, TOP_K = 50, max_width = 0.1, camera='realsense'):
    global ge
    if ge is None:
        try:
            # Optional speed up by specifying sceneIds
            ge = GraspNetEval(root='data', camera=camera, split='custom', sceneIds=[scene_id])
        except:
            ge = GraspNetEval(root='data', camera=camera, split='all')
    config = get_config()
    table = create_table_points(1.0, 1.0, 0.05, dx=-0.5, dy=-0.5, dz=-0.05, grid_size=0.008)

    list_coe_of_friction = [0.2,0.4,0.6,0.8,1.0,1.2]
    model_list, dexmodel_list, _ = ge.get_scene_models(scene_id, ann_id=0)

    model_sampled_list = list()
    for model in model_list:
        model_sampled = voxel_sample_points(model, 0.008)
        model_sampled_list.append(model_sampled)
    
    grasp_group = GraspGroup(grasp)
    _, pose_list, camera_pose, align_mat = ge.get_model_poses(scene_id, ann_id)
    table_trans = transform_points(table, np.linalg.inv(np.matmul(align_mat, camera_pose)))

    # clip width to [0,max_width]
    gg_array = grasp_group.grasp_group_array
    min_width_mask = (gg_array[:,1] < 0)
    max_width_mask = (gg_array[:,1] > max_width)
    gg_array[min_width_mask,1] = 0
    gg_array[max_width_mask,1] = max_width
    grasp_group.grasp_group_array = gg_array

    grasp_list, score_list, collision_mask_list = eval_grasp_api(grasp_group, model_sampled_list, dexmodel_list, pose_list, config, table=table_trans, voxel_size=0.008, TOP_K = TOP_K)

    # remove empty
    grasp_list = [x for x in grasp_list if len(x) != 0]
    score_list = [x for x in score_list if len(x) != 0]
    collision_mask_list = [x for x in collision_mask_list if len(x)!=0]

    if len(grasp_list) == 0:
        print('len grasp_list = 0')
        return

    # concat into scene level
    grasp_list, score_list, collision_mask_list = np.concatenate(grasp_list), np.concatenate(score_list), np.concatenate(collision_mask_list)

    grasp_confidence = grasp_list[:,0]
    indices = np.argsort(-grasp_confidence)
    grasp_list, score_list, collision_mask_list = grasp_list[indices], score_list[indices], collision_mask_list[indices]

    # grasp_list_list.append(grasp_list)
    # score_list_list.append(score_list)
    # collision_list_list.append(collision_mask_list)

    #calculate AP
    grasp_accuracy = np.zeros((TOP_K,len(list_coe_of_friction)))
    for fric_idx, fric in enumerate(list_coe_of_friction):
        for k in range(0,TOP_K):
            if k+1 > len(score_list):
                grasp_accuracy[k,fric_idx] = np.sum(((score_list<=fric) & (score_list>0)).astype(int))/(k+1)
            else:
                grasp_accuracy[k,fric_idx] = np.sum(((score_list[0:k+1]<=fric) & (score_list[0:k+1]>0)).astype(int))/(k+1)

    print('\rMean Accuracy for scene:%04d ann:%04d = %.3f' % (scene_id, ann_id, 100.0 * np.mean(grasp_accuracy[:,:])))
    # scene_accuracy.append(grasp_accuracy)
    return grasp_list, score_list, collision_mask_list, grasp_accuracy
