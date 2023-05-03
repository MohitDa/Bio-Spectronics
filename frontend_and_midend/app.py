from asyncio.windows_events import NULL
import os
from tkinter import NO
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import select
import analyzer
app = Flask(__name__)   # Create an instance of flask called "app"


import sys
sys.path.insert(1, '/backend_algorithms')


# # import backend_algorithms
# import backend_algorithms.run_motor #pump actions
# import backend_algorithms.peltier   #peltier


basedir = os.path.abspath(os.path.dirname(__file__))
# from testip import testip
# from push_data import push_data
# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)  # Sets up the RPi lib to use the Broadcom pin mappings
                        #  for the pin names. This corresponds to the pin names
                        #  given in most documentation of the Pi header
# GPIO.setwarnings(False) # Turn off warnings that may crop up if you have the
                        #  GPIO pins exported for use via command line
# GPIO.setup(2, GPIO.OUT) # Set GPIO2 as an output


app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class patient(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer,nullable=True)
    testname = db.Column(db.String(100), nullable=True)
    flag_level = db.Column(db.String(80), nullable=True)
    test_level = db.Column(db.String(80), nullable=True)
    date = db.Column(db.DateTime(timezone=True),server_default=func.now())

class new_test_visible(db.Model):
    test_name = db.Column(db.String(100), primary_key=True ,unique=True, nullable=True)
    test_type = db.Column(db.String(100), nullable=True)
    S = db.Column(db.Integer, nullable=True)
    H = db.Column(db.Integer, nullable=True)
    V = db.Column(db.Integer, nullable=True)
    L = db.Column(db.Integer, nullable=True)
    intercept = db.Column(db.Integer, nullable=True)
    test_temperature = db.Column(db.Integer, nullable=True)
    test_level_lower = db.Column(db.Integer, nullable=True)
    test_level_higher = db.Column(db.Integer, nullable=True)
    test_unit = db.Column(db.String(100), nullable=True)

class new_test_uv(db.Model):
    test_name = db.Column(db.String(100), primary_key=True ,unique=True, nullable=True)
    test_type = db.Column(db.String(100), nullable=True)
    test_stdval = db.Column(db.Integer,nullable=True)
    test_temperature = db.Column(db.Integer, nullable=True)
    test_level_lower = db.Column(db.Integer, nullable=True)
    test_level_higher = db.Column(db.Integer, nullable=True)
    test_unit = db.Column(db.String(100), nullable=True)

class new_tests(db.Model):

    test_id = db.Column(db.Integer, primary_key=True , nullable=False , autoincrement=True)
    test_name = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(100), nullable=True)
    temp = db.Column(db.Integer,nullable=True)
    wavelength = db.Column(db.Integer, nullable=True)
    unit = db.Column(db.String(100), nullable=True)
    result_low = db.Column(db.Integer, nullable=True)
    result_high = db.Column(db.Integer, nullable=True)
    sample_rest_time = db.Column(db.Integer, nullable=True)
    test_time = db.Column(db.Integer, nullable=True)
    delay_between_images = db.Column(db.Integer, nullable=True)
    standard_concentration = db.Column(db.Integer, nullable=True)
    m = db.Column(db.Integer, nullable=True)
    i = db.Column(db.Integer, nullable=True)
    R_w = db.Column(db.Integer, nullable=True)
    G_w = db.Column(db.Integer, nullable=True)
    B_w = db.Column(db.Integer, nullable=True)


@app.route("/")
def index():
    return render_template("index.html"), {"Refresh": "1; url=list_of_biochemistry"}

@app.route("/list_of_biochemistry")
def list_of_biochemistry():
    tests_visible = new_tests().query.filter(new_tests.wavelength > 400, new_tests.B_w != None)
    tests_uv = new_tests().query.filter(new_tests.wavelength <= 400, new_tests.B_w != None)

    # for data in tests_uv:
    #     print(data.B_w)
    # print(tests_uv)

    # tests = new_tests.query.all()
    
    # tests_visible =  select(new_tests).where(new_tests.wavelength >= 400)
    # tests_uv =  select(new_tests).where(new_tests.wavelength < 400)

    # tests_name =  select(new_tests).where(new_tests.test_name == "Albumin")

    # with db.engine.connect() as conn:
    #     for row in conn.execute(tests_uv):
    #         print(row)

    # print(tests_name)


    return render_template("list_of_biochemistry.html", tests_visible = tests_visible , tests_uv = tests_uv )

@app.route("/start_test",methods=['GET','POST'])
def start_test():
    # print("Something")
    # peltier.set_peltier("visible")

    # run_motor.run_pump(pump = 1, direction = "forward", duration = 1.2)

    return redirect("/list_of_biochemistry")

