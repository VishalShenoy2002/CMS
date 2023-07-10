import mysql.connector as mysql
import json
import db_functions


class Subject:
    def __init__(self):
        self.subject_name: str = None
        self.course_name: str = None
        self.subject_type: str = None


        with open("config.json", "r") as f:
            data = json.load(f)
            data = data['db']
            f.close()

        self._connection = mysql.connect(host=data['host'], user=data['user'], passwd=data['password'], database=data['database'])
        self._cursor = self._connection.cursor()

    def get_core_subject_names(self,semester:int):
        query=f'SELECT subject_name FROM subjects WHERE subject_type="{self.subject_type}" and semester={semester};'
        self._cursor.execute(query)

        self.records=self._cursor.fetchall()
        self.records=[x[0] for x in self.records]
        del query
        return self.records
    
    def get_subject_code_from_name(self,name:str,semester:int):
        query=f'SELECT subject_code FROM subjects WHERE subject_name="{name}" and semester={semester};'
        self._cursor.execute(query)

        self.records=self._cursor.fetchone()
        self.records=self.records[0]
        del query
        return self.records
    
    def allot_subjects_for_batch(self,batch:str,subject_dict:dict):
        if len(subject_dict) <= 7:
            subject_1,subject_2,subject_3,subject_4,subject_5,subject_6,subject_7=tuple(subject_dict.values())
            query=f'INSERT INTO subjects_for_batch(batch_id,subject_1,subject_2,subject_3,subject_4,subject_5,subject_6,subject_7)VALUES("{batch}","{subject_1}","{subject_2}","{subject_3}","{subject_4}","{subject_5}","{subject_6}","{subject_7}");'
            del subject_1,subject_2,subject_3,subject_4,subject_5,subject_6,subject_7
        else:
            subject_1,subject_2,subject_3,subject_4,subject_5,subject_6,subject_7,lab_1,lab_2=tuple(subject_dict.values())
            query=f'INSERT INTO subjects_for_batch(batch_id,subject_1,subject_2,subject_3,subject_4,subject_5,subject_6,subject_7,lab_1,lab_2)VALUES("{batch}","{subject_1}","{subject_2}","{subject_3}","{subject_4}","{subject_5}","{subject_6}","{subject_7}","{lab_1}","{lab_2}");'
            del subject_1,subject_2,subject_3,subject_4,subject_5,subject_6,subject_7,lab_1,lab_2
        
        self._cursor.execute(query)
        self._connection.commit()
        