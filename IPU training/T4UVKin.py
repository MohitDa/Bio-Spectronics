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

GPIO.setup(23,GPIO.OUT,initial = GPIO.LOW)

GPIO.setup(27,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c,1)

chan = AnalogIn(ads, ADS.P0, ADS.P1)
# import matplotlib.pyplot as plt
import Plot
import Backend_codes
# import analyzer
from threading import Thread
from mlx90614_rpi import *

# sample_time = 1 #in min           for how long to take sample images (for developer only, 10 min for testing)
test_time = 1.5 #in min             for how long he test to be run (2 to 4 minutes)
delay_between_images = 60 #in sec  gap between each sample
sample_rest_time = 15	 #time given to sample to rest before test starts. In sec 
lamp_hold_time = 1 #time in sec.

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
#     avg_v = 0
#     print("{:>5}\t{:>5}".format('raw', 'v'))
#     lamp(True)
    sleep(lamp_hold_time)
#     value = chan.value
    value = chan.voltage
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

    # factor= 100/absp

    

    # print('vtd : '+ str ("%5.4f" %(avg_v) +'\t absp :' + str (("%5.4f" %absp)) + '\t factor :' + str (("%5.3f" %factor))))

    #print('vout : '+ str ("%5.3f" %(avg_v) +'\t abs :' + str (("%5.3f" %absp)) + '\t conc :' + str (("%5.3f" %conc))))
    #print('conc : '+ str ("%5.3f" %(conc) +'\t abs :' + str (("%5.3f" %absp))+ '\t abs1 :'+ str (("%5.3f" %absp)) + '\t conc :' + str (("%5.3f" %conc))))
    
    return value

        
def kinatics():
    
    
    while time.time() - sample_mixed_time <= sample_rest_time - lamp_hold_time:
        pass
#     
#     print("process start")
    proess_init_time = time.time()

    i = 0
    
    y = []
    x = []
    while time.time() - proess_init_time <= 60 * test_time:
        
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
#         plot.plot_graph(x, y, "red", "Absorbances")
#         plt.pause(0.01)
#         plt.plot(x,y, color = 'red')
#         plt.pause(0.01)
#         print(y)
        if i >= test_time * 60 / delay_between_images:
            break
        while time.time() - start <= delay_between_images:
            continue
#     plt.show()
#     plot.close_graph()
#     plt.close()
    sum = 0
    
#     with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
#         file.write('\n') 
#         for i in y:
#             file.write(str(i) +",")
#     #         file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
#         file.flush()

    for i in range(0, len(y)-1):
        k = y[i+1] - y[i]
#         print(k)
        sum = sum + k
#             print(k)

    sum /= len(y) - 1
    print(sum)
    
    return sum

def function():
    
    input("Espirte Blank")
#     input("Press Enter when Sample is Mixed")
    global sample_mixed_time
    sample_mixed_time = time.time()
    
    print("motor on")
    while GPIO.input(27) == 0:
        pass
    
    run_pump(1, "forward", 1)
    print("motor off")
    
    lamp(True)
    
    deff_blank = kinatics()
#     deff_blank = read_adc_val()
#     sleep(5)
#     deff_blank = read_adc_val() - deff_blank
    
    print("Espirte Standard")
    q = backend.get_concentration("Standard")
    input("Press Enter when Sample is Mixed")
    sample_mixed_time = time.time()
    
    print("motor on")
    while GPIO.input(27) == 0:
        pass
    
    run_pump(1, "forward", 1)
    print("motor off")
    
    deff_standard = kinatics()
    
    m = q / (deff_standard - deff_blank)
    i = q - m * deff_standard
    
    plot.plot_graph([0,q],[i,i+m*deff_standard], "green", "Concentration")
    plot.close_graph(3)
    
    print("Press enter for next test, and enter 'E' to end test")

    state = "null"

    test_no = 0

    while True:
        
        test_no += 1
        print("Espirte Sample")
        state = input("Put Test " +str(test_no))
        
        if state == 'E' or state == 'e':
            break
        
        try:
            while True:
                
                input("Press Enter when Sample is Mixed")
                sample_mixed_time = time.time()
                
                print("motor on")
                while GPIO.input(27) == 0:
                    pass
                
                run_pump(1, "forward", 1)
                print("motor off")
                
                deff_sample = kinatics()
                
                c1 = i + m * deff_sample
                
                print("concentration: " +str(c1) +" mg/dl")
                break
        
        except:
            print("some error occured")


    lamp(False)

function()