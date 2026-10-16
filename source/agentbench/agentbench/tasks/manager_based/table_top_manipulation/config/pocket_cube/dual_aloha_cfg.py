"""Two AgileX Piper follower arms manipulating a physical 2x2 cube."""

import copy

import isaaclab.sim as sim_utils
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.utils import configclass

from agentbench.robot_agents.agilex_piper import (
    AGILEX_PIPER_ARM_JOINT_NAMES,
    AGILEX_PIPER_CFG,
    AGILEX_PIPER_EE_BODY_NAME,
    AGILEX_PIPER_GRIPPER_BODY_NAMES,
    AGILEX_PIPER_GRIPPER_JOINT_NAMES,
)

from ... import mdp
from .pocket_cube_cfg import (
    PocketCubeEnvCfgBase,
    PocketCubeEventsCfg,
    PocketCubeObservationsCfg,
    PocketCubeSceneCfg,
    TABLE_TOP_Z,
)


@configclass
class DualAlohaPocketCubeActionsCfg:
    left_arm = mdp.JointPositionActionCfg(
        asset_name="left_robot",
        joint_names=list(AGILEX_PIPER_ARM_JOINT_NAMES),
        scale=0.35,
        use_default_offset=True,
        preserve_order=True,
    )
    # The top-B pickup needs a compliant 21.2-mm enclosure followed by the
    # stronger 20.5-mm carrying target.  Expose both original gripper joints
    # through the declared action interface so this staging is expressed as
    # ordinary, logged position commands rather than hidden action-term state.
    left_gripper = mdp.JointPositionActionCfg(
        asset_name="left_robot",
        joint_names=list(AGILEX_PIPER_GRIPPER_JOINT_NAMES),
        scale=1.0,
        offset=0.0,
        use_default_offset=False,
        preserve_order=True,
    )
    right_arm = mdp.JointPositionActionCfg(
        asset_name="right_robot",
        joint_names=list(AGILEX_PIPER_ARM_JOINT_NAMES),
        scale=0.35,
        use_default_offset=True,
        preserve_order=True,
    )
    # Expose both physical right-gripper joint targets through the declared
    # action interface.  The R pickup needs a 22.6-mm compliant command while
    # the later fixed-core arc needs the original 22.0-mm command; a binary
    # action cannot express that legal staged motor command without mutating
    # private action-term state.  Absolute joint-position actions keep every
    # command finite, logged, effort-limited, and collision-audited.
    right_gripper = mdp.JointPositionActionCfg(
        asset_name="right_robot",
        joint_names=list(AGILEX_PIPER_GRIPPER_JOINT_NAMES),
        scale=1.0,
        offset=0.0,
        use_default_offset=False,
        preserve_order=True,
    )


@configclass
class DualAlohaPocketCubeObservationsCfg(PocketCubeObservationsCfg):
    @configclass
    class StateCfg(PocketCubeObservationsCfg.StateCfg):
        left_gripper_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={
                "asset_cfg": SceneEntityCfg(
                    "left_robot", body_names=[AGILEX_PIPER_EE_BODY_NAME]
                )
            },
        )
        right_gripper_pose = ObsTerm(
            func=mdp.body_pose_w,
            params={
                "asset_cfg": SceneEntityCfg(
                    "right_robot", body_names=[AGILEX_PIPER_EE_BODY_NAME]
                )
            },
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = True

    state: StateCfg = StateCfg()


@configclass
class DualAlohaPocketCubeEventsCfg(PocketCubeEventsCfg):
    left_gripper_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg(
                "left_robot",
                body_names=[AGILEX_PIPER_EE_BODY_NAME, *AGILEX_PIPER_GRIPPER_BODY_NAMES],
            ),
            "static_friction_range": (4.0, 4.0),
            "dynamic_friction_range": (3.0, 3.0),
            "restitution_range": (0.0, 0.0),
            "num_buckets": 1,
            "make_consistent": True,
        },
    )
    right_gripper_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg(
                "right_robot",
                body_names=[AGILEX_PIPER_EE_BODY_NAME, *AGILEX_PIPER_GRIPPER_BODY_NAMES],
            ),
            "static_friction_range": (4.0, 4.0),
            "dynamic_friction_range": (3.0, 3.0),
            "restitution_range": (0.0, 0.0),
            "num_buckets": 1,
            "make_consistent": True,
        },
    )


@configclass
class DualAlohaPocketCubeSceneCfg(PocketCubeSceneCfg):
    """ALOHA scene with one contact filter per physical corner body."""

    for side in ("left", "right"):
        for link_name in AGILEX_PIPER_GRIPPER_BODY_NAMES:
            locals()[f"{side}_{link_name}_face_contacts"] = ContactSensorCfg(
                prim_path=f"{{ENV_REGEX_NS}}/{side.title()}Piper/{link_name}",
                update_period=0.0,
                history_length=1,
                debug_vis=False,
                track_contact_points=True,
                # One 16x12 mm pad can generate more than four manifold
                # points across neighboring cubies.  The default four-entry
                # GPU buffer overflows before contact and then corrupts the
                # rigid-body tensor view.  This changes sensing capacity only,
                # not collision geometry or contact response.
                max_contact_data_count_per_prim=64,
                track_friction_forces=False,
                filter_prim_paths_expr=[
                    f"{{ENV_REGEX_NS}}/PocketCube/Cubies/Cubie_{corner}"
                    for corner in ("urf", "ufl", "ulb", "ubr", "dfr", "dlf", "dbl", "drb")
                ],
            )

    del side, link_name


