# Copyright (c) 2025-2026, The DexVerse Project Developers.
# SPDX-License-Identifier: BSD-3-Clause
"""Dual-Franka bookshelf organization environment configurations.

Two table-mounted Franka Panda arms (joint-position actions, binary grippers, 16 action
dimensions in the order ``left_arm, left_gripper, right_arm, right_gripper``) organize
books, display objects and a crate or boxes onto a desk hutch, and in the last variant
throw trash into a bin beside the desk. One base configuration is specialized per
authored variant (see ``variants.py``); the Play variants run a single environment.
"""

from __future__ import annotations

import copy
from dataclasses import MISSING

import isaaclab.envs.mdp as lab_mdp
import isaaclab.sim as sim_utils
import numpy as np
from isaaclab.assets import ArticulationCfg, AssetBaseCfg, RigidObjectCfg
from isaaclab.envs import ManagerBasedRLEnvCfg, ViewerCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors import CameraCfg, ContactSensorCfg
from isaaclab.utils import configclass
from isaaclab_assets.robots.franka import FRANKA_PANDA_HIGH_PD_CFG
from scipy.spatial.transform import Rotation

from . import mdp
from .assets import build_assets
from .catalog import BOOK_SLOTS, DISPLAY_SLOTS, LARGE_SLOTS, SLOT_NAMES, SLOT_PRIMS, TRASH_SLOTS
from .geometry import LAYOUTS, PEDESTAL_SIZE, ROBOT_BASE_HEIGHT, ROBOT_BASES, SHELF_QUAT, TABLE_TOP
from .variants import ALIASES, BY_ID, VARIANTS, alias_cfg_class

HOLD_ACTION = (0.0,) * 7 + (1.0,) + (0.0,) * 7 + (1.0,)
HAND_PRIMS = [
    f"{{ENV_REGEX_NS}}/{side}Panda/{body}"
    for side in ("Left", "Right")
    for body in ("panda_hand", "panda_leftfinger", "panda_rightfinger")
]
LOOK_AT = (0.10, 0.0, 0.95)
CAMERA_EYES = (
    ("third_person_camera", (-1.7, -1.9, 1.8)),
    ("third_person_camera_left", (-1.7, 1.9, 1.8)),
    ("third_person_camera_right", (-0.4, 1.6, 1.6)),  # hutch interior from its open side
)


def _panda_cfg(side: str) -> ArticulationCfg:
    """Kongming dual-Franka convention: fixed base on the table top, mirrored home pose."""
    cfg = copy.deepcopy(FRANKA_PANDA_HIGH_PD_CFG).replace(prim_path=f"{{ENV_REGEX_NS}}/{side.title()}Panda")
    cfg.spawn.rigid_props.disable_gravity = True
    cfg.spawn.activate_contact_sensors = True
    cfg.spawn.articulation_props.fix_root_link = True
    cfg.spawn.articulation_props.solver_position_iteration_count = 64
    cfg.spawn.articulation_props.solver_velocity_iteration_count = 8
    # Franka's continuous grip force: holds a book with margin, but a single gripper cannot
    # carry the 1.5 kg crate by one peg without it rolling, so the crate carry is bimanual.
    cfg.actuators["panda_hand"].effort_limit_sim = 70.0
    # Nominal Panda joint speed limits enforced by the simulator (the stock config leaves them unset).
    cfg.actuators["panda_shoulder"].velocity_limit_sim = 2.175
    cfg.actuators["panda_forearm"].velocity_limit_sim = 2.61
    cfg.actuators["panda_hand"].stiffness = 1800.0
    cfg.actuators["panda_hand"].damping = 120.0
    base = ROBOT_BASES[0 if side == "left" else 1]
    cfg.init_state.pos = (base[0], base[1], ROBOT_BASE_HEIGHT)
    cfg.init_state.rot = (1.0, 0.0, 0.0, 0.0)
    cfg.init_state.joint_pos = {
        "panda_joint1": 0.78 if side == "left" else -0.78,
        "panda_joint2": -0.78,
        "panda_joint3": 0.0,
        "panda_joint4": -2.35,
        "panda_joint5": 0.0,
        "panda_joint6": 1.57,
        "panda_joint7": 0.78 if side == "left" else -0.78,
        "panda_finger_joint.*": 0.04,
    }
    cfg.spawn.semantic_tags = [("class", f"{side}_franka")]
    return cfg


