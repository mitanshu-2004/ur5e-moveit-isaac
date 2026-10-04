# RViz with mock hardware

```bash
sudo apt install ros-jazzy-ur ros-jazzy-moveit
```

Three terminals, each after `source /opt/ros/jazzy/setup.bash`:

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

Position is in metres in `base_link`, angles in degrees. `180 0 0` points the tool down.

The script sends the pose to MoveIt as one `MoveGroup` goal. MoveIt plans the
motion and sends it to the UR driver, and RViz shows the result.
