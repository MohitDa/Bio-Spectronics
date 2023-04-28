import cv2
import numpy as np
from picamera import PiCamera
from time import sleep
import math
import matplotlib.pyplot as plt


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
camera.zoom = (0.45, 0.4, 0.18, 0.2)
camera.shutter_speed = 10000
# camera.exposure_speed = 1000
camera.framerate = 30
camera.exposure_compensation = 0
camera.awb_gains = 0
# camera.digital_gains = 1
# camera.analog_gain = 0.5


_Sr = 0.32
_Sg = 0.945
_Sb = 0.34

A_b
q
m = q / A_std
i = q - m * A_std 

factor = q/A_std

sleep(3)

date = input("Enter Date: ")
if input("Enter R to repeat caliberation, else press enter") == "R":

    input("Put Water")

    with open("/home/pi/Desktop/IPU training/V1Result.csv", 'a+') as file:
        file.write('\n')
        file.write("Date: " + str(date))
        file.write('\n')
        file.write("r,g,b,val,R,G,B,Ar,Ag,Ab,A")
        file.flush()

    camera.capture("/dev/shm/image.png", format='png')
    image = cv2.imread('/dev/shm/image.png')

    height, width, _ = np.shape(image)
    avg_color_per_row = np.average(image, axis=0)
    avg_colors = np.average(avg_color_per_row, axis=0)
    int_averages = np.array(avg_colors, dtype=np.uint8)
    average_image = np.zeros((height, width, 3), np.uint8)
    average_image[:] = int_averages

    rgba =cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB)
    ax0=rgba[1,1]
    ax0 = [104,97,90]

    R_w = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    G_w = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    B_w = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

    with open("/home/pi/Desktop/IPU training/V1Result.csv", 'a+') as file:
        file.write('\n') 
        file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
        file.write(",")
        file.write("water")
        file.write("," +str(R_w) + "," +str(G_w) + "," +str(B_w))        
        file.flush()
            


    input("Put Blank")

    camera.capture("/dev/shm/image.png", format='png')
    image = cv2.imread('/dev/shm/image.png')

    height, width, _ = np.shape(image)
    avg_color_per_row = np.average(image, axis=0)
    avg_colors = np.average(avg_color_per_row, axis=0)
    int_averages = np.array(avg_colors, dtype=np.uint8)
    average_image = np.zeros((height, width, 3), np.uint8)
    average_image[:] = int_averages

    rgba =cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB)
    ax0=rgba[1,1]
    ax0 = [103,89,74]

    R_b = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    G_b = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    B_b = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

    with open("/home/pi/Desktop/IPU training/V1Result.csv", 'a+') as file:
        file.write('\n') 
        file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
        file.write(",")
        file.write("blank")
        file.write("," +str(R_b) + "," +str(G_b) + "," +str(B_b))        
        file.flush()


    input("Put Standard")
    q = int(input("Enter Concentration: "))
    camera.capture("/dev/shm/image.png", format='png')
    image = cv2.imread('/dev/shm/image.png')

    height, width, _ = np.shape(image)
    avg_color_per_row = np.average(image, axis=0)
    avg_colors = np.average(avg_color_per_row, axis=0)
    int_averages = np.array(avg_colors, dtype=np.uint8)
    average_image = np.zeros((height, width, 3), np.uint8)
    average_image[:] = int_averages

    rgba =cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB)
    ax0=rgba[1,1]
    ax0=[94,49,51]

    R_s = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    G_s = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    B_s = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

    with open("/home/pi/Desktop/IPU training/V1Result.csv", 'a+') as file:
        file.write('\n') 
        file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
        file.write(",")
        file.write(str(q))
        file.write("," +str(R_s) + "," +str(G_s) + "," +str(B_s))        
        file.flush()

    A_b= -math.log((_Sr*R_b + _Sg*G_b + _Sb*B_b)/(_Sr*R_w + _Sg*G_w + _Sb*B_w), 10)
    A_s= -math.log((_Sr*R_s + _Sg*G_s + _Sb*B_s)/(_Sr*R_w + _Sg*G_w + _Sb*B_w), 10)

    A_std = A_s - A_b

    m = q / A_std
    i = q - m * A_std 

    k = 1224.207

    factor = q/A_std

print("Press enter for next test, and enter 'E' to end test")

state = "null"

test_no = 1

while state != "E":

    state = input("Put Test " +str(test_no))

    camera.capture("/dev/shm/image.png", format='png')
    image = cv2.imread('/dev/shm/image.png')

    height, width, _ = np.shape(image)
    avg_color_per_row = np.average(image, axis=0)
    avg_colors = np.average(avg_color_per_row, axis=0)
    int_averages = np.array(avg_colors, dtype=np.uint8)
    average_image = np.zeros((height, width, 3), np.uint8)
    average_image[:] = int_averages

    rgba =cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB)
    ax0=rgba[1,1]
    
    R_samp = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    G_samp = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    B_samp = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)


    A_samp= -math.log((_Sr*R_samp + _Sg*G_samp + _Sb*B_samp)/(_Sr*R_w + _Sg*G_w + _Sb*B_w), 10)
    A_sample = A_samp - A_b
    
    c1 = A_sample * factor
    
    c2 = i + m * A_sample

    print(c1, c2)

    with open("/home/pi/Desktop/IPU training/V1Result.csv", 'a+') as file:
        file.write('\n') 
        file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]) +",")
        file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
        file.flush()

camera.close()

