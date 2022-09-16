from vex import (
    Brain, Controller, Motor, Ports,
    FORWARD, PERCENT, REVERSE, SECONDS, DEGREES
)
from drivetrain import Drivetrain

# region Initialize
brain = Brain()

controller = Controller()
controller.set_deadband(3)

left_motor = Motor(Ports.PORT1)
right_motor = Motor(Ports.PORT6, True)
driver = Drivetrain(left_motor, right_motor)

spin_motor = Motor(Ports.PORT5)
arm_motor = Motor(Ports.PORT10)
shoot_motor = Motor(Ports.PORT7)
# endregion

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
    angle = joystick_position_to_angle(controller.axisC.position())
    arm_motor.spin_for(FORWARD, angle, DEGREES, None, PERCENT, False)


def spin(velocity=100):
    if controller.buttonLUp.pressing():
        spin_motor.spin(REVERSE, velocity, PERCENT)
        return
    if controller.buttonLDown.pressing():
        spin_motor.spin(FORWARD, velocity, PERCENT)
        return


def shoot(velocity=100):
    if controller.buttonRUp.pressing():
        shoot_motor.spin(FORWARD, velocity, PERCENT)
        return
    if controller.buttonRDown.pressing():
        shoot_motor.spin(REVERSE, velocity, PERCENT)
        return
# endregion


def main():
    drive_using_controller()
    move_arm_using_controller()
    spin()
    shoot()


while True:
    main()