# @app.route("/add_new_test",methods=['GET','POST'])
# def add_new_test_visible():
    if request.method == 'POST':

        test_name = request.form['testname']
        test_type = request.form['testtype']
        H = request.form['H']
        S = request.form['S']
        L = request.form['L']
        V = request.form['V']
        test_temperature = request.form['test_temperature']
        intercept = request.form['intercept']
        test_level_lower = request.form['test_level_lower']
        test_level_higher = request.form['test_level_higher']
        test_unit = request.form['test_level_higher']

        test = new_test_visible( 
                    test_name = test_name, 
                    test_type = test_type ,
                    S=S,H=H,V=V,L=L,
                    intercept = intercept,
                    test_temperature = test_temperature,
                    test_level_lower = test_level_lower, 
                    test_level_higher = test_level_higher,
                    test_unit = test_unit )

        db.session.add(test)
        db.session.commit()

    return render_template("new_test_added.html"),{"Refresh": "2; url=list_of_biochemistry"}

@app.route("/test_done",methods=['GET','POST'])
def test_done():
    visible_list = []
    uv_list=[]

    if request.method == "POST":
        test_list = request.form.getlist('test_list')
       
        for test in test_list:
            current_test = test.split(",")
            if current_test[1] == "uv":
                test_details = new_test_uv.query.get_or_404(current_test[0])
                flag_low = test_details.test_level_lower
                flag_high = test_details.test_level_higher
                temperature = test_details.test_temperature
                # uv =  analyzer.UV()
                # value,flag,absorbance =    uv.uv_spectrum(flag_low,flag_high,temperature)
                # uv_list.append(value)
                # uv_list.append(flag)
                # uv_list.append(absorbance)
                uv_list.append(10)
                uv_list.append("low")
                uv_list.append(24)



            elif current_test[1] == "visible":
                test_details = new_test_visible.query.get_or_404(current_test[0])
                h = test_details.H
                s = test_details.S
                l = test_details.L
                v = test_details.V
                intercept = test_details.intercept
                flag_low = test_details.test_level_lower
                flag_high = test_details.test_level_higher
                temperature = test_details.test_temperature
                # value,flag = analyzer.visible_spectrum(h,s,l,v,intercept,flag_low,flag_high,temperature)
                # visible_list.append(value)
                # visible_list.append(flag)
                visible_list.append(19 )
                visible_list.append("high")
                

            # x_axis = []
            # y_axis = []
            # for i in range(len(int(absorbance+1))):
            #     x_axis.append(i)
            # for i in range(len(int(absorbance+1))):
            #     x_axis.append(i)
            
    return render_template("test_done.html",uv_list = uv_list,visible_list = visible_list)

@app.route("/add_new_test",methods=['GET','POST'])
def add_new_test():
    
    new_test = new_tests()
    
    new_test.test_name = ""
    new_test.test_type = "Kinetic"
    return render_template("new_test.html", edit_test = new_test)

@app.route("/water",methods=['GET','POST'])
def water():
    print("Water")
    return None

@app.route("/reagent_blank",methods=['GET','POST'])
def reagent_blank():
    print("reagent Blank")
    return None

@app.route("/standard",methods=['GET','POST'])
def standard():
    print("standard")
    return None

@app.route("/delete_test",methods=['GET','POST'])
def delete_test():
    if request.method == "POST":
        test_list = request.form.getlist('test_list')
        for test in test_list:
            current_test = test.split(",")
           
            if current_test[1] == "uv":
                test_details = new_test_uv.query.get_or_404(current_test[0])

            else:
                test_details = new_test_visible.query.get_or_404(current_test[0])
        
        
            db.session.delete(test_details)
            db.session.commit()

    

    return redirect("/list_of_biochemistry")

