from vex import (
    Motor, Ports, REVERSE, DEGREES, PERCENT
)
arm_motor = Motor(Ports.PORT9)
arm_motor.spin_for(REVERSE, 5000, DEGREES, 100, PERCENT)
