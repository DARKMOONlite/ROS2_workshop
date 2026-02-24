#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class SimplePublisher : public rclcpp::Node
{
public:
  SimplePublisher() : Node("simple_publisher secret_code 1/3: " + std::to_string(0x1D ^ 0x5C))
  {
    // Create a publisher for String messages on the "chatter" topic
    publisher_ = this->create_publisher<std_msgs::msg::String>("Secret Code 2/3: " + std::to_string(code_3), 10);
    
    // Create a timer that triggers every 1 second
    timer_ = this->create_wall_timer(
      1s, std::bind(&SimplePublisher::timer_callback, this));
    
    RCLCPP_INFO(this->get_logger(), "Simple Publisher Node has been started.");
  }

private:
  void timer_callback()
  {
    // Create and populate the message
    auto message = std_msgs::msg::String();
    message.data = "Secret Code 3/3: " + std::to_string(code_1);
    
    publisher_->publish(message);
    

  }
  
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;   
  int code_1 = 0x2A ^ 0x10B; //
  int code_3 = 0x34 ^ 0001; //
}; 

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<SimplePublisher>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
