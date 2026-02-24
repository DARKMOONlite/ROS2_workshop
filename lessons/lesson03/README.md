# Lesson 03: Launch Files and Parameters

## Objective

Learn how to use ROS2 launch files to start multiple nodes and pass parameters from YAML configuration files.

## What You'll Learn

- How to create and use YAML configuration files
- How to write launch files to start multiple nodes
- How to pass parameters from YAML files to nodes
- Best practices for organizing launch files and configs

---

## Background

### Launch Files

Launch files in ROS2 allow you to:
- Start multiple nodes with a single command
- Configure node parameters
- Set up complex systems with many interdependent nodes
- Organize and document your system architecture

### Parameters

Parameters allow nodes to be configured without changing code. They can:
- Be set at runtime via launch files or command line
- Be loaded from YAML configuration files
- Be changed dynamically while nodes are running
- Make nodes reusable in different contexts

---

## The Challenge

You have three nodes that need specific parameters to function:

### 1. Robot Controller
**Required Parameters:**
- `robot_name` (string): Name of the robot
- `max_speed` (double): Maximum speed in m/s

**Expected Values:**
- robot_name: "Atlas"
- max_speed: 2.5

### 2. Sensor Monitor
**Required Parameters:**
- `sensor_type` (string): Type of sensor
- `update_rate` (integer): Updates per second

**Expected Values:**
- sensor_type: "lidar"
- update_rate: 10

### 3. Data Logger
**Required Parameters:**
- `log_file` (string): Path to log file
- `buffer_size` (integer): Buffer size in entries

**Expected Values:**
- log_file: "/tmp/robot_data.log"
- buffer_size: 100

---

## Your Task

Complete the launch file template (`lesson03_template.launch.py`) to:

1. **Load the YAML configuration file** (`config/params.yaml`)
   - Use `get_package_share_directory()` to find the package
   - Build the path to the config file using `os.path.join()`

2. **Launch all three nodes** with their parameters
   - robot_controller
   - sensor_monitor
   - data_logger

3. **Test your launch file** by running it and checking the validator

---

## Success Criteria

When your launch file is correct, the validator will show:

```
╔════════════════════════════════════════╗
║     ✓ LESSON 03 COMPLETED! ✓           ║
║                                        ║
║  All nodes are running with correct    ║
║  parameters from the YAML file!        ║
║                                        ║
║  ✓ Robot Controller: Atlas @ 2.5 m/s   ║
║  ✓ Sensor Monitor: lidar @ 10 Hz       ║
║  ✓ Data Logger: buffer = 100           ║
╚════════════════════════════════════════╝
```

---

## Understanding Launch Files

### Basic Components

**1. Imports**
```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
```

**2. Main Function**
```python
def generate_launch_description():
    # Must return a LaunchDescription object
    return LaunchDescription([...])
```

**3. Node Actions**
```python
Node(
    package='package_name',    # ROS2 package name
    executable='script.py',     # Script name (must be executable)
    name='node_name',           # Node instance name
    parameters=[config_file]    # Parameters to pass
)
```

### Finding Package Resources

Use `get_package_share_directory()` to find installed package files:

```python
pkg_dir = get_package_share_directory('lesson03')
# Returns: /workshop/install/lesson03/share/lesson03

config_file = os.path.join(pkg_dir, 'config', 'params.yaml')
# Returns: /workshop/install/lesson03/share/lesson03/config/params.yaml
```

### Parameter Passing Options

**From YAML file:**
```python
Node(
    package='lesson03',
    executable='node.py',
    name='my_node',
    parameters=['/path/to/params.yaml']
)
```

**Inline parameters:**
```python
Node(
    package='lesson03',
    executable='node.py',
    name='my_node',
    parameters=[{
        'param1': 'value1',
        'param2': 42
    }]
)
```

**Mix of both:**
```python
Node(
    package='lesson03',
    executable='node.py',
    name='my_node',
    parameters=[
        config_file,
        {'override_param': 'new_value'}
    ]
)
```

