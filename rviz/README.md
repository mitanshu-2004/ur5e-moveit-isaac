# Stage 1: pose_cmd.py

Single script to control UR5e in Rviz using end effector pose

[rviz_demo.webm](https://github.com/user-attachments/assets/d772afd3-e68c-45cb-9cc7-2a805b198086)

## Run

Required ROS 2 packages:

```bash
sudo apt install ros-jazzy-ur ros-jazzy-moveit
```

Three terminals, each with `source /opt/ros/jazzy/setup.bash` first.

```bash
ros2 launch ur_robot_driver ur5e.launch.py use_mock_hardware:=true robot_ip:=0
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e launch_rviz:=false
python3 pose_cmd.py
```

```
x y z roll pitch yaw   (m, deg)   q to quit
> 0.4 0.1 0.4 180 0 0
done
> 1.5 0 0.3 180 0 0
failed: GOAL_STATE_INVALID
```

## How it works

`pose_cmd.py` turns the terminal input to a `geometry_msgs/Pose` and sends one `MoveGroup` action goal to `/move_action`: a `PositionConstraint` (5 mm sphere at the target) and an `OrientationConstraint` (0.05 rad per axis), both on `tool0` in `base_link`.

MoveIt solves the IK, plans, and sends the trajectory to the UR driver's `scaled_joint_trajectory_controller`. The driver publishes `/joint_states`, which becomes TF, which RViz draws.

Angles are degrees, extrinsic XYZ (`R = Rz(yaw)·Ry(pitch)·Rx(roll)`). `180 0 0` points the tool down at the table.
