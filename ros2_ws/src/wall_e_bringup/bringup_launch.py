from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="wall_e_audio",
                executable="tts",
                name="tts_node",
                output="screen",
            ),
            Node(
                package="wall_e_content",
                executable="content",
                name="content_node",
                output="screen",
            ),
        ]
    )
