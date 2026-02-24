#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DataLogger(Node):
    """
    A data logging node that requires parameters to function.
    This node simulates logging data to a file.
    
    Required Parameters:
    - log_file (string): Path/name of the log file
    - buffer_size (integer): Size of the logging buffer in entries
    """
    
    def __init__(self):
        super().__init__('data_logger')
        
        # Declare parameters with no defaults - they MUST be provided
        self.declare_parameter('log_file', rclpy.Parameter.Type.STRING)
        self.declare_parameter('buffer_size', rclpy.Parameter.Type.INTEGER)
        
        # Get parameter values
        try:
            self.log_file = self.get_parameter('log_file').value
            self.buffer_size = self.get_parameter('buffer_size').value
            
            # Validate parameters
            if not self.log_file or self.log_file == '':
                raise ValueError("log_file cannot be empty")
            
            if self.buffer_size <= 0:
                raise ValueError("buffer_size must be positive")
            
            self.get_logger().info(f'Data Logger initialized!')
            self.get_logger().info(f'  Log File: {self.log_file}')
            self.get_logger().info(f'  Buffer Size: {self.buffer_size} entries')
            
        except Exception as e:
            self.get_logger().error(f'Failed to get parameters: {e}')
            self.get_logger().error('Make sure to pass log_file and buffer_size parameters!')
            raise
        
        # Create a publisher for logger status
        self.publisher = self.create_publisher(String, 'logger_status', 10)
        
        # Create a timer to publish status periodically
        self.timer = self.create_timer(2.0, self.publish_status)
        self.log_entries = 0
    
    def publish_status(self):
        """Publish logger status"""
        msg = String()
        buffer_usage = (self.log_entries % self.buffer_size)
        msg.data = f'Logging to {self.log_file} - Buffer: {buffer_usage}/{self.buffer_size}'
        self.publisher.publish(msg)
        self.log_entries += 1


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = DataLogger()
        rclpy.spin(node)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
