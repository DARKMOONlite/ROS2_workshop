cmake_minimum_required(VERSION 3.8)
project(lesson01)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)

# Include C++ headers
include_directories(include)

# Build C++ executable
add_executable(simple_publisher_cpp src/lesson1_node.cpp)
ament_target_dependencies(simple_publisher_cpp std_msgs)

# Install C++ executables
install(TARGETS
  simple_publisher_cpp
  DESTINATION lib/${PROJECT_NAME}
)

# Install C++ header files
install(DIRECTORY include/
  DESTINATION include
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
