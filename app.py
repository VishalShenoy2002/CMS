from flask import Flask,Session
from flask import render_template,redirect,url_for
from flask import request
from werkzeug.utils import secure_filename

from student import Student
from faculty import Faculty
from batch import Batch
from course import Course
from subject import Subject

import os
import csv
import openai
import hashlib
import logging
import json
import datetime
import mysql

import util_functions
import db_functions


with open("config.json","r") as f:
    data=json.load(f)
    f.close()

openai.api_key=data['tokens']['openai']
test_generator=openai.Completion()

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.join(os.getcwd(),"uploads")
app.secret_key="____"

session=Session()
# Setting Log Path
log_path=os.path.join(os.getcwd(),"logs")
if os.path.isdir(log_path) == False:
    os.makedirs(log_path)

if os.path.isdir(app.config['UPLOAD_FOLDER']) == False:
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'csv','png',"jpeg","jpg"}

@app.before_first_request
def before_first_request():
    session['logged_in'] = False
    session['username'] = ""
    session['role'] = ""
    session['department'] = ""

@app.route("/")
def cms_page():
    return render_template("cms_page.html",title="CMS")

@app.route("/home")
def index():
    if session['logged_in'] == True:
        return render_template("index.html",title="CMS",role=session["role"])
    else:
        return redirect("/login")

@app.route("/success")
def success_page():
    return render_template("success.html")

@app.route("/failed")
def fail_page():
    return render_template("failed.html",title="Task Failed")
# Admission Page Routes
@app.route("/admission")
def admission():
    return render_template("admission.html",title="Admission",role=session['role'])

@app.route("/admission/upload-batch",methods=["GET","POST"])
def upload_batch():
    if request.method == "POST":
        if 'file' not in request.form:
            # print("No File Uploaded")
            pass

        file=request.files['file']
        details=file.filename.split('.')[0].split('_')
        # Configuring Batch
        batch=Batch()
        batch.department=details[1]
        batch.start_year=int(details[3])
        batch.set_end_year()
        batch.create_batch()

        if util_functions.allowed_file(file.filename,ALLOWED_EXTENSIONS) == True:
            # 
            if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],"csv")) == False:
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],"csv"))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],"csv",secure_filename(file.filename)))
            db_functions.read_and_insert_batch(os.path.join(app.config['UPLOAD_FOLDER'],"csv",secure_filename(file.filename)))
            batch.generate_batch_table()
            return render_template("upload_batch.html",title="Upload Batch", filename=file.filename,message={"text":"File Saved Successfully","message_type":"success"},role=session['role'])

        elif util_functions.allowed_file(file.filename,ALLOWED_EXTENSIONS) == False:
            return render_template("upload_batch.html",title="Upload Batch", filename=file.filename,message={"text":"File Not Saved ","message_type":"error"},role=session['role'])
        
        else:
            return render_template("upload_batch.html",title="Upload Batch", filename=file.filename,message={"text":"No File Selcleted","message_type":"success"},role=session['role'])
    

    return render_template("upload_batch.html",title="Upload Batch",message={"text":"","message_type":""},role=session['role'])

@app.route("/admission/edit-batch")
def edit_batch():
    return render_template("edit_batch.html",title="Edit Batch",role=session['role'])

@app.route("/admission/delete-batch")
def delete_batch():
    return render_template("delete_batch.html",title="Delete Batch",role=session['role'])

@app.route("/search")
def search_batch():
    return render_template("search.html",title="Search",role=session['role'])

@app.route("/edit-batch/add-student")
def add_student():
    return render_template("add_student.html",title="Edit Batch | Add Student",role=session['role'])

@app.route("/edit-batch/remove-student")
def remove_student():
    return render_template("remove_student.html",title="Edit Batch | Remove Student",role=session['role'])

@app.route("/edit-batch/edit-student")
def edit_student():
    return render_template("edit_student.html",title="Edit Batch | Edit Student",role=session['role'])


# Internal Assesment Page Routes
@app.route("/internal-assesment")
def internal_assesment():
    return render_template("internal_assesment.html",title="Internal Assesment",role=session['role'])

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
    
    return render_template("upload_marks.html",title="Internal Assesment | Upload Marks",role=session["role"])

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
        
        return render_template("generate_test.html",title="Internal Assesment | Generate Test",questions=question,role=session['role'])
    return render_template("generate_test.html",title="Internal Assesment | Generate Test",role=session['role'])
    
@app.route("/account")
def account():
    if session.get("logged_in") == True:
        faculty=Faculty()
        faculty.faculty_id=session.get('username')
        faculty_details=dict(zip(("Faculty ID","Faculty Name","Email","Contact","Department","Designation"),faculty.get_faculty_details()))
        return render_template("account_page.html",title="Account",details_dict=faculty_details,role=session['role'])
    else:
        return redirect("/login")

@app.route("/change-password")
def change_password_page():
    return render_template("change_password_page.html",role=session['role'])
    
@app.route("/logout")
def logout():
    logging.info(f"{session['username']} is logging out")
    session.clear()
    return redirect("/")

