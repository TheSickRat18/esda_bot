

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys, tty, termios, select

# Movement commands
CMD_FORWARD  = "m 100 100\n"
CMD_BACKWARD = "m -100 -100\n"
CMD_LEFT     = "m -100 100\n"
CMD_RIGHT    = "m 100 -100\n"
CMD_STOP     = "m 0 0\n"

def get_key():
    """Non-blocking key read from terminal."""
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
    key = sys.stdin.read(1) if rlist else ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class TeleopPublisher(Node):
    def __init__(self):
        super().__init__('teleop_pc_node')
        self.pub = self.create_publisher(String, 'motor_cmd', 10)
        # Timer to poll the keyboard every 50 ms
        self.create_timer(0.05, self.timer_callback)
        self.get_logger().info("Teleop node started. Use w/a/s/d to move, space to stop, CTRL-C to quit.")

    def timer_callback(self):
        key = get_key()
        msg = String()
        if key == 'w':
            msg.data = CMD_FORWARD
        elif key == 's':
            msg.data = CMD_BACKWARD
        elif key == 'a':
            msg.data = CMD_LEFT
        elif key == 'd':
            msg.data = CMD_RIGHT
        elif key == ' ':
            msg.data = CMD_STOP
        elif key == '\x03':  # CTRL-C
            msg.data = CMD_STOP
            self.pub.publish(msg)
            self.get_logger().info("Stopping robot and shutting down teleop...")
            rclpy.shutdown()
            return
        else:
            return  # No key pressed, do nothing

        self.pub.publish(msg)
        self.get_logger().info(f"Published command: '{msg.data.strip()}'")

def main(args=None):
    global settings
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = TeleopPublisher()
    try:
        rclpy.spin(node)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
