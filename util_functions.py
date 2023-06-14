def allowed_file(filename:str,extensions:set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def insert_into_student(data:tuple):
    uucms_no,name,course,semester,batch,fathers_name,mothers_name,stream,sex,fathers_contact,mothers_contact,students_contact,whatsapp_no=data
    query= f'INSERT INTO students(uucms_no,name,course,semester,batch,fathers_name,mothers_name,stream,sex,fathers_contact,mothers_contact,students_contact,whatsapp_no)VALUES("{uucms_no}","{name}","{course}","{semester}","{batch}","{fathers_name}","{mothers_name}","{stream}","{sex}","{fathers_contact}","{mothers_contact}","{students_contact}","{whatsapp_no}");'
    del uucms_no,name,course,semester,batch,fathers_name,mothers_name,stream,sex,fathers_contact,mothers_contact,students_contact,whatsapp_no
    return query

def insert_into_uploaded_files(data:tuple):
    file,size=data
    query=f'INSERT INTO uploaded_files(filename,size)VALUES("{file}",{size});'
    del file,size
    return query

def check_cred_query(username):
    query=f'SELECT password from faculty WHERE username="{username}"'
    return query

