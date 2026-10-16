"""Hybrid 26-cubie Rubik's Cube scene with a Franka Panda gripper."""

from __future__ import annotations

from dataclasses import MISSING
from pathlib import Path

import torch

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg, AssetBaseCfg, RigidObjectCfg, RigidObjectCollectionCfg
from isaaclab.envs import ManagerBasedEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.utils import configclass
from isaaclab_assets.robots.franka import FRANKA_PANDA_HIGH_PD_CFG

from ... import mdp
from ..tabletop_background_cfg import background_asset_cfg
from .rubiks_cube_geometry import CUBIE_PITCH_M
from .rubiks_cube_rules import CubeState
from .rubiks_cube_usd_backend import spawn_rubiks_cube_with_hand_attachment


TABLE_TOP_Z = 0.60
CUBE_CENTER_POSITION = (0.70, 0.0, TABLE_TOP_Z + 0.0355)
ROBOT_BASE_POSITION = (0.36, 0.0, TABLE_TOP_Z)
CUBE_ASSET_DIR = Path(__file__).resolve().parents[5] / "assets" / "articulations" / "rubiks_cube"
CUBE_USD_PATH = str(CUBE_ASSET_DIR / "rubiks_cube.usda")
CUBIE_IDS = tuple(sorted(CubeState.solved().pieces))
COLLECTION_NAMES = ("world_anchor", "core", "carrier_x", "carrier_y", "carrier_z", *CUBIE_IDS)
CUBIE_FILTER_PATHS = [f"{{ENV_REGEX_NS}}/RubiksCube/Cubies/{identity}" for identity in CUBIE_IDS]


def _cube_part_cfg(name: str) -> RigidObjectCfg:
    if name in {"world_anchor", "core"}:
        suffix = f"Mechanism/{name}"
        offset = (0.0, 0.0, 0.0)
    elif name.startswith("carrier_"):
        suffix = f"Mechanism/{name}"
        offset = (0.0, 0.0, 0.0)
    else:
        suffix = f"Cubies/{name}"
        piece = CubeState.solved().pieces[name]
        offset = tuple(coordinate * CUBIE_PITCH_M for coordinate in piece.home_position)
    return RigidObjectCfg(
        prim_path=f"{{ENV_REGEX_NS}}/RubiksCube/{suffix}",
        spawn=None,
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=tuple(center + delta for center, delta in zip(CUBE_CENTER_POSITION, offset, strict=True)),
            rot=(1.0, 0.0, 0.0, 0.0),
            lin_vel=(0.0, 0.0, 0.0),
            ang_vel=(0.0, 0.0, 0.0),
        ),
    )


def cube_part_poses(env) -> torch.Tensor:
    """Return all 31 link poses, with positions relative to the environment origin."""

    parts = env.scene["cube_parts"]
    positions = parts.data.object_link_pos_w - env.scene.env_origins[:, None, :]
    return torch.cat((positions, parts.data.object_link_quat_w), dim=-1).flatten(start_dim=1)


def cube_part_velocities(env) -> torch.Tensor:
    """Return all 31 link linear and angular velocities."""

    return env.scene["cube_parts"].data.object_link_vel_w.flatten(start_dim=1)


def cube_discrete_state(env) -> torch.Tensor:
    """Return integer cubie coordinates and orientations in stable identity order."""

    values: list[int] = []
    for identity in CUBIE_IDS:
        piece = env.cube_state.pieces[identity]
        values.extend(piece.position)
        values.extend(value for row in piece.orientation for value in row)
    return torch.tensor(values, dtype=torch.float32, device=env.device).repeat(env.num_envs, 1)


def cube_frame_state(env) -> torch.Tensor:
    """Return the logical-to-world cube orientation as a flattened integer matrix."""

    values = [value for row in env.cube_frame.logical_to_world for value in row]
    return torch.tensor(values, dtype=torch.float32, device=env.device).repeat(env.num_envs, 1)


def active_turn_state(env) -> torch.Tensor:
    """Return active face code, accumulated carrier angle, and angular velocity."""

    face_code = -1 if env.active_cube_face is None else "URFDLB".index(env.active_cube_face)
    return torch.tensor(
        [face_code, env.active_cube_angle_rad, env.active_cube_angular_velocity_rad_s],
        dtype=torch.float32,
        device=env.device,
    ).repeat(env.num_envs, 1)


