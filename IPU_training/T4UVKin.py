import pandas as pd
import numpy as np
import math
from run_motor import *
# import cv2
# from picamera import PiCamera
import time
import math
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23,GPIO.OUT,initial = GPIO.HIGH)

GPIO.setup(27,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c,1)

chan = AnalogIn(ads, ADS.P0)
# import matplotlib.pyplot as plt
import Plot
import Backend_codes
# import analyzer
from threading import Thread
from mlx90614_rpi import *

# sample_time = 1 #in min           for how long to take sample images (for developer only, 10 min for testing)
test_time = 90 #in sec             for how long he test to be run (2 to 4 minutes)
delay_between_absorbancs = 60 #in sec  gap between each sample
sample_rest_time = 30	 #time given to sample to rest before test starts. In sec 
lamp_hold_time = 1 #time in sec.

vblank= 0.50
vdark=0.0936

plot = Plot.plot()
backend = Backend_codes.backend()

def manage_pelt():
    
    temp_set = [False]
    t1 = Thread(target=set_peltier_temperature,args=(38,18,0x5B,temp_set))
    t1.start()

    print("Setting Peltier Temp")

    while temp_set[0] == False:
        pass

def lamp(state = False):
    if state == True:
        GPIO.output(23, GPIO.HIGH)
    else:
        GPIO.output(23, GPIO.LOW)
        
def read_adc_val():
    
#     print("{:>5}\t{:>5.7f}".format(chan.value, chan.voltage))
    
#     od=round(2-math.log(((100*(chan.voltage/vemp))),10),3)
#     od = round(chan.voltage, 3)
#     print(od)
#     time.sleep(1)
#     avg_v = 0
#     print("{:>5}\t{:>5}".format('raw', 'v'))
#     lamp(True)
#     sleep(lamp_hold_time)
#     value = chan.value

    value = []
    for i in range(50):
        value.append(chan.value)
#     print(value)
#     print(value)
#     print(value)
    
#     for i in range(0,25):
#             
#             print("{:>5}\t{:>5.7f}".format(chan.value, chan.voltage))
#             avg_v += chan.voltage
#             time.sleep(0.2)
#     lamp(False)
#     avg_v /=  25       
#     print("avg_v:"+ str(avg_v))
#     
#     vzero=4.096
#     #factor=149.25
#             
#     absp= math.log(abs((vzero/avg_v)),10)
#     print ("a")
    average = sum(value)/len(value)
    print("Average ADC: "+ str(average))
    od = round(- math.log((average/vblank),10), 3) #2-math.log(((100*(average/vblank))),10)
    print ("od: "+ str(od))
    # factor= 100/absp

    

    # print('vtd : '+ str ("%5.4f" %(avg_v) +'\t absp :' + str (("%5.4f" %absp)) + '\t factor :' + str (("%5.3f" %factor))))

    #print('vout : '+ str ("%5.3f" %(avg_v) +'\t abs :' + str (("%5.3f" %absp)) + '\t conc :' + str (("%5.3f" %conc))))
    #print('conc : '+ str ("%5.3f" %(conc) +'\t abs :' + str (("%5.3f" %absp))+ '\t abs1 :'+ str (("%5.3f" %absp)) + '\t conc :' + str (("%5.3f" %conc))))
#     return 
    return od

        
def kinetic():
    
    
    while time.time() - sample_mixed_time <= sample_rest_time:
        pass
#     
#     print("process start")
    proess_init_time = time.time()

    i = 0
    
    y = []
    x = []
    while time.time() - proess_init_time <=  test_time:
        
        i= i + 1
        
        print(i)
        
        start = time.time()
        
        value = 0
        try:
            value = read_adc_val()
        except:
            print("some error occured")
        
#         with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
#             file.write('\n')
#             file.write(str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(A_sample))        
#             file.flush()

        y.append(value)
        x.append(len(y))
        plot.plot_graph(x, y, "red", "Absorbances")
#         plt.pause(0.01)
#         plt.plot(x,y, color = 'red')
#         plt.pause(0.01)
#         print(y)
        if i >= test_time / delay_between_absorbancs:
            break
        while time.time() - start <= delay_between_absorbancs:
            continue
#     plt.show()
    plot.close_graph(3)
#     plt.close()
    sum = 0
    
#     with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
#         file.write('\n') 
#         for i in y:
#             file.write(str(i) +",")
#     #         file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
#         file.flush()
#     print(y)
    if len(y) <= 1:
        print(y[0])
        return round(y[0], 3)
        
    else:
        count = 0
        for i in range(0, len(y)-1):
            k = y[i+1] - y[i]
            print(k)
            if k <= 0:
                count += 1
                sum = sum + k
#                 print("sum: " +str(sum))
#             print(k)
#         print(sum)
        average = round(sum / count , 3)
        print("average of differences: "+ str(average))
        
        return average

def function():
    
    print("Aspirate Blank")
#     input("Press Enter when Sample is Mixed")
    global sample_mixed_time
    
    print("motor on")
    while GPIO.input(27) == 0:
        pass
    
    sample_mixed_time = time.time()
    
    run_pump(1, "forward", 1.3)
    print("motor off")
    
    lamp(True)
    global vblank
    
    value = []
    for i in range(50):
        value.append(chan.value)
    vblank = sum(value)/len(value)
    
    
    deff_blank = kinetic()
    run_pump(1, "forward", 0.2)
#     deff_blank = read_adc_val()
#     sleep(5)
#     deff_blank = read_adc_val() - deff_blank
    
    print("Aspirate Standard")
    q = backend.get_concentration("Standard")
    input("Press Enter when Sample is Mixed")
    sample_mixed_time = time.time()
    
    print("motor on")
    while GPIO.input(27) == 0:
        pass
    
    run_pump(1, "forward", 1.3)
    print("motor off")
    
    deff_standard = kinetic()
    
    run_pump(1, "forward", 0.2)
    
    m = q / (deff_standard - deff_blank)
    i = q - m * deff_standard
    
    plot.plot_graph([0,q],[i,i+m*deff_standard], "green", "Concentration")
    plot.close_graph(3)
    
    print("Press enter for next test, and enter 'E' to end test, and 'C' to clean ")

    state = "null"

    test_no = 0

    while True:
        
       
        state = input("Put Test " +str(test_no))
        
        if state == 'C' or state == 'c':
            print("Aspirate Water")
            print("motor on")
            while GPIO.input(27) == 0:
                pass
            
            sample_mixed_time = time.time()
            
            run_pump(1, "forward",5)
            continue
        
        
        elif state == 'E' or state == 'e':
            break
        
        try:
            test_no += 1
            print("Aspirate Sample")
            while True:
                
                
                input("Press Enter when Sample is Mixed")
                sample_mixed_time = time.time()
                
                print("motor on")
                while GPIO.input(27) == 0:
                    pass
                
                run_pump(1, "forward", 1.3)
                print("motor off")
                
                deff_sample = kinetic()
                
                
                run_pump(1, "forward", 0.2)
                
                c1 = round(i + m * deff_sample, 3)
                
                print("concentration: " +str(c1) +" mg/dl")
                break
        
        except:
            print("some error occured")


    lamp(False)
    
    
# temp_set = [False]
# # print(temp_set)
# 
# t1 = Thread(target=set_peltier_temperature,args=(38,18,0x5B,temp_set))
# t1.start()
# 
# print("Setting Peltier Temp")
# # print(temp_set)
# 
# 
# while temp_set[0] == False:
#     pass

function()