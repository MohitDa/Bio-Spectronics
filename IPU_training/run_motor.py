import time
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(5,GPIO.OUT,initial = GPIO.LOW) #pump1_1
GPIO.setup(6,GPIO.OUT,initial = GPIO.LOW) #pump1_2
GPIO.setup(26,GPIO.OUT,initial = GPIO.LOW) #pump2_1
GPIO.setup(13,GPIO.OUT,initial = GPIO.LOW) #pump2_2

def run_pump(pump = 1, direction = "forward", duration = 1):
    
    if direction == "forward":
        if pump == 1:
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(6, GPIO.LOW)
            sleep(duration)
            GPIO.output(5, GPIO.LOW)
            GPIO.output(6, GPIO.LOW)
        if pump == 2:
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            sleep(duration)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
    elif direction == "backward":
        if pump == 1:
            GPIO.output(5, GPIO.LOW)
            GPIO.output(6, GPIO.HIGH)
            sleep(duration)
            GPIO.output(5, GPIO.LOW)
            GPIO.output(6, GPIO.LOW)
        if pump == 2:
            GPIO.output(26, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            sleep(duration)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            
# run_pump(1, "forward", 0.9)
# run_pump(1, "backward", 2)
# run_pump(2, "forward", 2)
# run_pump(2, "backward", 2)