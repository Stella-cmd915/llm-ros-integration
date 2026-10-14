from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="nl_cmdvel",
            executable="nl_cmdvel_node",
            name="nl_cmdvel_node",
            output="screen",
            parameters=[
                {"lin_speed": 0.15},
                {"ang_speed": 0.60},
                {"unknown_behavior": "stop"},
            ],
        )
    ])
