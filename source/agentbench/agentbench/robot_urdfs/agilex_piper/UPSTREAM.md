# AgileX Piper robot description

The files in this directory are derived from the official
[`agilexrobotics/agx_arm_urdf`](https://github.com/agilexrobotics/agx_arm_urdf)
repository at commit `f6642ce0d7872c686f29c99e9e10cd23d1d49313`.

`urdf/piper_with_gripper_description.urdf` combines the upstream Piper URDF
and electric-gripper Xacro into one Isaac-compatible URDF. Package mesh URIs
were made relative and the artificial `world` root was removed because
IsaacLab fixes `base_link`. The massless ROS actuator link and mimic joint were
replaced by two directly actuated finger joints; the task maps one binary
gripper action to their symmetric 0--40 mm travel, preserving the documented
80 mm total opening without adding a non-physical PhysX body. Geometry,
masses, inertias, collision meshes, kinematics, and arm joint limits otherwise
come from upstream.

The upstream MIT license is preserved in `LICENSE`.
