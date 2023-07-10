import mysql.connector as mysql
import json
import db_functions


class Course:
    def __init__(self):
        self.course_name: str = None
        with open("config.json", "r") as f:
            data = json.load(f)
            data = data['db']
            f.close()

        self._connection = mysql.connect(host=data['host'], user=data['user'], passwd=data['password'], database=data['database'])
        self._cursor = self._connection.cursor()

    def course_count(self):
        query = "SELECT count(*) FROM courses;"
        self._cursor.execute(query)

        count = self._cursor.fetchone()[0]
        del query
        return count

    def courses_available(self):
        query=f'SELECT course_name FROM courses;'
        self._cursor.execute(query)

        courses=[x[0] for x in self._cursor.fetchall()]
        del query
        return courses

    def exists(self):
        return self.course_count() != 0

        