def _fixed_root_reset(asset_name: str) -> EventTerm:
    return EventTerm(
        func=lab_mdp.reset_root_state_uniform,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg(asset_name),
            "pose_range": {key: (0.0, 0.0) for key in ("x", "y", "z", "roll", "pitch", "yaw")},
            "velocity_range": {key: (0.0, 0.0) for key in ("x", "y", "z", "roll", "pitch", "yaw")},
        },
    )


def prop(prim, usd, pos, *, mass, fixed=False, rot=(1.0, 0.0, 0.0, 0.0), solver=(32, 4)):
    return RigidObjectCfg(
        prim_path=f"{{ENV_REGEX_NS}}/{prim}",
        spawn=sim_utils.UsdFileCfg(
            usd_path=usd,
            activate_contact_sensors=not fixed,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                rigid_body_enabled=True,
                kinematic_enabled=fixed,
                disable_gravity=fixed,
                solver_position_iteration_count=solver[0],
                solver_velocity_iteration_count=solver[1],
                max_depenetration_velocity=1.0,
                linear_damping=0.02,
                angular_damping=0.05,
            ),
            collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.002, rest_offset=0.0),
            mass_props=sim_utils.MassPropertiesCfg(mass=mass),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=pos, rot=rot),
    )


def fixed_box(name, size, pos, color, friction=(0.6, 0.5)):
    return RigidObjectCfg(
        prim_path=f"{{ENV_REGEX_NS}}/{name}",
        spawn=sim_utils.CuboidCfg(
            size=size,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(kinematic_enabled=True),
            collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.002, rest_offset=0.0),
            physics_material=sim_utils.RigidBodyMaterialCfg(
                static_friction=friction[0], dynamic_friction=friction[1], restitution=0.0
            ),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=color),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=pos),
    )


def camera_rotation(eye, target):
    backward = np.array(eye) - np.array(target)
    backward /= np.linalg.norm(backward)
    right = np.cross((0.0, 0.0, 1.0), backward)
    right /= np.linalg.norm(right)
    up = np.cross(backward, right)
    return tuple(Rotation.from_matrix(np.stack((right, up, backward), axis=1)).as_quat(scalar_first=True))


def parking_pose(slot: int, height: float) -> tuple[float, float, float]:
    """Collision-free spawn pose used only until the first reset places the objects."""
    z = TABLE_TOP + height / 2 + 0.003
    if slot in BOOK_SLOTS:
        return (0.12, -0.45 + 0.10 * slot, z)
    if slot in LARGE_SLOTS:
        return (-0.18, 0.15 if slot == LARGE_SLOTS[0] else 0.58, z)
    if slot in TRASH_SLOTS:
        return (-0.02, -0.66 + 0.10 * (slot - min(TRASH_SLOTS)), z)
    return (-0.20, -0.60 + 0.15 * (slot - min(DISPLAY_SLOTS)), z)


@configclass
class BookshelfSceneCfg(InteractiveSceneCfg):
    left_robot: ArticulationCfg = MISSING
    right_robot: ArticulationCfg = MISSING
    shelf: RigidObjectCfg = MISSING
    table: RigidObjectCfg = MISSING
    pedestal_left: RigidObjectCfg | None = None
    pedestal_right: RigidObjectCfg | None = None
    slot_0: RigidObjectCfg | None = None
    slot_1: RigidObjectCfg | None = None
    slot_2: RigidObjectCfg | None = None
    slot_3: RigidObjectCfg | None = None
    slot_4: RigidObjectCfg | None = None
    slot_5: RigidObjectCfg | None = None
    slot_6: RigidObjectCfg | None = None
    slot_7: RigidObjectCfg | None = None
    slot_8: RigidObjectCfg | None = None
    slot_9: RigidObjectCfg | None = None
    slot_10: RigidObjectCfg | None = None
    slot_11: RigidObjectCfg | None = None
    slot_12: RigidObjectCfg | None = None
    slot_13: RigidObjectCfg | None = None
    slot_14: RigidObjectCfg | None = None
    slot_15: RigidObjectCfg | None = None
    slot_16: RigidObjectCfg | None = None
    slot_17: RigidObjectCfg | None = None
    slot_18: RigidObjectCfg | None = None
    slot_contact_0: ContactSensorCfg | None = None
    slot_contact_1: ContactSensorCfg | None = None
    slot_contact_2: ContactSensorCfg | None = None
    slot_contact_3: ContactSensorCfg | None = None
    slot_contact_4: ContactSensorCfg | None = None
    slot_contact_5: ContactSensorCfg | None = None
    slot_contact_6: ContactSensorCfg | None = None
    slot_contact_7: ContactSensorCfg | None = None
    slot_contact_8: ContactSensorCfg | None = None
    slot_contact_9: ContactSensorCfg | None = None
    slot_contact_10: ContactSensorCfg | None = None
    slot_contact_11: ContactSensorCfg | None = None
    slot_contact_12: ContactSensorCfg | None = None
    slot_contact_13: ContactSensorCfg | None = None
    slot_contact_14: ContactSensorCfg | None = None
    slot_contact_15: ContactSensorCfg | None = None
    slot_contact_16: ContactSensorCfg | None = None
    slot_contact_17: ContactSensorCfg | None = None
    slot_contact_18: ContactSensorCfg | None = None
    bin: RigidObjectCfg | None = None
    third_person_camera: CameraCfg | None = None
    third_person_camera_left: CameraCfg | None = None
    third_person_camera_right: CameraCfg | None = None
    plane = AssetBaseCfg(
        prim_path="/World/GroundPlane",
        collision_group=-1,
        spawn=sim_utils.GroundPlaneCfg(size=(100, 100), color=(0.52, 0.56, 0.58)),
    )
    sky_light = AssetBaseCfg(
        prim_path="/World/skyLight",
        spawn=sim_utils.DomeLightCfg(intensity=1800.0, color=(0.85, 0.90, 1.0)),
    )


