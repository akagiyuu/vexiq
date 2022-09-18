from sunau import AUDIO_FILE_ENCODING_LINEAR_16
import vex
import sys
import drivetrain
import smartdrive
import vision

from vex import (

    Brain, Motor, Ports, Colorsensor,
    FORWARD, PERCENT, REVERSE, SECONDS, DEGREES
)
from drivetrain import Drivetrain

# region Constant
ANGLE_TO_PREPARE_STATE = 180
GRID_SIZE = 315
STEP = 20
BRIGHTNESS_THRESHOLD = 6
ANGLE_FOR_BLUE_DISPENSER = 60


# endregion

class MoveType():
    Forward = FORWARD
    Reverse = REVERSE
    Turn = 2
    Spin = 3
    Shoot = 4
    Arm = 5

class DispenserType():
    Purple = 0
    Blue = 1
    Yellow = 2


class AutoDrive:
    move_sequence = [
        [[MoveType.Forward, 3], [MoveType.Turn, 90], [MoveType.Forward, 2], [MoveType.Spin, 200], [MoveType.Reverse, 1],
         [MoveType.Turn, 90], [MoveType.Forward, 1], [MoveType.Arm], [MoveType.Reverse, 2], [MoveType.Shoot, 2000]],

    ]

    def move(direction, number_of_grid):
        grid_pass = 0
        while grid_pass < number_of_grid:
            driver.drive_for(direction, STEP)
            if color_sensor.grayscale() > BRIGHTNESS_THRESHOLD:
                grid_pass += 1

    def start(this):
        this.get_dispensers(0)

    def get_disk_from_dispenser(type: DispenserType):
        if type == DispenserType.Purple:
            pass
        elif type == DispenserType.Blue:
            arm_motor.spin_for(REVERSE, ANGLE_FOR_BLUE_DISPENSER)
        elif type == DispenserType.Yellow:
            pass

    def get_dispensers(this, index):
        for move in this.move_sequence[index]:
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

# endregion


auto_drive = AutoDrive()
auto_drive.start()
