from vex import (

    Brain, Controller, Motor, Ports, BrakeType,
    FORWARD, PERCENT, REVERSE, SECONDS, DEGREES
)
from drivetrain import Drivetrain

# region Constant
AngleToPrepareState = 180
DefaultAngle = 20
DefaultVelocity = 80
DeadBand = 10
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
    def __init__(this):
        Controller.__init__(this)
        this.Angle = 20
        this.Velocity = 100

    def drive(this):
        drive_power = this.axisA.position()
        turn_power = this.axisC.position()

        driver.arcade(drive_power, turn_power)

    def move_arm(this):
        if this.buttonFUp.pressing():
            arm_motor.spin_for(REVERSE, DefaultAngle)
            return
        if this.buttonFDown.pressing():
            arm_motor.spin_for(FORWARD, DefaultAngle)
            return

    def spin(this):
        if this.buttonLUp.pressing():
            spin_motor.spin(REVERSE, DefaultVelocity)
            return
        if this.buttonLDown.pressing():
            spin_motor.stop(BrakeType.HOLD)
            return

    def shoot(this):
        if this.buttonRUp.pressing():
            shoot_motor.spin(FORWARD, DefaultVelocity)
            return
        if this.buttonRDown.pressing():
            shoot_motor.stop(BrakeType.COAST)
            return

    def shooting_prepare(this):
        if this.buttonEUp.pressing():
            shoot_motor.spin_for(FORWARD, AngleToPrepareState)

    def detect_input(this):
        this.drive()
        this.move_arm()
        this.spin()
        this.shoot()
        this.shooting_prepare()


controller = Controller_Extent()
controller.set_deadband(DeadBand)


while True:
    controller.detect_input()
