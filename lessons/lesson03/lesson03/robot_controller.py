#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RobotController(Node):
    """
    A robot controller node that requires parameters to function.
    This node publishes status messages about the robot it's controlling.
    
    Required Parameters:
    - robot_name (string): Name of the robot being controlled
    - max_speed (double): Maximum speed in m/s
    """
    
    def __init__(self):
        super().__init__('robot_controller')
        
        # Declare parameters with no defaults - they MUST be provided
        self.declare_parameter('robot_name', rclpy.Parameter.Type.STRING)
        self.declare_parameter('max_speed', rclpy.Parameter.Type.DOUBLE)
        
        # Get parameter values
        try:
            self.robot_name = self.get_parameter('robot_name').value
            self.max_speed = self.get_parameter('max_speed').value
            
            # Validate parameters
            if not self.robot_name or self.robot_name == '':
                raise ValueError("robot_name cannot be empty")
            
            if self.max_speed <= 0:
                raise ValueError("max_speed must be positive")
            
            self.get_logger().info(f'Robot Controller initialized!')
            self.get_logger().info(f'  Robot Name: {self.robot_name}')
            self.get_logger().info(f'  Max Speed: {self.max_speed} m/s')
            
        except Exception as e:
            self.get_logger().error(f'Failed to get parameters: {e}')
            self.get_logger().error('Make sure to pass robot_name and max_speed parameters!')
            raise
        
        # Create a publisher for robot status
        self.publisher = self.create_publisher(String, 'robot_status', 10)
        
        # Create a timer to publish status periodically
        self.timer = self.create_timer(1.0, self.publish_status)
        self.status_counter = 0
    
    def publish_status(self):
        """Publish robot status"""
        msg = String()
        msg.data = f'{self.robot_name} is operational (speed limit: {self.max_speed} m/s) - count: {self.status_counter}'
        self.publisher.publish(msg)
        self.status_counter += 1


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = RobotController()
        rclpy.spin(node)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
