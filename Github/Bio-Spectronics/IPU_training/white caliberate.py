import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
import math
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.OUT,initial = GPIO.LOW)

reds = blues = 1

camera = PiCamera()
camera.meter_mode = 'spot'
camera.exposure_mode = 'spotlight'
camera.flash_mode = 'off'
camera.awb_mode = 'off'
camera.drc_strength = 'off'
camera.image_effect = 'none'
# camera.raw_format = 'rgb'
camera.shutter_speed = 31098
camera.brightness = 50
camera.ISO = 200
camera.contrast= 1
camera.zoom = (0.49, 0.42, 0.1, 0.148)
camera.shutter_speed = 10000
# camera.exposure_speed = 1000
camera.framerate = 30
# camera.exposure_compensation = 0

height = 240
width = 320

camera.resolution      =   (width, height)

camera.awb_gains       =   (2,2)

# Wait for initialization        
sleep(5)

# Capture sample image
img = np.zeros((height, width, 3), np.uint8)
GPIO.output(24,GPIO.HIGH)
camera.capture(img, format = 'rgb')
GPIO.output(24,GPIO.LOW)
# Obtain the region of the image which is always gray
# img = img[(int(0.7*height)):(int(0.9*height)), (int(0.3*width)):(int(0.7*width))]
img = cv2.GaussianBlur(img,(5,5),0)

# Update image dimensions
height = img.shape[0]
width = img.shape[1]

# Initialize the gain values
redGain = 0.0
blueGain = 0.0

# Split the image into the rgb channels
r, g, b = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Compute and add the ratio of each pixel
for i in range(height):
        for j in range(width):
            reds += g[i, j] / r[i, j]
            blues += g[i, j] / b[i, j]
#             print(reds, blues)
            
# Compute the average of the ratios
reds /= (width * height)
blues /= (width * height)

print(reds, blues)