def _piper_arm_cfg(side: str):
    cfg = copy.deepcopy(AGILEX_PIPER_CFG)
    # A compact contact envelope avoids simultaneous response from neighboring
    # cube pads while retaining ordinary non-penetrating robot contact.
    cfg.spawn.collision_props = sim_utils.CollisionPropertiesCfg(
        contact_offset=0.0008,
        rest_offset=0.0,
        # Finite contact-patch model for the original 56 mm-wide Piper fingers. Without
        # this PhysX defaults to a zero-radius point patch, so the suspended
        # cube can spin about the pad normal regardless of Coulomb friction.
        # A 16 mm radius stays inside the visible finger-pad half-width and
        # acts only while the original collision mesh is touching.  The
        # former 9 mm point-like patch let a correctly enclosed layer slip by
        # roughly three quarters of the commanded relative wrist motion.
        torsional_patch_radius=0.016,
        min_torsional_patch_radius=0.016,
    )
    cfg.spawn.articulation_props.solver_position_iteration_count = 64
    cfg.spawn.articulation_props.solver_velocity_iteration_count = 8
    # The simulated follower should track its calibrated joint targets instead
    # of sagging several centimetres under the gripper mass.  This remains a
    # finite-effort physical position servo; no body pose is written directly.
    # A 70 g cube does not need the generic rigid-workcell gains.  Those gains
    # turn sub-millimetre IK error into multi-newton shocks and can spuriously
    # twist an adjacent face while grasping.  These finite compliant gains
    # still track the visual trajectory while permitting real contact yield.
    cfg.actuators["piper_arm"].stiffness = 500.0
    cfg.actuators["piper_arm"].damping = 35.0
    # The left B-row support carries the 0.687 N cube and needs the verified
    # 5.5 N limit to avoid slowly slipping during the airborne regrasp.  The
    # right F-layer jaw only has to overcome the 0.003 N m face detent.  Giving
    # it the same force produced a 0.25--0.33 mm side-pad compression on UFL
    # at the first close sample, so keep that operating jaw deliberately more
    # compliant while retaining ample finite contact torque.
    cfg.actuators["piper_gripper"].effort_limit_sim = (
        6.5 if side == "left" else 3.5
    )
    # The load-bearing left jaw retains the 22.0-mm enclosure.  Keep the right
    # jaw substantially softer: 280 N/m made the otherwise verified U arc
    # exceed the visible-shell tolerance.  F finish contact is supplied by
    # the smooth Cartesian normal compensation in the controller instead of
    # globally increasing squeeze across all three moves.
    cfg.actuators["piper_gripper"].stiffness = (
        600.0 if side == "left" else 190.0
    )
    cfg.actuators["piper_gripper"].damping = 12.0
    cfg.prim_path = f"{{ENV_REGEX_NS}}/{side.title()}Piper"
    # Mount the two followers closer to the cube's x=0.56 work point.  The
    # previous x=-0.02, y=+/-0.26 placement forced both arms to operate near
    # full extension.  These symmetric mounts shorten the forward reach by
    # 27 cm and the lateral reach by 6 cm per side.
    cfg.init_state.pos = (0.25, -0.20 if side == "left" else 0.20, TABLE_TOP_Z)
    cfg.init_state.rot = (1.0, 0.0, 0.0, 0.0)
    cfg.init_state.joint_pos.update(
        {
            # Collision-safe ready pose for the compact manipulation pad.  It
            # is an ordinary fixed initial robot posture (no cube state is
            # used): both tool points begin about 13 cm above the cube.
            # Re-solved for the closer bases while preserving the former safe
            # tool poses above the cube (sub-micrometre FK residual).
            "joint1": 0.5379616624 if side == "left" else -0.5401276864,
            "joint2": 1.4302596472 if side == "left" else 1.4270597933,
            "joint3": -0.7090977017 if side == "left" else -0.7140844008,
            "joint4": 0.9247591840 if side == "left" else -0.9512654969,
            "joint5": -0.1979574163 if side == "left" else -0.1946564818,
            "joint6": -0.8170113308 if side == "left" else 0.8568742224,
            "gripper_joint1": 0.04,
            "gripper_joint2": -0.04,
        }
    )
    cfg.spawn.semantic_tags = [("class", f"{side}_aloha_arm")]
    return cfg


@configclass
class DualAlohaPocketCubeEnvCfg(PocketCubeEnvCfgBase):
    scene: DualAlohaPocketCubeSceneCfg = DualAlohaPocketCubeSceneCfg(
        num_envs=128, env_spacing=2.2, replicate_physics=False
    )
    observations: DualAlohaPocketCubeObservationsCfg = DualAlohaPocketCubeObservationsCfg()
    actions: DualAlohaPocketCubeActionsCfg = DualAlohaPocketCubeActionsCfg()
    events: DualAlohaPocketCubeEventsCfg = DualAlohaPocketCubeEventsCfg()

    def __post_init__(self):
        super().__post_init__()
        self.scene.left_robot = _piper_arm_cfg("left")
        self.scene.right_robot = _piper_arm_cfg("right")


@configclass
class DualAlohaPocketCubeEnvCfg_PLAY(DualAlohaPocketCubeEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.2
