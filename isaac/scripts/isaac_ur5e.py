from isaacsim import SimulationApp

# a window, so it renders on the Xvfb display ffmpeg records
sim = SimulationApp({"headless": False})

import omni.graph.core as og
import omni.timeline
from isaacsim.core.utils.extensions import enable_extension
from isaacsim.core.utils.stage import add_reference_to_stage
from isaacsim.core.utils.viewports import set_camera_view
from isaacsim.storage.native import get_assets_root_path

enable_extension("isaacsim.ros2.bridge")

# ur5e ships with Isaac. The articulation root is under the reference; /ur5e itself is not one
add_reference_to_stage(get_assets_root_path() + "/Isaac/Robots/UniversalRobots/ur5e/ur5e.usd", "/ur5e")
ROBOT = "/ur5e/root_joint"

# floor and light, without them the scene is a white void
add_reference_to_stage(get_assets_root_path() + "/Isaac/Environments/Grid/default_environment.usd", "/World")
set_camera_view(eye=[2.2, 2.2, 1.6], target=[0.0, 0.0, 0.4])

# every tick: publish joint states, read joint commands, apply them. position only
og.Controller.edit(
    {"graph_path": "/ros2_bridge", "evaluator_name": "execution"},
    {
        og.Controller.Keys.CREATE_NODES: [
            ("tick", "omni.graph.action.OnPlaybackTick"),
            ("publish", "isaacsim.ros2.bridge.ROS2PublishJointState"),
            ("subscribe", "isaacsim.ros2.bridge.ROS2SubscribeJointState"),
            ("controller", "isaacsim.core.nodes.IsaacArticulationController"),
        ],
        og.Controller.Keys.CONNECT: [
            ("tick.outputs:tick", "publish.inputs:execIn"),
            ("tick.outputs:tick", "subscribe.inputs:execIn"),
            ("tick.outputs:tick", "controller.inputs:execIn"),
            ("subscribe.outputs:jointNames", "controller.inputs:jointNames"),
            ("subscribe.outputs:positionCommand", "controller.inputs:positionCommand"),
        ],
        og.Controller.Keys.SET_VALUES: [
            ("publish.inputs:topicName", "isaac_joint_states"),
            ("subscribe.inputs:topicName", "isaac_joint_commands"),
            ("publish.inputs:targetPrim", [ROBOT]),
            ("controller.inputs:targetPrim", [ROBOT]),
        ],
    },
)

omni.timeline.get_timeline_interface().play()
print("ISAAC_READY", flush=True)
while sim.is_running():
    sim.update()
sim.close()
