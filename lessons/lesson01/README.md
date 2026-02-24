# Lesson 01: ROS2 Nodes and Command Line Tools


## Exercises

### 1. Build This Lesson
This lesson already has its own c++ package, so using the techniques above build this package. Note that the package has 3 issues, review the `package.xml`, `.cpp` files and `CMakeLists.txt` file to determine what they are.
Successfully building the package without error completes this part. 
### 2. Run the included Node
This package has a node in it, run it and using command line tools find the hidden messages. You will need to read the node, the topics it publishes and 



## Success Criteria
Find all three sections of the numerical code



---

## Packages

In ROS2, **packages** are the fundamental unit of organization for your code. A package is a directory that contains:
- Source code (Python scripts, C++ files)
- Configuration files
- Launch files
- Message/Service/Action definitions
- Documentation
- Dependencies and metadata

### Why Use Packages?

1. **Organization**: Keep related code together in a logical structure
2. **Reusability**: Share packages across projects or with the community
3. **Dependency Management**: Explicitly declare what your code needs
4. **Build System Integration**: Automated building and installation
5. **Distribution**: Easy to distribute and install on other systems

### Package Types

ROS2 supports three main package types:

1. **ament_python** - Pure Python packages
2. **ament_cmake** - C++ packages or mixed C++/Python packages
3. **ament_cmake_python** - Python packages built with CMake (for mixed packages)

---

### Python Package Structure (ament_python)

A typical Python package structure:

```python
my_python_package/
├── package.xml              # Package metadata and dependencies
├── setup.py                 # Python install configuration
├── setup.cfg                # Setup configuration
├── resource/                # Package resource marker
│   └── my_python_package    # Empty marker file
├── my_python_package/       # Python module directory
│   └── __init__.py          # Makes it a Python module
├── scripts/                 # Optional: executable scripts
│   └── my_script.py
├── launch/                  # Optional: launch files
│   └── my_launch.launch.py
├── config/                  # Optional: configuration files
│   └── params.yaml
└── test/                    # Optional: test files
    └── test_my_node.py
```

#### Key Files for Python Packages

**package.xml** - Defines package metadata:
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_python_package</name>
  <version>0.0.1</version>
  <description>My awesome Python package</description>
  <maintainer email="user@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <exec_depend>rclpy</exec_depend>
  <exec_depend>std_msgs</exec_depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

**setup.py** - Python package installation:
```python
from setuptools import setup

package_name = 'my_python_package'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install launch files
        ('share/' + package_name + '/launch', ['launch/my_launch.launch.py']),
        # Install config files
        ('share/' + package_name + '/config', ['config/params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='user@example.com',
    description='My awesome Python package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = my_python_package.my_node:main',
            'my_script = scripts.my_script:main',
        ],
    },
)
```

**setup.cfg** - Installation directories:
```ini
[develop]
script_dir=$base/lib/my_python_package
[install]
install_scripts=$base/lib/my_python_package
```

---

### C++ Package Structure (ament_cmake)

A typical C++ package structure:

```
my_cpp_package/
├── CMakeLists.txt           # Build instructions
├── package.xml              # Package metadata
├── include/                 # Public header files
│   └── my_cpp_package/
│       └── my_class.hpp
├── src/                     # Source files
│   ├── my_node.cpp
│   └── my_class.cpp
├── launch/                  # Optional: launch files
│   └── my_launch.launch.py
├── config/                  # Optional: configuration files
│   └── params.yaml
└── test/                    # Optional: test files
    └── test_my_node.cpp
```

#### Key Files for C++ Packages

**package.xml** - Similar to Python but with C++ dependencies:
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_cpp_package</name>
  <version>0.0.1</version>
  <description>My awesome C++ package</description>
  <maintainer email="user@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>rclcpp</depend>
  <depend>std_msgs</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

**CMakeLists.txt** - Build configuration:
```cmake
cmake_minimum_required(VERSION 3.8)
project(my_cpp_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Include directories
include_directories(include)

# Create executable
add_executable(my_node src/my_node.cpp src/my_class.cpp)
ament_target_dependencies(my_node rclcpp std_msgs)

# Create library (optional)
add_library(my_library src/my_class.cpp)
ament_target_dependencies(my_library rclcpp)

# Install targets
install(TARGETS
  my_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install headers
install(DIRECTORY include/
  DESTINATION include
)

# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install config files
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
```

---

### Mixed C++/Python Package Structure

