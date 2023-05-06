from smbus2 import SMBus
from mlx90614 import MLX90614
import time
import os
import RPi.GPIO as IO
from sqlalchemy import null
IO.setwarnings(False)           #do not show any warnings
IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)


bus = SMBus(1)
time.sleep(2)
os.system('i2cdetect -y 1')

#wait here to avoid 121 IO Error



millis = lambda: int(round(time.time() * 1000))

def set_peltier_temperature(set_temperature = 37.0, gpio_pin_no = 18, address_recieved = 0x5A, temp_set = [False]):
    
    global sensor, p

    p = null

    try:
        sensor = MLX90614(bus, address = address_recieved)
        
        IO.setup(gpio_pin_no,IO.OUT)           # initialize GPIO19 as an output.
        # print("c")

        p = IO.PWM(gpio_pin_no,490.27)
        p.start(100)

        p.ChangeDutyCycle(100)
    except:
        pass

    temperature_read = 0.0
    PID_error = 0.0
    previous_error = 0.0
    elapsedTime=0.0
    Time=0.0
    timePrev=0.0
    PID_value=0.0

    #PID constants:
    kp=100.0
    ki=5.6
    kd=5.8
    
    
    maxtemp_error = 45
    mintemp_error = 10
    PID_p = 0.0
    PID_i = 0.0
    PID_d = 0.0

    millis = lambda: int(round(time.time() * 1000))


    while True: #(temperature_read <= set_temperature ):

        #print ("Ambient Temperature :", sensor.get_amb_temp())
#         
        time.sleep(1)
        if temperature_read >= set_temperature - 0.4 and temperature_read <= set_temperature + 0.4:
            temp_set[0] = True
        elif temp_set[0] == False:
            print ("Object Temperature :", sensor.get_obj_temp())
            print(PID_value)
        #First we read the real value of temperature
        temperature_read = sensor.get_obj_temp()
        if temperature_read < mintemp_error or temperature_read > maxtemp_error:
            print("temp or sensor error. try letting peltier cool down")
            p.ChangeDutyCycle(0)
            return
        #Next we calculate the error between the setpoint and the real value
        PID_error = set_temperature - temperature_read
        #Serial.print("PID_error :");
        #Serial.println(PID_error);
        #Calculate the P value
        PID_p = kp * PID_error
        #Calculate the I value in a range on +-3
        if(-10 < PID_error and PID_error < 10):

            PID_i = PID_i + (ki * PID_error)


        #For derivative we need real time to calculate speed change rate
        timePrev = Time                         # the previous time is stored before the actual time read
        Time = millis()                         # actual time read
        elapsedTime = (Time - timePrev) / 1000 
        #Now we can calculate the D calue
        PID_d = kd*((PID_error - previous_error)/elapsedTime)
        #Final total PID value is the sum of P + I + D
        PID_value = PID_p + PID_i + PID_d

        #We define PWM range between 0 and 255
        if(PID_value < 0):
        
            PID_value = 0   

        if(PID_value > 255)  :
        
            PID_value = 255 

        #Now we can write the PWM signal to the mosfet on digital pin D3
        #analogWrite(PWM_pin,255-PID_value)  #255-PID_value
#         print(PID_value)
        p.ChangeDutyCycle(((PID_value)/255)*100)
        #print(((255-PID_value)/255)*100)
        

        previous_error = PID_error     #Remember to store the previous error for next loop.
        time.sleep(0.200)

    p.ChangeDutyCycle(100)

def stop_pwm():
    p.stop()
    print('stopped pwm')
