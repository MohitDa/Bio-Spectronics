import sys, time, math
from threading import Thread

sys.path.insert(1, '/backend_algorithms')

from backend_algorithms.mlx90614_rpi import *

from backend_algorithms import Backend_codes, Plot, peltier, DB

db = DB.database()                  # DB functions
plot = Plot.plot()                  # graph plot functions
backend = Backend_codes.backend()   # camera and other

def perform_test(test):
    # print("Hello")
    # print(test.test_name)
    global S_r, S_g, S_b            # Sensitivity of R, G and B pixals at perticular wavelength
    S_r, S_g, S_b = backend.get_sens(wavelength = test.wavelength)

    sample_rest_time = 0            	 #in sec  time given to sample to rest before test starts
    delay_between_images = 0             #in sec  gap between each sample
    test_time = 0                        #in sec  total test time
    

    if test.type == "EP":

        sample_rest_time = test.sample_rest_time	
        delay_between_images = 0                  
        test_time = delay_between_images + 1    
    elif test.type == "TP":

        sample_rest_time = test.sample_rest_time	 
        delay_between_images = test.delay_between_images
        test_time = (delay_between_images * 2) + 1
    elif test.type == "Kinetic":

        sample_rest_time = test.sample_rest_time	
        delay_between_images = test.delay_between_images 
        test_time = test.test_time + 1 
    
        
    # print(test_time, delay_between_images, sample_rest_time)

    R_w, G_w, B_w = test.R_w, test.G_w, test.B_w

    return kinetic(R_w = R_w, G_w = G_w, B_w = B_w, test_time = test_time, sample_rest_time = sample_rest_time, delay_between_images = delay_between_images)


def kinetic(R_w = 0, G_w = 0, B_w = 0, test_time = 0, sample_rest_time = 0, delay_between_images = 0):
    
    y = []                  # for calculations
    x = []                  # for graph plot
    
    # print()
    # input("Press Enter when Sample is Mixed")
    sample_mixed_time = time.time()
    
    # input("press Enter After Loading Sample")
    while time.time() - sample_mixed_time <= sample_rest_time:
        pass
    print("process start")
    proess_init_time = time.time()

    i = 0
    
    while time.time() - proess_init_time <=  test_time:
        
        i= i + 1
        
        # print(i)
        
        start = time.time()
        
    
        ax0=backend.get_rgb() #save = True, name = str(i)
        
        R_samp = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        G_samp = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        B_samp = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        print(S_r, S_g, S_b, R_samp, G_samp, B_samp, R_w, G_w, B_w)
        try:
            print((S_r*R_samp + S_g*G_samp + S_b*B_samp)/(S_r*R_w + S_g*G_w + S_b*B_w))
            A_sample= -math.log((S_r*R_samp + S_g*G_samp + S_b*B_samp)/(S_r*R_w + S_g*G_w + S_b*B_w), 10)
            
            y.append(A_sample)
            x.append(len(y))
        
            while time.time() - start <= delay_between_images :
                continue
        except:
            print("some error occured")

        
    sum = 0
    

    if len(y) <= 1:
        print(y)
        return y[0]
    else:
        for i in range(0, len(y)-1):
            k = y[i+1] - y[i]
            sum = sum + k

        sum /= len(y) - 1
        
        return sum