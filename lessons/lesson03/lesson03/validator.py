#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time


class Lesson03Validator(Node):
    """
    Validator node for Lesson 03.
    Checks that all three nodes are running and publishing with correct parameters.
    """
    
    def __init__(self):
        super().__init__('lesson03_validator')
        
        # Track which topics we've received messages from
        self.robot_status_received = False
        self.sensor_data_received = False
        self.logger_status_received = False
        
        # Track the last messages to verify parameters
        self.last_robot_msg = None
        self.last_sensor_msg = None
        self.last_logger_msg = None
        
        # Create subscriptions to monitor each node's output
        self.robot_sub = self.create_subscription(
            String, 'robot_status', self.robot_callback, 10)
        
        self.sensor_sub = self.create_subscription(
            String, 'sensor_data', self.sensor_callback, 10)
        
        self.logger_sub = self.create_subscription(
            String, 'logger_status', self.logger_callback, 10)
        
        # Timer to check status
        self.check_timer = self.create_timer(2.0, self.check_status)
        
        # Timer to validate after initial grace period
        self.validation_timer = self.create_timer(5.0, self.validate_lesson)
        self.validation_done = False
        
        self.get_logger().info('Lesson 03 Validator started!')
        self.get_logger().info('Waiting for all nodes to start...')
    
    def robot_callback(self, msg):
        """Callback for robot_status topic"""
        self.robot_status_received = True
        self.last_robot_msg = msg.data
    
    def sensor_callback(self, msg):
        """Callback for sensor_data topic"""
        self.sensor_data_received = True
        self.last_sensor_msg = msg.data
    
    def logger_callback(self, msg):
        """Callback for logger_status topic"""
        self.logger_status_received = True
        self.last_logger_msg = msg.data
    
    def check_status(self):
        """Periodically check which nodes are active"""
        status = []
        status.append(f"Robot Controller: {'✓' if self.robot_status_received else '✗'}")
        status.append(f"Sensor Monitor: {'✓' if self.sensor_data_received else '✗'}")
        status.append(f"Data Logger: {'✓' if self.logger_status_received else '✗'}")
        
        if not all([self.robot_status_received, self.sensor_data_received, self.logger_status_received]):
            self.get_logger().info(' | '.join(status))
    
    def validate_lesson(self):
        """Validate that all nodes are running with correct parameters"""
        if self.validation_done:
            return
        
        # Check if all nodes are running
        if not all([self.robot_status_received, self.sensor_data_received, self.logger_status_received]):
            self.get_logger().warn('Not all nodes are running yet. Keep waiting...')
            return
        
        # Validate parameters from messages
        errors = []
        
        # Check robot_controller parameters
        if self.last_robot_msg:
            if 'Atlas' not in self.last_robot_msg:
                errors.append("Robot name should be 'Atlas'")
            if '2.5' not in self.last_robot_msg:
                errors.append("Max speed should be 2.5 m/s")
        
        # Check sensor_monitor parameters
        if self.last_sensor_msg:
            if 'lidar' not in self.last_sensor_msg:
                errors.append("Sensor type should be 'lidar'")
        
        # Check data_logger parameters
        if self.last_logger_msg:
            if 'robot_data.log' not in self.last_logger_msg:
                errors.append("Log file should be 'robot_data.log'")
            if '/100' not in self.last_logger_msg:
                errors.append("Buffer size should be 100")
        
        if errors:
            self.get_logger().error('Parameter validation failed:')
            for error in errors:
                self.get_logger().error(f'  - {error}')
            self.get_logger().error('Check your params.yaml file and launch file!')
        else:
            self.print_success()
            self.validation_done = True
    
    def print_success(self):
        """Print success message"""
        self.get_logger().info('')
        self.get_logger().info('╔════════════════════════════════════════╗')
        self.get_logger().info('║     ✓ LESSON 03 COMPLETED! ✓           ║')
        self.get_logger().info('║                                        ║')
        self.get_logger().info('║  All nodes are running with correct    ║')
        self.get_logger().info('║  parameters from the YAML file!        ║')
        self.get_logger().info('║                                        ║')
        self.get_logger().info('║  ✓ Robot Controller: Atlas @ 2.5 m/s   ║')
        self.get_logger().info('║  ✓ Sensor Monitor: lidar @ 10 Hz       ║')
        self.get_logger().info('║  ✓ Data Logger: buffer = 100           ║')
        self.get_logger().info('╚════════════════════════════════════════╝')
        self.get_logger().info('')


def main(args=None):
    rclpy.init(args=args)
    node = Lesson03Validator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