@configclass
class BookshelfActionsCfg:
    """Seven Panda joint positions and one binary gripper per arm (Kongming convention)."""

    left_arm = lab_mdp.JointPositionActionCfg(
        asset_name="left_robot", joint_names=["panda_joint.*"], scale=0.5, use_default_offset=True
    )
    left_gripper = lab_mdp.BinaryJointPositionActionCfg(
        asset_name="left_robot",
        joint_names=["panda_finger.*"],
        open_command_expr={"panda_finger_.*": 0.04},
        close_command_expr={"panda_finger_.*": 0.0},
    )
    right_arm = lab_mdp.JointPositionActionCfg(
        asset_name="right_robot", joint_names=["panda_joint.*"], scale=0.5, use_default_offset=True
    )
    right_gripper = lab_mdp.BinaryJointPositionActionCfg(
        asset_name="right_robot",
        joint_names=["panda_finger.*"],
        open_command_expr={"panda_finger_.*": 0.04},
        close_command_expr={"panda_finger_.*": 0.0},
    )


@configclass
class BookshelfEventsCfg:
    reset_left_root = _fixed_root_reset("left_robot")
    reset_right_root = _fixed_root_reset("right_robot")
    reset_left_joints = EventTerm(
        func=lab_mdp.reset_joints_by_offset,
        mode="reset",
        params={"asset_cfg": SceneEntityCfg("left_robot"), "position_range": (0.0, 0.0), "velocity_range": (0.0, 0.0)},
    )
    reset_right_joints = EventTerm(
        func=lab_mdp.reset_joints_by_offset,
        mode="reset",
        params={"asset_cfg": SceneEntityCfg("right_robot"), "position_range": (0.0, 0.0), "velocity_range": (0.0, 0.0)},
    )
    reset_objects = EventTerm(func=mdp.reset_objects, mode="reset")


@configclass
class BookshelfObservationsCfg:
    @configclass
    class PolicyCfg(ObsGroup):
        actions = ObsTerm(func=lab_mdp.last_action)
        left_joint_pos = ObsTerm(func=lab_mdp.joint_pos_rel, params={"asset_cfg": SceneEntityCfg("left_robot")})
        left_joint_vel = ObsTerm(func=lab_mdp.joint_vel_rel, params={"asset_cfg": SceneEntityCfg("left_robot")})
        right_joint_pos = ObsTerm(func=lab_mdp.joint_pos_rel, params={"asset_cfg": SceneEntityCfg("right_robot")})
        right_joint_vel = ObsTerm(func=lab_mdp.joint_vel_rel, params={"asset_cfg": SceneEntityCfg("right_robot")})

        def __post_init__(self):
            self.concatenate_terms = True
            self.enable_corruption = False

    @configclass
    class StateCfg(ObsGroup):
        objects = ObsTerm(func=mdp.task_state)

        def __post_init__(self):
            self.concatenate_terms = True
            self.enable_corruption = False

    @configclass
    class GoalCfg(ObsGroup):
        shelf = ObsTerm(func=mdp.task_goal)

        def __post_init__(self):
            self.concatenate_terms = True
            self.enable_corruption = False

    @configclass
    class PrivilegedCfg(ObsGroup):
        velocities = ObsTerm(func=mdp.task_velocities)
        progress = ObsTerm(func=mdp.task_progress)

        def __post_init__(self):
            self.concatenate_terms = True
            self.enable_corruption = False

    @configclass
    class ContactCfg(ObsGroup):
        contact = ObsTerm(func=mdp.contact_forces)

        def __post_init__(self):
            self.concatenate_terms = True
            self.enable_corruption = False

    policy: PolicyCfg = PolicyCfg()
    state: StateCfg = StateCfg()
    goal: GoalCfg = GoalCfg()
    privileged: PrivilegedCfg = PrivilegedCfg()
    contact: ContactCfg = ContactCfg()
    rgb: ObsGroup | None = None
    depth: ObsGroup | None = None
    pointcloud: ObsGroup | None = None


