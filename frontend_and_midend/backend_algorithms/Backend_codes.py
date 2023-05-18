import wave
from backend_algorithms import Sens
sens = Sens.data()

from backend_algorithms import DB
db = DB.database()

try:
    import RPi.GPIO as GPIO
    from picamera import PiCamera
    import numpy as np
    import cv2
    from time import sleep
    from PIL import Image


    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(24,GPIO.OUT,initial = GPIO.LOW)

except:
    pass

class backend:
    def get_date(self):
        date = input("Enter Date: ")
        return date
    
    def get_test(self):
        test = input("Enter test name: ")
        return test
    
    def get_sens(self, name = "none", wavelength = 0):
        S = []
        if wavelength != 0:
            return sens.getVal(wavelength)
        
        try:
            if name == "none":
                S = sens.getVal(int(input("Enter filter value. {400, 410, 420, 430,...., 700}: ")))

            else:
                wavelength = db.execute_command('select wavelength from tests where test_name = "' + name +'"')
                S = sens.getVal(wavelength[0])
        except:
            print("Wrong Input")
            return
        
        return S
    
    def get_rgb(self):
        
        camera = PiCamera()
        
        camera.exposure_mode = 'off'
        camera.flash_mode = 'off'
        camera.awb_mode = 'off'
        camera.awb_gains = (3.33, 1.6)
        camera.drc_strength = 'off'
        camera.image_effect = 'none'
        camera.resolution = (320, 240)
        camera.shutter_speed = 32000
        camera.brightness = 45
        camera.ISO = 0
        camera.contrast= 0
        camera.zoom = (0.465, 0.425, 0.1, 0.148)
        
        
#         if save == True:
#             camera.capture("/dev/shm/" +name + ".png", format='png')
#             image = cv2.imread("/dev/shm/" +name + ".png")
#         else:
#         image = np.empty((240, 320, 3), dtype=np.uint8)
#         camera.capture(image, 'rgb')

#         im = Image.fromarray(image, "RGB")
#         im.show()

        GPIO.output(24,GPIO.HIGH)
        sleep(0.25)
#         
        image = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(image, "rgb")
        
#         sleep(0.25)
        GPIO.output(24,GPIO.LOW)

        camera.close()
#         cv2.imshow("image", image)
        # img = Image.fromarray(image, "RGB")
        # img.show()
#         sleep(1)
        # img.close()
        # height, width, _ = np.shape(image)
        avg_color_per_row = np.average(image, axis=0)
        avg_colors = np.average(avg_color_per_row, axis=0)
        int_averages = np.array(avg_colors, dtype=np.uint8)
    #     average_image = np.zeros((height, width, 3), np.uint8)
    #     average_image[:] = int_averages

    #     rgba =cv2.cvtColor(average_image, cv2.COLOR_BGR2RGB)
#         print(int_averages)
        return [int_averages[2],int_averages[1],int_averages[0]], image
    
    def get_concentration(self, sample = ""):
        sample = sample + " "
        q = 0
        while True:
            try:
                q = float(input("Enter " +sample+ "Concentration: "))
                break
            except:
                pass
        
        return q
    
    def get_test_name(self, type = "none"):
        
        if type == "none":
            table_test_names = db.execute_command("select test_name from " +db.table_name)

        else:
            table_test_names = db.execute_command("select test_name from " +db.table_name +' where type ="' +type +'"')
            
        if len(table_test_names) < 1:
            print("table is empty")
            return ""
        
        
        print("Select test. Press y or n: ")
    

        for i in table_test_names:
            while True:
                
                response = input("Select "+str(i)+"? ")
                if response == "y":
                    return str(i)
                    break
#                 print(i)
                elif response == 'n':
                    break
                else:
                    print("wrong input")
        return ""
    
    def get_factor(self, name = "null", water = False):
        
        try:
            m, i, unit = db.execute_command("select m , i , unit from " +db.table_name +' where test_name ="' +name +'"')
            R_w, G_w, B_w = 0,0,0

            if water == True:
                R_w, G_w, B_w = db.execute_command("select R_w, G_w, G_w from "+db.table_name +' where test_name ="' +name +'"')

            return m,i, R_w, G_w, B_w, unit
        except:
            print("error from get_factor()")
            
    def set_factor(self, name = "null", m = 0, i = 0, R_w = 0, G_w = 0, B_w = 0, standard_concentration = 0):
        
        try:
            print("update " +db.table_name +" set m = " +str(m) + ", i = " +str(i) +", R_w = " +str(R_w) + ", G_w = " +str(G_w) +", B_w = " +str(B_w) +", " +db.attributes[11] +" = " +str(standard_concentration) +' where test_name ="' +name +'"')
            
            db.execute_command("update " +db.table_name +" set m = " +str(m) + ", i = " +str(i) +", R_w = " +str(R_w) + ", G_w = " +str(G_w) +", B_w = " +str(B_w) +", " +db.attributes[11] +" = " +str(standard_concentration) +' where test_name ="' +name +'"')
            db.commit()
        except:
            print("error from set_factor()")
                                 
    def set_times(self, name = "null", sample_rest_time = 0, test_time = 0, delay_between_images = 0):
        try:
            print("update " +db.table_name +" set sample_rest_time = " +str(sample_rest_time) + ", test_time = " +str(test_time)  + ", delay_between_images = " +str(delay_between_images) +' where test_name ="' +name +'"')
            
            db.execute_command("update " +db.table_name +" set sample_rest_time = " +str(sample_rest_time) + ", test_time = " +str(test_time)  + ", delay_between_images = " +str(delay_between_images) +' where test_name ="' +name +'"')
            db.commit()
        except:
            print("error from set_times()")
                 
    def get_times(self, name = "null"):
        try:
            
            sample_rest_time, test_time, delay_between_images = db.execute_command("select sample_rest_time, test_time, delay_between_images from " +db.table_name +' where test_name ="' +name +'"')
            return sample_rest_time, test_time, delay_between_images
        
        except:
            print("error from get_factor()")


# backend().get_rgb()

