import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.OUT,initial = GPIO.LOW)

camera = PiCamera()

camera.meter_mode = 'spot'
camera.exposure_mode = 'spotlight'
camera.flash_mode = 'off'
camera.awb_mode = 'shade'
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
camera.exposure_compensation = 0
camera.awb_gains = 0
# camera.digital_gains = 1
# camera.analog_gain = 0.5

# sleep(3)

GPIO.output(24,GPIO.HIGH)
camera.start_preview()
input()
camera.stop_preview()
GPIO.output(24,GPIO.LOW)

# camera.capture("image.jpg")

#camera.raw_format = 'rgb'

#camera.capture("image.jpg")
#im=cv2.imread("image.jpg")
#imshape = im.shape
#roff, goff, boff = im[int(int(imshape[0])/2)][int(int(imshape[1])/2)]

#roff = 255 - roff
#goff = 255 - goff
#boff = 255 - boff

#range = int(30)

#r = [0.0] * 500
#g = [0.0] * 500
#b = [0.0] * 500
#

#with open("/home/pi/Desktop/data.csv", 'a+') as file: 
 #       file.write("r,g,b,h,s,v,l,a,b")  
  #      file.flush()
  
date = input("Enter Date: ")

# file = "/home/pi/Desktop/IPU training/DataSetTriG1.csv"
file = "/home/pi/Desktop/IPU training/ModelAlterPrev.csv"
with open("/home/pi/Desktop/IPU training/Sensitivity.csv", 'a+') as file:
        file.write('\n')
        file.write("Date: " + str(date))
        file.write('\n')
        file.write("r,g,b,h,s,v,l,a,lab,y,cr,cb")
        file.flush()
        
        
for i in range (0, 10):
    
    q = int(input("Enter Concentration: "))

#     camera.start_preview()
#     sleep(20)
#     camera.stop_preview()

    #     print(i)
    GPIO.output(24,GPIO.HIGH)
    camera.start_preview()
    input()
    camera.stop_preview()
    camera.capture("/dev/shm/dataSetImage.png", format='png')
#       sleep(0.3)

    GPIO.output(24,GPIO.LOW)
    
    image = cv2.imread('/dev/shm/dataSetImage.png')
    
    #sleep(1)
    #cv2.startWindowThread()
    #cv2.namedWindow('image')
    #cv2.imshow('image', image)
    
#print(image_read)
#camera.stop_preview()

#crop image
# input coordinates generated from coordinates.py script.

    image = image[500:600,800:900]
    cv2.startWindowThread()
    cv2.namedWindow('image1')
    cv2.imshow('image1', image)
#         cv2.namedWindow('image')
#         cv2.imshow('image', imgCrop)
# cv
# Average


    height, width, _ = np.shape(image)
# calculate the average color of each row of our image
    avg_color_per_row = np.average(image, axis=0)
# calculate the averages of our rows
    avg_colors = np.average(avg_color_per_row, axis=0)
# print(avg_colors)
    int_averages = np.array(avg_colors, dtype=np.uint8)
# print(f'BGR: {int_averages}')
## create a new image of the same height/width as the original
    average_image = np.zeros((height, width, 3), np.uint8)
# # and fill its pixels with our average color
    average_image[:] = int_averages
#     cv2.startWindowThread()
#         cv2.namedWindow('avg img')
#         cv2.imshow('avg img', average_image)
#         cv2.namedWindow('image')
#         cv2.imshow('image', imgCrop)
# #finally, show it side-by-side with the original
    #cv2.imshow("Avg Color", np.hstack([imgCrop, average_image]))

# Data extraction

#     rgba = average_image
    rgba =cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB)
#     cv2.startWindowThread()
#     cv2.namedWindow('rgb')
#     cv2.imshow('rgb', rgba)
#     cv2.namedWindow('hsv')
#     cv2.imshow('hsv', hsva)
#     cv2.namedWindow('lab')
#     cv2.imshow('lab', laba)
#     cv2.namedWindow('ycrcb')
#     cv2.imshow('ycrcb', ycrcba)

    #roff, goff, boff = image[int(int(imshape[0])/2)][int(int(imshape[1])/2)]
#     imshape = image.shape
#     r, g, b =cv2.cvtColor(image, cv2.COLOR_BGR2RGB)[int(int(imshape[0])/2)][int(int(imshape[1])/2)]
#     h, s, v =cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[int(int(imshape[0])/2)][int(int(imshape[1])/2)]
#     l, a, lab =cv2.cvtColor(image, cv2.COLOR_BGR2LAB)[int(int(imshape[0])/2)][int(int(imshape[1])/2)]
#     y, c, ycr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)[int(int(imshape[0])/2)][int(int(imshape[1])/2)]

#
    ax0=rgba[1,1]

#         print(r, g, b, " , ", h, s, v, " , ", l, a, lab, " , ", y, c, ycr)
    print(str(ax0))
    
    r = ax0[0]/255
    g = ax0[1]/255
    b = ax0[2]/255

    #im=cv2.imread("image.jpg")
    #imshape = im.shape

    #sleep(0)
    
    with open("/home/pi/Desktop/IPU training/Sensitivity.csv", 'a+') as file:
        file.write('\n') 
        file.write(str(r) + "," + str(g) + "," +str(b))  
        file.write(",")
        file.write(str(q))
        #file.write(" ml")
        file.flush()
        
    #     with open("/home/pi/Desktop/dataPixal.csv", 'a+') as file:
    #         file.write('\n') 
    #         file.write(str(r) + "," + str(g) + "," +str(b) + "," + str(h) + "," + str(s) + "," +str(v) + "," + str(l) + "," + str(a) + "," +str(lab))  
    #         file.write(", ")
    #         file.write(str(q))
    #         #file.write(" ml")
    #         file.flush()
    #     print(str(r) + "," + str(g) + "," +str(b) + "," + str(h) + "," + str(s) + "," +str(v) + "," + str(l) + "," + str(a) + "," +str(lab))
    #print(r)
    #print(g)
    #print(b)
        
    #r.append(0)
    #r.append(255)
    #g.append(0)
    #g.append(255)
    #b.append(0)
    #b.append(255)

    #plt.plot(np.array(r), color = "red")
    #plt.show()
    #plt.plot(np.array(g), color = "green")
    #plt.show()
    #plt.plot(np.array(b), color = "blue")
#plt.show()
camera.close()


#camera.exposure_mode = 'off'

