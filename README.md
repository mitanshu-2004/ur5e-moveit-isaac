# UR5e end-effector pose control

One Python script takes a goal position and orientation from the terminal and
moves the UR5e there through the UR ROS 2 driver and MoveIt.

## [Stage 1: RViz](rviz/)

RViz shows the arm following the UR driver's mock hardware. The last pose is
out of reach on purpose.

https://github.com/user-attachments/assets/d772afd3-e68c-45cb-9cc7-2a805b198086

## [Stage 2: Isaac Sim](isaac/)

I did not have a GPU that could run Isaac Sim, so I burned a few credits on a
Lightning AI Studio. Two videos of the same run.

**Screencast.** The simulator is a browser stream from the cloud, so it is laggy and low resolution.

https://github.com/user-attachments/assets/c900e40e-52c3-478c-bb5b-e6fe19f12252

**Simulator recording.** Captured on the cloud machine itself.

https://github.com/user-attachments/assets/dfdd6568-1701-4558-b485-67d6784170f8

## How it works

`pose_cmd.py` turns `x y z roll pitch yaw` into a `geometry_msgs/Pose` and sends
one `MoveGroup` action goal to `/move_action`. MoveIt solves IK, plans, and
executes through `scaled_joint_trajectory_controller`. In Stage 1 the controller
drives the UR driver's mock hardware. In Stage 2 it drives Isaac Sim through
`topic_based_ros2_control`.
