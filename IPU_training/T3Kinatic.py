import pandas as pd
import numpy as np
import math
# import cv2
# from picamera import PiCamera
import time
from time import sleep
import math
# import matplotlib.pyplot as plt
import Plot
import Backend_codes
# import analyzer
from threading import Thread
from mlx90614_rpi import *

# import RPi.GPIO as GPIO

# camera = PiCamera()
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# 
# GPIO.setup(24,GPIO.OUT,initial = GPIO.LOW)
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
# camera.resolution = (320, 240)
# 
# GPIO.output(24,GPIO.HIGH)
# camera.start_preview()
# sleep(20)
# camera.sop_preview()
# GPIO.output(24,GPIO.LOW)

# sample_time = 1 #in min           for how long to take sample images (for developer only, 10 min for testing)
test_time = 50 #in sec             for how long he test to be run (2 to 4 minutes)
delay_between_images = 10 #in sec  gap between each sample
sample_rest_time = 0	 #time given to sample to rest before test starts. In sec 

plot = Plot.plot()
backend = Backend_codes.backend()
Sr, Sg, Sb, R_w, G_w, B_w, A_b = 0.0,0.0,0.0,0.0,0.0,0.0,0.0


def kinamatics():
    
    y = []
    x = []
    
    print()
    input("Press Enter when Sample is Mixed")
    sample_mixed_time = time.time()
    
    input("press Enter After Loading Sample")
    while time.time() - sample_mixed_time <= sample_rest_time:
        pass
    print("process start")
    proess_init_time = time.time()

    i = 0
    
    while time.time() - proess_init_time <=  test_time:
        
        i= i + 1
        
        print(i)
        
        start = time.time()
        
    
        ax0=backend.get_rgb() #save = True, name = str(i)
        
        R_samp = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        G_samp = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        B_samp = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
#         print(Sr, Sg, Sb, R_samp, G_samp, B_samp, R_w, G_w, B_w)
        try:
            A_sample= -math.log((Sr*R_samp + Sg*G_samp + Sb*B_samp)/(Sr*R_w + Sg*G_w + Sb*B_w), 10)
        except:
            print("some error  occured")
#         A_sample = -math.log((Sr*R_samp + Sg*G_samp + Sb*B_samp)/(Sr*R_b + Sg*G_b + Sb*B_b), 10)
#         print(A_sample)
        
        with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
            file.write('\n')
            file.write(str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(A_sample))        
            file.flush()

        y.append(A_sample)
        x.append(len(y))
        plot.plot_graph(x, y, "red", "Absorbances")
#         plt.pause(0.01)
#         plt.plot(x,y, color = 'red')
#         plt.pause(0.01)
    
        while time.time() - start <= delay_between_images :
            continue
#     plt.show()
    plot.close_graph(0.5)
#     plt.close()
    sum = 0
    
    with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
        file.write('\n') 
        for i in y:
            file.write(str(i) +",")
    #         file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
        file.flush()

    for i in range(0, len(y)-1):
        k = y[i+1] - y[i]
        sum = sum + k
#             print(k)

    sum /= len(y) - 1
#     print(sum)
    
    return sum



temp_set = [False]
# print(temp_set)

t1 = Thread(target=set_peltier_temperature,args=(38,19,0x5A,temp_set))
t1.start()

print("Setting Peltier Temp")
# print(temp_set)


while temp_set[0] == False:
    pass
#     print(temp_set[0])
# 
# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)



date = backend.get_date()
test = backend.get_test_name(type = "Kinetic")
# Sr, Sg, Sb = switch(int(input("Enter filter value. {340, 405, 492, 510, 545, 578, 630}: ")))

R_w, G_w, B_w = 0,0,0

Sr, Sg, Sb = backend.get_sens(name = test)
# Sr, Sg, Sb = 1,1,1
print(Sr, Sg, Sb)

with open("/home/pi/Desktop/IPU training/KinaticResult.csv", 'a+') as file:
    file.write('\n')
    file.write("Date: " + str(date))
    file.write('\n')
    file.write("Test: " + str(test))
    file.write('\n')
    file.write("val,R,G,B")
    file.flush()