---

## Understanding Parameters in Nodes

### Python: Declaring and Using Parameters

```python
class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        
        # Declare parameter (with optional default)
        self.declare_parameter('my_param', 'default_value')
        
        # Get parameter value
        value = self.get_parameter('my_param').value
        
        # Use the parameter
        self.get_logger().info(f'Parameter value: {value}')
```

### Parameter Types

```python
# String parameter
self.declare_parameter('name', rclpy.Parameter.Type.STRING)

# Integer parameter
self.declare_parameter('count', rclpy.Parameter.Type.INTEGER)

# Double (float) parameter
self.declare_parameter('speed', rclpy.Parameter.Type.DOUBLE)

# Boolean parameter
self.declare_parameter('enabled', rclpy.Parameter.Type.BOOL)
```

### YAML File Structure

```yaml
# Node name must match the name in the launch file
node_name:
  ros__parameters:
    param1: "string value"
    param2: 42
    param3: 3.14
    param4: true
```

**Important:**
- Node name in YAML must match the `name` field in the launch file
- `ros__parameters` is mandatory syntax (with two underscores)
- Indentation matters in YAML files

---

## Common Launch File Patterns

### Multiple Nodes with Same Config

```python
    node1 = Node(package='pkg', executable='node1.py', name='node1', parameters=[config_file])
    node2 = Node(package='pkg', executable='node2.py', name='node2', parameters=[config_file])
    node3 = Node(package='pkg', executable='node3.py', name='node3', parameters=[config_file])
return LaunchDescription([node1,node2,node3])

```
### Remapping Topics

```python
Node(
    package='pkg',
    executable='node.py',
    name='node',
    remappings=[
        ('old_topic', 'new_topic'),
        ('input', 'camera/image')
    ]
)
```

---

## Debugging Tips

### Check Node Parameters

```bash
# See all parameters for a node
ros2 param list /robot_controller

# Get a specific parameter value
ros2 param get /robot_controller robot_name
```
### Common Errors

**Error: "Parameter not declared"**
- The YAML node name doesn't match the node name in launch file
- Check spelling and capitalization

**Error: "No such file or directory: params.yaml"**
- Path to config file is wrong
- Make sure `config/` directory is installed (check CMakeLists.txt)

**Error: "Node not found"**
- Python script not installed properly
- Check `install/lib/lesson03/` for your scripts

---

## Advanced: Installing Launch Files

To make launch files available to `ros2 launch`, you need to install them install the install folder, to do so add to `CMakeLists.txt`:

```cmake
# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# Install config files
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)
```

---

## Including Other Launch Files

As your ROS2 system grows, you may want to organize it into multiple launch files and compose them together. ROS2 provides the `IncludeLaunchDescription` action to include one launch file within another.

### Why Include Launch Files?

- **Modularity**: Break complex systems into manageable pieces
- **Reusability**: Use the same launch file in different contexts
- **Organization**: Group related nodes together
- **Flexibility**: Mix and match components for different configurations

### Basic Example


### Including Launch Files from Other Packages

```python
# Include a launch file from a different package
from ament_index_python.packages import get_package_share_directory

other_pkg_dir = get_package_share_directory('other_package')
other_launch = os.path.join(other_pkg_dir, 'launch', 'sensors.launch.py')

return LaunchDescription([
    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(other_launch)
    ),
])
```

### Passing Parameters into launch files

**child_launch.py (accepts arguments):**
```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Declare an argument
        DeclareLaunchArgument(
            'robot_name',
            default_value='robot1',
            description='Name of the robot'
        ),
        
        # Use the argument
        Node(
            package='my_package',
            executable='robot_node.py',
            name='robot',
            parameters=[{
                'robot_name': LaunchConfiguration('robot_name')
            }]
        ),
    ])
```

**parent_launch.py (passes arguments):**
```python
return LaunchDescription([
    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(child_launch),
        launch_arguments={
            'robot_name': 'atlas'
        }.items()
    ),
])
```


