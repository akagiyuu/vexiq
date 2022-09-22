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
ARM_STEP = 750
TIMEOUT = 2000
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
    def get_actual_turn(self, angle):
        return angle * 3 / 2

    def turn(self, angle):
        angle = self.get_actual_turn(angle)
        driver.turn_for(FORWARD, angle)



class SpinMotor(Motor):
    def run(self, time=TIMEOUT):
        self.spin_for_time(REVERSE, time, TimeUnits.MSEC, 100, PERCENT)
class ShootMotor(Motor):
    def shoot(self, time):
        self.spin_for_time(FORWARD, time, TimeUnits.MSEC, 100, PERCENT)


# region Initialize
brain = Brain()

left_motor = Motor(Ports.PORT12)
right_motor = Motor(Ports.PORT4, True)
driver = Drivetrain(left_motor, right_motor, 7.85, 7.5, INCHES)

spin_motor = SpinMotor(Ports.PORT10)
arm_motor = Motor(Ports.PORT9)
shoot_motor = ShootMotor(Ports.PORT7)
# endregion


class Helpers:
    def get_disk_from_dispenser(type):
        if type == DispenserType.Purple:
            spin_motor.run()
        elif type == DispenserType.Blue:
            arm_motor.spin_for(REVERSE, ARM_STEP)
            spin_motor.run()
        elif type == DispenserType.Yellow:
            arm_motor.spin_for(FORWARD, ARM_STEP)
            driver.move_forward_and_back(YELLOW_DISPENSER_BACKWARD_MOVE)
            arm_motor.start_spin_for(REVERSE, ARM_STEP)
            spin_motor.run()
            driver.move(-1)
            arm_motor.spin_for(FORWARD, ARM_STEP)


class AutoDrive:
    get_yellow_dispenser = [
        [MoveType.Straight, 2.06],  # Move until reach yellow dispenser
        [MoveType.GetDisk, DispenserType.Yellow],
    ]
    get_blue_dispenser_1 = [
        [MoveType.Turn, 40],
        [MoveType.Straight, 1.96],
        [MoveType.Turn, 118],
        [MoveType.Straight, 0.81],
        [MoveType.Turn, 22],
        [MoveType.GetDisk, DispenserType.Blue],
    ]
    get_purple_dispenser_1 = [
        [MoveType.Straight, -0.5],
        [MoveType.Turn, -90],
        [MoveType.Straight, 0.8],
        [MoveType.GetDisk, DispenserType.Purple],
    ]
    shoot_1 = [
        [MoveType.Turn, math.atan(3/4)],
        [MoveType.Straight, -2.5],
        [MoveType.Turn, math.atan(4/3)],
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
        [MoveType.Turn, -math.atan(3/4)],
        [MoveType.Straight, -2.5],
        [MoveType.Turn, -math.atan(4/3)],
        [MoveType.Shoot, 2000]
    ]

    def execute(self, move_sequence):
        for move_type, value in move_sequence:
            if move_type == MoveType.Straight:
                driver.move(value)
            elif move_type == MoveType.Turn:
                driver.turn(value)
            elif move_type == MoveType.Shoot:
                shoot_motor.shoot(value)
            elif move_type == MoveType.GetDisk:
                Helpers.get_disk_from_dispenser(value)

    def start_moving(self):
        self.execute(self.get_yellow_dispenser)
        self.execute(self.get_blue_dispenser_1)
        self.execute(self.get_purple_dispenser_1)
        self.execute(self.shoot_1)
        self.execute(self.get_blue_dispenser_2)
        self.execute(self.get_purple_dispenser_2)
        self.execute(self.shoot_2)


auto_drive = AutoDrive()
auto_drive.start_moving()
