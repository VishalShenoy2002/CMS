import mysql.connector as mysql
import json
import db_functions
class Batch:

    def __init__(self):
        self.start_year:int=None
        self.department:str=None

        with open("config.json","r") as f:
                    data=json.load(f)
                    data=data['db']
                    f.close()

        self._connection=mysql.connect(host=data['host'],user=data['user'],passwd=data['password'],database=data['database'])
        self._cursor=self._connection.cursor()


    def set_end_year(self):
        query=f'SELECT num_of_sems FROM courses WHERE course_name="{self.department}";'
        self._cursor.execute(query)

        self.no_of_sems=self._cursor.fetchone()[0]
        self.end_year=int(self.start_year) + (int(self.no_of_sems)//2)


    def generate_batch_code(self):
        short_start_year=self.start_year % 2000
        short_end_year=self.end_year % 2000

        self.year_code=f"{short_start_year}{short_end_year}"
        code=f"NEP-{self.department}-{self.year_code}"
        return code
    
    def get_year_code(self):
        short_start_year=str(self.start_year % 2000)
        short_end_year=str(self.end_year % 2000)
        return f"20{short_start_year}-{short_end_year}"
    
    def create_batch(self):
        batch_code=self.generate_batch_code()
        year_code=self.get_year_code()
        record=(batch_code,self.start_year,self.end_year,self.department,year_code)
        db_functions.insert_batch(record)

    def generate_batch_table(self):
        db_functions.generate_batch_table_view(self.department,self.start_year)




