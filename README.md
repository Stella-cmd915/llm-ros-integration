# Natural Language → ROS 2 Robot Control

A ROS 2 package that turns natural-language commands (from an LLM or a user, on `/nl_cmd`) into robot motion on `/cmd_vel`, tested with TurtleBot3 in simulation.

## Tech stack
- ROS 2 Jazzy · Python (rclpy)
- TurtleBot3 simulation

## Features
- Node that parses natural-language commands (forward/back/left/right/stop, with durations) into `Twist` messages
- Configurable parameters and launch file
- Logging and metrics tools (`tools/`)

## Getting started
```bash
cd ~/ros_ws && cp -r <this repo>/src/nl_cmdvel src/
colcon build --packages-select nl_cmdvel
source install/setup.bash
ros2 launch nl_cmdvel nl_cmdvel.launch.py
```

---
Part of the **SIGMA LAB** project portfolio.
