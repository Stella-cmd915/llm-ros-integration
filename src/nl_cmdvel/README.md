# nl_cmdvel (ROS 2 Jazzy)

ROS 2 package: Natural Language -> ROS actions (here: /cmd_vel).

## 0) Προαπαιτούμενα
- Ubuntu (WSL2) + ROS 2 Jazzy
- TurtleBot3 packages (αν τρέχεις simulation)

## 1) Build
```bash
cd ~/llm_ros_ws
colcon build --packages-select nl_cmdvel
source install/setup.bash
```

## 2) Run node
```bash
source /opt/ros/jazzy/setup.bash
source ~/llm_ros_ws/install/setup.bash
ros2 run nl_cmdvel nl_cmdvel_node
```

## 3) Send commands (tests)
```bash
ros2 topic pub --once /nl_cmd std_msgs/msg/String "{data: 'forward'}"
ros2 topic pub --once /nl_cmd std_msgs/msg/String "{data: 'αριστερά'}"
ros2 topic pub --once /nl_cmd std_msgs/msg/String "{data: 'stop'}"
```

## 4) Verify output
```bash
ros2 topic echo /cmd_vel
```

## 5) Log to file (for Chapter 5 tables/plots)
```bash
stdbuf -oL -eL ros2 run nl_cmdvel nl_cmdvel_node 2>&1 | tee run_log.txt
```

Convert logs to CSV:
```bash
python3 src/nl_cmdvel/tools/log_to_csv.py --log run_log.txt --csv runs.csv
python3 src/nl_cmdvel/tools/metrics_summary.py --csv runs.csv --out summary.csv
```


