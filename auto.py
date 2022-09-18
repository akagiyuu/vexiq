import vex
import sys
import drivetrain
import smartdrive
import vision

from vex import (

    Brain, Controller, Motor, Ports, Colorsensor,
    FORWARD, PERCENT, REVERSE, SECONDS, DEGREES
)
from drivetrain import Drivetrain

# region Constant
angle_to_prepare_state = 180
grid_size = 315
step = 20
brightness_threshold = 6


class Move():
    Forward = FORWARD
    Reverse = REVERSE
    Turn = 2
    Spin = 3
    Shoot = 4
    Arm = 5

# endregion


class AutoDrive:
    move_sequence = [
        [[Move.Forward, 3], [Move.Turn, 90], [Move.Forward, 2], [Move.Spin, 200], [Move.Reverse, 1],
         [Move.Turn, 90], [Move.Forward, 1], [Move.Arm], [Move.Reverse, 2], [Move.Shoot, 2000]],

    ]

    def start(this):
        this.get_dispensers(0)

    def get_dispensers(this, index):
        for move in this.move_sequence[index]:
            if move[0] == Move.Forward or move[0] == Move.Reverse:
                move(move[0], move[1])
            elif move[0] == Move.Turn:
                driver.turn_for(FORWARD, move[1])
            elif move[0] == Move.Spin:
                pass
            elif move[0] == Move.Shoot:
                shoot()
            elif move[0] == Move.Arm:
                arm_motor.spin_for(REVERSE, 60)


# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT7, True)
driver = Drivetrain(left_motor, right_motor)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)

color_sensor = Colorsensor(Ports.PORT8)
# endregion


# region Helpers
def move(direction, number_of_grid):
    grid_pass = 0
    while grid_pass < number_of_grid:
        driver.drive_for(direction, step)
        if color_sensor.grayscale() > brightness_threshold:
            grid_pass += 1
# endregion

auto_drive = AutoDrive()
auto_drive.start()