def finger_cube_contact_forces(env) -> torch.Tensor:
    """Return each finger-to-cubie force vector in stable cubie identity order."""

    from isaaclab.utils.math import quat_apply_inverse

    force_w = []
    for name in ("left_finger_cube_contact", "right_finger_cube_contact"):
        matrix = torch.nan_to_num(env.scene.sensors[name].data.force_matrix_w)
        force_w.append(matrix.reshape(env.num_envs, len(CUBIE_IDS), 3))
    stacked = torch.stack(force_w, dim=1)
    robot = env.scene["robot"]
    root_quat = robot.data.root_link_quat_w[:, None, None, :].expand(
        -1, stacked.shape[1], stacked.shape[2], -1
    )
    return quat_apply_inverse(root_quat, stacked).flatten(start_dim=1)


@configclass
class RubiksCubeSceneCfg(InteractiveSceneCfg):
    """One robot, one native USD cube, and a collection exposing all 31 bodies."""

    robot: ArticulationCfg = MISSING

    # This asset owns the visual tree and all pre-generated joints.  Its bodies
    # are then exposed through ``cube_parts`` without spawning them a second time.
    rubiks_cube_asset: AssetBaseCfg = AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/RubiksCube",
        spawn=sim_utils.UsdFileCfg(
            usd_path=CUBE_USD_PATH,
            func=spawn_rubiks_cube_with_hand_attachment,
        ),
        init_state=AssetBaseCfg.InitialStateCfg(pos=CUBE_CENTER_POSITION, rot=(1.0, 0.0, 0.0, 0.0)),
    )
    cube_parts: RigidObjectCollectionCfg = RigidObjectCollectionCfg(
        rigid_objects={name: _cube_part_cfg(name) for name in COLLECTION_NAMES}
    )

    background: AssetBaseCfg | None = background_asset_cfg(
        "laboratory", (.5, 0., .35), (1., 1.2, .5)
    )
    table: RigidObjectCfg = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/Table",
        spawn=sim_utils.CuboidCfg(
            size=(1.0, 1.2, 0.5),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            physics_material=sim_utils.RigidBodyMaterialCfg(
                static_friction=0.8, dynamic_friction=0.6, restitution=0.0
            ),
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(0.44, 0.43, 0.41), roughness=0.6
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.5, 0.0, 0.35), rot=(1.0, 0.0, 0.0, 0.0)
        ),
    )

    left_finger_cube_contact: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/Robot/panda_leftfinger",
        update_period=0.0,
        history_length=3,
        debug_vis=False,
        track_contact_points=False,
        filter_prim_paths_expr=CUBIE_FILTER_PATHS,
    )
    right_finger_cube_contact: ContactSensorCfg = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/Robot/panda_rightfinger",
        update_period=0.0,
        history_length=3,
        debug_vis=False,
        track_contact_points=False,
        filter_prim_paths_expr=CUBIE_FILTER_PATHS,
    )

    plane = AssetBaseCfg(
        prim_path="/World/GroundPlane",
        spawn=sim_utils.GroundPlaneCfg(color=(0.52, 0.56, 0.58), visible=False),
        collision_group=-1,
    )
    sky_light = AssetBaseCfg(
        prim_path="/World/skyLight",
        spawn=sim_utils.DomeLightCfg(intensity=900.0, color=(1.0, 1.0, 1.0)),
    )


@configclass
class RubiksCubeActionsCfg:
    """Seven Franka arm positions and one symmetric gripper command."""

    arm_action = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["panda_joint.*"],
        scale=0.5,
        use_default_offset=True,
    )
    gripper_action = mdp.BinaryJointPositionActionCfg(
        asset_name="robot",
        joint_names=["panda_finger.*"],
        open_command_expr={"panda_finger_.*": 0.04},
        close_command_expr={"panda_finger_.*": 0.0},
    )


