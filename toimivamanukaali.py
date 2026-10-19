from vex import *

brain = Brain()
controller = Controller(PRIMARY)


front_left = Motor(
    Ports.PORT1,
    GearSetting.RATIO_18_1,
    False
)

front_right = Motor(
    Ports.PORT2,
    GearSetting.RATIO_18_1,
    True
)

back_right = Motor(
    Ports.PORT3,
    GearSetting.RATIO_18_1,
    True
)

back_left = Motor(
    Ports.PORT4,
    GearSetting.RATIO_18_1,
    False
)


lift_motor1 = Motor(
    Ports.PORT6,
    GearSetting.RATIO_18_1,
    False
)

lift_motor2 = Motor(
    Ports.PORT8,
    GearSetting.RATIO_18_1,
    True
)


claw_motor = Motor(
    Ports.PORT7,
    GearSetting.RATIO_18_1,
    False
)


DEADZONE = 10
LIFT_SPEED = 60
CLAW_SPEED = 60


def apply_deadzone(value):
    if abs(value) < DEADZONE:
        return 0
    return value


def spin_signed(motor, speed):
    if speed > 0:
        motor.spin(FORWARD, speed, PERCENT)

    elif speed < 0:
        motor.spin(REVERSE, -speed, PERCENT)

    else:
        motor.stop(BRAKE)



while True:


    forward = apply_deadzone(controller.axis3.position())
    strafe = apply_deadzone(controller.axis4.position())
    turn = apply_deadzone(controller.axis1.position())
    front_left_speed = forward + strafe + turn
    front_right_speed = forward - strafe - turn
    back_right_speed = forward + strafe - turn
    back_left_speed = forward - strafe + turn

    largest_speed = max(
        abs(front_left_speed),
        abs(front_right_speed),
        abs(back_right_speed),
        abs(back_left_speed)
    )

    if largest_speed > 100:
        front_left_speed = front_left_speed / largest_speed * 100
        front_right_speed = front_right_speed / largest_speed * 100
        back_right_speed = back_right_speed / largest_speed * 100
        back_left_speed = back_left_speed / largest_speed * 100

    spin_signed(front_left, front_left_speed)
    spin_signed(front_right, front_right_speed)
    spin_signed(back_right, back_right_speed)
    spin_signed(back_left, back_left_speed)


    if controller.buttonL1.pressing():
        lift_motor1.spin(REVERSE, LIFT_SPEED, PERCENT)
        lift_motor2.spin(REVERSE, LIFT_SPEED, PERCENT)

    elif controller.buttonL2.pressing():
        lift_motor1.spin(FORWARD, LIFT_SPEED, PERCENT)
        lift_motor2.spin(FORWARD, LIFT_SPEED, PERCENT)

    else:
        lift_motor1.stop(HOLD)
        lift_motor2.stop(HOLD)


    if controller.buttonR1.pressing():
        claw_motor.spin(FORWARD, CLAW_SPEED, PERCENT)

    elif controller.buttonR2.pressing():
        claw_motor.spin(REVERSE, CLAW_SPEED, PERCENT)

    else:
        claw_motor.stop(HOLD)


    wait(20, MSEC)
