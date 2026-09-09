import os

from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

HERE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")

# value_type=str, or launch tries to parse the URDF xml as yaml
urdf = {"robot_description": ParameterValue(Command(["xacro ", os.path.join(HERE, "ur5e_isaac.urdf.xacro")]), value_type=str)}


def generate_launch_description():
    return LaunchDescription([
        Node(package="robot_state_publisher", executable="robot_state_publisher", parameters=[urdf]),
        Node(package="controller_manager", executable="ros2_control_node", parameters=[os.path.join(HERE, "controllers.yaml")]),
        Node(package="controller_manager", executable="spawner", arguments=["joint_state_broadcaster", "scaled_joint_trajectory_controller"]),
    ])
