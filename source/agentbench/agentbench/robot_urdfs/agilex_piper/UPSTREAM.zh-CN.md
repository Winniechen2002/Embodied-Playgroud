<a id="section-1"></a>
# AgileX Piper 机器人描述

本目录中的文件源于官方 [`agilexrobotics/agx_arm_urdf`](https://github.com/agilexrobotics/agx_arm_urdf) 仓库，commit 为 `f6642ce0d7872c686f29c99e9e10cd23d1d49313`。

`urdf/piper_with_gripper_description.urdf` 将上游 Piper URDF 与电动夹爪 Xacro 合并为一个兼容 Isaac 的 URDF。包内网格 URI 已改为相对路径；由于 IsaacLab 固定 `base_link`，人为添加的 `world` 根节点已移除。无质量的 ROS 执行器连杆和 mimic 关节被替换为两个直接驱动的手指关节；任务将一个二值夹爪动作映射为两指对称的 0--40 mm 行程，在不添加非物理 PhysX 刚体的情况下保留文档规定的 80 mm 总开口。其余几何、质量、惯量、碰撞网格、运动学和机械臂关节限位均来自上游。

上游 MIT 许可证保留在 `LICENSE` 中。
