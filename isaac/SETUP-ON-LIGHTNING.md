# Studio setup

Ubuntu 24.04, Tesla T4, NVIDIA driver 580, Isaac Sim 5.1, ROS 2 Jazzy. Use zsh and place this folder at `~/ur5e-moveit-isaac/isaac`.

## 1. ROS and display tools

```sh
sudo curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu noble main" | sudo tee /etc/apt/sources.list.d/ros2.list
sudo apt update
sudo apt install -y ros-jazzy-ur ros-jazzy-ros2launch python3-colcon-common-extensions xvfb ffmpeg
```

The tested studio needed this Vulkan driver registration:

```sh
sudo mkdir -p /usr/share/vulkan/icd.d
echo '{"file_format_version":"1.0.0","ICD":{"library_path":"libGLX_nvidia.so.0","api_version":"1.3.277"}}' | sudo tee /usr/share/vulkan/icd.d/nvidia_icd.json
```

## 2. Isaac Sim

```sh
curl -fL -o /tmp/isaac.zip https://download.isaacsim.omniverse.nvidia.com/isaac-sim-standalone-5.1.0-linux-x86_64.zip
unzip -q /tmp/isaac.zip -d ~/isaacsim
~/isaacsim/post_install.sh
```

## 3. Topic-based hardware plugin

```sh
mkdir -p ~/ws/src
git clone https://github.com/PickNikRobotics/topic_based_ros2_control.git ~/ws/src/topic_based_ros2_control
git -C ~/ws/src/topic_based_ros2_control checkout 6bd8d55e1c4ad3188770fe5c8b93b942bcede4a2
source /opt/ros/jazzy/setup.zsh
cd ~/ws
colcon build --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3
```

## 4. Live view tools

Install go2rtc to stream display `:1`, nginx to serve the viewer, and cloudflared to provide a public link.

```sh
sudo apt install -y nginx-light
mkdir -p ~/.local/bin
curl -fL -o ~/.local/bin/go2rtc https://github.com/AlexxIT/go2rtc/releases/download/v1.9.14/go2rtc_linux_amd64
curl -fL -o ~/.local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/download/2026.8.3/cloudflared-linux-amd64
chmod +x ~/.local/bin/go2rtc ~/.local/bin/cloudflared
```

## 5. Virtual display

Start the display used by the simulator, recording, and live view. Leave this terminal running:

```sh
Xvfb :1 -screen 0 1280x720x24
```

## 6. Live view

Run each command block in a separate studio terminal.

Start the video stream:

```sh
cd ~/ur5e-moveit-isaac/isaac/live_view
~/.local/bin/go2rtc -config live_view.yaml
```

Serve the browser viewer:

```sh
cd ~/ur5e-moveit-isaac/isaac/live_view
nginx -c "$PWD/live_view.nginx.conf" -p "$PWD" -g 'daemon off;'
```

Create the public link:

```sh
~/.local/bin/cloudflared tunnel --url http://127.0.0.1:8080 --no-autoupdate
```

Open the `https://…trycloudflare.com` address printed by cloudflared. Anyone with the link can watch; restarting the tunnel changes the address.

The viewer will show the robot once the simulator starts. Leave the display and live-view terminals running and continue with [Run in the README](README.md#run).
