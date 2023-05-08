import sys
sys.path.insert(1, '/backend_algorithms')

from backend_algorithms.mlx90614_rpi import *

from threading import Thread

def set_peltier(type = "null", temp = 0):
    temp_set = [False]

    print(type)
    if type == "visible":
        t1 = Thread(target=set_peltier_temperature,args=(temp,19,0x5A,temp_set))
        t1.start()

    elif type == "uv":
        t1 = Thread(target=set_peltier_temperature,args=(temp,18,0x5B,temp_set))
        t1.start()
        
    else:
        print("else")
    
    print("Setting Peltier Temp")

    while temp_set[0] == False:
        pass

    return

    

