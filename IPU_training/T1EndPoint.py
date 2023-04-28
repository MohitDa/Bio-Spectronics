
#code minimized using function defination

# import cv2
# import numpy as np
# from picamera import PiCamera
from time import sleep
import math
# import matplotlib.pyplot as plt
# import RPi.GPIO as GPIO
# import pandas as pd
# import numpy as np
# import Sens

import Plot
import Backend_codes
import DB
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# 
# GPIO.setup(24,GPIO.OUT,initial = GPIO.LOW)



# camera = PiCamera()
# 
# camera.meter_mode = 'spot'
# camera.exposure_mode = 'spotlight'
# camera.flash_mode = 'off'
# camera.awb_mode = 'cloudy'
# # camera.awb_gains = (-1, -2)
# camera.drc_strength = 'off'
# camera.image_effect = 'none'
# # camera.raw_format = 'rgb'
# # camera.shutter_speed = 31098
# camera.brightness = 50
# camera.ISO = 200
# camera.contrast= 0
# camera.zoom = (0.49, 0.42, 0.1, 0.148)
# camera.shutter_speed = 10000
# # camera.exposure_speed = 1000
# # camera.framerate = 30
# # camera.exposure_compensation = 0
# # camera.digital_gains = 1
# # camera.analog_gain = 0.5
# 
# # camera.start_preview()
# # sleep(3)
# # camera.stop_preview()
# # sleep(5)


from threading import Thread
from mlx90614_rpi import *

# def switch(case):
#     
#     situations_camera = {
#         340 : (0.0,0.0,0.0),
#         492 : (0.0,0.996078431372549,0.984313725490196),
#         405 : (0.3411764705882353,0.0,0.6352941176470588),
#         510 : (0.0,0.9333333333333333,0.4235294117647059),
#         545 : (0.0,0.9490196078431372,0.0),
#         578 : (0.996078431372549,0.996078431372549,0.10980392156862745),
#         630 : (0.9921568627450981,0.054901960784313725,0.17647058823529413)
#         }
# 
#     situations_graph = {
#         340 : (0.0,0.0,0.0),
#         492 : (0.02321,0.79211,0.57657),
#         405 : (0.06644,0.05016,0.47644),
#         510 : (0.03081,0.93695,0.35),
#         545 : (0.03562,0.97196,0.10392),
#         578 : (0.30012,0.77994,0.03964),
#         630 : (0.92292,0.19255,0.19255)
#         }
# 
#     return situations_graph.get(case, situations_graph.get(510))
#     
    
# def get_rgb():
#     GPIO.output(24,GPIO.HIGH)
#     camera.capture("/dev/shm/image.png", format='png')
#     GPIO.output(24,GPIO.LOW)
#     image = cv2.imread('/dev/shm/image.png')
# 
#     height, width, _ = np.shape(image)
#     avg_color_per_row = np.average(image, axis=0)
#     avg_colors = np.average(avg_color_per_row, axis=0)
#     int_averages = np.array(avg_colors, dtype=np.uint16)
# #     average_image = np.zeros((height, width, 3), np.uint8)
#     return int_averages

temp_set = [False]
# print(temp_set)

t1 = Thread(target=set_peltier_temperature,args=(38,19,0x5A,temp_set))
t1.start()

print("Setting Peltier Temp")
# print(temp_set)


while temp_set[0] == False:
    pass

backend = Backend_codes.backend()
plot = Plot.plot()
db = DB.database()
date = backend.get_date()
test = backend.get_test_name(type = "EP")
# print(test)
# 
# table_test_names = db.execute_command('select test_name from tests where type = "EP"' )
# print(table_test_names)

# Sr, Sg, Sb = switch(int(input("Enter filter value. {340, 405, 492, 510, 545, 578, 630}: ")))

# global Sr
# global Sg
# global Sb

R_w, G_w, B_w = 0,0,0

Sr, Sg, Sb = backend.get_sens(name = test)
# Sr, Sg, Sb = 1,1,1
print(Sr, Sg, Sb)

with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
    file.write('\n')
    file.write("Date: " + str(date))
    file.write('\n')
    file.write("Test: " + str(test))
    file.write('\n')
    file.write("r,g,b,val,R,G,B,A")
    file.flush()

m,i= 0,0
unit = 'mg/dl'

if input("Load standard?: y/n ") == 'y':
    
    m,i, R_w, G_w, B_w, unit = backend.get_factor(name = test, water = True)
