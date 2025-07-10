import math

class RobotArm2D:
    def __init__(self, shoulder_motor, armpit_motor, l1, l2):
        """
        A 2-link arm using inverted coordinates:
        (0,0) is top-right, positive x goes left, positive y goes down.
        """
        self.shoulder = shoulder_motor
        self.armpit = armpit_motor
        self.l1 = l1
        self.l2 = l2

    def angle_to_pulse(self, angle_deg, reverse=False):
        """Convert angle (0–180°) to servo pulse (500–2500)."""
        pulse = 500 + (angle_deg / 180.0) * 2000
        return int(3000 - pulse) if reverse else int(pulse)

    def move_to(self, user_x, user_y):
        """
        Moves the end effector to a position in inverse quadrant
        where x increases leftward and y increases downward from the shoulder.
        """
        if user_x < 0 or user_y < 0:
            raise ValueError("Inputs must be positive in inverse coordinate space")

        x = -user_x
        y = -user_y

        r_squared = x**2 + y**2
        r = math.sqrt(r_squared)

        # Check reachability
        if r > self.l1 + self.l2 or r < abs(self.l1 - self.l2):
            raise ValueError("Target out of reach")

        # Inverse kinematics
        cos_theta2 = (r_squared - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)
        theta2 = math.acos(cos_theta2)

        k1 = self.l1 + self.l2 * math.cos(theta2)
        k2 = self.l2 * math.sin(theta2)
        theta1 = math.atan2(y, x) - math.atan2(k2, k1)

        # Convert to degrees
        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)

        # Map to servo pulses
        pulse1 = self.angle_to_pulse(theta1_deg, reverse=True)   # shoulder reversed
        pulse2 = self.angle_to_pulse(theta2_deg, reverse=False)  # armpit normal

        # Send to motors
        self.shoulder.move(pulse1)
        self.armpit.move(pulse2)

        print(f"Moved to (user coords): x={user_x}, y={user_y}")