import sys
sys.path.insert(1, '/backend_algorithms')

from backend_algorithms.mlx90614_rpi import *
from backend_algorithms import helper

from threading import Thread

def set_peltier(type = "null", temp = 0):
    temp_set = [False]

    try:
        print("killing thread")
        t = helper.helper().get_thread()
        print(t)
        print("thread killed")
    except:
        pass
    
    # print(type)
    t1 = Thread()
    if type == "visible":
        t1 = Thread(target=set_peltier_temperature,args=(temp,19,0x5A,temp_set))
        t1.start()
        helper.helper().set_thread(t1)

    elif type == "uv":
        t1 = Thread(target=set_peltier_temperature,args=(temp,18,0x5B,temp_set))
        t1.start()
        helper.helper().set_thread(t1)
    
    print("Setting Peltier Temp")

    while temp_set[0] == False:
        pass
    print("temp set")
    return
