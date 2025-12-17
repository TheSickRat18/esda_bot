

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
import serial
import time
import math

class SerialMotorBridge(Node):
    def __init__(self):
        super().__init__('serial_motor_bridge')

        # Parameters
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud', 115200)
        self.declare_parameter('timeout', 0.01)

        port = self.get_parameter('port').value
        baud = self.get_parameter('baud').value
        timeout = self.get_parameter('timeout').value

        # Serial connection
        try:
            self.ser = serial.Serial(port, baud, timeout=timeout)
            time.sleep(2.0)  # Arduino reset delay
            self.get_logger().info(f"Connected to {port} @ {baud}")
        except serial.SerialException as e:
            self.get_logger().fatal(f"Serial connection failed: {e}")
            raise SystemExit

        # Wheel odometry
        self.d_l = 0.0
        self.d_r = 0.0
        self.wheel_radius = 0.0315  # meters
        self.time_interval = 0.1     # seconds per odom update

        # Publisher (wheel odometry)
        self.odom_pub = self.create_publisher(String, 'wheel_odom', 10)
        self.create_timer(self.time_interval, self.read_serial_data)

        # Subscriber (motor commands)
        self.motor_sub = self.create_subscription(
            String, 'motor_cmd', self.motor_cmd_callback, 10
        )

        # Watchdog timer (stop motors if no command for >1s)
        self.last_cmd_time = self.get_clock().now()
        self.create_timer(0.5, self.watchdog)

    def motor_cmd_callback(self, msg: String):
        """Receive motor commands from ROS2 and send to Arduino."""
        cmd = msg.data.strip()
        if not cmd.endswith('\n'):
            cmd += '\n'
        try:
            self.ser.write(cmd.encode('ascii'))
            self.get_logger().info(f"Sent command: '{cmd.strip()}'")
            self.last_cmd_time = self.get_clock().now()
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write failed: {e}")

    def read_serial_data(self):
        """Read wheel encoder data from Arduino and publish it."""
        try:
            while self.ser.in_waiting > 0:
                line = self.ser.readline().decode().strip()
                if not line:
                    continue

                parts = line.split(' ')
                if len(parts) >= 2:
                    try:
                        wl, wr = float(parts[0]), float(parts[1])
                        # Convert RPM to distance traveled
                        self.d_l += (wl / 60.0) * (2 * math.pi * self.wheel_radius) * self.time_interval
                        self.d_r += (wr / 60.0) * (2 * math.pi * self.wheel_radius) * self.time_interval

                        msg = String()
                        msg.data = f"{self.d_l:.4f} {self.d_r:.4f}"
                        self.odom_pub.publish(msg)
                        self.get_logger().debug(f"Wheel odom: {msg.data}")
                    except ValueError:
                        self.get_logger().warn(f"Invalid encoder values: {parts}")
                else:
                    self.get_logger().warn(f"Invalid serial line: '{line}'")
        except serial.SerialException as e:
            self.get_logger().error(f"Serial read failed: {e}")

    def watchdog(self):
        """Stop motors if no command received recently."""
        elapsed = (self.get_clock().now() - self.last_cmd_time).nanoseconds / 1e9
        if elapsed > 1.0:
            try:
                self.ser.write(b"m 0 0\n")
            except serial.SerialException:
                pass

def main(args=None):
    rclpy.init(args=args)
    node = SerialMotorBridge()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

