import mysql.connector as mysql
import datetime
import json
import util_functions

class Faculty:

    def __init__(self) -> None:

        self.faculty_id:str=None
        self.name:str=None
        self.faculty_email:str=None
        self.faculty_contact:str=None
        self.department=None

        with open("config.json","r") as f:
            data=json.load(f)
            data=data['db']
            f.close()

        self._connection=mysql.connect(host=data['host'],user=data['user'],passwd=data['password'],database=data['database'])
        self._cursor=self._connection.cursor()

    def exists(self):
        query=f'SELECT count(*) FROM faculty WHERE faculty_id="{self.faculty_id}";'
        self._cursor.execute(query)
        self.records=self._cursor.fetchall()
        print(int(self.records[0][0]))
        return int(self.records[0][0]) != 0
    
    def add_faculty(self,data:tuple):
        query=f'INSERT INTO faculty(faculty_id,faculty_name,email,contact,department)VALUES("{self.faculty_id}","{self.name}","{self.faculty_email}","{self.faculty_contact}","{self.department}");'
        self._cursor.execute(query)
        self._connection.commit()

    def get_faculty_details(self):
        query=f'SELECT * FROM faculty WHERE faculty_id="{self.faculty_id}";'
        self._cursor.execute(query)
        self.records=self._cursor.fetchone()
        return self.records