@app.route("/teachers-dashboard")
def teachers_dashboard():
    return render_template("teachers_dashboard.html",title="Teacher's Dashboard",timetable={1:"SE",2:"DAA",3:"GE"},topics={"27-09-2023":"Stack DS, Queue DS","26-09-2023":"Linked List DS"},date="28-09-2023",role=session['role'])

@app.route("/admin-dashboard/subject-allotment/1",methods=["GET","POST"])
def subject_allotment_page_1():
    if session.get("role") == "HOD" and session.get('logged_in') == True:
        if request.method == "POST":
            return render_template("subject_allotment_page_2.html",title="Subject Allotment",role=session['role'],subjects=['a','b','c'],batches=[1,2,4],batch_id="nep-bca-2124")
        return render_template("subject_allotment_page_1.html",title="Subject Allotment",role=session['role'],subjects=['a','b','c'],batches=[1,2,4])
    else:
        return redirect("/login")
@app.route("/admin-dashboard/subject-allotment/2/<batch_id><semester>",methods=["GET","POST"])
def subject_allotment_page_2(batch_id,semester):
    if request.method == "GET":
        subject=Subject()
        subject_list=subject.get_subject_list(semester)
        return render_template("subject_allotment_page_2.html",title="Subject Allotment",role=session['role'],subjects=subject_list,batches=[1,2,4],)
    if request.method == "POST":
        # return render_template("")
        pass
    return render_template("subject_allotment_page_2.html",title="Subject Allotment",role=session['role'],subjects=['a','b','c'],batches=[1,2,4])

@app.route("/attendance",methods=["GET","POST"])
def attendance():
    return render_template("attendance_page.html",title="Attendance",role=session['role'])

@app.route("/reports")
def reports():
    return render_template("reports.html",title="Reports",role=session['role'])

@app.route("/login",methods=["GET","POST"])
def login_page():
    if request.method == "POST":
        faculty=Faculty()
        username=request.form.get("faculty_id")
        password=request.form.get("password")

        faculty.faculty_id=username
        password=hashlib.sha256(password.encode()).hexdigest()

        if db_functions.check_cred(username,password) == True:
            logging.info(f"Login Successful - {username}")
            session['logged_in'] = True
            session['username'] = username
            session['role'] = faculty.fetch_designation()
            return redirect("/home")
        else:
            session['logged_in'] = False
            logging.info("Login Failed")
        print(f"Username: {username} Password: {password}")
        print(session['logged_in'])
    return render_template("login_page.html",title="Login")

@app.route("/student-registration",methods=["GET","POST"])
def student_registration():
    return render_template("student_registration_info_page.html",title="Student Registration")

@app.route("/student-registration/1",methods=["GET","POST"])
def student_registration_page_1():
    student=Student()
    course=Course()
    if request.method == "POST":
        form_data=request.form
        print(form_data)
        
        student.uucms_no=form_data.get('uucms_no')
        student.batch=int(form_data.get('batch').split("-")[0])
        student.department=form_data.get('department')
        if student.exists():
            return render_template("student_registration_page_1.html",title="Student Registration",records=student.get_record(),departments=course.courses_available())

    
    return render_template("student_registration_page_1.html",title="Student Registration",records=student.get_record(),departments=course.courses_available())

@app.route("/student-registration/2/<uucms_no>",methods=["GET","POST"])
def student_registration_page_2(uucms_no):
    student=Student()
    student.uucms_no=uucms_no
    record=student.get_full_record()[0]
    fieldnames=["uucms_no","name","course","batch","semester"]

    if request.method == "GET":
        record=dict(zip(fieldnames,record))
        print(record)
        return render_template("student_registration_page_2.html",title="Student Registration",uucms_no=record['uucms_no'],name=record['name'],department=record['course'],batch=record['batch'],semester=record['semester'])

    if request.method == "POST":

        form_data=request.form
        photo=request.files['photo']

        
        # unpacking record from previous page i.e /student-registration/1
        uucms_no,name,course,batch,semester=record

        fieldnames=["uucms_no","name","course","semester","batch","fathers_name","mothers_name","stream","sex","fathers_contact","mothers_contact","students_contact","whatsapp_no","photo"]
        
        # Converting the form data into a dictionary because it'll be easier to insert into the csv file
        record=dict(form_data)
        record["uucms_no"],record["name"],record["course"],record["batch"],record["semester"]=uucms_no,name,course,batch,semester


        if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],"pics","student")) == False:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],"pics","student"))
        # saving the photo if exists
        if util_functions.allowed_file(photo.filename,ALLOWED_EXTENSIONS) == True:
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],"pics","student",f"student_{record['uucms_no']}_pic.png"))
        # checking if any field is left empty if it is left mpty then its redirected to failed page.
        # else it stores the data in the csv if the it record doesn't exist
        if '' in record.values():
            return redirect("/failed")
        
        else:
            student_data=(record['fathers_name'],record['mothers_name'],record['stream'],record['sex'],record['fathers_contact'],record['mothers_contact'],record['students_contact'],record['whatsapp_no'])
            student.update(student_data)
            if os.path.isfile(f"dept_{course.lower()}_batch_{batch}.csv") == False:

                with open(f"dept_{course.lower()}_batch_{batch}.csv","a+",newline="") as f:
                    reader=csv.DictReader(f)
                    writer=csv.DictWriter(f,fieldnames=fieldnames)
                    if record['uucms_no'] not in [row['uucms_no'] for row in reader]:
                        writer.writeheader()
                        writer.writerow(record)
                    f.close()
                    del reader,writer,f

            else:

                with open(f"dept_{record['course'].lower()}_batch_{record['batch']}.csv","a+",newline="") as f:
                    reader=csv.DictReader(f)
                    writer=csv.DictWriter(f,fieldnames=fieldnames)
                    if record['uucms_no'] not in [row['uucms_no'] for row in reader]:
                        writer.writerow(record)
                    f.close()
                    del reader,writer,f

            return redirect("/success")
    return render_template("student_registration_page_2.html",title="Student Registration")