@configclass
class RubiksCubeObservationsCfg:
    """Robot, continuous/discrete cube state, active turn, and contact state."""

    @configclass
    class StateCfg(ObsGroup):
        actions = ObsTerm(func=mdp.last_action)
        joint_pos = ObsTerm(func=mdp.joint_pos_rel)
        joint_vel = ObsTerm(func=mdp.joint_vel_rel)
        ee_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={"asset_cfg": SceneEntityCfg("robot", body_names=["panda_hand"])},
        )
        cube_part_poses = ObsTerm(func=cube_part_poses)
        cube_part_velocities = ObsTerm(func=cube_part_velocities)
        cube_discrete_state = ObsTerm(func=cube_discrete_state)
        cube_frame_state = ObsTerm(func=cube_frame_state)
        active_turn_state = ObsTerm(func=active_turn_state)
        finger_contact_forces = ObsTerm(func=finger_cube_contact_forces)

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class RubiksCubeEventsCfg:
    """Deterministic reset with high-friction Franka finger pads."""

    fingertip_physics_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg(
                "robot", body_names="panda_leftfinger|panda_rightfinger"
            ),
            "static_friction_range": [4.0, 4.0],
            "dynamic_friction_range": [3.0, 3.0],
            "restitution_range": [0.0, 0.0],
            "num_buckets": 1,
            "make_consistent": True,
        },
    )
    reset_scene = EventTerm(
        func=mdp.reset_scene_to_default,
        mode="reset",
        params={"reset_joint_targets": True},
    )


@configclass
class RubiksCubeEnvFrankaPandaCfg(ManagerBasedEnvCfg):
    """Deterministic hybrid Rubik's Cube task."""

    viewer: ViewerCfg = ViewerCfg(
        eye=(1.45, -1.55, 1.25), lookat=(0.62, 0.0, 0.66), origin_type="env"
    )
    scene: RubiksCubeSceneCfg = RubiksCubeSceneCfg(
        num_envs=1, env_spacing=2.5, replicate_physics=False
    )
    observations: RubiksCubeObservationsCfg = RubiksCubeObservationsCfg()
    actions: RubiksCubeActionsCfg = RubiksCubeActionsCfg()
    events: RubiksCubeEventsCfg = RubiksCubeEventsCfg()

    def __post_init__(self):
        robot_cfg = FRANKA_PANDA_HIGH_PD_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        robot_cfg.spawn.rigid_props.disable_gravity = True
        robot_cfg.spawn.activate_contact_sensors = True
        robot_cfg.spawn.articulation_props.fix_root_link = True
        robot_cfg.spawn.articulation_props.solver_position_iteration_count = 64
        robot_cfg.spawn.articulation_props.solver_velocity_iteration_count = 4
        robot_cfg.actuators["panda_hand"].effort_limit_sim = 140.0
        robot_cfg.actuators["panda_hand"].stiffness = 1800.0
        robot_cfg.actuators["panda_hand"].damping = 120.0
        robot_cfg.init_state.pos = ROBOT_BASE_POSITION
        robot_cfg.init_state.rot = (1.0, 0.0, 0.0, 0.0)
        robot_cfg.init_state.joint_pos = {
            "panda_joint1": 0.78,
            "panda_joint2": -0.78,
            "panda_joint3": 0.0,
            "panda_joint4": -2.35,
            "panda_joint5": 0.0,
            "panda_joint6": 1.57,
            "panda_joint7": 0.78,
            "panda_finger_joint.*": 0.04,
        }
        self.scene.robot = robot_cfg
        self.scene.robot.spawn.semantic_tags = [("class", "robot")]
        self.scene.rubiks_cube_asset.spawn.semantic_tags = [("class", "rubiks_cube")]
        self.scene.table.spawn.semantic_tags = [("class", "table")]

        self.decimation = 4
        self.sim.dt = 1 / 120
        self.sim.render_interval = self.decimation
        self.sim.physx.bounce_threshold_velocity = 0.01
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_max_rigid_patch_count = 4 * 5 * 2**15


@configclass
class RubiksCubeEnvFrankaPandaCfg_PLAY(RubiksCubeEnvFrankaPandaCfg):
    """Single-scene variant for deterministic evaluation and editing."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5