For packages with both C++ and Python code:

```
my_mixed_package/
├── CMakeLists.txt           # Must use ament_cmake
├── package.xml              # Hybrid dependencies
├── include/                 # C++ headers
│   └── my_mixed_package/
│       └── my_class.hpp
├── src/                     # C++ source
│   └── my_node.cpp
├── my_mixed_package/        # Python module
│   ├── __init__.py
│   └── my_python_node.py
├── launch/
│   └── mixed_launch.launch.py
└── config/
    └── params.yaml
```

**CMakeLists.txt** for mixed packages:
```cmake
cmake_minimum_required(VERSION 3.8)
project(my_mixed_package)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

# C++ executable
add_executable(cpp_node src/my_node.cpp)
ament_target_dependencies(cpp_node rclcpp)

# Install C++ targets
install(TARGETS cpp_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  my_mixed_package/my_python_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
```

---

### Creating a New Package

#### Create Python Package

```bash
# Navigate to your workspace src directory
cd ~/ros2_ws/src

# Create the package
ros2 pkg create --build-type ament_python my_python_pkg \
  --dependencies rclpy std_msgs

# This creates the package with basic structure and adds dependencies
```

#### Create C++ Package

```bash
# Navigate to your workspace src directory
cd ~/ros2_ws/src

# Create the package
ros2 pkg create --build-type ament_cmake my_cpp_pkg \
  --dependencies rclcpp std_msgs

# Add license (optional)
ros2 pkg create --build-type ament_cmake my_cpp_pkg \
  --dependencies rclcpp std_msgs \
  --license Apache-2.0
```

#### Create Mixed Package

```bash
# Create with ament_cmake for mixed support
ros2 pkg create --build-type ament_cmake my_mixed_pkg \
  --dependencies rclcpp rclpy std_msgs

# Then manually add Python support in CMakeLists.txt
```

---

### Understanding Dependencies

Dependencies in `package.xml` have different types:

1. **`<buildtool_depend>`** - Tools needed to build (e.g., `ament_cmake`)
2. **`<build_depend>`** - Dependencies needed during compilation
3. **`<exec_depend>`** - Dependencies needed at runtime
4. **`<depend>`** - Shorthand for both build and exec dependencies
5. **`<test_depend>`** - Dependencies only needed for testing

generally however if you're unsure which to use, just use `<depend>`

Example with different dependency types:
```xml
<!-- Build tool -->
<buildtool_depend>ament_cmake</buildtool_depend>

<!-- Used in both build and runtime -->
<depend>rclcpp</depend>
<depend>std_msgs</depend>

<!-- Only needed during build (e.g., headers) -->
<build_depend>geometry_msgs</build_depend>

<!-- Only needed at runtime -->
<exec_depend>launch_ros</exec_depend>

<!-- Testing dependencies -->
<test_depend>ament_lint_auto</test_depend>
<test_depend>ament_lint_common</test_depend>
```

---

### Building Packages

ROS2 uses **colcon** as its build tool. using it you can build all files located within the local workspace. The Workspace looks like:
```
workspace/
├── src
│   ├── Package 1
│   ├── Package 2
│   └── Package 3
```
once you build it, it will populate with other important folders `include`, `build` and `log`
#### Building Packages

```bash
# From workspace root
cd ~/ros2_ws
colcon build

# Build only one package
colcon build --packages-select my_package

# Build a package and its dependencies
colcon build --packages-up-to my_package
```

#### Build Options

```bash
# Build with symbolic links (Very useful this should be your default)
colcon build --symlink-install

# Build with specific CMAKE arguments
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release

```

---

### Using Packages

#### Sourcing the Workspace

After building, source the workspace to use your packages:

```bash
# Source the setup file (do this in every new terminal)
source ./install/setup.bash

# Optioanl: Add to .bashrc to source automatically
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

#### Running Executables from Packages

```bash
# Run a node from a package
ros2 run <package_name> <executable_name>
```

#### Finding Package Information

```bash
# List all packages
ros2 pkg list
# List executables in a package
ros2 pkg executables <package_name>
```

---

### Common Package Operations

#### Clean Build

```bash
# Remove build artifacts
rm -rf build/ install/ log/
```

#### Check Package Dependencies
```bash
# Show all dependencies of a package
rosdep check <package_name>

