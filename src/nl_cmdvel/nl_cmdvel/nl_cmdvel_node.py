import re
import time
from typing import Optional, Tuple

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class NLCmdVelNode(Node):
    """
    ROS 2 node that converts natural-language commands to /cmd_vel.

    Subscribes:  /nl_cmd   (std_msgs/String)
    Publishes:   /cmd_vel  (geometry_msgs/Twist)

    Default mapping (default):
      forward  -> linear.x = +0.15, angular.z = 0.00
      backward -> linear.x = -0.15, angular.z = 0.00
      left     -> linear.x =  0.00, angular.z = +0.60
      right    -> linear.x =  0.00, angular.z = -0.60
      stop     -> linear.x =  0.00, angular.z = 0.00
    """

    def __init__(self):
        super().__init__("nl_cmdvel_node")

        # Parameters (default values)
        self.declare_parameter("lin_speed", 0.15)
        self.declare_parameter("ang_speed", 0.60)
        self.declare_parameter("unknown_behavior", "stop")  # stop | ignore

        self.lin_speed = float(self.get_parameter("lin_speed").value)
        self.ang_speed = float(self.get_parameter("ang_speed").value)
        self.unknown_behavior = str(self.get_parameter("unknown_behavior").value).strip().lower()

        self.sub = self.create_subscription(String, "/nl_cmd", self.on_cmd, 10)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)

        self.get_logger().info(
            f"Started nl_cmdvel_node | lin_speed={self.lin_speed:.2f} m/s | "
            f"ang_speed={self.ang_speed:.2f} rad/s | unknown_behavior={self.unknown_behavior}"
        )

        # Inter-command interval (dt_ms) is derived from reception timestamps
        self._last_rx_ts = None

    @staticmethod
    def normalize(text: str) -> str:
        t = (text or "").strip().lower()
        t = re.sub(r"\s+", " ", t)
        return t

    def map_to_action(self, text: str) -> Optional[str]:
        """
        Map text to one of: forward | backward | left | right | stop
        Returns None if not recognized.
        Supports Greek + English and small keyword tolerance.
        """
        t = self.normalize(text)

        # English (exact phrases)
        if t in {"forward", "go forward", "ahead", "go ahead", "move forward"}:
            return "forward"
        if t in {"backward", "go backward", "back", "go back", "move backward"}:
            return "backward"
        if t in {"left", "turn left", "go left"}:
            return "left"
        if t in {"right", "turn right", "go right"}:
            return "right"
        if t in {"stop", "halt", "freeze"}:
            return "stop"

        # Greek (common variants)
        if t in {"μπροστα", "μπροστά", "πανε μπροστα", "πήγαινε μπροστά", "προχωρα", "προχώρα"}:
            return "forward"
        if t in {"πισω", "πίσω", "πανε πισω", "πήγαινε πίσω", "κανε πισω", "κάνε πίσω"}:
            return "backward"
        if t in {"αριστερα", "αριστερά", "στριψε αριστερα", "στρίψε αριστερά"}:
            return "left"
        if t in {"δεξια", "δεξιά", "στριψε δεξια", "στρίψε δεξιά"}:
            return "right"
        if t in {"στοπ", "σταματα", "σταμάτα", "σταση", "στάση"}:
            return "stop"

        # Keyword tolerance (minimal, safe)
        if "αριστερ" in t:
            return "left"
        if "δεξ" in t:
            return "right"
        if "μπρο" in t or "forward" in t or "ahead" in t:
            return "forward"
        if "πισ" in t or "back" in t:
            return "backward"
        if "stop" in t or "σταμ" in t or "στοπ" in t:
            return "stop"

        return None

    def action_to_twist(self, action: str) -> Tuple[float, float]:
        lin = 0.0
        ang = 0.0

        if action == "forward":
            lin = +self.lin_speed
        elif action == "backward":
            lin = -self.lin_speed
        elif action == "left":
            ang = +self.ang_speed
        elif action == "right":
            ang = -self.ang_speed
        elif action == "stop":
            lin = 0.0
            ang = 0.0

        return lin, ang

    def publish_twist(self, lin: float, ang: float) -> None:
        msg = Twist()
        msg.linear.x = float(lin)
        msg.angular.z = float(ang)
        self.pub.publish(msg)

    def on_cmd(self, msg: String) -> None:
        rx_ts = time.time()
        dt_ms = None
        if self._last_rx_ts is not None:
            dt_ms = (rx_ts - self._last_rx_ts) * 1000.0
        self._last_rx_ts = rx_ts

        raw = msg.data
        action = self.map_to_action(raw)

        if action is None:
            # Unknown command: stop (safe default) or ignore, per parameter
            if self.unknown_behavior == "stop":
                self.publish_twist(0.0, 0.0)
                if dt_ms is None:
                    self.get_logger().warn(f"cmd='UNKNOWN' from='{raw}' -> stop (first msg)")
                else:
                    self.get_logger().warn(f"cmd='UNKNOWN' from='{raw}' -> stop, dt_ms={dt_ms:.1f}")
            else:
                if dt_ms is None:
                    self.get_logger().warn(f"cmd='UNKNOWN' from='{raw}' -> ignored (first msg)")
                else:
                    self.get_logger().warn(f"cmd='UNKNOWN' from='{raw}' -> ignored, dt_ms={dt_ms:.1f}")
            return

        lin, ang = self.action_to_twist(action)
        self.publish_twist(lin, ang)

        # Log line is intentionally structured so it can be parsed to CSV
        if dt_ms is None:
            self.get_logger().info(f"cmd='{action}' -> lin={lin:.2f}, ang={ang:.2f} (first msg)")
        else:
            self.get_logger().info(f"cmd='{action}' -> lin={lin:.2f}, ang={ang:.2f}, dt_ms={dt_ms:.1f}")


def main():
    rclpy.init()
    node = NLCmdVelNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
