import serial
import time

class MotorDriver:
    def __init__(self, motor_id, serial_port=None, port='/dev/ttyS0'):
        """
        Initializes the MotorDriver for a specific servo channel (motor ID).

        :param motor_id: Servo ID (1-16)
        :param serial_port: An existing serial.Serial object (optional)
        :param port: Serial port to connect to if serial_port not provided
        """
        if not (1 <= motor_id <= 16):
            raise ValueError("Motor ID must be between 1 and 16")

        self.motor_id = motor_id

        # Use shared serial port if passed, otherwise open new one
        if serial_port is not None:
            self.ser = serial_port
        else:
            self.ser = serial.Serial(port, baudrate=115200, timeout=1)
            time.sleep(2)  # Wait for serial connection to initialize

    def move(self, position, speed=1000, delay=800):
        """
        Sends a command to move this motor to a given position.

        :param position: Target servo position (500–2500)
        :param speed: Speed of motion (100–9999)
        :param delay: Delay after command (100–9999)
        """
        # Validate input
        if not (500 <= position <= 2500):
            raise ValueError("Position must be between 500 and 2500")
        if not (100 <= speed <= 9999):
            raise ValueError("Speed must be between 100 and 9999")
        if not (100 <= delay <= 9999):
            raise ValueError("Delay must be between 100 and 9999")

        # Format and send command
        command = f"#{self.motor_id}P{position}T{speed}D{delay}\r\n"
        self.ser.write(command.encode('utf-8'))
        print(f"[Motor {self.motor_id}] Sent: {command.strip()}")

    def close(self):
        """Close the serial connection if it was created here."""
        if self.ser and self.ser.is_open:
            self.ser.close()




