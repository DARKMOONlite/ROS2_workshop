# Lesson 02: Topic Publishing and Frequency Validation

## Objective

Learn how to publish messages to ROS2 topics at specific frequencies. You'll need to create publishers that send messages to two different topics at the correct rates.

## Challenge

Create ROS2 publishers that publish to the following topics at the specified frequencies:

- **topic_alpha**: Publish at 2-3 Hz (2-3 messages per second) - Uses `sensor_msgs/msg/Image`
- **topic_beta**: Publish at 4-6 Hz (4-6 messages per second) - Uses `std_msgs/msg/String`

## Validator Node

A frequency validator node is provided that will:
- Subscribe to both topics
- Calculate the publishing frequency
- Display status updates showing if frequencies are correct
- Print a completion message when both topics are publishing at the correct rates

### Running the Validator

```bash
ros2 run lesson02 frequency_validator.py
```

**Note:** The validator expects `sensor_msgs/msg/Image` on `topic_alpha` and `std_msgs/msg/String` on `topic_beta`.


## Template Files

Blank template nodes are provided to help you get started:

### C++ Template
- **File**: `src/my_publisher.cpp`
- Edit this file to create your publisher  

### Python Template
- **File**: `lesson02/my_publisher.py`
- Edit this file to create your publisher




## Success Criteria

When both publishers are running with correct frequencies, you'll see:

```
╔════════════════════════════════════════╗
║     ✓ LESSON 02 COMPLETED! ✓           ║
║                                        ║
║  Both topics are publishing at the     ║
║  correct frequencies!                  ║
║                                        ║
║  - topic_alpha: 2.5 Hz ✓               ║
║  - topic_beta:  5.0 Hz ✓               ║
╚════════════════════════════════════════╝
```

---

## Publishers, Subscribers, and Timers

### Publishers

Publishers send messages to topics. Multiple nodes can publish to the same topic, and multiple nodes can subscribe to it.

**Python:**
```python
# Create a publisher
self.publisher = self.create_publisher(MessageType, 'topic_name', queue_size)

# Publish a message
msg = MessageType()
self.publisher.publish(msg)
```

**C++:**
```cpp
// Create a publisher
publisher_ = this->create_publisher<MessageType>("topic_name", queue_size);

// Publish a message
auto msg = MessageType();
publisher_->publish(msg);
```

**Key Points:**
- `MessageType`: The type of message (e.g., `String`,`Integer`, `Image`)
- `topic_name`: Name of the topic (use descriptive names)
- `queue_size`: Number of messages to buffer (typically 10)

---

### Subscribers

Subscribers receive messages from topics and execute a callback function when messages arrive.

**Python:**
```python
# Create a subscriber
self.subscription = self.create_subscription(
    MessageType,
    'topic_name',
    self.callback_function,
    queue_size)

# Callback function
def callback_function(self, msg):
    # Process the incoming message
    self.get_logger().info(f'Received: {msg.data}')
```

**C++:**
```cpp
// Create a subscriber
subscription_ = this->create_subscription<MessageType>(
    "topic_name", 
    queue_size,
    std::bind(&ClassName::callback_function, this, std::placeholders::_1));

// Callback function
void callback_function(const MessageType::SharedPtr msg)
{
    RCLCPP_INFO(this->get_logger(), "Received: %s", msg->data.c_str());
}
```

**Key Points:**
- Callbacks execute automatically when messages arrive
- Keep callbacks short and fast to avoid blocking
- Store the subscription object to prevent it from being destroyed

---

### Timers

Timers execute callback functions at regular intervals, perfect for publishing at specific frequencies.

**Python:**
```python
# Create a timer (period in seconds)
self.timer = self.create_timer(period_in_seconds, self.timer_callback)

# Timer callback
def timer_callback(self):
    # This runs at the specified rate
    self.get_logger().info('Timer triggered!')
```

**C++:**
```cpp
// Create a timer
using namespace std::chrono_literals;
timer_ = this->create_wall_timer(
    500ms,  // period (milliseconds, seconds, etc.)
    std::bind(&ClassName::timer_callback, this));

// Timer callback
void timer_callback()
{
    RCLCPP_INFO(this->get_logger(), "Timer triggered!");
}
```

**Frequency Examples:**
- **1 Hz**: `create_timer(1.0, ...)` or `create_wall_timer(1s, ...)`
- **2 Hz**: `create_timer(0.5, ...)` or `create_wall_timer(500ms, ...)`
- **10 Hz**: `create_timer(0.1, ...)` or `create_wall_timer(100ms, ...)`

**Key Points:**
- Period = 1 / Frequency (e.g., 5 Hz = 0.2 seconds period)
- Timers run in a separate thread, don't block other operations
- Use timers for regular publishing or periodic checks

---

### Combining Publishers and Timers

This is the most common pattern for periodic publishing:

**Python:**
```python
class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        # Create publisher
        self.publisher = self.create_publisher(String, 'my_topic', 10)
        # Create timer for 5 Hz publishing
        self.timer = self.create_timer(0.2, self.publish_message)
    
    def publish_message(self):
        msg = String()
        msg.data = 'Hello at 5 Hz'
        self.publisher.publish(msg)
```

**C++:**
```cpp
class MyNode : public rclcpp::Node
{
public:
  MyNode() : Node("my_node")
  {
    // Create publisher
    publisher_ = this->create_publisher<std_msgs::msg::String>("my_topic", 10);
    // Create timer for 5 Hz publishing
    timer_ = this->create_wall_timer(
      200ms, std::bind(&MyNode::publish_message, this));
  }

private:
  void publish_message()
  {
    auto msg = std_msgs::msg::String();
    msg.data = "Hello at 5 Hz";
    publisher_->publish(msg);
  }
  
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};
```

---

### Common Patterns

**One Node, Multiple Publishers:**
```python
class MultiPublisher(Node):
    def __init__(self):
        super().__init__('multi_publisher')
        
        # Different publishers for different topics
        self.pub1 = self.create_publisher(Image, 'topic_alpha', 10)
        self.pub2 = self.create_publisher(String, 'topic_beta', 10)
        
        # Different timers for different rates
        self.timer1 = self.create_timer(0.4, self.callback1)  # 2.5 Hz
        self.timer2 = self.create_timer(0.2, self.callback2)  # 5 Hz
```

**Publisher and Subscriber in Same Node:**
```python
class ProcessNode(Node):
    def __init__(self):
        super().__init__('process_node')
        
        # Subscribe to input
        self.subscription = self.create_subscription(
            String, 'input_topic', self.process_callback, 10)
        
        # Publish to output
        self.publisher = self.create_publisher(String, 'output_topic', 10)
    
    def process_callback(self, msg):
        # Process incoming message
        output_msg = String()
        output_msg.data = msg.data.upper()  # Example: convert to uppercase
        self.publisher.publish(output_msg)
```

---

### Debugging Tips

**Check topic rates:**
```bash
ros2 topic hz /topic_name
```

**View messages:**
```bash
ros2 topic echo /topic_name
```

**List all active topics:**
```bash
ros2 topic list
```

**See topic details:**
```bash
ros2 topic info /topic_name
```
