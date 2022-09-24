import vex
from vex import (
    Brain, Motor, Ports, BrakeType,
    FORWARD, PERCENT, REVERSE, DEGREES, MM
)
from drivetrain import Drivetrain
import sys

# region Constant
ANGLE_TO_PREPARE_STATE = 180
DEFAULT_ANGLE = 100
ARM_STEP = 500
DEFAULT_VELOCITY = 80
DEAD_BAND = 10
YELLOW_DISPENSER_BACKWARD_MOVE = 32  # mm
TIMEOUT = 200  # ms
# endregion

# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT4, True)
driver = Drivetrain(left_motor, right_motor)
driver.set_drive_velocity(100)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)
stretcher = Motor(Ports.PORT7)
# endregion


class Controller(vex.Controller):
    direction = 1

    def drive(self):
        drive_power = self.direction * self.axisA.position()
        turn_power = self.axisC.position() * 2 / 3
        driver.arcade(drive_power, turn_power)

    def reverse_drive(self):
        if self.buttonRUp.pressing():
            self.direction = - self.direction

    def move_arm(self):
        if self.buttonFUp.pressing():
            arm_motor.start_spin_for(REVERSE, ARM_STEP, DEGREES, 100)
            return
        if self.buttonFDown.pressing():
            arm_motor.start_spin_for(FORWARD, ARM_STEP, DEGREES, 100)
            return

    def shoot(self):
        if self.buttonLUp.pressing():
            shoot_motor.spin(FORWARD, DEFAULT_VELOCITY)
            return
        if self.buttonLDown.pressing():
            shoot_motor.stop(BrakeType.COAST)
            return

    def shooting_prepare(self):
        if self.buttonEUp.pressing():
            shoot_motor.spin_for(FORWARD, ANGLE_TO_PREPARE_STATE)

    def get_disk_from_yellow_dispenser(self):
        if self.buttonEDown.pressing():
            driver.drive_for(REVERSE, YELLOW_DISPENSER_BACKWARD_MOVE, MM, 100)
            driver.drive_for(FORWARD, YELLOW_DISPENSER_BACKWARD_MOVE, MM, 100)

    def expand_stretcher(self):
        if self.buttonRDown.pressing():
            stretcher.spin_for(FORWARD, 80, DEGREES, 100)

    def detect_input(self):
        self.drive()
        self.reverse_drive()
        self.move_arm()
        self.shoot()
        self.shooting_prepare()
        self.get_disk_from_yellow_dispenser()
        self.expand_stretcher()


controller = Controller()
controller.set_deadband(DEAD_BAND)

while True:
    controller.detect_input()
    spin_motor.spin(REVERSE, 100)
