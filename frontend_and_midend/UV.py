import time
import board
import busio
import math 
import RPi.GPIO as GPIO

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c,1)

# Create single-ended input on channel 0
#chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1


chan = AnalogIn(ads, ADS.P0, ADS.P1)


# print("{:>5}\t{:>5.5f}".format(chan.value, chan.voltage))
# while True:
#     print("{:>5}\t{:>5.5f}".format(chan.value, chan.voltage))
#     time.sleep(0.5)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(26,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(19,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(6,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(13,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(16,GPIO.OUT,initial = GPIO.LOW)
factor1 = 246.72;

def readAdcVal():
    avg_v = 0
    print("{:>5}\t{:>5}".format('raw', 'v'))
    for i in range(0,25):
            
            print("{:>5}\t{:>5.7f}".format(chan.value, chan.voltage))
            avg_v += chan.voltage
            time.sleep(0.2)
    avg_v /=  25       
    print("avg_v:"+ str(avg_v))
    
    vzero=4.096
    #factor=149.25
            
    absp= math.log((vzero/avg_v),10)

    # factor= 100/absp

    

    # print('vtd : '+ str ("%5.4f" %(avg_v) +'\t absp :' + str (("%5.4f" %absp)) + '\t factor :' + str (("%5.3f" %factor))))

    #print('vout : '+ str ("%5.3f" %(avg_v) +'\t abs :' + str (("%5.3f" %absp)) + '\t conc :' + str (("%5.3f" %conc))))
    #print('conc : '+ str ("%5.3f" %(conc) +'\t abs :' + str (("%5.3f" %absp))+ '\t abs1 :'+ str (("%5.3f" %absp)) + '\t conc :' + str (("%5.3f" %conc))))
    
    return absp

while True:
    
    command = input("run ?")
    
    
    if command == "r":
        
        GPIO.setup(16,GPIO.OUT,initial = GPIO.HIGH)
        while True:
            types = input("s1 : std calc || s2: sample calc : ")
            if types == "s1":
                std_val  = int(input("input std concentration : "))
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(6,GPIO.HIGH)
                print("motor on")
                time.sleep(0.3) #respiration delay
                
                GPIO.output(26,GPIO.LOW)
                GPIO.output(6,GPIO.LOW)
                
                print("motor off")


                std_absp = readAdcVal()
                
                factor = std_val/std_absp
                print("factor : " + str(factor) + "  std_absp: " + str(std_absp))
                
                
                
                print("cleansing....")
                time.sleep(1)
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(6,GPIO.HIGH)
                print("motor on")
                time.sleep(3)  ##cleansing delay
                GPIO.output(26,GPIO.LOW)
                GPIO.output(6,GPIO.LOW)
                print("motor off")
                
            else:
                
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(6,GPIO.HIGH)
                print("motor on")
                time.sleep(0.3)               ####respiration delay
                GPIO.output(26,GPIO.LOW)
                GPIO.output(6,GPIO.LOW)
                print("motor off")


                absp = readAdcVal()
    #             
                print("sample absp : " + str(absp))

                result = factor1 * absp
                
                print("sample conc :" + str(result))
                
                
                
                
                
                
                print("cleansing....")
                time.sleep(1)
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(6,GPIO.HIGH)
                print("motor on")
                time.sleep(3)  #cleansing delay
                GPIO.output(26,GPIO.LOW)
                GPIO.output(6,GPIO.LOW)
                print("motor off") 
            
        
        
    else:
        print("wrong command")