#     m,i = factor[0], factor[1]
    print(m, i)
else:
    
    input("Put Water")
    # ax0 = [0,0,0]
    # for i in range(10):
    #     ax0 = ax0 + backend.get_rgb()
    # for i in range(3):
    #     ax0[i] = ax0[i] / 10 
    # print(ax0)
    ax0 = backend.get_rgb(save = True, name = "Water")
    R_w = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    G_w = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    B_w = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

    with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
        file.write('\n') 
        file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
        file.write(",")
        file.write("water")
        file.write("," +str(R_w) + "," +str(G_w) + "," +str(B_w))        
        file.flush()
            


    input("Put Blank")
    ax0 = backend.get_rgb(save = True, name = "Blank")
    # ax0 = [0,0,0]
    # for i in range(10):
    #     ax0 = ax0 + backend.get_rgb()
    # for i in range(3):
    #     ax0[i] = ax0[i] / 10 
    # print(ax0)
    R_b = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    G_b = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
    B_b = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

    A_b = 0
    try:
        A_b = -math.log((Sr*R_b + Sg*G_b + Sb*B_b)/(Sr*R_w + Sg*G_w + Sb*B_w), 10)
    except:
        print("some error occured")

    with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
        file.write('\n') 
        file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
        file.write(",")
        file.write("blank")
        file.write("," +str(R_b) + "," +str(G_b) + "," +str(B_b))        
        file.flush()


    input("Put Standard")
    q = backend.get_concentration()

    R_s, G_s, B_s = 0,0,0

    try:
        
        ax0=[]
        while True:
    #         ax0 = [0,0,0]
    #         for i in range(10):
    #             ax0 = ax0 + backend.get_rgb()
    #         for pi in range(3):
    #             ax0[i] = ax0[i] / 10
            ax0 = backend.get_rgb(save = True, name = "Standard")
            R_s = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
            G_s = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
            B_s = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
            
            A_s = -math.log((Sr*R_s + Sg*G_s + Sb*B_s)/(Sr*R_w + Sg*G_w + Sb*B_w), 10)
            A_std = A_s - A_b
            
            m = q / (A_std)
            i = q - m * A_s
#             factor = q/A_std

            backend.set_factor(name = test, m = m, i = i, R_w = R_w, G_w = G_w, B_w = B_w, standard_concentration = q)
    #         print(str(m) +" " +str(i) + " " + str(factor)) 
            plot.plot_graph([0,q],[i,i+m*A_s], "green")
#             plot.plot_graph([0,q],[0,factor* A_std], "blue")
            plot.close_graph(4)
            sleep(0.25)
            break
        
        with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
            file.write('\n') 
            file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
            file.write(",")
            file.write(str(q))
            file.write("," +str(R_s) + "," +str(G_s) + "," +str(B_s))        
            file.flush()
        
    except:
        print("some error occured")
# A_std = -math.log((_Sr*R_s + _Sg*G_s + _Sb*B_s)/(_Sr*R_b + _Sg*G_b + _Sb*B_b), 10)
    

print("Press enter for next test, and enter 'E' to end test")

state = "null"

test_no = 0

while True:
    
    test_no += 1
    state = input("Put Test " +str(test_no))
    
    if state == 'E' or state == 'e':
        break
    
    try:
        R_samp, G_samp, B_samp = 0,0,0
        ax0=[]
        while True:
#             ax0 = [0,0,0]
#             for i in range(10):
#                 ax0 = ax0 + backend.get_rgb()
#             for i in range(3):
#                 ax0[i] = ax0[i] / 10
            ax0 = backend.get_rgb(save = True, name = str(test_no))
            R_samp = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
            G_samp = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
            B_samp = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
            
            A_samp = -math.log((Sr*R_samp + Sg*G_samp + Sb*B_samp)/(Sr*R_w + Sg*G_w + Sb*B_w), 10)
#             

#             A_sample = A_samp - A_b
#             c2 = A_sample * factor
            
            c1 = i + m * A_samp
            
            print("concentration: " +str(c1)  +" " + str(unit)) #+ " " + str(c2)
            break
        
        with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
            file.write('\n') 
            file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]) +",")
            file.write("sample " +str(test_no))
            file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1)) #+ "," + str(c2)   
            file.flush()
    
    except:
        print("some error occured")

