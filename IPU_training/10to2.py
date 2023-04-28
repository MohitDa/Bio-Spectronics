import pandas as pd
import numpy as np
import math
import cv2
from picamera import PiCamera
import time
import math
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import Sens

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.OUT,initial = GPIO.LOW)

camera = PiCamera()

camera.meter_mode = 'spot'
camera.exposure_mode = 'spotlight'
camera.flash_mode = 'off'
camera.awb_mode = 'cloudy'
# camera.awb_gains = (-1, -2)
camera.drc_strength = 'off'
camera.image_effect = 'none'
# camera.raw_format = 'rgb'
# camera.shutter_speed = 31098
camera.brightness = 50
camera.ISO = 200
camera.contrast= 0
camera.zoom = (0.49, 0.42, 0.1, 0.148)
camera.shutter_speed = 10000

sample_time = 3 #in min           for how long to takwe sample images (for developer only, 10 min for testing)
test_time = 3 #in min             for how long he test to be run (2 to 4 minutes)
prediction_time = 10 #in           min  predict absorbance value after this much time 
delay_between_images = 4 #in sec  gap between each sample
# camera.digital_gains = 1
# camera.analog_gain = 0.5

# camera.start_preview()
# sleep(3)
# camera.stop_preview()
def switch(case):
    
    situations_camera = {
        340 : (0.0,0.0,0.0),
        492 : (0.0,0.996078431372549,0.984313725490196),
        405 : (0.3411764705882353,0.0,0.6352941176470588),
        510 : (0.0,0.9333333333333333,0.4235294117647059),
        545 : (0.0,0.9490196078431372,0.0),
        578 : (0.996078431372549,0.996078431372549,0.10980392156862745),
        630 : (0.9921568627450981,0.054901960784313725,0.17647058823529413)
        }

    situations_graph = {
        340 : (0.0,0.0,0.0),
        492 : (0.02321,0.79211,0.57657),
        405 : (0.06644,0.05016,0.47644),
        510 : (0.03081,0.93695,0.35),
        545 : (0.03562,0.97196,0.10392),
        578 : (0.30012,0.77994,0.03964),
        630 : (0.92292,0.19255,0.19255)
        }

    return situations_graph.get(case, situations_graph.get(510))
    
    
def get_rgb():
    GPIO.output(24,GPIO.HIGH)
    camera.capture("/dev/shm/image.png", format='png')
    GPIO.output(24,GPIO.LOW)
    image = cv2.imread('/dev/shm/image.png')

    height, width, _ = np.shape(image)
    avg_color_per_row = np.average(image, axis=0)
    avg_colors = np.average(avg_color_per_row, axis=0)
    int_averages = np.array(avg_colors, dtype=np.uint8)
#     average_image = np.zeros((height, width, 3), np.uint8)
#     average_image[:] = int_averages

#     rgba =cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB)
#     print(int_averages)
    return int_averages

time.sleep(3)

date = input("Enter Date: ")
test = input("Enter test name: ")
# _Sr, _Sg, _Sb = switch(int(input("Enter filter value. {340, 405, 492, 510, 545, 578, 630}: ")))
sensitivity = Sens.data()
_Sr, _Sg, _Sb = sensitivity.getVal(int(input("Enter filter value. {400 to 700}: "))) #Sensoitivity data

# print(_Sr, _Sg, _Sb)

with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
    file.write('\n')
    file.write("Date: " + str(date))
    file.write('\n')
    file.write("Test: " + str(test))
    file.write('\n')
    file.write("r,g,b,val,R,G,B,A")
    file.flush()
    
input("Put Water")
ax0 = get_rgb()

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
ax0=get_rgb()

R_b = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
G_b = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
B_b = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

A_b = -math.log((_Sr*R_b + _Sg*G_b + _Sb*B_b)/(_Sr*R_w + _Sg*G_w + _Sb*B_w), 10)

with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
    file.write('\n') 
    file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
    file.write(",")
    file.write("blank")
    file.write("," +str(R_b) + "," +str(G_b) + "," +str(B_b))        
    file.flush()


input("Put Standard")
q = float(input("Enter Concentration: "))

