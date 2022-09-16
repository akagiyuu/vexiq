from vex import (
    Brain, Controller, Motor,
    Ports, BrakeType, FORWARD, PERCENT, REVERSE, SECONDS
)
from drivetrain import Drivetrain

# region Initialize
brain = Brain()

controller = Controller()
# nếu joystick không di chuyển hơn 3% thì coi như joystick không di chuyển
controller.set_deadband(3)

left_motor = Motor(Ports.PORT1)
right_motor = Motor(Ports.PORT6, True)
driver = Drivetrain(left_motor, right_motor)

tension_motor = Motor(Ports.PORT5)
arm_motor = Motor(Ports.PORT10)
shooting_motor = Motor(Ports.PORT7)
# endregion

# region Helpers
# def lower_or_raise_arm_by_controller(arm_motor_velocity_percent=100):
#     if controller.buttonLDown.pressing() or controller.buttonRDown.pressing():
#         arm_motor.spin(REVERSE, arm_motor_velocity_percent, PERCENT)

#     elif controller.buttonLUp.pressing() or controller.buttonRUp.pressing():
#         arm_motor.spin(FORWARD, arm_motor_velocity_percent, PERCENT)

#     else:
#         arm_motor.stop(BrakeType.HOLD)

# def close_or_open_claw_by_controller(claw_motor_velocity_percent=100):
#     if controller.buttonEDown.pressing():
#         claw_motor.spin(REVERSE, claw_motor_velocity_percent, PERCENT)

#     elif controller.buttonEUp.pressing():
#         claw_motor.spin(FORWARD, claw_motor_velocity_percent, PERCENT)

#     else:
#         claw_motor.stop(BrakeType.HOLD)

def drive_by_controller():
    drive_power = controller.axisA.position()
    turn_power = controller.axisB.position()

    driver.arcade(drive_power, turn_power)

def move_arm():
    pass



def spin():
    if controller.buttonLUp.pressing():
        return
    if controller.buttonLDown.pressing():
        return

def ...
# endregion

def main():
    pass

while True:
    main()