m,i= 0,0
unit = 'mg/dl'

sample_rest_time, test_time, delay_between_images = backend.get_times(name = test)

while True:
    responce = input("Load standard, timigs?: y/n ")
    if responce == 'y':
        
        m,i, R_w, G_w, B_w, unit = backend.get_factor(name = test, water = True)
    #     global sample_rest_time, test_time
        
        
    #     m,i = factor[0], factor[1]
#         print(m, i)
        break
        
    elif responce == 'n':
        if input("Set Timings?: y/n ") == 'y':
    #         global sample_rest_time
    #         global test_time
            while True:
                try:
                    sample_rest_time = int(input("Initial Reading Time (rest time) (in seconds): "))
                    delay_between_images = int(input("Delay Between Images (in seconds): "))
                    test_time = int(input("Test Time (in seconds): "))
                    print(sample_rest_time, test_time, delay_between_images)
                    backend.set_times(name = test, sample_rest_time = sample_rest_time, delay_between_images = delay_between_images, test_time = test_time)
                    break
                except:
                    print("enter correct values")
                    pass
        
        print(sample_rest_time, test_time, delay_between_images)


    
        input("Put Water")
        ax0 = backend.get_rgb(save = True, name = "Water")

        R_w = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        G_w = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        B_w = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

        with open("/home/pi/Desktop/IPU training/KinaticResult.csv", 'a+') as file:
            file.write('\n') 
        #         file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
        #         file.write(",")
            file.write("water")
            file.write("," +str(R_w) + "," +str(G_w) + "," +str(B_w))        
            file.flush()
                


        input("Put Blank")
        ax0=backend.get_rgb(save = True, name = "Blank")

        R_b = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        G_b = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        B_b = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

        A_b = 0
        try:
            A_b = -math.log((Sr*R_b + Sg*G_b + Sb*B_b)/(Sr*R_w + Sg*G_w + Sb*B_w), 10)
        except:
            print("some error occured")
            
        with open("/home/pi/Desktop/IPU training/KinaticResult.csv", 'a+') as file:
            file.write('\n') 
        #         file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
        #         file.write(",")
            file.write("blank")
            file.write("," +str(R_b) + "," +str(G_b) + "," +str(B_b))        
            file.flush()


        input("Put Standard")

        q = backend.get_concentration()

        R_s, G_s, B_s = 0,0,0

        with open("/home/pi/Desktop/IPU training/KinaticResult.csv", 'a+') as file:
            file.write('\n') 
            file.write(str(q))
            file.flush()
            
        with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
            file.write('\n') 
            file.write("std: " +str(q) +",")
            file.flush()
        sum = kinamatics()
        #     plt.show()
        #     plt.close()
        m = q / sum
        i = q - m * sum
        
        backend.set_factor(name = test, m = m, i = i, R_w = R_w, G_w = G_w, B_w = B_w, standard_concentration = q)
    #     factor = q/sum


        plot.plot_graph([0,q],[i,i+m*sum], "green", "y = mx + c")
    #     plot.plot_graph([0,q],[0,factor * sum], "blue", "factor")
        plot.close_graph(4)
        sleep(0.25)
        with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
            file.write(str(sum) + "," + str(m) + "," + str(i))        
            file.flush()
            
        break
            
    else:
        print("wrong input")
        
print("Press enter for next test, and enter 'E' to end test")
print("")
state = "null"

test_no = [1]


while True:
    
    state = input("Put Test " +str(test_no[0]))
    test_no[0] += 1
    
    if state == 'E' or state == 'e':
        break
    
    with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
        file.write('\n') 
#         file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]) +",")
        file.write("sample " +str(test_no[0]))
#         file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
        file.flush()
    
    sum = kinamatics()
#         plt.show()
#         plt.close()
    
#     c1 = sum * factor
    
    c1 = i + m * sum

    print("Concentration: "+ str(c1) +" " + str(unit))

    
    with open("/home/pi/Desktop/IPU training/KinaticResult.csv", 'a+') as file:
        file.write('\n') 
#         file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]) +",")
        file.write("sample " +str(test_no[0]) +"," +str(c1))
#         file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
        file.flush()

camera.close()

t1.join()


