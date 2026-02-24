# ROS2_workshop
A Workshop for learning the basics of ROS2 




## Installation Process

1. Install Docker
2. isntall ROS image
```bash
docker pull osrf/ros:humble-desktop
docker run -it osrf/ros:humble-desktop
```

## Running the Lesson

1. Use the helper script from the workspace root:

```bash
./run_lesson.sh lesson01
```
2. Connect VSCode to the running docker container

    -  Install the **Dev Containers** extension in VS Code (extension ID: `ms-vscode-remote.remote-containers`).
    - In VS Code, open the Command Palette with `Ctrl+Shift+P`.
    - Run: **Dev Containers: Attach to Running Container...**
    - Select `ros2_humble_dev` (or whichever container name you started).

> [!NOTE]
> you can open up the included terminal by pressing `ctrl + tilda` or additional with `ctrl + shift + tilda`
> tilda = `

VS Code will open a new window attached to the container, and your terminal/extensions will run inside that container environment.


## Testing
you can test your code by running the following script within the container, for now you do not need to know what it does, but it will check that everything is correct.


## Lessons
### [**Lesson 1**](/lessons/lesson01/): Nodes, Packages and the ROS command line
### [**Lesson 2**](/lessons/lesson02/): Topics Publishers and Subscribers
### [**Lesson 3**](/lessons/lesson03/): Parameters and Launch Files
### [**Lesson 4**](/lessons/lesson04/): RVIZ and visualising Data
### [**Lesson 5**](/lessons/lesson05/): Services and Actions
### [**Lesson 6**](/lessons/lesson06/): Custom Interfaces
### [**Lesson 7**](/lessons/lesson07/): Gazebo and Simulations
### [**Lesson 8**](/lessons/lesson08/): ROS2 Control




### Helpful Docker commands
```bash
# list running containers
docker ps

# start an existing container by name
docker start -ai ros2_humble_dev
```




## Quick Reference

### Essential Commands Cheat Sheet

```bash
# Nodes
ros2 node list                    # List running nodes
ros2 node info /node              # Node details

# Topics
ros2 topic list                   # List topics
ros2 topic echo /topic            # View messages
ros2 topic pub /topic type "data" # Publish message
ros2 topic hz /topic              # Show rate
ros2 topic info /topic            # Topic details

# Services
ros2 service list                 # List services
ros2 service call /srv type args  # Call service

# Parameters
ros2 param list                   # List all parameters
ros2 param get /node param        # Get value
ros2 param set /node param value  # Set value

# Actions
ros2 action list                  # List actions
ros2 action send_goal /act type goal  # Send goal

# Packages
ros2 pkg list                     # List packages
ros2 pkg executables pkg          # List executables

# Run & Launch
ros2 run pkg executable           # Run node
ros2 launch pkg launch_file       # Run launch file

# Recording
ros2 bag record -a                # Record all topics
ros2 bag play bagfile             # Play bag file

# Debugging
ros2 doctor                       # System check
ros2 interface show type          # Show message structure
```
