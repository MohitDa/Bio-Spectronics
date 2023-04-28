import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import Plot
from run_motor import *
plot = Plot.plot()

from threading import Thread
from mlx90614_rpi import *
GPIO.setup(27,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


GPIO.setup(23,GPIO.OUT,initial = GPIO.LOW)
def lamp(state = False):
    if state == True:
        GPIO.output(23, GPIO.HIGH)
    else:
        GPIO.output(23, GPIO.LOW)
        
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c,1)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1

vzero= 0.50 #1.41
vdark=0.0936

#chan = AnalogIn(ads, ADS.P0, ADS.P1)

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


print("{:>5}\t{:>5}".format('raw', 'v'))
od = []
x = []
# for i in range(180):
#     x.append(i)
# x = [1,2]
lamp(True)

print("motor on")
while GPIO.input(27) == 0:
    pass
    
run_pump(1, "forward", 1)
print("motor off")
# t1.join()

while True:
    val = 2-math.log(((100*(chan.voltage/vzero))),10)
    od.append(val)
    if GPIO.input(27) == 1:
        run_pump(1, "forward", 1)
    print("{:>5}\t{:>5.7f}\t{:>5.2f}".format(chan.value, chan.voltage,val))
    x.append(len(od))
    plot.plot_graph(x, od)
#     print(od)
    time.sleep(2)
lamp(False)


