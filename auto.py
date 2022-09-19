import math
from sre_constants import IN
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

    def get_disk_from_dispenser(this, type: DispenserType):
        spin_motor.spin_for_time(
            REVERSE,
            GET_DISK_TIME,
            TimeUnits.MSEC,
            100,
            PERCENT
        )
        if type == DispenserType.Blue:
            arm_motor.spin_for(REVERSE, ARM_STEP)
        elif type == DispenserType.Yellow:
            arm_motor.spin_for(FORWARD, ARM_STEP)
            driver.start_drive_for(REVERSE, YELLOW_DISPENSER_BACKWARD_MOVE, INCHES, 100)
            driver.start_drive_for(FORWARD, YELLOW_DISPENSER_BACKWARD_MOVE, INCHES, 100)


    def turn(angle):
        driver.turn_for(FORWARD, angle)

    def shoot(time):
        Timer.start()
        while Timer.elapsed_time() <= time:
            shoot_motor.spin(FORWARD, 100)


class AutoDrive:
    get_yellow_dispenser = [
        [MoveType.Straight, 2.06],  # Move until reach yellow dispenser
        [MoveType.GetDisk, DispenserType.Yellow],
        [MoveType.Straight, -1],
    ]
    shoot_1 = [
        [MoveType.Turn, 135],
        [MoveType.Straight, -math.sqrt(2)],
        [MoveType.Turn, 45],
        [MoveType.Straight, -2]
        [MoveType.Shoot, 2000],
    ]
    get_purple_dispenser_1 = [
        [MoveType.Straight, -1.5],
        [MoveType.Turn, 90],
        [MoveType.Straight, 1],
        [MoveType.GetDisk, DispenserType.Purple],
    ]
    get_blue_dispenser_1 = [
        [MoveType.Turn, -135],
        [MoveType.Straight, math.sqrt(2) / 2],
        [MoveType.Turn, 45],
        [MoveType.GetDisk, DispenserType.Blue],
    ]
    shoot_2 = [
        [MoveType.Turn, 90 - math.degrees(math.atan(3))]
        [MoveType.Straight, -math.sqrt(10)/2],
        [MoveType.Turn, -(90 - math.degrees(math.atan(3)))]
        [MoveType.Shoot, 2000]
    ]
    get_blue_dispenser_2 = [
        [MoveType.Straight, 0.3],
        [MoveType.Turn, -90],
        [MoveType.Straight, 2.5],
        [MoveType.Straight, 2 - 0.2],
        [MoveType.GetDisk, DispenserType.Blue],
    ]
    get_purple_dispenser_2 = [
        [MoveType.Straight, -0.1],
        [MoveType.Turn, - 90],
        [MoveType.Straight, 0.5],
        [MoveType.GetDisk, DispenserType.Purple],
    ]
    shoot_3 = [
        [MoveType.Straight, -1],
        [MoveType.Turn, 90],
        [MoveType.Straight, -1.5],
        [MoveType.Shoot, 2000]
    ]
    # move_sequence = [
    #     # [MoveType.Straight, 1],
    #     # [MoveType.Turn, 45],
    #     # [MoveType.Straight, math.sqrt(2)],
    #     # [MoveType.Turn, 45],
    #     # [MoveType.Straight, 0.2],
    #     # [MoveType.GetDisk, DispenserType.Purple]
    #     # [MoveType.Straight, 0.2],
    #     # [MoveType.Turn, 90],
    #     # [MoveType.GetDisk, DispenserType.Blue]
    #     # [MoveType.Turn, - 30]
    #     # [MoveType.Straight, math.sqrt(5) / 2],
    #     # [MoveType.Turn, 30]
    #     # [MoveType.Straight, (1 + math.sqrt(2))]
    #     # [MoveType.Shoot, 2000]

    # ]
    def execute(this, move_sequence):
        for move_type, value in move_sequence:
            if MoveType.Straight:
                Helpers.move(value)
            elif move_type == MoveType.Turn:
                Helpers.turn(value)
            elif move_type == MoveType.Shoot:
                Helpers.shoot(value)
            elif move_type == MoveType.GetDisk:
                Helpers.get_disk_from_dispenser(value)
    def start_moving(this):
        this.execute(this.get_yellow_dispenser)
        this.execute(this.shoot_1)
        this.execute(this.get_purple_dispenser_1)
        this.execute(this.get_blue_dispenser_1)
        this.execute(this.shoot_2)
        this.execute(this.get_blue_dispenser_2)
        this.execute(this.get_purple_dispenser_2)
        this.execute(this.shoot_3)


auto_drive = AutoDrive()
auto_drive.start_moving()
