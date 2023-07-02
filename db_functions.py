import mysql.connector as mysql
import csv
import json
import os

import util_functions


with open("config.json","r") as f:
    data=json.load(f)
    f.close()


connection=mysql.connect(host=data['db']['host'],user=data['db']['user'],passwd=data['db']['password'],database=data['db']['database'])
cursor=connection.cursor()

def read_and_insert_batch(csvfile:str):
    with open(csvfile,"r") as f:
        reader=csv.reader(f)

        records=[row for row in reader]
        records=[util_functions.insert_into_student(row) for row in records]

        for index,query in enumerate(records,start=1):
            try:
                cursor.execute(query)
                print(f"{index} records inserted.",end='\r')
            except:
                continue

        connection.commit()

def check_cred(username,password):
    query=util_functions.check_cred_query(username)
    cursor.execute(query)
    dbpassword=cursor.fetchone()[0]
    
    return password == dbpassword

def read_and_insert_students(csvfile:str):
    with open(csvfile,"r") as f:
        reader=csv.reader(f)

        records=[row for row in reader]
        records=[util_functions.insert_basic_student_details(row) for row in records]

        for index,query in enumerate(records,start=1):
            try:
                cursor.execute(query)
                print(f"{index} records inserted.",end='\r')
            except:
                continue

        connection.commit()
        del records,reader

def insert_course(data:tuple):
    query=util_functions.insert_course_query(data)
    cursor.execute(query)
    connection.commit()  
    del query 

def insert_subject(data:tuple):
    query=util_functions.insert_subject_query(data)
    cursor.execute(query)  
    connection.commit()
    del query

def get_similar_key_count(key:str):
    query=util_functions.get_similar_key_count_query(key)
    cursor.execute(query)
    count=cursor.fetchone()
    count=count[0]
    return int(count)

def insert_batch(data:tuple):
    query=util_functions.insert_batch_query(data)
    cursor.execute(query)
    connection.commit()
    del query

def generate_batch_table_view(department:str,batch:int):
    query=util_functions.generate_batch_table_view_query(department,batch)
    cursor.execute(query)
    connection.commit()
    del query