#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "sensor_msgs/msg/image.hpp"

using namespace std::chrono_literals;

class MyPublisher : public rclcpp::Node
{
public:
  MyPublisher() : Node("my_publisher")
  {
    // TODO: Create your publishers here

    // TODO: Create your timers here (adjust periods for desired frequencies)

    
    RCLCPP_INFO(this->get_logger(), "Publisher node started");
  }

private:
  void timer_callback1()
  {
    // TODO: Create and publish Image message to topic_alpha

  }
  
  void timer_callback2()
  {
    // TODO: Create and publish String message to topic_beta

  }
  
  rclcpp::TimerBase::SharedPtr timer1_;
  rclcpp::TimerBase::SharedPtr timer2_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_alpha_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_beta_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MyPublisher>());
  rclcpp::shutdown();
  return 0;
}
