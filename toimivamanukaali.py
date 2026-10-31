from vex import *

# --- MOTOR & HARDWARE SETUP ---
brain = Brain()
controller = Controller(PRIMARY)

front_left = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
front_right = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
back_right = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
back_left = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)

lift_motor1 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
lift_motor2 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)

claw_motor = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)

LIFT_SPEED = 25
CLAW_SPEED = 15

lift_manukal = 45
claw_manukal = 25





# Smooth driving settings
ACCELERATION = 3.0
DECELERATION = 5.0

current_fl = 0
current_fr = 0
current_br = 0
current_bl = 0








DEADZONE = 5
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
def stop_drivetrain():
    front_left.stop(BRAKE)
    front_right.stop(BRAKE)
    back_right.stop(BRAKE)
    back_left.stop(BRAKE)

def drive_forward(speed, duration_ms):
    front_left.spin(FORWARD, speed, PERCENT)
    front_right.spin(FORWARD, speed, PERCENT)
    back_right.spin(FORWARD, speed, PERCENT)
    back_left.spin(FORWARD, speed, PERCENT)
    wait(duration_ms, MSEC)
    stop_drivetrain()

def drive_backward(speed, duration_ms):
    front_left.spin(REVERSE, speed, PERCENT)
    front_right.spin(REVERSE, speed, PERCENT)
    back_right.spin(REVERSE, speed, PERCENT)
    back_left.spin(REVERSE, speed, PERCENT)
    wait(duration_ms, MSEC)
    stop_drivetrain()

def turn_right(speed, duration_ms):
    front_left.spin(FORWARD, speed, PERCENT)
    front_right.spin(REVERSE, speed, PERCENT)
    back_right.spin(REVERSE, speed, PERCENT)
    back_left.spin(FORWARD, speed, PERCENT)
    wait(duration_ms, MSEC)
    stop_drivetrain()

def turn_left(speed, duration_ms):
    front_left.spin(REVERSE, speed, PERCENT)
    front_right.spin(FORWARD, speed, PERCENT)
    back_right.spin(FORWARD, speed, PERCENT)
    back_left.spin(REVERSE, speed, PERCENT)
    wait(duration_ms, MSEC)
    stop_drivetrain()

def claw_close(duration_ms=500):
    claw_motor.spin(FORWARD, CLAW_SPEED, PERCENT)
    wait(duration_ms, MSEC)
    claw_motor.stop(HOLD)

def claw_open(duration_ms=500):
    claw_motor.spin(REVERSE, CLAW_SPEED, PERCENT)
    wait(duration_ms, MSEC)
    claw_motor.stop(HOLD)

def lift_up(duration_ms):
    lift_motor1.spin(REVERSE, LIFT_SPEED, PERCENT)
    lift_motor2.spin(REVERSE, LIFT_SPEED, PERCENT)
    wait(duration_ms, MSEC)
    lift_motor1.stop(HOLD)
    lift_motor2.stop(HOLD)

def lift_down(duration_ms):
    lift_motor1.spin(FORWARD, LIFT_SPEED, PERCENT)
    lift_motor2.spin(FORWARD, LIFT_SPEED, PERCENT)
    wait(duration_ms, MSEC)
    lift_motor1.stop(HOLD)
    lift_motor2.stop(HOLD)
def smooth_speed(current, target):
    if abs(target) > abs(current):
        change = ACCELERATION
    else:
        change = DECELERATION

    if target > current:
        current += change
        if current > target:
            current = target

    elif target < current:
        current -= change
        if current < target:
            current = target

    return current

# --- YOUR AUTONOMOUS ROUTINE ---
def autonomous():
    lift_up(1200)
    claw_open(1000)
    
    drive_forward(20, 2900)
    claw_close(1000)
    lift_up(1000)         
    drive_backward(20, 500)
    turn_right(30, 700)    
    drive_forward(20, 1200)
    turn_left(30, 500)     
    drive_forward(20, 500)
    turn_left(30, 600) 
    drive_forward(25, 1700)
    lift_down(300)  
    claw_open(400)
   
def ajo():
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
            lift_motor1.spin(REVERSE, lift_manukal, PERCENT)
            lift_motor2.spin(REVERSE, lift_manukal, PERCENT)
        elif controller.buttonL2.pressing():
            lift_motor1.spin(FORWARD, lift_manukal, PERCENT)
            lift_motor2.spin(FORWARD, lift_manukal, PERCENT)
        else:
            lift_motor1.stop(HOLD)
            lift_motor2.stop(HOLD)
        
        if controller.buttonR1.pressing():
            claw_motor.spin(FORWARD, claw_manukal, PERCENT)
        elif controller.buttonR2.pressing():
            claw_motor.spin(REVERSE, claw_manukal, PERCENT)
        else:
            claw_motor.stop(HOLD)
        
        wait(20, MSEC)
# Uncomment below when you are ready to run autonomous:



def pre_autonomous():
    # This function is called before autonomous starts
    # You can use it to set up sensors, reset encoders, etc.
    pass




def user_control():
    ajo()

#comp = Competition(user_control, autonomous)

user_control()
