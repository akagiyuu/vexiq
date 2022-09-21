import math
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
ARM_STEP = 750
GET_DISK_TIME = 2000
YELLOW_DISPENSER_BACKWARD_MOVE = 1  # inch
# endregion

# region Enums


class MoveType:
    Straight = 0
    Turn = 1
    Shoot = 2
    GetDisk = 3


class DispenserType:
    Purple = 0
    Blue = 1
    Yellow = 2
# endregion


# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT7, True)
driver = Drivetrain(left_motor, right_motor, 7.85, 7.5, INCHES)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = Motor(Ports.PORT11)

color_sensor = Colorsensor(Ports.PORT8)
# endregion


class Helpers:
    @staticmethod
    def move(number_of_grid):
        driver.drive_for(
            FORWARD,
            GRID_SIZE * number_of_grid,
            INCHES,
            100,
            PERCENT,
        )
        # grid_pass = 0
        # grids = math.floor(number_of_grid)

        # while not driver.is_done() and grid_pass < grids:
        #     if color_sensor.grayscale() <= BRIGHTNESS_THRESHOLD:
        #         grid_pass += 1
    @staticmethod
    def get_disk_from_dispenser(type):
        if type == DispenserType.Purple:
            spin_motor.spin_for_time(
                REVERSE,
                GET_DISK_TIME,
                TimeUnits.MSEC,
                5000,
                PERCENT,
            )
        elif type == DispenserType.Blue:
            arm_motor.spin_for(REVERSE, ARM_STEP)
            spin_motor.spin_for_time(
                REVERSE,
                GET_DISK_TIME,
                TimeUnits.MSEC,
                5000,
                PERCENT,
            )
        elif type == DispenserType.Yellow:
            arm_motor.spin_for(REVERSE, ARM_STEP)
            driver.drive_for(
                REVERSE, YELLOW_DISPENSER_BACKWARD_MOVE, INCHES, 100)
            driver.drive_for(
                FORWARD, YELLOW_DISPENSER_BACKWARD_MOVE, INCHES, 100)
            spin_motor.spin_for_time(
                REVERSE,
                GET_DISK_TIME,
                TimeUnits.MSEC,
                5000,
                PERCENT,
            )

    @staticmethod
    def get_actual_turn(angle):
        return angle * 3 / 2

    @staticmethod
    def turn(angle):
        angle = Helpers.get_actual_turn(angle)
        driver.turn_for(FORWARD, angle)

    @staticmethod
    def shoot(time):
        shoot_motor.spin_for_time(FORWARD, time, TimeUnits.MSEC, 100, PERCENT)

class AutoDrive:
    get_yellow_dispenser = [
        [MoveType.Straight, 2.06],  # Move until reach yellow dispenser
        [MoveType.GetDisk, DispenserType.Yellow],
        [MoveType.Straight, -1],
    ]
    get_blue_dispenser_1 = [
        [MoveType.Turn, 45],
        [MoveType.Straight, 3 * sqrt(2) / 2],
        [MoveType.Turn, 135],
        [MoveType.GetDisk, DispenserType.Blue],
    ]
    get_purple_dispenser_1 = [
        [MoveType.Turn, 90],
        [MoveType.Straight, math.sqrt(2) / 2],
        [MoveType.GetDisk, DispenserType.Purple],
    ]
    shoot_1 = [
        [MoveType.Turn, math.arctan(3/4)],
        [MoveType.Straight, -2.5],
        [MoveType.Turn, math.arctan(4/3)],
        [MoveType.Shoot, 2000]
    ]

    get_blue_dispenser_2 = [
        [MoveType.Turn, 90],
        [MoveType.Straight, 1.5],
        [MoveType.Turn, -90],
        [MoveType.Straight, 2],
        [MoveType.GetDisk, DispenserType.Blue],
    ]
    get_purple_dispenser_2 = [
        [MoveType.Straight, -0.5],
        [MoveType.Turn, 90],
        [MoveType.Straight, math.sqrt(2) / 2],
        [MoveType.GetDisk, DispenserType.Purple],
    ]
    shoot_2 = [
        [MoveType.Turn, -math.arctan(3/4)],
        [MoveType.Straight, -2.5],
        [MoveType.Turn, -math.arctan(4/3)],
        [MoveType.Shoot, 2000]
    ]

    def execute(self, move_sequence):
        for move_type, value in move_sequence:
            if move_type == MoveType.Straight:
                Helpers.move(value)
            elif move_type == MoveType.Turn:
                Helpers.turn(value)
            elif move_type == MoveType.Shoot:
                Helpers.shoot(value)
            elif move_type == MoveType.GetDisk:
                Helpers.get_disk_from_dispenser(value)

    def start_moving(self):
        self.execute(self.get_yellow_dispenser)
        self.execute(self.get_purple_dispenser_1)
        self.execute(self.get_blue_dispenser_1)
        self.execute(self.shoot_1)
        self.execute(self.get_blue_dispenser_2)
        self.execute(self.get_purple_dispenser_2)
        self.execute(self.shoot_2)


auto_drive = AutoDrive()
auto_drive.start_moving()
