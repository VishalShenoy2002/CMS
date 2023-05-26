from flask import Flask
from flask import render_template,flash,redirect
from flask import request
from werkzeug.utils import secure_filename

import os
import csv
import util_functions


app=Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.join(os.getcwd(),"uploads")

ALLOWED_EXTENSIONS = {'csv'}


@app.route("/upload-batch",methods=["GET","POST"])
def upload_batch():
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
    

    return render_template("upload_batch.html",title="Upload Batch")

@app.route("/edit-batch")
def edit_batch():
    return render_template("edit_batch.html",title="Edit Batch")

@app.route("/add-student")
def add_student():
    return render_template("add_student.html",title="Edit Batch | Add Student")

@app.route("/remove-student")
def remove_student():
    return render_template("remove_student.html",title="Edit Batch | Remove Student")

@app.route("/admission")
def admission():
    return render_template("admission.html",title="Admission")

if __name__ == "__main__":
    app.run(debug=True)