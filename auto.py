import math
from vex import (
    Brain, Motor, Ports, Colorsensor, TimeUnits,
    FORWARD, PERCENT, REVERSE, DEGREES, INCHES
)
import drivetrain

# region Constant
ANGLE_TO_PREPARE_STATE = 180
GRID_SIZE = 12  # 315
STEP = 20
BRIGHTNESS_THRESHOLD = 6
ARM_STEP = 2000
TIMEOUT = 2000
YELLOW_DISPENSER_BACKWARD_MOVE = 1  # inch
# endregion

# region Enums


class MoveType:
    Straight = 0
    Turn = 1
    Shoot = 2
    Arm = 3
    GetDisk = 4
    Expand = 5


class DispenserType:
    Purple = 0
    Blue = 1
    Yellow = 2
# endregion


class Drivetrain(drivetrain.Drivetrain):
    def move(self, number_of_grid):
        self.drive_for(
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
    def move_forward_and_back(self, distance):
        self.drive_for(REVERSE, distance, INCHES, 100)
        self.drive_for(FORWARD, distance, INCHES, 100)

    def calibrate_angle(self, angle):
        return angle * 3 / 2

    def turn(self, angle):
        angle = self.calibrate_angle(angle)
        driver.turn_for(REVERSE, angle, DEGREES, 100, PERCENT)


class ShootMotor(Motor):
    def shoot(self, time):
        self.spin_for_time(FORWARD, time, TimeUnits.MSEC, 100, PERCENT)


# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT4, True)
driver = Drivetrain(left_motor, right_motor, 7.85, 7.5, INCHES)

spin_motor = Motor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = ShootMotor(Ports.PORT11)
stretcher = Motor(Ports.PORT7)
# endregion


class Helpers:
    def get_disk_from_dispenser(type):
        if type == DispenserType.Blue:
            arm_motor.spin_for(REVERSE, ARM_STEP)
        elif type == DispenserType.Yellow:
            arm_motor.spin_for(FORWARD, ARM_STEP)
            driver.move_forward_and_back(YELLOW_DISPENSER_BACKWARD_MOVE)


class AutoDrive:
    get_yellow_dispenser = [
        [MoveType.Straight, 1.06],  # Move until reach yellow dispenser
        [MoveType.GetDisk, DispenserType.Yellow],
        [MoveType.Arm, - 1 / 2],

    ]
    get_blue_dispenser_1 = [
        [MoveType.Straight, - 0.5],
        [MoveType.Turn, 45],
        [MoveType.Straight, 2.25],
        [MoveType.Turn, 135],
        [MoveType.Arm, 1],
        [MoveType.Turn, 15],
        [MoveType.GetDisk, DispenserType.Blue],
    ]
    shoot_1 = [
        [MoveType.Turn, -65],
        [MoveType.Straight, -1.25],
        [MoveType.Shoot, 2000],
    ]
    get_blue_dispenser_2 = [
        [MoveType.Turn, -40],
        [MoveType.Straight, -1.5],
        [MoveType.Turn, 115],
        [MoveType.Arm, 1],
        [MoveType.Straight, 1],
        [MoveType.GetDisk, DispenserType.Blue],
    ]
    shoot_2 = [
        [MoveType.Turn, 20],
        [MoveType.Shoot, 2000],

    ]
    end = [
        [MoveType.Turn, -20],
        [MoveType.Straight, -1],
        [MoveType.Turn, 65],
        [MoveType.Straight, 1.25],
        [MoveType.Turn, -90],
        [MoveType.Expand, 160],
    ]
    
    def execute(self, move_sequence):
        for move_type, value in move_sequence:
            if move_type == MoveType.Straight:
                driver.move(value)
            elif move_type == MoveType.Turn:
                driver.turn(value)
            elif move_type == MoveType.Arm:
                arm_motor.spin_for(
                    FORWARD,
                    ARM_STEP * value, DEGREES,
                    100, PERCENT
                )
            elif move_type == MoveType.Shoot:
                shoot_motor.shoot(value)
            elif move_type == MoveType.GetDisk:
                Helpers.get_disk_from_dispenser(value)
            elif move_type == MoveType.Expand:
                stretcher.spin_for(FORWARD, value, DEGREES, 50, PERCENT)

    def start_moving(self):
        spin_motor.spin(REVERSE, 100)
        self.execute(self.get_yellow_dispenser)
        self.execute(self.get_blue_dispenser_1)
        self.execute(self.shoot_1)
        self.execute(self.get_blue_dispenser_2)
        self.execute(self.shoot_2)
        self.execute(self.end)


auto_drive = AutoDrive()
auto_drive.start_moving()
