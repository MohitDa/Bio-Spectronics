import MySQLdb as mysql
import datetime
#from iot_camera_test import analyze
#from Swadeshi import spectro_processing
from testip import testtip


import webbrowser as wb

def push_data(glucoselevel):
    # enter your server IP address/domain name
    HOST = "remotemysql.com" # or "domain.com"
    # database name, if you want just to connect to MySQL server, leave it empty
    DATABASE = "4oVbYEVFyz"
    # this is the user you create
    USER = "4oVbYEVFyz"
    # user password
    PASSWORD = "NoVXHQhyjT"
    # connect to MySQL server
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    #print("Connected to:", db_connection.get_server_info())

    # get the db cursor
    cursor = db_connection.cursor()
    # get database information
    cursor.execute("select database();")
    database_name = cursor.fetchone()
    print("You are connected to the database:", database_name)
    patient=''
   # Python code to illustrate with()
    file =  open("patient_id.txt",'r') 
    patient = file.read()
    file.close()
    patient = int(float(patient))+1
    
    
    patient_name = "Test Patient"
    patient_mobile = "721892205" + str(int(float(patient)))
    patient_glucose = glucoselevel
    date = datetime.datetime.now()
    patient_id = "TP000" + str(int(float(patient)))
    
    if patient_glucose <66 :
        flag = 'LOW'
    elif patient_glucose >99:
        flag = 'HIGH'
    else:
        flag = 'NORMAL'
        

    cursor.execute("""insert into patient_details (patient_name, patient_mobile, patient_glucose, date, patient_id, flag) values (
            %s, %s, %s, %s, %s, %s
        )
        """,(patient_name, patient_mobile, patient_glucose, date, patient_id, flag))
    print("[+] Inserted")
    # commit insertion
    db_connection.commit()
    
    file = open("patient_id.txt",'w')
    file.write(str(patient))
    file.close()
    
    
    wb.open_new_tab('https://patientiot.000webhostapp.com/?patient_id=' + patient_id)

    
# driver function 
if __name__=="__main__": 

    glucoselevel = testtip()
    
    push_data(glucoselevel)

#commands to install dependencies:
# sudo apt-get install python-mysql.connector
#pip install --upgrade setuptools
#pip install scikit-build; pip install cmake
#pip2 install opencv-python==4.2.0.32
#pip install scipy

#or directly run the following commands:
#pip install -r requirements.txt



