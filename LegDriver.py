import math
#from MotorDriver import MotorDriver
from matplotlib import pyplot as plt

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

    def angle_to_pulse(angle_deg):
        """
        Maps an angle in degrees (-90 to 90) to a PWM signal in microseconds (500 to 2500).
        """
        # Clamp angle just in case
        angle_deg = max(-90, min(90, angle_deg))

        # Map from [-90, 90] to [500, 2500]
        pwm = 500 + ((angle_deg + 90) / 180) * 2000
        return int(pwm)

    def move_to(self, x, y):
        """
        Moves the end effector to a position in inverse quadrant
        where x increases leftward and y increases downward from the shoulder.
        """

        r_squared = x ** 2 + y ** 2
        r = math.sqrt(r_squared)

        cos_alpha = (r_squared - self.l1 ** 2 - self.l2 ** 2) / (- 2 * self.l1 * self.l2)

        alpha_rad = math.acos(cos_alpha)

        sin_beta = (self.l2 * math.sin(alpha_rad)) / r

        if not -1 <= sin_beta <= 1:
            return "impossible"

        beta_rad = math.asin(sin_beta)

        alpha = math.degrees(alpha_rad)
        beta = math.degrees(beta_rad)
        beta_alt = -beta
        gamma = math.degrees(math.atan2(y, x))


        print(f"alpha (degrees): {alpha}")
        print(f"beta (degrees): {beta}")
        print(f"gamma (degrees): {gamma}")

        # Your logic here is now good
        theta_1 = (beta-gamma)-90
        theta_1_alt = (beta_alt-gamma)-90
        theta_2 = alpha - 180

        theta_2_alt = - theta_2

        # Normalize
        # theta_1 = (theta_1+360) % 360
        # theta_2 = (theta_2+360) % 360

        print(f"theta_1 (degrees): {theta_1}")
        print(f"theta_2 (degrees): {theta_2}")

        # print alternative angles
        print(f"theta_1_alt (degrees): {theta_1_alt}")
        print(f"theta_2_alt (degrees): {theta_2_alt}")

        # motors launch
        if self.shoulder:
            self.shoulder.move(self.angle_to_pulse(theta_1), speed=1000, delay=800)
        if self.armpit:
            self.armpit.move(self.angle_to_pulse(theta_2), speed=1000, delay=800)










arm = RobotArm2D(None, None, 3, 5)
arm.move_to(-3, -6)