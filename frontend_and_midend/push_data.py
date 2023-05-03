import MySQLdb as mysql
import datetime
#from iot_camera_test import analyze
#from Swadeshi import spectro_processing
# from testip import testtip


import webbrowser as wb

def push_data(value,flag,testname):
    flag_level = flag
    test_level = value
    # enter your server IP address/domain name
    HOST = "sql.freedb.tech" # or "domain.com"
    # database name, if you want just to connect to MySQL server, leave it empty
    DATABASE = "freedb_patient_details"
    # this is the user you create
    USER = "freedb_Huzefa"
    # user password
    PASSWORD = "u%#*J!!tr@E5Gz7"
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
    patient_age = "25"
    patient_gender = "M"
    patient_mobile = "7218922052"
    patient_testname = testname
    # test_level = triglyceridelevel
    date = datetime.datetime.now()
    patient_id = "TP000" + str(int(float(patient)))
    
    
    
    # if test_level <150 :
    #     flag = 'LOW'
    # elif test_level >200:
    #     flag = 'HIGH'
    # else:
    #     flag = 'NORMAL'
        

    cursor.execute("""insert into patient_details ( patient_id,patient_name,patient_gender, patient_mobile,patient_age,patient_testname, test_level, date, flag) values (
            %s, %s, %s, %s, %s, %s,%s, %s, %s
        )
        """,(patient_id,patient_name,patient_gender, patient_mobile,patient_age,patient_testname, test_level, date, flag_level))
    print("[+] Inserted")
    # commit insertion
    db_connection.commit()
    
    file = open("patient_id.txt",'w')
    file.write(str(patient))
    file.close()
    
    
    wb.open_new_tab('https://patientiot.000webhostapp.com/?patient_id=' + patient_id)
    return "Push complete"
    
# # driver function 
# if __name__=="__main__": 

#     triglyceridelevel,flag = testtip()
    
#     push_data(triglyceridelevel,flag)

#commands to install dependencies:
# sudo apt-get install python-mysql.connector
#pip install --upgrade setuptools
#pip install scikit-build; pip install cmake
#pip2 install opencv-python==4.2.0.32
#pip install scipy

#or directly run the following commands:
#pip install -r requirements.txt