# Install missing dependencies
rosdep install --from-paths src --ignore-src -r -y
```

---

## Introduction to ROS2 Nodes

A **node** is a fundamental building block in ROS2. It's an executable program that performs a specific computation or task. Nodes communicate with each other using:

### Key Concepts
- **Modularity**: Each node should have a single, well-defined purpose
- **Reusability**: Nodes can be composed into different robot systems
- **Distributed**: Nodes can run on different machines
- **Language Agnostic**: Nodes can be written in C++, Python, or other supported languages

---

## Understanding Nodes

### Node Lifecycle

ROS2 nodes can have a managed lifecycle with the following states:

1. **Unconfigured** - Initial state after creation
2. **Inactive** - Configured but not running
3. **Active** - Fully operational
4. **Finalized** - Shutting down

### Node Components

A typical ROS2 node includes:
which will be covered in later lessons
```
Node
├── Publishers (send data to topics)
├── Subscribers (receive data from topics)
├── Service Servers (respond to requests)
├── Service Clients (make requests)
├── Action Servers (handle long-running goals)
├── Action Clients (send goals)
└── Parameters (configuration)
```

---

## Creating Nodes
The following are two examples of ros2 nodes in both Python and C++, 
### Python Node Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### C++ Node Example

```cpp
#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class MinimalPublisher : public rclcpp::Node
{
public:
  MinimalPublisher() : Node("minimal_publisher"), count_(0)
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    timer_ = this->create_wall_timer(
      500ms, std::bind(&MinimalPublisher::timer_callback, this));
  }

private:
  void timer_callback()
  {
    auto message = std_msgs::msg::String();
    message.data = "Hello, world! " + std::to_string(count_++);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher_->publish(message);
  }
  
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
  return 0;
}
```

---

## ROS2 Command Line Interface

The `ros2` CLI is your primary tool for interacting with ROS2 systems. All commands follow the pattern:

```bash
ros2 <verb> <subcommand> [options]
```

### Main Verbs

| Verb | Purpose |
|------|---------|
| `node` | Interact with nodes |
| `topic` | Interact with topics |
| `service` | Interact with services |
| `param` | Interact with parameters |
| `action` | Interact with actions |
| `pkg` | Interact with packages |
| `run` | Run executables from packages |
| `launch` | Run launch files |
| `interface` | Show message/service/action types |
| `doctor` | Check ROS2 setup |
| `bag` | Record/playback data |
| `daemon` | Manage ROS2 daemon |

---

## Working with Nodes

### List All Running Nodes

```bash
ros2 node list
```
### Get Node Information

```bash
ros2 node info /node_name
```

Output shows:
- Subscribers
- Publishers
- Services
- Action Servers 
- Action Clients

Example:
```bash
ros2 node info /turtlesim

# Output:
/turtlesim
  Subscribers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /turtle1/cmd_vel: geometry_msgs/msg/Twist
  Publishers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
    /turtle1/color_sensor: turtlesim/msg/Color
    /turtle1/pose: turtlesim/msg/Pose
  Service Servers:
    /clear: std_srvs/srv/Empty
    /kill: turtlesim/srv/Kill
    /reset: std_srvs/srv/Empty
    /spawn: turtlesim/srv/Spawn
    /turtle1/set_pen: turtlesim/srv/SetPen
    /turtle1/teleport_absolute: turtlesim/srv/TeleportAbsolute
    /turtle1/teleport_relative: turtlesim/srv/TeleportRelative
```

---

## Working with Topics

Topics are named buses over which nodes exchange messages using publish/subscribe.

### List All Topics

```bash
ros2 topic list
# add `-t` to show message types:
ros2 topic list -t


# Show Topic information
ros2 topic info /topic_name

# Example:
ros2 topic info /turtle1/cmd_vel

# Output:
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 1

# View messages in real-time by echoing the topic:
ros2 topic echo /topic_name

# Example:
ros2 topic echo /turtle1/pose
```



---
### Command Line Tips

1. **Tab Completion**: Use tab completion for commands, nodes, topics, etc.
2. **Use Aliases**: Create shell aliases for frequently used commands

---
## Additional Resources

- [ROS2 Documentation](https://docs.ros.org/en/humble/)
- [ROS2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS2 CLI Tools](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools.html)
- [Creating Nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries.html)

---

## Next Steps

- **Lesson 02**: Deep dive into Topics and Publishers/Subscribers
- **Lesson 03**: Services and Client/Server patterns
- **Lesson 04**: Actions for long-running tasks
- **Lesson 05**: Parameters and dynamic reconfiguration
