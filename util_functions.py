# util_functions.py

# util_functions.py is a file which contains all the utility function. 
# Its a mix of db utility and other utility functions for the program.

# allowed_file() is used to check if a file is in the allowed extensions or not
def allowed_file(filename:str,extensions:set) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

# insert_into_student() is used to generate an insert query for the students table
def insert_into_student(data:tuple) -> str:
    uucms_no,name,course,semester,batch,fathers_name,mothers_name,stream,sex,fathers_contact,mothers_contact,students_contact,whatsapp_no=data
    query= f'INSERT INTO students(uucms_no,name,course,semester,batch,fathers_name,mothers_name,stream,sex,fathers_contact,mothers_contact,students_contact,whatsapp_no,photo)VALUES("{uucms_no}","{name}","{course}","{semester}","{batch}","{fathers_name}","{mothers_name}","{stream}","{sex}","{fathers_contact}","{mothers_contact}","{students_contact}","{whatsapp_no}","123");'
    del uucms_no,name,course,semester,batch,fathers_name,mothers_name,stream,sex,fathers_contact,mothers_contact,students_contact,whatsapp_no
    return query

# insert_into_uploaded_files() is used to generate an insert query for the uploaded_files table
def insert_into_uploaded_files(data:tuple) -> str:
    file,size=data
    query=f'INSERT INTO uploaded_files(filename,size)VALUES("{file}",{size});'
    del file,size
    return query

# check_cred_query() is a function that is used to generate a query to check the credentials
def check_cred_query(username) -> str:
    query=f'SELECT password from faculty WHERE username="{username}"'
    return query

