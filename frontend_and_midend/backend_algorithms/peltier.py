
from mlx90614_rpi import *

from threading import Thread

def set_peltier(type = "null"):
    temp_set = [False]

    print(type)
    if type == "visible":
        # print("a")
        t1 = Thread(target=set_peltier_temperature,args=(38,19,0x5A,temp_set))
        t1.start()
    elif type == "uv":
        # print("b")
        t1 = Thread(target=set_peltier_temperature,args=(38,18,0x5B,temp_set))
        t1.start()
    else:
        print("else")
    
    print("Setting Peltier Temp")

    while temp_set[0] == False:
        pass

    stop_pwm()

# set_peltier(type = "visible")