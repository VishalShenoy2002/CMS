import mysql.connector as mysql
import json

with open("config.json","r") as f:
    data=json.load(f)
    f.close()


connection=mysql.connect(host=data['db']['host'],user=data['db']['user'],passwd=data['db']['password'],database=data['db']['database'])
cursor=connection.cursor()


# Creating Tables
# ------------------

# Creating Student Table
query="""
CREATE TABLE IF NOT EXISTS students (uucms_no VARCHAR(50) NOT NULL PRIMARY KEY,name VARCHAR(100) NOT NULL, course VARCHAR(5) NOT NULL,
  semester INT NOT NULL,
  batch INT NOT NULL,
  fathers_name VARCHAR(100) NOT NULL,
  mothers_name VARCHAR(100) NOT NULL,
  stream VARCHAR(3)   NOT NULL,
  sex VARCHAR(1)   NOT NULL,
  fathers_contact VARCHAR(15)  NOT NULL,
  mothers_contact VARCHAR(15)  NOT NULL,
  students_contact VARCHAR(15)  NOT NULL,
  whatsapp_no VARCHAR(15)  NOT NULL,
  photo   BLOB  NOT NULL
  );
  """

cursor.execute(query)

# Creating Faculty Table
query="""
CREATE TABLE IF NOT EXISTS faculty (
  faculty_id   VARCHAR(25)  NOT NULL PRIMARY KEY,
  faculty_name VARCHAR(250) NOT NULL,
  email        VARCHAR(100) NOT NULL,
  contact      VARCHAR(15)  NOT NULL,
  password     VARCHAR(64)  NOT NULL DEFAULT "4bddb0a3e00962416386fea5bca2cfd9759c9ba2ead9deeb65c1727277987698",
  photo        BLOB         NOT NULL
);
"""
cursor.execute(query)

# Creating Upload Files Table
query="""
CREATE TABLE IF NOT EXISTS uploaded_files (
  id INT AUTO_INCREMENT PRIMARY KEY,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  filename VARCHAR(255) NOT NULL,
  size INT NOT NULL
);
"""
cursor.execute(query)


connection.commit()
connection.close()






