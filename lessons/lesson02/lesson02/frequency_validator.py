#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from collections import deque
from rclpy.time import Time


class FrequencyValidator(Node):
    def __init__(self):
        super().__init__('frequency_validator')
        
        # Subscribe to two topics
        self.subscription1 = self.create_subscription(
            Image,
            'topic_alpha',
            self.topic1_callback,
            10)
        
        self.subscription2 = self.create_subscription(
            String,
            'topic_beta',
            self.topic2_callback,
            10)
        
        # Timer to check frequencies every second
        self.timer = self.create_timer(1.0, self.check_frequencies)
        
        # Store timestamps for frequency calculation
        self.topic1_timestamps = deque()
        self.topic2_timestamps = deque()
        
        self.topic1_valid = False
        self.topic2_valid = False
        self.completion_shown = False
        
        self.get_logger().info('Frequency Validator started!')
        self.get_logger().info("Waiting for Image messages on 'topic_alpha' (2-3 Hz) and String messages on 'topic_beta' (4-6 Hz)...")
    
    def topic1_callback(self, msg):
        now = self.get_clock().now()
        self.topic1_timestamps.append(now)
        
        # Keep only last 5 seconds of data
        while self.topic1_timestamps and \
              (now - self.topic1_timestamps[0]).nanoseconds / 1e9 > 5.0:
            self.topic1_timestamps.popleft()
    
    def topic2_callback(self, msg):
        now = self.get_clock().now()
        self.topic2_timestamps.append(now)
        
        # Keep only last 5 seconds of data
        while self.topic2_timestamps and \
              (now - self.topic2_timestamps[0]).nanoseconds / 1e9 > 5.0:
            self.topic2_timestamps.popleft()
    
    def calculate_frequency(self, timestamps):
        if len(timestamps) < 2:
            return 0.0
        
        duration = (timestamps[-1] - timestamps[0]).nanoseconds / 1e9
        if duration < 0.5:
            return 0.0
        
        return (len(timestamps) - 1) / duration
    
    def check_frequencies(self):
        freq1 = self.calculate_frequency(self.topic1_timestamps)
        freq2 = self.calculate_frequency(self.topic2_timestamps)
        
        # Check if topic_alpha is publishing at 2-3 Hz
        topic1_ok = (2.0 <= freq1 <= 3.0)
        
        # Check if topic_beta is publishing at 4-6 Hz
        topic2_ok = (4.0 <= freq2 <= 6.0)
        
        # Update status
        if topic1_ok != self.topic1_valid or topic2_ok != self.topic2_valid:
            self.topic1_valid = topic1_ok
            self.topic2_valid = topic2_ok
            
            self.get_logger().info(
                f"Status - topic_alpha: {freq1:.2f} Hz [{'✓' if topic1_ok else '✗'}] | "
                f"topic_beta: {freq2:.2f} Hz [{'✓' if topic2_ok else '✗'}]")
        
        # Check for completion
        if self.topic1_valid and self.topic2_valid and not self.completion_shown:
            self.completion_shown = True
            self.get_logger().info('\n')
            self.get_logger().info('╔════════════════════════════════════════╗')
            self.get_logger().info('║     ✓ LESSON 02 COMPLETED! ✓          ║')
            self.get_logger().info('║                                        ║')
            self.get_logger().info('║  Both topics are publishing at the     ║')
            self.get_logger().info('║  correct frequencies!                  ║')
            self.get_logger().info('║                                        ║')
            self.get_logger().info(f'║  - topic_alpha: {freq1:.1f} Hz ✓               ║')
            self.get_logger().info(f'║  - topic_beta:  {freq2:.1f} Hz ✓               ║')
            self.get_logger().info('╚════════════════════════════════════════╝')
            self.get_logger().info('\n')
        elif self.completion_shown and (not self.topic1_valid or not self.topic2_valid):
            # Reset if frequencies drop out of range
            self.completion_shown = False
            self.get_logger().warn('Frequencies no longer valid. Keep publishing!')


def main(args=None):
    rclpy.init(args=args)
    node = FrequencyValidator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
