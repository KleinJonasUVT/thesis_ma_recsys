from sqlalchemy import create_engine
from sqlalchemy import text
import os
import math

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }
)

def load_courses_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM courses"))
    courses = []
    columns = result.keys()
    for row in result:
      result_dict = {column: value for column, value in zip(columns, row)}
      courses.append(result_dict)
    return courses

def load_course_from_db(course_code):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courses WHERE course_code = :val"), parameters=dict(val=course_code))
        course = []
        columns = result.keys()
        for row in result:
            result_dict = {column: value for column, value in zip(columns, row)}
            if len(row) == 0:
                return None
            else:
                return result_dict

def load_courselist_from_db(courselist_page_number):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM (SELECT *, (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1) DIV 3 + 1 AS pair_num FROM courses) AS numbered_rows WHERE pair_num = :val;"), parameters=dict(val=courselist_page_number))
    courselist = []
    columns = result.keys()
    for row in result:
      result_dict = {column: value for column, value in zip(columns, row)}
      courselist.append(result_dict)
    return courselist

def get_max_courselist_pages():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM courses"))
        total_rows = result.scalar()
    max_pages = math.floor((total_rows - 1) / 3) + 1
    return max_pages

def add_rating_to_db(course_code, data):
    with engine.connect() as conn:
        existing_rating = conn.execute(
            text("SELECT course_code FROM ratings WHERE course_code = :course_code"),
            {"course_code": course_code}
        ).fetchone()
      
        if existing_rating:
            conn.execute(
                text("UPDATE ratings SET rating = :rating WHERE course_code = :course_code"),
                {"course_code": course_code, "rating": data['rate']}
            )
        else:
            conn.execute(
                text("INSERT INTO ratings (course_code, rating) VALUES (:course_code, :rating)"),
                {"course_code": course_code, "rating": data['rate']}
            )


  
  







