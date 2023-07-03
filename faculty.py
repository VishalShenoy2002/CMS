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
        self.designation=None

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
        del query
        return int(self.records[0][0]) != 0
    
    def add_faculty(self,data:tuple):
        query=f'INSERT INTO faculty(faculty_id,faculty_name,email,contact,department,designation)VALUES("{self.faculty_id}","{self.name}","{self.faculty_email}","{self.faculty_contact}","{self.department}","{self.designation}");'
        self._cursor.execute(query)
        del query
        self._connection.commit()

    def get_faculty_details(self):
        query=f'SELECT * FROM faculty WHERE faculty_id="{self.faculty_id}";'
        self._cursor.execute(query)
        self.records=self._cursor.fetchone()
        del query
        return self.records
    
    def fetch_designation(self):
        query=f'SELECT designation FROM faculty WHERE faculty_id="{self.faculty_id}";'
        self._cursor.execute(query)
        self.records=self._cursor.fetchone()[0]
        del query
        return self.records


