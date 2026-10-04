# UR5e end-effector pose control

One Python script takes a goal position and orientation from the terminal and
moves the UR5e there through MoveIt, on the UR ROS 2 driver's mock hardware or
in Isaac Sim.

## [RViz with mock hardware](rviz/)

RViz shows the arm following the UR driver's mock hardware. The last pose is
out of reach on purpose.

[rviz_demo.webm](https://github.com/user-attachments/assets/1d0ba2a9-3bba-4c1b-b730-7f97bd389c49)


## [Isaac Sim](isaac/)

I did not have a GPU that could run Isaac Sim, so I burned a few credits on a
Lightning AI Studio. Two videos of the same run.

**Screencast.** The simulator is a browser stream from the cloud, so it is laggy and low resolution.



https://github.com/user-attachments/assets/a316df73-7c69-4ed7-abdf-12b8682456aa



**Simulator recording.** Captured on the cloud machine itself.



https://github.com/user-attachments/assets/953d5bca-b81c-4d0a-860c-7b8bf3854d63



## How it works

`pose_cmd.py` turns `x y z roll pitch yaw` into a `geometry_msgs/Pose` and sends
one `MoveGroup` action goal to `/move_action`. MoveIt solves IK, plans, and
executes through `scaled_joint_trajectory_controller`. With RViz the controller
drives the UR driver's mock hardware. With Isaac Sim it drives Isaac through
`topic_based_ros2_control`.
