"""Vision-only Hanoi environment backed by a post-initialization RGB camera."""

from __future__ import annotations

import gymnasium as gym
import numpy as np
import omni.replicator.core as rep
import omni.usd
import torch
from pxr import UsdGeom

from isaaclab.envs import ManagerBasedEnv
from isaaclab.sensors.camera.camera import create_rotation_matrix_from_view
from isaaclab.sim.utils import create_prim
from isaaclab.utils.math import quat_from_matrix

from .hanoi_cfg import (
    VISION_CAMERA_EYE,
    VISION_CAMERA_HEIGHT,
    VISION_CAMERA_TARGET,
    VISION_CAMERA_WIDTH,
)


class HanoiVisionEnv(ManagerBasedEnv, gym.Env):
    """Return rendered RGB plus robot proprioception, without object state terms."""

    def __init__(self, cfg, **kwargs):
        super().__init__(cfg=cfg, **kwargs)
        if self.num_envs != 1:
            raise ValueError("HanoiVisionEnv currently supports exactly one environment.")

        self._camera_path = "/World/HanoiVisionAgentCamera"
        self._rgb_annotator = None
        self._camera_warmed_up = False
        self._configure_gym_spaces()

    def _configure_gym_spaces(self) -> None:
        policy_spaces = {}
        group_name = "policy"
        term_names = self.observation_manager.active_terms[group_name]
        term_dims = self.observation_manager.group_obs_dim[group_name]
        for term_name, term_dim in zip(term_names, term_dims):
            policy_spaces[term_name] = gym.spaces.Box(low=-np.inf, high=np.inf, shape=term_dim)
        policy_spaces["rgb"] = gym.spaces.Box(
            low=0,
            high=255,
            shape=(VISION_CAMERA_HEIGHT, VISION_CAMERA_WIDTH, 3),
            dtype=np.uint8,
        )

        self.single_observation_space = gym.spaces.Dict({"policy": gym.spaces.Dict(policy_spaces)})
        action_dim = sum(self.action_manager.action_term_dim)
        self.single_action_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(action_dim,))
        self.observation_space = gym.vector.utils.batch_space(self.single_observation_space, self.num_envs)
        self.action_space = gym.vector.utils.batch_space(self.single_action_space, self.num_envs)

    def _setup_camera(self) -> None:
        self._create_camera()
        render_product = rep.create.render_product(
            self._camera_path,
            resolution=(VISION_CAMERA_WIDTH, VISION_CAMERA_HEIGHT),
        )
        render_product_path = render_product.path if not isinstance(render_product, str) else render_product
        self._rgb_annotator = rep.AnnotatorRegistry.get_annotator("rgb", device="cpu")
        self._rgb_annotator.attach(render_product_path)

    def _create_camera(self) -> None:
        stage = omni.usd.get_context().get_stage()
        eyes = torch.tensor([VISION_CAMERA_EYE], dtype=torch.float32, device="cpu")
        targets = torch.tensor([VISION_CAMERA_TARGET], dtype=torch.float32, device="cpu")
        up_axis = UsdGeom.GetStageUpAxis(stage)
        orientation = quat_from_matrix(create_rotation_matrix_from_view(eyes, targets, up_axis, device="cpu"))[0]
        camera_prim = create_prim(
            self._camera_path,
            "Camera",
            position=VISION_CAMERA_EYE,
            orientation=orientation.numpy(),
            stage=stage,
        )
        camera = UsdGeom.Camera(camera_prim)
        camera.GetFocalLengthAttr().Set(28.0)
        camera.GetHorizontalApertureAttr().Set(24.0)
        self.sim.set_camera_view(eye=VISION_CAMERA_EYE, target=VISION_CAMERA_TARGET)

    def _capture_rgb(self) -> torch.Tensor:
        attempts = 30 if not self._camera_warmed_up else 2
        rgb = None
        for _ in range(attempts):
            self.sim.render()
            data = self._rgb_annotator.get_data()
            if data is None:
                continue
            array = np.asarray(data)
            if array.ndim == 3 and array.shape[-1] >= 3 and array.size:
                rgb = np.ascontiguousarray(array[..., :3], dtype=np.uint8)
                if float(rgb.std()) >= 1.0:
                    break
        if rgb is None or float(rgb.std()) < 1.0:
            raise RuntimeError("Hanoi vision camera did not return a non-blank RGB frame.")
        self._camera_warmed_up = True
        return torch.from_numpy(rgb).unsqueeze(0)

    def _add_rgb(self, observations):
        policy = observations.get("policy")
        if not isinstance(policy, dict):
            raise RuntimeError("Hanoi vision observations must contain a named policy group.")
        policy["rgb"] = self._capture_rgb()
        return observations

    def reset(self, *args, **kwargs):
        observations, extras = super().reset(*args, **kwargs)
        if self._rgb_annotator is None:
            self._setup_camera()
        return self._add_rgb(observations), extras

    def reset_to(self, *args, **kwargs):
        observations, extras = super().reset_to(*args, **kwargs)
        if self._rgb_annotator is None:
            self._setup_camera()
        return self._add_rgb(observations), extras

    def step(self, action: torch.Tensor):
        observations, extras = super().step(action)
        return self._add_rgb(observations), extras

    def close(self):
        annotator = getattr(self, "_rgb_annotator", None)
        if annotator is not None:
            annotator.detach()
            self._rgb_annotator = None
        super().close()
