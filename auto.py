from sunau import AUDIO_FILE_ENCODING_LINEAR_16
from tkinter import W
import vex
import sys
import drivetrain
import smartdrive
import vision
import math

from vex import (

    Brain, Motor, Ports, Colorsensor,
    FORWARD, PERCENT, REVERSE, SECONDS, DEGREES, INCHES
)
from drivetrain import Drivetrain

# region Constant
ANGLE_TO_PREPARE_STATE = 180
GRID_SIZE = 12  # 315
STEP = 20
BRIGHTNESS_THRESHOLD = 6
ANGLE_FOR_BLUE_DISPENSER = 60
# endregion

# region Enums


class MoveType():
    Forward = FORWARD
    Reverse = REVERSE
    Turn = 2
    Shoot = 3
    GetDisk = 4


class DispenserType():
    Purple = 0
    Blue = 1
    Yellow = 2
# endregion


# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT7, True)
driver = Drivetrain(left_motor, right_motor, 8, 11, INCHES)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)

color_sensor = Colorsensor(Ports.PORT8)
# endregion


class AutoDrive:
    move_sequence = [
        # [MoveType.Forward, 1],
        # [MoveType.Turn, 45],
        # [MoveType.Forward, math.sqrt(2)],
        # [MoveType.Turn, 45],
        # [MoveType.Forward, 0.2],
        # [MoveType.GetDisk, DispenserType.Purple]
        # [MoveType.Reverse, 0.2],
        # [MoveType.Turn, 90],
        # [MoveType.GetDisk, DispenserType.Blue]
        # [MoveType.Turn, - 30]
        # [MoveType.Reverse, math.sqrt(5) / 2],
        # [MoveType.Turn, 30]
        # [MoveType.Reverse, (1 + math.sqrt(2))]
        # [MoveType.Shoot, 2000]
        [MoveType.Forward, 2.06], #Move until reach yellow dispenser
        [MoveType.GetDisk, DispenserType.Yellow],
        [MoveType.Reverse, 1],
        [MoveType.Turn, 135],
        [MoveType.Reverse, math.sqrt(2)],
        [MoveType.Turn, 45],
        [MoveType.Reverse, 2]
        [MoveType.Shoot, 2],
        [MoveType.Forward, 1.5],
        [MoveType.Turn, 90],
        [MoveType.Forward, 1.5],
    ]

    def move(direction, number_of_grid):
        driver.drive_for(direction, GRID_SIZE * number_of_grid,
                         INCHES, None, PERCENT, False)
        # grid_pass = 0
        # grids = math.floor(number_of_grid)

        # while not driver.is_done() and grid_pass < grids:
        #     if color_sensor.grayscale() <= BRIGHTNESS_THRESHOLD:
        #         grid_pass += 1

    def get_disk_from_dispenser(type: DispenserType):
        if type == DispenserType.Purple:
            pass
        elif type == DispenserType.Blue:
            arm_motor.spin_for(REVERSE, ANGLE_FOR_BLUE_DISPENSER)
        elif type == DispenserType.Yellow:
            pass

    def start_moving(this):
        for move in this.move_sequence:
            if move[0] == MoveType.Forward or move[0] == MoveType.Reverse:
                move(move[0], move[1])
            elif move[0] == MoveType.Turn:
                driver.turn_for(FORWARD, move[1])
            elif move[0] == MoveType.Spin:
                pass
            elif move[0] == MoveType.Shoot:
                shoot()
            elif move[0] == MoveType.Arm:
                arm_motor.spin_for(REVERSE, 60)


auto_drive = AutoDrive()
auto_drive.start
