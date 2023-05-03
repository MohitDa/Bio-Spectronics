import sqlite3 as sql

conn = sql.connect("")

class database:
    
    attributes = ['primary_key', 'test_name', 'type', 'temp', 'wavelength', 'unit', 'result_low', 'result_high', 'sample_rest_time', 'test_time', 'delay_between_images', "standard_concentration", 'm', 'i']
    attributes_type = {'primary_key' : "int", 'test_name' : "text", 'type' : "text", 'temp' : "int", 'wavelength' : "int", 'unit' : "text", 'result_low' : "int", 'result_high' : "int", 'sample_rest_time' : "int", 'test_time' : "float", 'delay_between_images' : "int", "standard_concentration" : "float", 'm' : "float", 'i' : "float"}
    attributes_string = "primary_key, test_name, type, temp, wavelength, unit, result_low, result_high, sample_rest_time, test_time, delay_between_images, standard_concentration, m, i"
    table_name = 'tests'
    
    def connect(self, path = "/home/pi/Aditya_Work/Github/Bio-Spectronics/IPU_training/Database/database"):
        global conn
        conn = sql.connect(path)
        
    def close_connection(self):
        conn.close()
    
    def execute_command(self, command = ""):
        cursor = conn.execute(command)
#         print(cursor)
        result = list()
        for i in cursor:
            for j in i:
#                 print(j)
                result.append(j)
#         print(result)
        return result
    
    def commit(self):
        
        while True:
            ans = input("commit? y/n: ")
            if ans == 'y':
                conn.commit()
                return
            elif ans == 'n':
                return
    
    def edit_entry(self):
        
        edits = []
        values = []

        test_name =""
        
        
        table_test_names = database().execute_command("select test_name from " +database().table_name)
        
        if len(table_test_names) < 1:
            print("table is empty")
            return
        
        print("Select test. Press y or n: ")
        
        choose = False
        
        for i in table_test_names:
            while True:
                
                response = input("edit in "+str(i)+"? ")
                if response == "y":
                    test_name = i
                    choose = True
                    break
#                 print(i)
                elif response == 'n':
                    break
                else:
                    print("wrong input")
            
            if choose == True:
                break
        
        if len(test_name) < 1:
                    return
                
        print("Select Parameters. Press y or n: ")
                                  
        for i in database().attributes[1:]:
            while True:
                
                responce = input(i +": ")
                if responce == 'y':
                    edits.append(i)
                    if database().attributes_type.get(i) == 'int':
                        while True:
                            try:
                                values.append(int(input("Enter Value: ")))
                                break
                            except:
                                print("wrong value")
                    elif database().attributes_type.get(i) == 'float':
                        while True:
                            try:
                                values.append(float(input("Enter Value: ")))
                                break
                            except:
                                print("wrong value")
                    else :
                        while True:
                            try:
                                values.append('"' + input("Enter Value: ") + '"')
                                break
                            except:
                                print("wrong value")
                    break
                
                elif responce == 'n':
                    break
                else:
                    print("wrong command")
        
#         print(edits)
#         print(values)
        
        if len(values) < 1:
                    return
                
        string = "update " +database().table_name +" set "
        
        for (i,j) in zip(edits,values):
            string = string + str(i) + "=" + str(j) + ","
            
        string = string[0:len(string)-1] + ' where test_name = "' +test_name +'"'        
        database().execute_command(string)
        database().commit()
        
    def add_entry(self):
        
        values = list()
        for i in database().attributes[1:]:
            
#             print(i +": ")
            
            if database().attributes_type.get(i) == 'int':
                while True:
                    try:
                        values.append(int(input(i +": ")))
                        break
                    except:
                        print("wrong value1")
                        
            elif database().attributes_type.get(i) == 'float':
                while True:
                    try:
                        values.append(float(input(i +": ")))
                        break
                    except:
                        print("wrong value2")
                        
            else :
                while True:
                    try:
                        values.append('"' + input(i +": ") + '"')
                        break
                    except:
                        print("wrong value3")
                        
        
#         print(edits)
#         print(values)

        if len(values) < 1:
            return
        
        string = "insert into " +database().table_name +" ("
        
        for i in database().attributes[1:]:
            string = string + str(i) +","
        
        string = string[0:-1] + ") values ("
        
        for i in values:
            string = string + str(i) + ','
        
        string = string[0:-1] + ")"
        print(string)
            
#         string = string[0:len(string)-1] + ' where test_name = "' +test_name +'"'        
        database().execute_command(string)
        database().commit()
        
    
    def delete_entry(self):
        
        table_test_names = database().execute_command("select test_name from " +database().table_name)
        
        if len(table_test_names) < 1:
            print("table is empty")
            return
        
        
        print("Select test. Press y or n: ")
        
        test_names = list()

        for i in table_test_names:
            while True:
                
                response = input("delete "+str(i)+"? ")
                if response == "y":
                    test_names.append(i)
                    break
#                 print(i)
                elif response == 'n':
                    break
                else:
                    print("wrong input")
        
        string = "delete from " +database().table_name +" where " +str(database().attributes[1]) +" in ("
        
        if len(test_names) < 1:
            return
        
        for i in test_names:
            string = string + '"' +str(i) + '",'
        
        string = string[0:len(string) - 1] + ")"
#         print(string)
        database().execute_command(string)
        database().commit()
    
    def truncate_table(self):
        string = "delete from " + database().table_name
#         print(string)
        database().execute_command(string)
        database().commit()
        
    def create_table(self):
        string = """CREATE TABLE "Tests" (
            "primary_key"	INTEGER NOT NULL,
            "test_name"	TEXT NOT NULL,
            "type"	TEXT NOT NULL,
            "temp"	INTEGER NOT NULL,
            "wavelength"	INTEGER NOT NULL,
            "unit"	TEXT NOT NULL,
            "result_low"	INTEGER NOT NULL,
            "result_high"	INTEGER NOT NULL,
            "sample_rest_time"	INTEGER NOT NULL,
            "test_time"	INTEGER NOT NULL,
            "delay_between_images"	INTEGER NOT NULL,
            "standard_concentration"	INTEGER NOT NULL,
            "m"	INTEGER NOT NULL,
            "i"	INTEGER NOT NULL,
            PRIMARY KEY("primary_key" AUTOINCREMENT)"""
        
        database().execute_command(string)
        database().commit()
    
    
    
db = database()
db.connect()
# db.execute_command('update tests set m = 82.60613293913033, i = 6.663643406522594, R_w = 0.6056309756811918, G_w = 0.580911344020735, B_w = 0.5438318965300498, standard_concentration = 4 where test_name ="Albumin"')
# db.commit()
# db.truncate_table()
# db.edit_entry()
# db.add_entry()
# print(db.get_test_name())
# db.delete_entry()
# db.commit()
