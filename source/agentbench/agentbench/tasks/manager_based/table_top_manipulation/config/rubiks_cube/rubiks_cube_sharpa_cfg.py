"""One floating right Sharpa Wave hand with the unchanged hybrid 3x3 cube."""

import copy

import torch
import isaaclab.sim as sim_utils
from isaaclab.envs import ManagerBasedEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.utils import configclass

from agentbench.robot_agents.franka_sharpa_right import FLOATING_SHARPA_RIGHT_CFG
from agentbench.sharpa_joint_names import (
    SHARPA_CONTACT_BODY_NAMES, SHARPA_FINGER_JOINT_NAMES,
    SHARPA_MOTION_JOINT_NAMES, SHARPA_PALM_BODY_NAME,
)
from ... import mdp
from .rubiks_cube_cfg import (
    CUBIE_FILTER_PATHS, CUBIE_IDS, RubiksCubeEventsCfg,
    RubiksCubeObservationsCfg, RubiksCubeSceneCfg,
)


SHARPA_SENSOR_NAMES = tuple(f"{name}_cube_contact" for name in SHARPA_CONTACT_BODY_NAMES)


def sharpa_cube_contact_forces(env):
    """Five actual one-to-many force matrices, in world coordinates."""
    matrices = []
    for name in SHARPA_SENSOR_NAMES:
        matrix = env.scene.sensors[name].data.force_matrix_w
        if matrix is None or matrix.shape != (env.num_envs, 1, len(CUBIE_IDS), 3):
            raise RuntimeError(f"missing or invalid Sharpa contact matrix: {name}")
        if not bool(torch.isfinite(matrix).all()):
            raise RuntimeError(f"nonfinite Sharpa contact matrix: {name}")
        matrices.append(matrix[:, 0])
    return torch.stack(matrices, dim=1).flatten(start_dim=1)


@configclass
class RubiksCubeSharpaSceneCfg(RubiksCubeSceneCfg):
    left_finger_cube_contact = None
    right_finger_cube_contact = None

    for body_name, sensor_name in zip(SHARPA_CONTACT_BODY_NAMES, SHARPA_SENSOR_NAMES):
        locals()[sensor_name] = ContactSensorCfg(
            prim_path=f"{{ENV_REGEX_NS}}/Robot/{body_name}",
            update_period=0.0, history_length=3, debug_vis=False,
            track_contact_points=False, filter_prim_paths_expr=list(CUBIE_FILTER_PATHS),
        )
    del body_name, sensor_name


@configclass
class RubiksCubeSharpaActionsCfg:
    motion = mdp.JointPositionActionCfg(
        asset_name="robot", joint_names=list(SHARPA_MOTION_JOINT_NAMES),
        scale=1.0, use_default_offset=False, preserve_order=True,
    )
    fingers = mdp.JointPositionActionCfg(
        asset_name="robot", joint_names=list(SHARPA_FINGER_JOINT_NAMES),
        scale=1.0, use_default_offset=False, preserve_order=True,
    )


@configclass
class RubiksCubeSharpaObservationsCfg(RubiksCubeObservationsCfg):
    @configclass
    class StateCfg(RubiksCubeObservationsCfg.StateCfg):
        ee_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={"asset_cfg": SceneEntityCfg("robot", body_names=[SHARPA_PALM_BODY_NAME])},
        )
        finger_contact_forces = ObsTerm(func=sharpa_cube_contact_forces)

    state: StateCfg = StateCfg()


@configclass
class RubiksCubeSharpaEventsCfg(RubiksCubeEventsCfg):
    fingertip_physics_material = EventTerm(
        # ManagerBasedEnv only applies startup events for its own exact class.
        # RubiksCubeEnv is a subclass; reset runs after its managers exist.
        func=mdp.randomize_rigid_body_material, mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names=list(SHARPA_CONTACT_BODY_NAMES)),
            "static_friction_range": (3.0, 3.0), "dynamic_friction_range": (2.5, 2.5),
            "restitution_range": (0.0, 0.0), "num_buckets": 1, "make_consistent": True,
        },
    )


@configclass
class RubiksCubeEnvFloatingSharpaRightCfg(ManagerBasedEnvCfg):
    viewer: ViewerCfg = ViewerCfg(
        eye=(1.45, -1.55, 1.25), lookat=(0.70, -0.10, 0.75), origin_type="env",
    )
    scene: RubiksCubeSharpaSceneCfg = RubiksCubeSharpaSceneCfg(
        num_envs=1, env_spacing=2.5, replicate_physics=False,
    )
    observations: RubiksCubeSharpaObservationsCfg = RubiksCubeSharpaObservationsCfg()
    actions: RubiksCubeSharpaActionsCfg = RubiksCubeSharpaActionsCfg()
    events: RubiksCubeSharpaEventsCfg = RubiksCubeSharpaEventsCfg()

    def __post_init__(self):
        robot = copy.deepcopy(FLOATING_SHARPA_RIGHT_CFG)
        robot.prim_path = "{ENV_REGEX_NS}/Robot"
        robot.spawn.articulation_props.fix_root_link = True
        robot.init_state.pos = (0.70, -0.32, 0.85)
        robot.init_state.rot = (1.0, 0.0, 0.0, 0.0)
        robot.spawn.semantic_tags = [("class", "robot")]
        # Native calibration at stiffness 200 produced only 0.474 N in the
        # middle pad at the collision-qualified closing limit. Increase finger
        # stiffness while preserving the official mount gains and geometry.
        actuator = robot.actuators["floating_sharpa_right_actuators"]
        for expression in actuator.stiffness:
            if any(f"right_{finger}_" in expression for finger in ("index", "middle", "ring", "pinky", "thumb")):
                actuator.stiffness[expression] = 400.0
        self.scene.robot = robot
        self.scene.rubiks_cube_asset.spawn.attachment_hand_body_name = SHARPA_PALM_BODY_NAME
        self.scene.rubiks_cube_asset.spawn.semantic_tags = [("class", "rubiks_cube")]
        self.scene.table.spawn.semantic_tags = [("class", "table")]
        self.decimation = 4
        self.sim.dt = 1 / 120
        self.sim.render_interval = self.decimation
        self.sim.physx.bounce_threshold_velocity = 0.01
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_max_rigid_patch_count = 4 * 5 * 2**15


@configclass
class RubiksCubeEnvFloatingSharpaRightCfg_PLAY(RubiksCubeEnvFloatingSharpaRightCfg):
    pass