@app.route("/faculty-registration",methods=["GET","POST"])
def faculty_registation():
    course=Course()
    if request.method == "POST":
        faculty=Faculty()

        faculty.faculty_id=request.form.get('faculty_id')
        faculty.name=request.form.get('faculty_name')
        faculty.faculty_email=request.form.get('faculty_email')
        faculty.faculty_contact=request.form.get('faculty_contact')
        faculty.department=request.form.get('department')
        faculty.designation=request.form.get('designation')
        photo=request.files['photo']

        if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],"pics","faculty")) == False:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],"pics","faculty"))


        if util_functions.allowed_file(photo.filename,ALLOWED_EXTENSIONS) == True:
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],"pics","faculty",f"faculty_{faculty.faculty_id}_pic.png"))

        data=(faculty.faculty_id,faculty.name,faculty.faculty_email,faculty.faculty_contact,faculty.department)

        if faculty.exists() == False:
            faculty.add_faculty(data=data)
            return redirect("/success")
        else:
            return redirect("/failed")
        
    return render_template("faculty_registration.html",title="Faculty Registration",departments=course.courses_available())


@app.route("/admin-dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html",title="Admin Dashboard",role=session["role"])

@app.route("/admin-dashboard/add-subject",methods=["GET","POST"])
def add_subject():
    if request.method == "POST":
        syllabus_type="NEP"

        subject_name=request.form.get("subject_name")
        course_name=request.form.get("course_name")
        subject_type=request.form.get("subject_type")
        semester=request.form.get("semester")
        
        subject_abbreviation="".join([x[0] for x in subject_name.strip().split(' ')])
        subject_code=util_functions.generate_subject_code(syllabus_type,course_name,subject_abbreviation)
        
        record=(subject_code,subject_name,course_name,subject_type,semester)
        try:
            db_functions.insert_subject(record)
        except mysql.connector.errors.IntegrityError:
            count=db_functions.get_similar_key_count(subject_code) + 1
            new_key=f"{subject_code}{count}"
            record=(new_key,subject_name,course_name,subject_type,semester)
            db_functions.insert_subject(record)

    return render_template("add_subject.html",title="Add Subject")

@app.route("/admin-dashboard/add-course",methods=["GET","POST"])
def add_course():
    if request.method == "POST":
        course_name=request.form.get("course_name")
        full_form=request.form.get("full_form")
        no_of_sems=request.form.get("no_of_sems")

        record=(course_name,full_form,no_of_sems)
        db_functions.insert_course(record)

    return render_template("add_course.html",title="Add Course")

@app.route("/admin-dashboard/manage-batch-subjects/1",methods=["GET","POST"])
def manage_batch_subjects_page_1():
    course=Course()
    batch=Batch()
    if request.method == "POST":
        batch.department=request.form.get('department')
        batch.start_year=request.form.get('start_year')
        batch.end_year=request.form.get('end_year')
        
        if batch.exists():
            return render_template("manage_batch_subjects_page_1.html",title="Manage Batch Subjects",departments=course.courses_available(),records=batch.get_record())

    return render_template("manage_batch_subjects_page_1.html",title="Manage Batch Subjects",departments=course.courses_available())


@app.route("/admin-dashboard/manage-batch-subjects/2/<batch_id>",methods=["GET","POST"])
def manage_batch_subjects_page_2(batch_id):
    subject=Subject()
    if request.method == "POST":
        form_data=dict(request.form)
        subject_codes=[subject.get_subject_code_from_name(name,4) for name in form_data.values() if name != '']
        subject_dict=dict(zip(list(form_data.keys()),subject_codes))
        del form_data,subject_codes
        print(subject_dict)


        subject.course_name=batch_id.split('-')[1]
        subject.subject_type="core"
        subject.allot_subjects_for_batch(batch_id,subject_dict)
        
    return render_template("manage_batch_subjects_page_2.html",title="Manage Batch Subjects",batch_id=batch_id.upper())

if __name__ == "__main__":
    timestamp=datetime.date.today().strftime("%Y-%m-%d")
    filename=os.path.join(log_path,f"log_{timestamp}.log")
    logging.basicConfig(filename=filename,level=logging.DEBUG)
    app.run(host=data['http']['host'],debug=True)