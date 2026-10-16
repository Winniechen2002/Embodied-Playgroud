"""One public aperture command driving both Panda finger position targets."""

from isaaclab.envs.mdp.actions.actions_cfg import BinaryJointPositionActionCfg
from isaaclab.envs.mdp.actions.binary_joint_actions import BinaryJointPositionAction
from isaaclab.utils import configclass


class ContinuousGripperPositionAction(BinaryJointPositionAction):
    """Interpolate the ordinary open/closed joint targets with a scalar action.

    -1 requests closed fingers and +1 requests fully open fingers. Intermediate
    apertures reduce spring compression against a grasped bar; the inherited
    apply_actions method only submits joint position targets to the drive.
    """

    def process_actions(self, actions):
        self._raw_actions[:] = actions
        fraction = (actions.clamp(-1., 1.) + 1.) * .5
        self._processed_actions[:] = (
            self._close_command + fraction * (self._open_command - self._close_command))
        if self.cfg.clip is not None:
            self._processed_actions[:] = self._processed_actions.clamp(
                min=self._clip[:, :, 0], max=self._clip[:, :, 1])


@configclass
class ContinuousGripperPositionActionCfg(BinaryJointPositionActionCfg):
    class_type: type = ContinuousGripperPositionAction
