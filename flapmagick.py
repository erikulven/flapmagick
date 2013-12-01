import time
import RPi.GPIO as io
from servo import set_servo
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import sys


logger = logging.getLogger('bergro')
logger_format = ("%(asctime)s %(levelname)s: %(message)s"
                 " [%(pathname)s:%(lineno)d]")

logger_filename = "%s/flapmagick.log" % '/home/pi/app'
vlh = RotatingFileHandler(logger_filename, mode='a', maxBytes=50485760,
                          backupCount=5)
vlh.setFormatter(Formatter(logger_format))

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(Formatter(logger_format))
logger.addHandler(ch)
vlh.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)

logger.addHandler(vlh)
logger.info("Initializing flapmagick, logging to: %s" % logger_filename)

current_servo_pos = 100
io.setmode(io.BCM)
 
door_pin = 23
outside_pin = 24
inside_pin = 25
led_pin = 17


io.setup(led_pin, io.OUT)         # activate input
io.setup(inside_pin, io.IN)         # activate input
io.setup(outside_pin, io.IN)         # activate input
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp


def servo(pos=0):
    global current_servo_pos
    if current_servo_pos != pos:
        current_servo_pos = pos
        set_servo(pos)


def open_door():
    global current_servo_pos
    if current_servo_pos > 0:
        cpos = current_servo_pos
        for i in range(0, current_servo_pos, 1):
            servo(cpos - i)
            time.sleep(0.02)
        servo(0)


def close_door():
    global current_servo_pos
    if current_servo_pos < 170:
        for i in range(current_servo_pos, 170, 1):
            servo(i)
            time.sleep(0.02)
        servo(170)


def is_open():
    global current_servo_pos
    return current_servo_pos == 0


def is_in_motion():
    global current_servo_pos
    return current_servo_pos == 0


def has_visitor():
    global inside_pin
    global outside_pin
    return io.input(inside_pin) or io.input(outside_pin)


def is_door_open():
    global door_pin
    return io.input(door_pin)


if __name__ == '__main__':
    close_door()
    DELAY_CLOSE = 15L
    visit_time = None
    while True:
        try:
            if has_visitor():
                visit_time = time.time()
                if not is_open():
                    if not is_in_motion():
                        logger.info("Has visitor, so is opening door!")
                        open_door()
                    else:
                        logger.info("Visitor detected, but flap in motion!")
            else:
                if visit_time is None:
                    logger.info("First time, no visitor so far!")
                    time_since_visit = DELAY_CLOSE + 1
                else:
                    time_since_visit = long(time.time() - visit_time)
                    if time_since_visit < DELAY_CLOSE:
                        logger.info("Had visit %s ago" % time_since_visit)
                if time_since_visit > DELAY_CLOSE:
                    if is_open():
                        logger.info("Visitor has left so we close the door!")
                        close_door()
            time.sleep(0.9)
        except Exception as e:
            logger.exception("Error occured: %s" % e)
    logger.info("Flapmagick is done...!")