ax0=get_rgb()

R_s = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
G_s = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
B_s = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)

with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
    file.write('\n') 
    file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]))  
    file.write(",")
    file.write(str(q))
    file.write("," +str(R_s) + "," +str(G_s) + "," +str(B_s))        
    file.flush()

A_s = -math.log((_Sr*R_s + _Sg*G_s + _Sb*B_s)/(_Sr*R_w + _Sg*G_w + _Sb*B_w), 10)
# A_std = -math.log((_Sr*R_s + _Sg*G_s + _Sb*B_s)/(_Sr*R_b + _Sg*G_b + _Sb*B_b), 10)
A_std = A_s - A_b
m = q / (A_std)  #slope
i = q - m * A_s        #intercept

factor = q/A_std       #factor

print("Press enter for next test, and enter 'E' to end test")

state = "null"

test_no = 0

with open("/home/pi/Desktop/IPU training/2to10rgb.csv", 'a+') as file:
    file.write('\n')
    file.write("Date: " + str(date))
    file.write('\n')
    file.write("Test: " + str(test))
    file.write('\n')
    file.write("r,g,b,val,r,g,b,a")
    file.flush()

while True:
    with open("/home/pi/Desktop/IPU training/2to10rgb.csv", 'a+') as file:
        file.write('\n')
        file.write("Test: " + str(test_no))
        file.flush()
    
    array = []
    index = []
    test_no += 1
    state = input("Put Test " +str(test_no))
    
    if state == 'E' or state == 'e':
        break
    
    proess_init_time = time.time()

    i = 0;

    while time.time() - proess_init_time <= 60 * sample_time:
        
        i= i + 1;
        
        print(i)
        
        start = time.time()
        
    
        ax0=get_rgb()
        
        
        R_samp = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        G_samp = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        B_samp = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)


        A_samp= -math.log((_Sr*R_samp + _Sg*G_samp + _Sb*B_samp)/(_Sr*R_w + _Sg*G_w + _Sb*B_w), 10)
        A_sample = A_samp - A_b
        
        with open("/home/pi/Desktop/IPU training/2to10rgb.csv", 'a+') as file:
            file.write('\n')
            file.write(str(ax0[2]) + "," + str(ax0[1]) + "," + str(ax0[0]) + "," + str(A_sample))
            file.flush()
#         print(A_sample)
        
        array.append(A_sample)
        index.append(len(array))
        
#         c1 = A_sample * factor
#         
#         c2 = i + m * A_sample
# 
#         print(c1, c2)
# 
#         with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
#             file.write('\n') 
#             file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]) +",")
#             file.write("sample " +str(test_no))
#             file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
#             file.flush()
    
        while time.time() - start <= delay_between_images :
            continue
        
    y=np.array(array[0:int(60 * test_time/delay_between_images)])
#     print(y)
    x=np.array(index[0:int(60 * test_time/delay_between_images)])


    x_float=x.astype("float")
    y_float=y

    log_x = np.log10(x_float)
    log_y = np.log10(y_float)


    x1=np.array(log_x)
    y1=np.array(log_y)


    #create scatterplot
#     plt.scatter(x1, y1)

    #calculate equation for trendline
    z = np.polyfit(x1, y1, 1)
    p = np.poly1d(z)

    #add trendline to plot
#     q = plt.plot(x1, p(x1))

#     print(z)

    y = math.pow(10,z[0]*math.log10(60 * prediction_time/delay_between_images)+(z[1]))
    with open("/home/pi/Desktop/IPU training/2to10rgb.csv", 'a+') as file:
        file.write('\n')
        file.write(str(y))
        file.flush()
            
    c1 = y * factor
    
    c2 = i + m * y

    print(y, c1, c2)

#     print("y= ",y)
    
    with open("/home/pi/Desktop/IPU training/V2Result.csv", 'a+') as file:
        file.write('\n') 
#         file.write(str(ax0[0]) + "," + str(ax0[1]) + "," +str(ax0[2]) +",")
        file.write("sample " +str(test_no) +"," +str(c1) +"," +str(c2))
#         file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
        file.flush()

camera.close()



# two min to ten
#code minimized using function defination






