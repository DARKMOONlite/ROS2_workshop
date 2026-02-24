#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image


class MyPublisher(Node):
    def __init__(self):
        super().__init__('my_publisher')
        
        # TODO: Create your publishers here

        # TODO: Create your timers here (adjust periods for desired frequencies)

        
        self.get_logger().info('Publisher node started')
    
    def timer_callback1(self):
        # TODO: Create and publish Image message to topic_alpha

        pass
    
    def timer_callback2(self):
        # TODO: Create and publish String message to topic_beta

        pass


def main(args=None):
    rclpy.init(args=args)
    node = MyPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
