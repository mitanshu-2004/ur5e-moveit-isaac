# Isaac Sim

Same pose code as the RViz version, plus an ffmpeg recorder. Isaac Sim replaces the mock hardware:
`topic_based_ros2_control` sends joint commands to Isaac on
`/isaac_joint_commands` and reads `/isaac_joint_states` back.

## Setup

Needs an NVIDIA GPU. Follow [SETUP-ON-LIGHTNING.md](SETUP-ON-LIGHTNING.md),
then return here. Steps 5 and 6 there start processes; start them again in each
new session.

## Run

Each block in its own terminal. Keep every process running while starting the next.

```sh
source /opt/ros/jazzy/setup.zsh
DISPLAY=:1 OMNI_KIT_ACCEPT_EULA=YES ~/isaacsim/python.sh ~/ur5e-moveit-isaac/isaac/scripts/isaac_ur5e.py
```

Wait for `ISAAC_READY`.

```sh
source ~/ws/install/setup.zsh
ros2 launch ~/ur5e-moveit-isaac/isaac/scripts/bringup.launch.py
```

Wait for both controllers to report `Configured and activated`.

```sh
source /opt/ros/jazzy/setup.zsh
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e launch_rviz:=false
```

Wait for `You can start planning now`.

```sh
source /opt/ros/jazzy/setup.zsh
python3 ~/ur5e-moveit-isaac/isaac/scripts/pose_cmd.py
```

This also records display `:1` to `~/isaac_demo.mp4`. Move an existing
recording first. Enter poses and wait for each result:

```text
0.30 -0.25 0.50 180 0 0
0.40 0.10 0.40 180 0 0
1.5 0 0.3 180 0 0
q
```

The third pose is out of reach. `q` stops the script and finishes the recording.
