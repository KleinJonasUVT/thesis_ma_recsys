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

#Retrieving data from SQL
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
    filters = get_filter_from_db()
    filter_conditions = []
    filter_params = {}
    for filter_key, filter_value in filters.items():
        filter_param_name = f"filter_{filter_key}"
        filter_conditions.append(f"{filter_key} = :{filter_param_name}")
        filter_params[filter_param_name] = filter_value

    filter_sql = " AND ".join(filter_conditions)

    query = text(
        f"SELECT * FROM (SELECT *, (ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) - 1) DIV 3 + 1 AS pair_num FROM courses WHERE {filter_sql}) AS numbered_rows WHERE pair_num = :val;"
    )

    with engine.connect() as conn:
        result = conn.execute(query, parameters={**filter_params, "val": courselist_page_number})

    courselist = []
    columns = result.keys()
    for row in result:
        result_dict = {column: value for column, value in zip(columns, row)}
        courselist.append(result_dict)
    return courselist

def get_max_courselist_pages():
    filters = get_filter_from_db()  # Retrieve filter dictionary
    filter_conditions = []
    filter_params = {}
    for filter_key, filter_value in filters.items():
        filter_param_name = f"filter_{filter_key}"
        filter_conditions.append(f"{filter_key} = :{filter_param_name}")
        filter_params[filter_param_name] = filter_value

    filter_sql = " AND ".join(filter_conditions)

    query = text(
        f"SELECT COUNT(*) FROM courses WHERE {filter_sql};"
    )

    with engine.connect() as conn:
        result = conn.execute(query, parameters=filter_params)
        total_rows = result.scalar()

    max_pages = math.floor((total_rows - 1) / 3) + 1
    return max_pages

def get_rating_from_db(course_code):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT rating FROM ratings WHERE course_code = :val"), parameters=dict(val=course_code))
        rating_row = result.fetchone()
        if rating_row is not None:
            rating = rating_row[0]
            return rating
        else:
            return 0

def get_filter_from_db():
    with engine.connect() as conn:
      result = conn.execute(text("SELECT filter, filter_value FROM filters;"))
      filters = result.fetchall()
      filters_dict = {row[0]: row[1] for row in filters}

      return filters_dict

#Adding data to SQL
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

def add_filter_to_db(filter_name, filter_value):
    with engine.connect() as conn:
        existing_filter = conn.execute(
            text("SELECT filter_value FROM filters WHERE filter = :filter"), {"filter": filter_name})
      
        if existing_filter:
            conn.execute(
                text("UPDATE filters SET filter_value = :filter_value WHERE filter = :filter"),
                {"filter": filter_name, "filter_value": filter_value}
            )
        else:
            conn.execute(
                text("INSERT INTO filters (filter, filter_value) VALUES (:filter, :filter_value)"),
                {"filter": filter_name, "filter_value": filter_value}
            )





  
  







