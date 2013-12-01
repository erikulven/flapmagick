# Servo Control
import time


delay_period = 0.01


def set(property, value):
    try:
        f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
        f.write(value)
        f.close()   
    except:
        print("Error writing to: " + property + " value: " + value)
     
     
def set_servo(angle):
    set("servo", str(angle))


def test_servo():     
    for angle in range(0, 180):
        set_servo(angle)
        time.sleep(delay_period)
    for angle in range(0, 180):
        set_servo(180 - angle)
        time.sleep(delay_period)


set("delayed", "0")
set("mode", "servo")
set("servo_max", "180")
set("active", "1")
