import Sens
import RPi.GPIO as GPIO
from picamera import PiCamera
import numpy as np
import cv2
from time import sleep
camera = PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.OUT,initial = GPIO.LOW)

camera.meter_mode = 'spot'
camera.exposure_mode = 'spotlight'
camera.flash_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = (3.75,1.125)
camera.drc_strength = 'off'
camera.image_effect = 'none'
# camera.raw_format = 'rgb'
# camera.shutter_speed = 31098
camera.brightness = 50
camera.ISO = 200
camera.contrast= 0
camera.zoom = (0.49, 0.42, 0.1, 0.148)
camera.shutter_speed = 10000
camera.resolution = (320, 240)
sleep(3)
sens = Sens.data()

class backend:
    def get_date(self):
        date = input("Enter Date: ")
        return date
    
    def get_test(self):
        test = input("Enter test name: ")
        return test
    
    def get_sens(self):
        S = []
        while True:
            try:
                S = sens.getVal(int(input("Enter filter value. {400, 410, 420, 430,...., 700}: ")))
                break
            except:
                pass
        
        return S
    
    def get_rgb(self, save = False, name = "image"):
        
        GPIO.output(24,GPIO.HIGH)
        sleep(0.25)
        image = []
#         if save == True:
#             camera.capture("/dev/shm/" +name + ".png", format='png')
#             image = cv2.imread("/dev/shm/" +name + ".png")
#         else:
#             image = np.empty((320, 240, 3), dtype=np.uint8)
#             camera.capture(image, format='png')
            
        camera.capture("/dev/shm/" +name + ".png", format='png')
        image = cv2.imread("/dev/shm/" +name + ".png")
#             print(image)
    #     camera.capture("/dev/shm/image.png", format='png')
        
        GPIO.output(24,GPIO.LOW)
    #     image = cv2.imread('/dev/shm/image.png')

        height, width, _ = np.shape(image)
        avg_color_per_row = np.average(image, axis=0)
        avg_colors = np.average(avg_color_per_row, axis=0)
        int_averages = np.array(avg_colors, dtype=np.uint8)
    #     average_image = np.zeros((height, width, 3), np.uint8)
    #     average_image[:] = int_averages

    #     rgba =cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB)
#         print(int_averages)
        return int_averages
    
    def get_concentration(self, sample = ""):
        sample = sample + " "
        q = 0
        while True:
            try:
                q = float(input("Enter " +sample+ "Concentration: "))
                break
            except:
                pass
        
        return q
        