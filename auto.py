import math
from timer import Timer
from vex import (
    Brain, Motor, Ports, Colorsensor, TimeUnits,
    FORWARD, PERCENT, REVERSE, DEGREES, INCHES
)
from drivetrain import Drivetrain

# region Constant
ANGLE_TO_PREPARE_STATE = 180
GRID_SIZE = 12  # 315
STEP = 20
BRIGHTNESS_THRESHOLD = 6
ARM_STEP = 60
PURPLE_DISPENSER_SPIN_TIME = 2000
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
driver = Drivetrain(left_motor, right_motor, 7.85 ,7.5 , INCHES)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)

color_sensor = Colorsensor(Ports.PORT8)
# endregion


class Helpers:
    def move(direction, number_of_grid):
        driver.drive_for(
            direction,
            GRID_SIZE * number_of_grid,
            INCHES,
            None,
            PERCENT,
            False
        )
        # grid_pass = 0
        # grids = math.floor(number_of_grid)

        # while not driver.is_done() and grid_pass < grids:
        #     if color_sensor.grayscale() <= BRIGHTNESS_THRESHOLD:
        #         grid_pass += 1

    def get_disk_from_dispenser(this, type: DispenserType):
        if type == DispenserType.Purple:
            spin_motor.spin_for_time(
                REVERSE,
                PURPLE_DISPENSER_SPIN_TIME,
                TimeUnits.MSEC,
                100,
                PERCENT
            )
        elif type == DispenserType.Blue:
            arm_motor.spin_for(REVERSE, ARM_STEP)
        elif type == DispenserType.Yellow:
            pass
    def turn(angle):
        driver.turn_for(FORWARD, angle)
    def shoot(time):
        Timer.start()
        while Timer.elapsed_time() <= time:
            shoot_motor.spin(FORWARD, 100)


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
        [MoveType.Forward, 2.06],  # Move until reach yellow dispenser
        [MoveType.GetDisk, DispenserType.Yellow],
        [MoveType.Reverse, 1],
        [MoveType.Turn, 135],
        [MoveType.Reverse, math.sqrt(2)],
        [MoveType.Turn, 45],
        [MoveType.Reverse, 2]
        [MoveType.Shoot, 2000],

        [MoveType.Forward, 1.5],
        [MoveType.Turn, 90],
        [MoveType.Forward, 1],
        [MoveType.GetDisk, DispenserType.Purple],
        [MoveType.Turn, -135],
        [MoveType.Forward, math.sqrt(2) / 2],
        [MoveType.Turn, 45],
        [MoveType.GetDisk, DispenserType.Blue],
        [MoveType.Turn, 90 - math.degrees(math.atan(3))]
        [MoveType.Reverse, math.sqrt(10)/2],
        [MoveType.Turn, -(90 - math.degrees(math.atan(3)))]
        [MoveType.Shoot, 2000]

        [MoveType.Forward, 0.3],
        [MoveType.Turn, -90],
        [MoveType.Forward, 2.5],
        [MoveType.Forward, 2 - 0.2],
        [MoveType.GetDisk, DispenserType.Blue],
        [MoveType.Reverse, 0.1],
        [MoveType.Turn, - 90],
        [MoveType.Forward, 0.5],
        [MoveType.GetDisk, DispenserType.Purple],
        [MoveType.Reverse, 1],
        [MoveType.Turn, 90],
        [MoveType.Reverse, 1.5],
        [MoveType.Shoot, 2000]
    ]

    def start_moving(this):
        for move_type, value in this.move_sequence:
            if move_type == MoveType.Forward or move_type == MoveType.Reverse:
                Helpers.move(move_type, value)
            elif move_type == MoveType.Turn:
                Helpers.turn(value)
            elif move_type == MoveType.Shoot:
                Helpers.shoot(value)
            elif move_type == MoveType.GetDisk:
                Helpers.get_disk_from_dispenser(value)


auto_drive = AutoDrive()
auto_drive.start_moving()
