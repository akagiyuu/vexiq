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

# region Initialize
brain = Brain()

controller = Controller()
controller.set_deadband(10)

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT7, True)
driver = Drivetrain(left_motor, right_motor)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)
# endregion

angle_to_prepare_state = 180

# region Helpers


def joystick_position_to_angle(position):
    if position < - 100 or position > 100:
        return 0
    return position * 9 / 5


def drive_using_controller():
    drive_power = controller.axisA.position()
    turn_power = controller.axisB.position()

    driver.arcade(drive_power, turn_power)


def move_arm_using_controller():
    angle = joystick_position_to_angle(controller.axisD.position())
    arm_motor.spin_for(FORWARD, angle, DEGREES, None, PERCENT, False)


def spin(velocity=100):
    if controller.buttonLUp.pressing():
        spin_motor.spin(REVERSE, velocity, PERCENT)
        return
    if controller.buttonLDown.pressing():
        spin_motor.stop(vex.BrakeType.HOLD)
        return


def shoot(velocity=100):
    if controller.buttonRUp.pressing():
        shoot_motor.spin(FORWARD, velocity, PERCENT)
        # print(shoot_motor.rotation(vex.RotationUnits.DEG))
        return
    if controller.buttonRDown.pressing():
        shoot_motor.stop(vex.BrakeType.COAST)
        # shoot_motor.spin_to(FORWARD, 0)
        return


def shooting_prepare(velocity=100):
    if controller.buttonEUp.pressing():
        shoot_motor.spin_for(FORWARD, angle_to_prepare_state)

# endregion


def main():
    drive_using_controller()
    move_arm_using_controller()
    spin()
    shoot()
    shooting_prepare()


while True:
    main()