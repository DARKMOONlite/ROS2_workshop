cmake_minimum_required(VERSION 3.8)
project(lesson02)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# Include C++ headers
include_directories(include)

# Build C++ executable
add_executable(my_publisher src/my_publisher.cpp)
ament_target_dependencies(my_publisher rclcpp std_msgs sensor_msgs)

# Install C++ executables
install(TARGETS
  my_publisher
  DESTINATION lib/${PROJECT_NAME}
)

# Install C++ header files
install(DIRECTORY include/
  DESTINATION include
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python scripts
install(PROGRAMS
  lesson02/frequency_validator.py
  lesson02/my_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