@configclass
class CameraObservationsCfg(ObsGroup):
    concatenate_terms: bool = False
    enable_corruption: bool = False


@configclass
class PointCloudObservationsCfg(ObsGroup):
    camera_point_cloud_w = ObsTerm(
        func=mdp.workspace_point_cloud,
        params={"sensor_cfgs": [SceneEntityCfg("third_person_camera")], "num_points": 4096},
    )
    concatenate_terms: bool = True
    enable_corruption: bool = False


@configclass
class BookshelfRewardsCfg:
    milestone = RewTerm(func=mdp.milestone_reward, weight=2.0)
    success = RewTerm(func=mdp.success_reward, weight=20.0)
    action_l2 = RewTerm(func=mdp.action_l2_clamped, weight=-0.005)
    action_rate_l2 = RewTerm(func=mdp.action_rate_l2_clamped, weight=-0.005)


@configclass
class BookshelfTerminationsCfg:
    time_out = DoneTerm(func=lab_mdp.time_out, time_out=True)
    success = DoneTerm(func=mdp.task_success)
    object_lost = DoneTerm(func=mdp.objects_lost)
    physics_violation = DoneTerm(func=mdp.physics_violation)


@configclass
class OrganizeBookshelfEnvCfg(ManagerBasedRLEnvCfg):
    """Base configuration; subclasses only choose the authored variant."""

    variant_id: str = "ShelfTable"
    task_instruction: str = ""
    default_action: tuple[float, ...] = HOLD_ACTION
    scene: BookshelfSceneCfg = BookshelfSceneCfg(num_envs=16, env_spacing=3.0, replicate_physics=False)
    observations: BookshelfObservationsCfg = BookshelfObservationsCfg()
    actions: BookshelfActionsCfg = BookshelfActionsCfg()
    events: BookshelfEventsCfg = BookshelfEventsCfg()
    rewards: BookshelfRewardsCfg = BookshelfRewardsCfg()
    terminations: BookshelfTerminationsCfg = BookshelfTerminationsCfg()
    viewer: ViewerCfg = ViewerCfg(eye=(-2.1, -2.2, 1.9), lookat=LOOK_AT, origin_type="env")
    episode_length_s: float = 120.0
    is_finite_horizon: bool = True
    decimation: int = 4

    def configure_cameras(self, enabled=True, multiview=False, names=None):
        """Toggle camera sensors and all dependent observations together.

        ``names`` selects a subset of ``CAMERA_EYES``; otherwise the first view is used, or
        all three when ``multiview`` is set.
        """
        if names is None:
            names = tuple(name for index, (name, _) in enumerate(CAMERA_EYES) if multiview or index == 0)
        self.observations.rgb = CameraObservationsCfg() if enabled else None
        self.observations.depth = CameraObservationsCfg() if enabled else None
        self.observations.pointcloud = PointCloudObservationsCfg() if enabled else None
        cameras = []
        for name, eye in CAMERA_EYES:
            if not enabled or name not in names:
                setattr(self.scene, name, None)
                continue
            setattr(
                self.scene,
                name,
                CameraCfg(
                    prim_path=f"{{ENV_REGEX_NS}}/{name}",
                    update_period=0.0,
                    height=480,
                    width=640,
                    data_types=["rgb", "distance_to_image_plane"],
                    spawn=sim_utils.PinholeCameraCfg(
                        focal_length=24.0, horizontal_aperture=24.0, clipping_range=(0.05, 10.0)
                    ),
                    offset=CameraCfg.OffsetCfg(pos=eye, rot=camera_rotation(eye, LOOK_AT), convention="opengl"),
                ),
            )
            cameras.append(SceneEntityCfg(name))
            for group, data_type in (
                (self.observations.rgb, "rgb"),
                (self.observations.depth, "distance_to_image_plane"),
            ):
                setattr(
                    group,
                    name,
                    ObsTerm(
                        func=lab_mdp.image,
                        params={"sensor_cfg": SceneEntityCfg(name), "data_type": data_type, "normalize": False},
                    ),
                )
        if enabled:
            self.observations.pointcloud.camera_point_cloud_w.params["sensor_cfgs"] = cameras

    def __post_init__(self):
        variant = BY_ID[self.variant_id]
        table = variant.slot_table()
        layout = LAYOUTS[variant.layout]
        self.task_instruction = variant.instruction()
        self.episode_length_s = variant.episode_length_s
        manifest = build_assets()
        self.scene.left_robot = _panda_cfg("left")
        self.scene.right_robot = _panda_cfg("right")
        for side, base in zip(("left", "right"), ROBOT_BASES):
            setattr(
                self.scene,
                f"pedestal_{side}",
                fixed_box(
                    f"Pedestal{side.title()}",
                    (PEDESTAL_SIZE, PEDESTAL_SIZE, ROBOT_BASE_HEIGHT),
                    (base[0], base[1], ROBOT_BASE_HEIGHT / 2),
                    (0.22, 0.24, 0.26),
                ),
            )
        self.scene.shelf = prop(
            "Shelf", manifest["shelves"][layout.name], layout.shelf_pos, mass=40.0, fixed=True, rot=SHELF_QUAT
        )
        # One kinematic prop per layout: wood-textured top, legs and blockers (see assets.py).
        self.scene.table = prop("Desk", manifest["desks"][layout.name], (0.0, 0.0, 0.0), mass=60.0, fixed=True)
        if table.trash:
            self.scene.bin = prop("Bin", manifest["props"]["bin"], layout.bin_pos, mass=5.0, fixed=True)
        furniture = ["{ENV_REGEX_NS}/Desk", "{ENV_REGEX_NS}/Shelf"] + (["{ENV_REGEX_NS}/Bin"] if table.trash else [])
        for slot in table.present_indices():
            cls = table.classes[slot]
            solver = (64, 8) if slot in LARGE_SLOTS else (32, 4)
            setattr(
                self.scene,
                SLOT_NAMES[slot],
                prop(
                    SLOT_PRIMS[slot],
                    manifest["props"][cls.name],
                    parking_pose(slot, cls.sizes[2]),
                    mass=cls.mass,
                    solver=solver,
                ),
            )
            setattr(
                self.scene,
                f"slot_contact_{slot}",
                ContactSensorCfg(
                    prim_path=f"{{ENV_REGEX_NS}}/{SLOT_PRIMS[slot]}",
                    update_period=0.0,
                    # Hands first (release detection sums these), then the furniture (penetration audit).
                    filter_prim_paths_expr=HAND_PRIMS + furniture,
                    max_contact_data_count_per_prim=64,
                ),
            )
        self.sim.dt = 1 / 120
        self.sim.render_interval = self.decimation
        self.sim.physx.bounce_threshold_velocity = 0.01
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_max_rigid_patch_count = 2**20
        self.num_rerenders_on_reset = 2
        self.configure_cameras(False)


def _level_cfg(name: str, variant_id: str, play: bool):
    """A configuration class for one level; the Play twin runs a single environment."""

    def __post_init__(self):
        OrganizeBookshelfEnvCfg.__post_init__(self)
        if play:
            self.scene.num_envs = 1

    namespace = {
        "__module__": __name__,
        "__qualname__": name,
        "__doc__": f"Bookshelf level {variant_id}{' (one environment)' if play else ''}.",
        "__annotations__": {"variant_id": str},
        "variant_id": variant_id,
        "__post_init__": __post_init__,
    }
    return configclass(type(name, (OrganizeBookshelfEnvCfg,), namespace))


# One class per level and Play twin, e.g. OrganizeBookshelfBooksTableD1EnvCfg(_PLAY); the five
# original class names stay valid as aliases of their D3 levels.
for _variant in VARIANTS:
    for _play in (False, True):
        globals()[_variant.cfg_class(_play)] = _level_cfg(_variant.cfg_class(_play), _variant.id, _play)
for _alias, _target in ALIASES.items():
    for _play in (False, True):
        globals()[alias_cfg_class(_alias, _play)] = globals()[BY_ID[_target].cfg_class(_play)]
