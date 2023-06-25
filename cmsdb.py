# cmsdb.py

# cmsdb.py is mainly written to configure the database for the college management system.
# It contains queries to create tables and configure the database.

# Importing required Modules

import mysql.connector as mysql
import json
import sys

# The config.json file contains information such as host, user, password and database under the db key.
# Reading the file to extract the required information to establish database connectivity.
with open("config.json", "r") as f:
    data = json.load(f)
    f.close()


# Trying to establish a connection
connection = mysql.connect(host=data['db']['host'], user=data['db']['user'],
                           passwd=data['db']['password'], database=data['db']['database'])

# After establishing the connection checking if the connection is successful of not.
# If the is_connected() return True then its connected else its not connected
if connection.is_connected():

    # Creating a cursor object which will execute the queries in the database
    cursor = connection.cursor()
    # Query to create courses table if it doesn't exist
    query = """
  CREATE TABLE IF NOT EXISTS courses (
      course_name VARCHAR(5) PRIMARY KEY  NOT NULL,
      full_form VARCHAR(250) NOT NULL,
      num_of_sems INT NOT NULL
  );
  """
    # execute() will execute the query that is given as paramenter
    cursor.execute(query)

    # Query to create the students table if it doesn't exist
    query = """
  CREATE TABLE IF NOT EXISTS students (uucms_no VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, 
    course VARCHAR(5) NOT NULL,
    semester INT NOT NULL,
    batch INT NOT NULL,
    fathers_name VARCHAR(100) NOT NULL DEFAULT "Not Mentioned",
    mothers_name VARCHAR(100) NOT NULL DEFAULT "Not Mentioned",
    stream VARCHAR(10)   NOT NULL DEFAULT "NA",
    sex VARCHAR(1)   NOT NULL DEFAULT "-",
    fathers_contact VARCHAR(15)  NOT NULL DEFAULT "Not Mentioned",
    mothers_contact VARCHAR(15)  NOT NULL DEFAULT "Not Mentioned",
    students_contact VARCHAR(15)  NOT NULL DEFAULT "Not Mentioned",
    whatsapp_no VARCHAR(15)  NOT NULL DEFAULT "Not Mentioned",
    photo   BLOB,
    year_code VARCHAR(15) NOT NULL
    FOREIGN KEY (course) REFERENCES courses(course_name),
    FOREIGN KEY (year_code) REFERENCES batches(year_code)
    );
    """
    # execute() will execute the query that is given as paramenter
    cursor.execute(query)

    # Query to create faculty table if it doesn't exist
    query = """
  CREATE TABLE IF NOT EXISTS faculty (
    faculty_id   VARCHAR(25)  NOT NULL PRIMARY KEY,
    faculty_name VARCHAR(250) NOT NULL,
    email        VARCHAR(100) NOT NULL,
    contact      VARCHAR(15)  NOT NULL,
    department   VARCHAR(5) NOT NULL,
    current_status VARCHAR(10) NOT NULL DEFAULT "Working",
    post         VARCHAR(50) NOT NULL DEFAULT "HOD",
    password     VARCHAR(64)  NOT NULL DEFAULT "4bddb0a3e00962416386fea5bca2cfd9759c9ba2ead9deeb65c1727277987698",
    photo        BLOB   

  );
  """
    # execute() will execute the query that is given as paramenter
    cursor.execute(query)

    # Query to create ppload files table if it doesn't exist
    query = """
  CREATE TABLE IF NOT EXISTS uploaded_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    filename VARCHAR(255) NOT NULL,
    size INT NOT NULL
  );
  """
    # execute() will execute the query that is given as paramenter
    cursor.execute(query)


    # Query to create batchs table if it doesn't exist
    query = """
  CREATE TABLE IF NOT EXISTS batches (
    batch_id VARCHAR(50) NOT NULL PRIMARY KEY,
    year_start INT NOT NULL,
    year_end INT NOT NULL,
    course_name VARCHAR(5) NOT NULL,
    year_code varchar(15) NOT NULL,
    FOREIGN KEY (course_name) REFERENCES courses (course_name)
);
  """
    # execute() will execute the query that is given as paramenter
    cursor.execute(query)

    # Query to create subject table
    query = """
CREATE TABLE IF NOT EXISTS subjects (
  subject_code VARCHAR(20) NOT NULL PRIMARY KEY,
  subject_name VARCHAR(100) NOT NULL,
  course_name VARCHAR(5) NOT NULL,
  subject_type VARCHAR(50) NOT NULL DEFAULT 'Core',
  syllabus_type VARCHAR(10) NOT NULL DEFAULT 'NEP',
  semester int(2) not null default 1,
  FOREIGN KEY (course_name) REFERENCES courses (course_name)
);
  """
    
    # execute() will execute the query that is given as paramenter
    cursor.execute(query)

    # Query to create subjects_for_batch table
    query = """
 CREATE TABLE IF NOT EXISTS subjects_for_batch (
  batch_id VARCHAR(50) NOT NULL,
  subject_1 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  subject_2 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  subject_3 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  subject_4 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  subject_5 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  subject_6 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  subject_7 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  lab_1 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  lab_2 VARCHAR(20) NOT NULL DEFAULT 'N/A',
  FOREIGN KEY (batch_id) REFERENCES batches (batch_id),
  FOREIGN KEY (subject_1) REFERENCES subjects (subject_code),
  FOREIGN KEY (subject_2) REFERENCES subjects (subject_code),
  FOREIGN KEY (subject_3) REFERENCES subjects (subject_code),
  FOREIGN KEY (subject_4) REFERENCES subjects (subject_code),
  FOREIGN KEY (subject_5) REFERENCES subjects (subject_code),
  FOREIGN KEY (subject_6) REFERENCES subjects (subject_code),
  FOREIGN KEY (subject_7) REFERENCES subjects (subject_code),
  FOREIGN KEY (lab_1) REFERENCES subjects (subject_code),
  FOREIGN KEY (lab_2) REFERENCES subjects (subject_code)
);

    """
    
    # execute() will execute the query that is given as paramenter
    cursor.execute(query)

    # Commiting all additions and changes that is made so that it reflects in the database.
    connection.commit()

  # Closing the database connection
    connection.close()

# If the connection is not established then the program exists with a message saying "Database is not connected"
else:
    sys.exit("Database is not connected")