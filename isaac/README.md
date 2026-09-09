# UR5e in Isaac Sim

A terminal pose command moves a UR5e arm in Isaac Sim. MoveIt plans the motion; ros2_control sends joint commands to Isaac Sim and receives joint states.

## Videos


https://github.com/user-attachments/assets/dfdd6568-1701-4558-b485-67d6784170f8

https://github.com/user-attachments/assets/c900e40e-52c3-478c-bb5b-e6fe19f12252



## Setup

Complete [Studio setup](SETUP-ON-LIGHTNING.md) for installation, the virtual display, and live viewing. Its final step returns here to run the robot.

## Run

Run the following command blocks in separate studio terminals, in order. Keep each process running while starting the next.

### 1. Simulator

```sh
source /opt/ros/jazzy/setup.zsh
DISPLAY=:1 OMNI_KIT_ACCEPT_EULA=YES ~/isaacsim/python.sh ~/mowito/isaac/scripts/isaac_ur5e.py
```

Wait for `ISAAC_READY`.

### 2. Controllers and MoveIt

In a new terminal, start the controllers:

```sh
source ~/ws/install/setup.zsh
ros2 launch ~/mowito/isaac/scripts/bringup.launch.py
```

Wait for both controllers to report `Configured and activated`. In another terminal, start MoveIt:

```sh
source /opt/ros/jazzy/setup.zsh
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e launch_rviz:=false
```

Wait for `You can start planning now`.

### 3. Pose input and recording

In a new studio terminal, start the pose script. It also records display `:1` to `~/isaac_demo.mp4`; move or rename an existing recording before starting.

```sh
source /opt/ros/jazzy/setup.zsh
python3 ~/mowito/isaac/scripts/pose_cmd.py
```

Enter `x y z roll pitch yaw` in metres and degrees. Wait for each result before entering the next pose:

```text
0.30 -0.25 0.50 180 0 0
0.40 0.10 0.40 180 0 0
1.5 0 0.3 180 0 0
q
```

The third pose is outside the workspace. Enter `q` or press Ctrl+C to finish the video.