@app.route("/edit_test",methods=['GET','POST'])
def edit_test():
    if request.method == "POST":
        test_list = request.form.getlist('test_list')
        # print(test_list)
        edit_test = dict(test_id = "", test_name = "" , test_type = "" , test_temp = "" , test_wavelength = "" , test_unit = "" , test_result_low = "" , test_result_high = "" , test_sample_rest_time = "" , test_test_time = "" , test_delay_between_images = "" , test_standard_concentration = "")
    
        for test in test_list:
            current_test = test.split(",")
            # print("current tests: " +str(current_test[0]))
            test_details = new_tests.query.get_or_404(current_test[0])
            # print(test_details)

            # if test_details.wavelength <= 400 :

            test_id = test_details.test_id
            test_name = test_details.test_name
            test_type = test_details.type
            test_temp = test_details.temp
            test_wavelength = str(test_details.wavelength)
            test_unit = test_details.unit
            test_result_low = test_details.result_low
            test_result_high = test_details.result_high
            test_sample_rest_time = test_details.sample_rest_time
            test_test_time = test_details.test_time
            test_delay_between_images = test_details.delay_between_images
            test_standard_concentration = test_details.standard_concentration
            test_m = test_details.m
            test_i = test_details.i
            test_R_w = test_details.R_w
            test_G_w = test_details.G_w
            test_B_w = test_details.B_w
            
            edit_test["test_id"] = test_id
            edit_test["test_name"] = test_name
            edit_test["test_type"] = test_type
            edit_test["test_temp"] = test_temp
            edit_test["test_wavelength1"] = test_wavelength
            edit_test["test_unit"] = test_unit
            edit_test["test_result_low"] = test_result_low
            edit_test["test_result_high"] = test_result_high
            edit_test["test_sample_rest_time"] = test_sample_rest_time
            edit_test["test_test_time"] = test_test_time
            edit_test["test_delay_between_images"] = test_delay_between_images
            edit_test["test_standard_concentration"] = test_standard_concentration
            # print(edit_test)

            # else:
            #     test_name = test_details.test_name
            #     test_type = test_details.type
            #     test_temp = test_details.temp
            #     test_wavelength = test_details.wavelength
            #     test_unit = test_details.unit
            #     test_result_low = test_details.result_low
            #     test_result_high = test_details.result_high
            #     test_sample_rest_time = test_details.sample_rest_time
            #     test_test_time = test_details.test_time
            #     test_delay_between_images = test_details.delay_between_images
            #     test_standard_concentration = test_details.standard_concentration
            #     test_m = test_details.m
            #     test_i = test_details.i
            #     test_R_w = test_details.R_w
            #     test_G_w = test_details.G_w
            #     test_B_w = test_details.B_w

                
            #     edit_test["test_name"] = test_name
            #     edit_test["test_type"] = test_type
            #     edit_test["test_temp"] = test_temp
            #     edit_test["test_wavelength"] = test_wavelength
            #     edit_test["test_unit"] = test_unit
            #     edit_test["test_result_low"] = test_result_low
            #     edit_test["test_result_high"] = test_result_high
            #     edit_test["test_sample_rest_time"] = test_sample_rest_time
            #     edit_test["test_test_time"] = test_test_time
            #     edit_test["test_delay_between_images"] = test_delay_between_images
            #     edit_test["test_standard_concentration"] = test_standard_concentration
            #     print(edit_test)
    
        # print("edit test")

    return render_template("edit_test.html", edit_test = edit_test)

@app.route("/update_test",methods=['GET','POST'])
def update_test():
    if request.method == "POST":
        # test_name = request.form['testname']
        # print(test_name)

        test_id = request.form['testid']
        # print(test_id)
        test_update = new_tests.query.get(test_id)
        if test_update == None: #test do not exist. Add new test
            test_update = new_tests()
            test_update.m = 0
            test_update.i = 0
        test_update.test_name = request.form['testname']
        test_update.type = request.form['testmethod']
        test_update.temp = request.form['testtemp']
        test_update.wavelength = request.form['testwavelength1']
        test_update.unit = request.form['testunit']
        test_update.result_low = request.form['testlevellow']
        test_update.result_high = request.form['testlevelhigh']
        test_update.sample_rest_time = request.form['testdelaytime']
        
        try:
            test_update.test_time = request.form['testtesttime']
        except:
            pass

        try:
            test_update.delay_between_images = request.form['testdelaybetweenimages']
        except:
            pass

        test_update.standard_concentration = request.form['testconc1']
        
        # print (test_update.test_id)
        db.session.add(test_update)
        db.session.commit()

        # if(test_type=="visible"):
        #     test_name = request.form['testnameold']
        #     test_details = new_test_visible.query.get_or_404(test_name)
        #     test_details.test_name = request.form['testname']
        #     test_details.H = request.form['H']
        #     test_details.S = request.form['S']
        #     test_details.L = request.form['L']
        #     test_details.V = request.form['V']
        #     test_details.test_temperature = request.form['test_temperature']
        #     test_details.intercept = request.form['intercept']
        #     test_details.test_level_lower = request.form['test_level_lower']
        #     test_details.test_level_higher = request.form['test_level_higher']
        #     test_details.test_unit = request.form['test_unit']
        #     db.session.add(test_details)
        #     db.session.commit()
        
        # if test_type == "uv":
        #     test_name = request.form['testnameold']
        #     test_details = new_test_uv.query.get_or_404(test_name)
        #     test_details.test_name = request.form['testname']
        #     test_details.test_temperature = request.form['test_temperature']
        #     test_details.test_level_lower = request.form['test_level_lower']
        #     test_details.test_level_higher = request.form['test_level_higher']
        #     test_details.test_unit = request.form['test_unit']
        #     db.session.add(test_details)
        #     db.session.commit()



        return redirect("/list_of_biochemistry")

@app.route("/clean",methods=['GET','POST'])
def clean():

    print("Something")
    # peltier.set_peltier(type = "visible")
    # print("cleaning from app.py")
    # run_motor.run_pump(pump = 1, direction = "forward", duration = 5)
    return redirect("/list_of_biochemistry")

if __name__ == '__main__':
   app.run(debug = True)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)