# util_functions.py

# util_functions.py is a file which contains all the utility function. 
# Its a mix of db utility and other utility functions for the program.

# allowed_file() is used to check if a file is in the allowed extensions or not
def allowed_file(filename:str,extensions:set) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

# insert_into_student() is used to generate an insert query for the students table
def insert_into_student(data:tuple) -> str:
    uucms_no,name,course,semester,batch=data
    query= f'INSERT INTO students(uucms_no,name,course,semester,batch)VALUES("{uucms_no}","{name}","{course}","{semester}","{batch}");'
    del uucms_no,name,course,semester,batch
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

def insert_basic_student_details(data:tuple):
    uucms_no,name,course,semester,batch=data
    query=f'INSERT INTO students(uucms_no,name,course,semester,batch)VALUES("{uucms_no}","{name}","{course}","{semester}","{batch}");'
    del uucms_no,name,course,semester,batch
    return query

def update_student_record(uucms_no:str,data:tuple):
    fathers_name,mothers_name,stream,sex,fathers_contact,mothers_contact,student_contact,whatsapp_no=data
    query=f'UPDATE students SET fathers_name="{fathers_name}",mothers_name="{mothers_name}",stream="{stream}",sex="{sex}",fathers_contact="{fathers_contact}",mothers_contact="{mothers_contact}",students_contact="{student_contact}",whatsapp_no="{whatsapp_no}" where uucms_no="{uucms_no}";'
    del fathers_name,mothers_name,stream,sex,fathers_contact,mothers_contact,student_contact,whatsapp_no
    return query

def generate_subject_code(syllabus_type:str,course_name:str,subject_abbreviation:str):
    return f"{syllabus_type}-{course_name}-{subject_abbreviation}".upper()

def insert_course_query(data:tuple):
    course_name,full_form,num_of_sems=data
    query=f'INSERT INTO courses(course_name,full_form,num_of_sems) VALUES("{course_name}","{full_form}",{num_of_sems});'
    del course_name,full_form,num_of_sems
    return query

def insert_subject_query(data:tuple):
    subject_code,subject_name,course_name,subject_type,semester=data
    query=f'INSERT INTO subjects(subject_code,subject_name,course_name,subject_type,semester) VALUES("{subject_code}","{subject_name.title()}","{course_name}","{subject_type}",{semester});'
    del subject_code,subject_name,course_name,subject_type,semester
    return query

def get_similar_key_count_query(key:str):
    query= f'SELECT count(*) FROM subjects where subject_code regexp "^{key}[0-9]";'
    return query

def insert_batch_query(data:tuple):
    batch_id,year_start,year_end,course_name,year_code=data
    query=f'INSERT INTO batches(batch_id,year_start,year_end,course_name,year_code) VALUES("{batch_id}",{year_start},{year_end},"{course_name}","{year_code}");'
    del batch_id,year_start,year_end,course_name,year_code
    return query
