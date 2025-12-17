
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import serial
import os
import sys
import termios
import tty
import select
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200  

#Movement commands
CMD_FORWARD  = "m 100 100\n"
CMD_BACKWARD = "m -100 -100\n"
CMD_LEFT     = "m -100 100\n"
CMD_RIGHT    = "m 100 -100\n"
CMD_STOP     = "m 0 0\n"

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1) if rlist else ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_serial_node')

        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)
            time.sleep(2.0)
            self.get_logger().info(f"Connected to {SERIAL_PORT} @ {BAUD_RATE}")
        except serial.SerialException as e:
            self.get_logger().fatal(f"Failed to open serial: {e}")
            raise SystemExit

    def send_command(self, cmd: str):
        try:
            self.ser.write(cmd.encode('ascii'))
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write failed: {e}")

    def run(self, settings):
        print("Control robot: w/a/s/d for movement, space to stop, CTRL-C to quit.")
        try:
            while True:
                key = get_key(settings)
                if key == 'w':
                    self.send_command(CMD_FORWARD)
                elif key == 's':
                    self.send_command(CMD_BACKWARD)
                elif key == 'a':
                    self.send_command(CMD_LEFT)
                elif key == 'd':
                    self.send_command(CMD_RIGHT)
                elif key == ' ':
                    self.send_command(CMD_STOP)
                elif key == '\x03':  
                    self.send_command(CMD_STOP)
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.send_command(CMD_STOP)

def main(args=None):
    settings = termios.tcgetattr(sys.stdin)  
    rclpy.init(args=args)
    node = TeleopNode()
    try:
        node.run(settings)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

