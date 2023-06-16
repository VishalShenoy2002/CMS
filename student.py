# student.py

# student.py contains the student class which will be used to verify the student, add the student 
# and perform other db functionalities.

# Importing required modules
import mysql.connector as mysql
import datetime
import json

class Student:

    def __init__(self) -> None:

        self.uucms_no:str=None
        self.name=None
        self.batch=datetime.date.today().year
        self.department=None

        with open("config.json","r") as f:
            data=json.load(f)
            data=data['db']
            f.close()
        

        
        self._connection=mysql.connect(host=data['host'],user=data['user'],passwd=data['password'],database=data['database'])
        self._cursor=self._connection.cursor()

    def exists(self):
        query=f'SELECT * FROM students WHERE batch={self.batch} and uucms_no="{self.uucms_no}"'
        self._cursor.execute(query)
        self.records=self._cursor.fetchone()
        try:
            return len(self.records) is not 0
        
        except TypeError:
            return None
    def get_student_name(self):
        query=f'SELECT name FROM students WHERE batch={self.batch} and uucms_no="{self.uucms_no}"'
        self._cursor.execute(query)
        self.name=self._cursor.fetchone()[0]
        return self.name
