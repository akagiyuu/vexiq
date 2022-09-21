
import vex
from timer import Timer
from vex import (
    Brain, Motor, Ports, BrakeType,
    FORWARD, PERCENT, REVERSE, SECONDS, DEGREES, MM
)
from drivetrain import Drivetrain

# region Constant
ANGLE_TO_PREPARE_STATE = 180
DEFAULT_ANGLE = 100
DEFAULT_VELOCITY = 80
DEAD_BAND = 10
YELLOW_DISPENSER_BACKWARD_MOVE = 32  # mm
TIMEOUT = 200 #ms
# endregion

# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT7, True)
driver = Drivetrain(left_motor, right_motor)
driver.set_drive_velocity(100)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)
# endregion


class Controller(vex.Controller):
    number_of_LDown_press = 0
    def drive(self):
        drive_power = self.axisA.position()
        turn_power = self.axisC.position()

        driver.arcade(drive_power, turn_power)

    def move_arm(self):
        if self.buttonFUp.pressing():
            arm_motor.start_spin_for(REVERSE, DEFAULT_ANGLE)
            return
        if self.buttonFDown.pressing():
            arm_motor.start_spin_for(FORWARD, DEFAULT_ANGLE)
            return

    def spin(self):
        if self.buttonLUp.pressing():
            spin_motor.spin(REVERSE, DEFAULT_VELOCITY)
            return
        if self.buttonLDown.pressing():
            spin_motor.stop(BrakeType.HOLD)
            return

    def shoot(self):
        if self.buttonRUp.pressing():
            shoot_motor.spin(FORWARD, DEFAULT_VELOCITY)
            return
        if self.buttonRDown.pressing():
            shoot_motor.stop(BrakeType.COAST)
            return

    def shooting_prepare(self):
        if self.buttonEUp.pressing():
            shoot_motor.spin_for(FORWARD, ANGLE_TO_PREPARE_STATE)

    def get_disk_from_yellow_dispenser(self):
        if self.buttonEDown.pressing():
            driver.start_drive_for(REVERSE, YELLOW_DISPENSER_BACKWARD_MOVE, MM, 100)
            driver.start_drive_for(FORWARD, YELLOW_DISPENSER_BACKWARD_MOVE, MM, 100)
    
    def expand_stretcher(self):
        if not self.buttonLDown.pressing():
            return
        self.number_of_LDown_press += 1
        if self.number_of_LDown_press == 1:
            Timer.start()
            return
        self.number_of_LDown_press = 0
        print(Timer.elapsed_time())



    def detect_input(self):
        self.drive()
        self.move_arm()
        self.spin()
        self.shoot()
        self.shooting_prepare()
        self.get_disk_from_yellow_dispenser()


controller = Controller()
controller.set_deadband(DEAD_BAND)


while True:
    controller.detect_input()
