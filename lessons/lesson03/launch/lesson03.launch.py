"""
Lesson 03 Launch File Template

Your task: Complete this launch file to launch all three nodes with their parameters.

The launch file should:
1. Load parameters from the 'params.yaml' file in the config directory
2. Launch robot_controller node with its parameters
3. Launch sensor_monitor node with its parameters
4. Launch data_logger node with its parameters

Hints:
- Use get_package_share_directory() to find the package directory
- Use os.path.join() to build the path to the config file
- Each Node() needs: package, executable, name, and parameters
- The parameters argument should point to the yaml file path
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    
    # TODO: Get the package directory

    
    # TODO: Build the path to params.yaml in the config directory

    
    # TODO: Launch robot_controller node

    
    # TODO: Launch sensor_monitor node
    # Hint: Similar structure to robot_controller
    
    # TODO: Launch data_logger node
    # Hint: Similar structure to robot_controller



    node_list = []
    return LaunchDescription(node_list) 



