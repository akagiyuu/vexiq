import vex
import sys
import drivetrain
import smartdrive
import vision

from vex import (

    Brain, Controller, Motor, Ports,
    FORWARD, PERCENT, REVERSE, SECONDS, DEGREES
)
from drivetrain import Drivetrain

# region Constant
AngleToPrepareState = 180
DefaultAngle = 20
DefaultVelocity = 80
DeadBand = 10
# endregion

class Controller_Extent(Controller):
    def __init__(this, driver: Drivetrain, spin_motor: Motor, shoot_motor: Motor, arm_motor: Motor):
        Controller.__init__(this)
        this.Angle = 20
        this.Velocity = 100

        this.driver = driver
        this.spin_motor = spin_motor
        this.shoot_motor = shoot_motor
        this.arm_motor = arm_motor

    def drive(this):
        drive_power = this.axisA.position()
        turn_power = this.axisC.position()

        this.driver.arcade(drive_power, turn_power)

    def move_arm(this):
        if this.buttonFUp.pressing():
            this.arm_motor.spin_for(REVERSE, DefaultAngle)
            return
        if this.buttonFDown.pressing():
            this.arm_motor.spin_for(FORWARD, DefaultAngle)
            return

    def spin(this):
        if this.buttonLUp.pressing():
            this.spin_motor.spin(REVERSE, DefaultVelocity)
            return
        if this.buttonLDown.pressing():
            this.spin_motor.stop(vex.BrakeType.HOLD)
            return

    def shoot(this):
        if this.buttonRUp.pressing():
            this.shoot_motor.spin(FORWARD, DefaultVelocity)
            return
        if this.buttonRDown.pressing():
            this.shoot_motor.stop(vex.BrakeType.COAST)
            return

    def shooting_prepare(this):
        if this.buttonEUp.pressing():
            this.shoot_motor.spin_for(FORWARD, AngleToPrepareState)

    def detect_input(this):
        this.drive()
        this.move_arm()
        this.spin()
        this.shoot()
        this.shooting_prepare()


# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT7, True)
driver = Drivetrain(left_motor, right_motor)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)

controller = Controller_Extent(driver, spin_motor, shoot_motor, arm_motor)
controller.set_deadband(DeadBand)
# endregion

while True:
    controller.detect_input()
