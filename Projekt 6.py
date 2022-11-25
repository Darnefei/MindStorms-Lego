from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
from time import sleep
import math
import random

# Create your objects here.
hub = MSHub()

# Write your program here.
hub.speaker.beep()

motor = MotorPair('B', 'F')
color = ColorSensor('D')
sleep(3)
running = True
velocity = 50
look_around_angle = 92
motor.start_tank(-velocity, -velocity)


def look_left():
    hub.motion_sensor.reset_yaw_angle()
    motor.start_tank(velocity, -velocity)
    turning = True
    has_line_found = False
    while turning:
        if hub.motion_sensor.get_yaw_angle() < -look_around_angle:
            turning = False
        if color.get_color() == "white":
            #center_to_road()
            has_line_found = True
            turning = False
    motor.stop()
    return has_line_found

def look_right():
    hub.motion_sensor.reset_yaw_angle()
    motor.start_tank(-velocity, velocity)
    has_line_found = False
    turning = True
    while turning:
        if hub.motion_sensor.get_yaw_angle() > look_around_angle:
            turning = False
        if color.get_color() == "white":
            print("Color was white")
            #center_to_road()
            has_line_found = True
            turning = False
    motor.stop()
    return has_line_found

def center():
    is_not_straight = True
    if hub.motion_sensor.get_yaw_angle() < 0:
        # turn right
        motor.start_tank(-velocity, velocity)
    else:
        # turn left
        motor.start_tank(velocity,-velocity)
    while is_not_straight:
        if hub.motion_sensor.get_yaw_angle() == 0:
            motor.stop()
            is_not_straight = False

#def center_to_road():
#    start_angle = hub.motion_sensor.reset_yaw_angle()
#    while color.get_color() != "black":
#        pass
#    end_angle = hub.motion_sensor.reset_yaw_angle()
#    mid_angle = (start_angle + end_angle)/2
#    print("test")
#    motor.move_tank(2, 'rotations', 25,75)


while running:
    current_color = color.get_color()
    if current_color == "black":
        look_first_right = random.random() < 0.5
        found_line = look_right() if look_first_right else look_left()
        if found_line:
            motor.start_tank(-velocity, -velocity)
        else:
            center()
            found_line = look_left() if look_first_right else look_right()
            if not found_line:
                running = False
                motor.stop()
                break
            motor.start_tank(-velocity, -velocity)
