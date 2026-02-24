#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SensorMonitor(Node):
    """
    A sensor monitoring node that requires parameters to function.
    This node publishes sensor readings at a specified rate.
    
    Required Parameters:
    - sensor_type (string): Type of sensor being monitored (e.g., "lidar", "camera")
    - update_rate (integer): How many updates per second
    """
    
    def __init__(self):
        super().__init__('sensor_monitor')
        
        # Declare parameters with no defaults - they MUST be provided
        self.declare_parameter('sensor_type', rclpy.Parameter.Type.STRING)
        self.declare_parameter('update_rate', rclpy.Parameter.Type.INTEGER)
        
        # Get parameter values
        try:
            self.sensor_type = self.get_parameter('sensor_type').value
            self.update_rate = self.get_parameter('update_rate').value
            
            # Validate parameters
            if not self.sensor_type or self.sensor_type == '':
                raise ValueError("sensor_type cannot be empty")
            
            if self.update_rate <= 0:
                raise ValueError("update_rate must be positive")
            
            self.get_logger().info(f'Sensor Monitor initialized!')
            self.get_logger().info(f'  Sensor Type: {self.sensor_type}')
            self.get_logger().info(f'  Update Rate: {self.update_rate} Hz')
            
        except Exception as e:
            self.get_logger().error(f'Failed to get parameters: {e}')
            self.get_logger().error('Make sure to pass sensor_type and update_rate parameters!')
            raise
        
        # Create a publisher for sensor data
        self.publisher = self.create_publisher(String, 'sensor_data', 10)
        
        # Create a timer based on update rate
        timer_period = 1.0 / self.update_rate
        self.timer = self.create_timer(timer_period, self.publish_sensor_data)
        self.reading_counter = 0
    
    def publish_sensor_data(self):
        """Publish sensor data"""
        msg = String()
        msg.data = f'{self.sensor_type} reading #{self.reading_counter}: OK'
        self.publisher.publish(msg)
        self.reading_counter += 1


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = SensorMonitor()
        rclpy.spin(node)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
