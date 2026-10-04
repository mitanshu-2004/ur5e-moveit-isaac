#!/usr/bin/env python3
import math
from pathlib import Path
import subprocess
import threading

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from geometry_msgs.msg import Pose
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, MoveItErrorCodes
from moveit_msgs.msg import OrientationConstraint, PositionConstraint
from shape_msgs.msg import SolidPrimitive

GROUP = "ur_manipulator"
BASE = "base_link"
TIP = "tool0"

ERRORS = {-1: "PLANNING_FAILED", -2: "INVALID_MOTION_PLAN", -4: "CONTROL_FAILED", -6: "TIMED_OUT",
          -10: "START_STATE_IN_COLLISION", -12: "GOAL_IN_COLLISION", -27: "GOAL_STATE_INVALID", -31: "NO_IK_SOLUTION"}


# degrees, XYZ, to quaternion xyzw
def rpy_to_quat(roll, pitch, yaw):
    r, p, y = (math.radians(a) / 2 for a in (roll, pitch, yaw))
    cr, sr = math.cos(r), math.sin(r)
    cp, sp = math.cos(p), math.sin(p)
    cy, sy = math.cos(y), math.sin(y)
    return (sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy)


def build_goal(pose):
    goal = MoveGroup.Goal()
    goal.request.group_name = GROUP
    goal.request.allowed_planning_time = 15.0
    # slow enough to watch. both, or the arm snaps to cruise speed instead of easing into it
    goal.request.max_velocity_scaling_factor = 0.1
    goal.request.max_acceleration_scaling_factor = 0.1

    # where the tool must land, 5 mm radius sphere
    region = SolidPrimitive()
    region.type = SolidPrimitive.SPHERE
    region.dimensions = [0.005]
    position = PositionConstraint()
    position.header.frame_id = BASE
    position.link_name = TIP
    position.constraint_region.primitives.append(region)
    position.constraint_region.primitive_poses.append(pose)
    position.weight = 1.0

    # how it must be aimed, 0.05 rad per axis
    orientation = OrientationConstraint()
    orientation.header.frame_id = BASE
    orientation.link_name = TIP
    orientation.orientation = pose.orientation
    orientation.absolute_x_axis_tolerance = 0.05
    orientation.absolute_y_axis_tolerance = 0.05
    orientation.absolute_z_axis_tolerance = 0.05
    orientation.weight = 1.0

    constraints = Constraints()
    constraints.position_constraints.append(position)
    constraints.orientation_constraints.append(orientation)
    goal.request.goal_constraints.append(constraints)
    return goal


def main():
    rclpy.init()
    node = Node("pose_cmd")
    client = ActionClient(node, MoveGroup, "/move_action")

    # input() blocks the main thread, callbacks need their own
    threading.Thread(target=rclpy.spin, args=(node,), daemon=True).start()

    if not client.wait_for_server(timeout_sec=15.0):
        print("no /move_action, is move_group up?")
        return

    print("x y z roll pitch yaw   (m, deg)   q to quit")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if line == "q":
            break

        try:
            x, y, z, roll, pitch, yaw = (float(v) for v in line.split())
        except ValueError:
            print("need six numbers")
            continue

        pose = Pose()
        pose.position.x, pose.position.y, pose.position.z = x, y, z
        (pose.orientation.x, pose.orientation.y,
         pose.orientation.z, pose.orientation.w) = rpy_to_quat(roll, pitch, yaw)

        code = client.send_goal(build_goal(pose)).result.error_code.val
        print("done" if code == MoveItErrorCodes.SUCCESS
              else f"failed: {ERRORS.get(code, code)}")


def record_and_run():
    output = Path.home() / "isaac_demo.mp4"
    if output.exists():
        raise SystemExit(f"Move or rename {output} before starting a new recording.")
    recorder = subprocess.Popen([
        "ffmpeg", "-n", "-hide_banner", "-loglevel", "error",
        "-f", "x11grab", "-video_size", "1280x720", "-framerate", "20", "-i", ":1",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
    ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, start_new_session=True)
    try:
        print(f"Recording to {output}", flush=True)
        main()
    finally:
        # Ask ffmpeg to finish the MP4 before the pose client exits.
        try:
            recorder.communicate("q\n", timeout=30)
        except subprocess.TimeoutExpired:
            recorder.kill()
            recorder.wait()
            raise RuntimeError(f"Recording did not finish cleanly: {output}")
        if recorder.returncode != 0:
            raise RuntimeError(f"Recording failed; check ffmpeg's error above: {output}")


if __name__ == "__main__":
    try:
        record_and_run()
    except KeyboardInterrupt:
        pass
