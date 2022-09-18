from vex import (

    Brain, Controller, Motor, Ports, BrakeType,
    FORWARD, PERCENT, REVERSE, SECONDS, DEGREES
)
from drivetrain import Drivetrain

# region Constant
ANGLE_TO_PREPARE_STATE = 180
DEFAULT_ANGLE = 20
DEFAULT_VELOCITY = 80
DEAD_BAND = 10
# endregion

# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT7, True)
driver = Drivetrain(left_motor, right_motor)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)
# endregion


class Controller_Extent(Controller):
    def drive(this):
        drive_power = this.axisA.position()
        turn_power = this.axisC.position()

        driver.arcade(drive_power, turn_power)

    def move_arm(this):
        if this.buttonFUp.pressing():
            arm_motor.spin_for(REVERSE, DEFAULT_ANGLE)
            return
        if this.buttonFDown.pressing():
            arm_motor.spin_for(FORWARD, DEFAULT_ANGLE)
            return

    def spin(this):
        if this.buttonLUp.pressing():
            spin_motor.spin(REVERSE, DEFAULT_VELOCITY)
            return
        if this.buttonLDown.pressing():
            spin_motor.stop(BrakeType.HOLD)
            return

    def shoot(this):
        if this.buttonRUp.pressing():
            shoot_motor.spin(FORWARD, DEFAULT_VELOCITY)
            return
        if this.buttonRDown.pressing():
            shoot_motor.stop(BrakeType.COAST)
            return

    def shooting_prepare(this):
        if this.buttonEUp.pressing():
            shoot_motor.spin_for(FORWARD, ANGLE_TO_PREPARE_STATE)

    def detect_input(this):
        this.drive()
        this.move_arm()
        this.spin()
        this.shoot()
        this.shooting_prepare()


controller = Controller_Extent()
controller.set_deadband(DEAD_BAND)


while True:
    controller.detect_input()
