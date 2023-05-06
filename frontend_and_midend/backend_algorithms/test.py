import sys, time, math
from threading import Thread

sys.path.insert(1, '/backend_algorithms')

from backend_algorithms.mlx90614_rpi import *

from backend_algorithms import Backend_codes, Plot, peltier, DB

db = DB.database()
plot = Plot.plot()
backend = Backend_codes.backend()

edit_test = dict(test_id = "", test_name = "" , test_type = "" , test_temp = "" , test_wavelength = "" , test_unit = "" , test_result_low = "" , test_result_high = "" , test_sample_rest_time = "" , test_test_time = "" , test_delay_between_images = "" , test_standard_concentration = "")

def perform_test(test):

    print(test.test_name)
    global S_r, S_g, S_b
    S_r, S_g, S_b = backend.get_sens(wavelength = test.wavelength)

    sample_rest_time = 0	 #time given to sample to rest before test starts. In sec 
    delay_between_images = 0 #in sec  gap between each sample
    test_time = 0 #in sec             for how long he test to be run (2 to 4 minutes)
    

    # stmt = "select * from new_tests where test_id = " +str(test_id)
    # list = db.execute_command(stmt)
    # global test_time, sample_rest_time, delay_between_images
    if test.type == "EP":

        sample_rest_time = test.sample_rest_time	 #time given to sample to rest before test starts. In sec 
        delay_between_images = 0 #in sec  gap between each sample
        test_time = delay_between_images + 1 #in sec             for how long he test to be run (2 to 4 minutes)
    elif test.type == "TP":

        sample_rest_time = test.sample_rest_time	 #time given to sample to rest before test starts. In sec 
        delay_between_images = test.delay_between_images #in sec  gap between each sample
        test_time = (delay_between_images * 2) + 1 #in sec             for how long he test to be run (2 to 4 minutes)
    elif test.type == "Kinetic":

        sample_rest_time = test.sample_rest_time	 #time given to sample to rest before test starts. In sec 
        delay_between_images = test.delay_between_images #in sec  gap between each sample
        test_time = test.test_time + 1#in sec             for how long he test to be run (2 to 4 minutes)
    
        
    print(test_time, delay_between_images, sample_rest_time)

    R_w, G_w, B_w = test.R_w, test.G_w, test.B_w

    peltier.set_peltier(type = "visible", temp = test.temp)

    return kinetic(R_w = R_w, G_w = G_w, B_w = B_w, test_time = test_time, sample_rest_time = sample_rest_time, delay_between_images = delay_between_images)


def kinetic(R_w = 0, G_w = 0, B_w = 0, test_time = 0, sample_rest_time = 0, delay_between_images = 0):
    
    y = []
    x = []
    
    print()
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
        
        print(i)
        
        start = time.time()
        
    
        ax0=backend.get_rgb() #save = True, name = str(i)
        
        R_samp = ax0[2]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        G_samp = ax0[1]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        B_samp = ax0[0]/((ax0[0]**2 + ax0[1]**2 + ax0[2]**2)**0.5)
        print(S_r, S_g, S_b, R_samp, G_samp, B_samp, R_w, G_w, B_w)
        try:
            print((S_r*R_samp + S_g*G_samp + S_b*B_samp)/(S_r*R_w + S_g*G_w + S_b*B_w))
            A_sample= -math.log((S_r*R_samp + S_g*G_samp + S_b*B_samp)/(S_r*R_w + S_g*G_w + S_b*B_w), 10)
            
        except:
            print("some error  occured")
#         A_sample = -math.log((Sr*R_samp + Sg*G_samp + Sb*B_samp)/(Sr*R_b + Sg*G_b + Sb*B_b), 10)
#         print(A_sample)
        
        # with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
        #     file.write('\n')
        #     file.write(str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(A_sample))        
        #     file.flush()

        y.append(A_sample)
        x.append(len(y))
        # plot.plot_graph(x, y, "red", "Absorbances")
        # plot.close_graph(3)
#         plt.pause(0.01)
#         plt.plot(x,y, color = 'red')
#         plt.pause(0.01)
    
        while time.time() - start <= delay_between_images :
            continue
#     plt.show()
    # plot.close_graph(0.5)
#     plt.close()
    sum = 0
    
    # with open("/home/pi/Desktop/IPU training/KinaticTestData.csv", 'a+') as file:
    #     file.write('\n') 
    #     for i in y:
    #         file.write(str(i) +",")
    # #         file.write("," +str(R_samp) + "," +str(G_samp) + "," +str(B_samp) + "," + str(c1) + "," + str(c2))   
    #     file.flush()

    if len(y) <= 1:
        print(y)
        return y[0]
    else:
        for i in range(0, len(y)-1):
            k = y[i+1] - y[i]
            sum = sum + k
#             print(k)

        sum /= len(y) - 1
    #     print(sum)
        
        return sum