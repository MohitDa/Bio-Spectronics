import time
import board
import busio
import math 

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23,GPIO.OUT,initial = GPIO.LOW)

GPIO.setup(27,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from threading import Thread
from mlx90614_rpi import *
from run_motor import *

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c,1)

chan = AnalogIn(ads, ADS.P0, ADS.P1)

factor1 = 246.72;

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
        

def readAdcVal():
    avg_v = 0
    print("{:>5}\t{:>5}".format('raw', 'v'))
    lamp(True)
    for i in range(0,25):
            
            print("{:>5}\t{:>5.7f}".format(chan.value, chan.voltage))
            avg_v += chan.voltage
            time.sleep(0.2)
    lamp(False)
    avg_v /=  25       
    print("avg_v:"+ str(avg_v))
    
    vzero=4.096
    #factor=149.25
            
    absp= math.log(abs((vzero/avg_v)),10)

    # factor= 100/absp

    

    # print('vtd : '+ str ("%5.4f" %(avg_v) +'\t absp :' + str (("%5.4f" %absp)) + '\t factor :' + str (("%5.3f" %factor))))

    #print('vout : '+ str ("%5.3f" %(avg_v) +'\t abs :' + str (("%5.3f" %absp)) + '\t conc :' + str (("%5.3f" %conc))))
    #print('conc : '+ str ("%5.3f" %(conc) +'\t abs :' + str (("%5.3f" %absp))+ '\t abs1 :'+ str (("%5.3f" %absp)) + '\t conc :' + str (("%5.3f" %conc))))
    
    return absp

# manage_pelt()

while True:
    
    command = input("run ?")
    
    
    if command == "r":
        
        
        while True:
            types = input("s1 : std calc || s2: sample calc : ")
            
            if types == "s1":
                std_val  = int(input("input std concentration : "))
                
                
                print("motor on")
                while GPIO.input(27) == 0:
                    pass
                
                run_pump(1, "forward", 1)
                print("motor off")
                
                lamp(True)
                std_absp = readAdcVal()
                
                factor = std_val/std_absp
                print("factor : " + str(factor) + "  std_absp: " + str(std_absp))
                lamp(False)
                
                
                print("cleansing....")
                print("motor on")
                while GPIO.input(27) == 0:
                    pass
                
                run_pump(1, "forward", 4)
                print("motor off")
                
            else:
                
                
                print("motor on")
                while GPIO.input(27) == 0:
                    pass
                
                run_pump(1, "forward", 1)
                print("motor off")

                lamp(True)
                absp = readAdcVal()
    #             
                print("sample absp : " + str(absp))

                result = factor1 * absp
                lamp(False)
                print("sample conc :" + str(result))
                
                
                print("cleansing....")
                print("motor on")
                while GPIO.input(27) == 0:
                    pass
                
                run_pump(1, "forward", 4)
                print("motor off")
            
        
        
    else:
        print("wrong command")