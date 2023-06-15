from flask import Flask
from flask import render_template,flash,redirect
from flask import request
from werkzeug.utils import secure_filename

import os
import csv
import openai
import hashlib
import json

import util_functions
import db_functions
with open("config.json","r") as f:
    data=json.load(f)
    f.close()

openai.api_key=data['tokens']['openai']
test_generator=openai.Completion()

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.join(os.getcwd(),"uploads")

ALLOWED_EXTENSIONS = {'csv'}

@app.route("/")
def index():
    return render_template("index.html",title="Home")

@app.route("/success")
def success_page():
    return render_template("success.html")

@app.route("/failed")
def fail_page():
    return render_template("failed.html")
# Admission Page Routes
@app.route("/admission")
def admission():
    return render_template("admission.html",title="Admission")

@app.route("/admission/upload-batch",methods=["GET","POST"])
def upload_batch():
    if request.method == "POST":
        if 'file' not in request.form:
            print("No File Uploaded")
            

        file=request.files['file']

        if util_functions.allowed_file(file.filename,ALLOWED_EXTENSIONS) == True:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],"csv",secure_filename(file.filename)))
            
            db_functions.read_and_insert_batch(os.path.join(app.config['UPLOAD_FOLDER'],"csv",secure_filename(file.filename)))
            return render_template("upload_batch.html",title="Upload Batch", filename=file.filename,message={"text":"File Saved Successfully","message_type":"success"})
            return "File Saved"

        elif util_functions.allowed_file(file.filename,ALLOWED_EXTENSIONS) == False:
            return render_template("upload_batch.html",title="Upload Batch", filename=file.filename,message={"text":"File Not Saved ","message_type":"error"})
        
        else:
            return render_template("upload_batch.html",title="Upload Batch", filename=file.filename,message={"text":"No File Selcleted","message_type":"success"})
    

    return render_template("upload_batch.html",title="Upload Batch",message={"text":"","message_type":""})

@app.route("/admission/edit-batch")
def edit_batch():
    return render_template("edit_batch.html",title="Edit Batch")

@app.route("/admission/delete-batch")
def delete_batch():
    return render_template("delete_batch.html",title="Delete Batch")

@app.route("/search")
def search_batch():
    return render_template("search.html",title="Search")

@app.route("/edit-batch/add-student")
def add_student():
    return render_template("add_student.html",title="Edit Batch | Add Student")

@app.route("/edit-batch/remove-student")
def remove_student():
    return render_template("remove_student.html",title="Edit Batch | Remove Student")

@app.route("/edit-batch/edit-student")
def edit_student():
    return render_template("edit_student.html",title="Edit Batch | Edit Student")


# Internal Assesment Page Routes
@app.route("/internal-assesment")
def internal_assesment():
    return render_template("internal_assesment.html",title="Internal Assesment")

@app.route("/internal-assesment/upload-marks")
def upload_marks():
    if request.method == "POST":
        if 'file' not in request.form:
            print("No File Uploaded")

        file=request.files['file']
        print(file,type(file))
        if util_functions.allowed_file(file.filename,ALLOWED_EXTENSIONS) == True:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
            return "File Saved"
        else:
            return "File Not Saved (expected CSV)"
    
    return render_template("upload_marks.html",title="Internal Assesment | Upload Marks")

@app.route("/internal-assesment/generate-test",methods=["GET","POST"])
def generate_test():
    if request.method == "POST":
        subject=request.form.get('subject')
        marks=request.form.get('marks')
        dept=request.form.get('department')
        prompt=f"[You are a teacher of {dept} department.]Generate a test on {subject} for {marks} marks.  The format of the questions should be 'question number-question-marks'.<stop>"
        response=test_generator.create(model="text-davinci-003",prompt=prompt,max_tokens=2500,stop="<stop>")
        response=response['choices'][0]['text'].strip()
        question=[tuple(question.split("-")) for question in response.split("\n")]
        
        return render_template("generate_test.html",title="Internal Assesment | Generate Test",questions=question)
    return render_template("generate_test.html",title="Internal Assesment | Generate Test")
    
@app.route("/account")
def account():
    return render_template("account_page.html",title="Account",details_dict={"Name":"Vishal","Age":20})

@app.route("/teachers-dashboard")
def teachers_dashboard():
    return render_template("teachers_dashboard.html",title="Teacher's Dashboard",timetable={1:"SE",2:"DAA",3:"GE"},topics={"27-09-2023":"Stack DS, Queue DS","26-09-2023":"Linked List DS"},date="28-09-2023")

@app.route("/teachers-dashboard/subject-allotment",methods=["GET","POST"])
def subject_allotment():
    if request.method == "POST":
        print(request.form)
    return render_template("subject_allotment_page.html",title="Subject Allotment",user_type='hod',semesters=[1,2,3,4,5,6,7,8])

@app.route("/attendance",methods=["GET","POST"])
def attendance():
    return render_template("attendance_page.html",title="Attendance")

@app.route("/reports")
def reports():
    return render_template("reports.html",title="Reports")

@app.route("/login",methods=["GET","POST"])
def login_page():
    if request.method == "POST":
        username=request.form.get("username")
        password=request.form.get("password")
        password=hashlib.sha256(password.encode()).hexdigest()
        if db_functions.check_cred(username,password) == True:
            return redirect("/")
        print(f"Username: {username} Password: {password}")
    return render_template("login_page.html",title="Login")

@app.route("/student-registration-form",methods=["GET","POST"])
def student_registration():
    if request.method == "POST":
        form_data=request.form
        fieldnames=["uucms_no","name","course","semester","batch","fathers_name","mothers_name","stream","sex","fathers_contact","mothers_contact","students_contact","whatsapp_no","photo"]
        record=dict(form_data)
        if '' in record.values():
            return redirect("/failed")
        else:
            with open(f"dept_{record['course'].lower()}_batch_{record['batch']}.csv","a+") as f:
                writer=csv.DictWriter(f,fieldnames=fieldnames)
                writer.writerow(record)
                f.close()
            return redirect("/success")
    
    return render_template("student_registration_page.html",title="Student Registration")


if __name__ == "__main__":
    app.run(host=data['http']['host'],debug=True)