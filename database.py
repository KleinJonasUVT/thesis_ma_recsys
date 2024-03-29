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
    query = text("SELECT * FROM filters WHERE current_value = 'yes'")

    with engine.connect() as conn:
        filters_db = conn.execute(query).fetchall()

    current_filters = {}
    for filter_name, value, option in filters_db:
        if filter_name not in current_filters:
            current_filters[filter_name] = []
        current_filters[filter_name].append((value, option))

    filter_conditions = []
    for filter_name, filter_values in current_filters.items():
        for value, option in filter_values:
            # Modify the condition based on your table columns
            condition = f"{filter_name} = '{value}'"
            filter_conditions.append(condition)

    where_clause = " AND ".join(filter_conditions)

    query_template = """
        SELECT *
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS row_num
            FROM courses
            {where_clause}
        ) AS filtered_courses
        WHERE (row_num - 1) DIV 3 + 1 = :val
    """
    
    if filter_conditions:
        where_clause = "WHERE " + " AND ".join(filter_conditions)
    else:
        where_clause = ""
    
    query = text(query_template.format(where_clause=where_clause))

    with engine.connect() as conn:
        result = conn.execute(query, parameters={"val": courselist_page_number})

    courselist = []
    columns = result.keys()
    for row in result:
        result_dict = {column: value for column, value in zip(columns, row)}
        courselist.append(result_dict)
    return courselist

def get_max_courselist_pages():
    query = text("SELECT * FROM filters WHERE current_value = 'yes'")

    with engine.connect() as conn:
        filters_db = conn.execute(query).fetchall()

    current_filters = {}
    for filter_name, value, option in filters_db:
        if filter_name not in current_filters:
            current_filters[filter_name] = []
        current_filters[filter_name].append((value, option))

    filter_conditions = []
    for filter_name, filter_values in current_filters.items():
        for value, option in filter_values:
            # Modify the condition based on your table columns
            condition = f"{filter_name} = '{value}'"
            filter_conditions.append(condition)

    where_clause = " AND ".join(filter_conditions)

    if filter_conditions:
        query_template = "SELECT COUNT(*) FROM courses WHERE {where_clause};"
    else:
        query_template = "SELECT COUNT(*) FROM courses;"

    query = text(query_template.format(where_clause=where_clause))

    with engine.connect() as conn:
        result = conn.execute(query)
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
      query = text("SELECT * FROM filters")
      filters_db = conn.execute(query).fetchall()

      filters = {}
      for filter_name, value, option in filters_db:
        if filter_name not in filters:
            filters[filter_name] = []
        filters[filter_name].append((value, option))

      return filters

def remove_rating_from_db(course_code):
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM ratings WHERE course_code = :course_code"),
            {"course_code": course_code}
        )

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
    
    conn.execute(text("UPDATE filters SET current_value = 'no' WHERE filter_name = :name"), {"name": filter_name}
                    )
    
    conn.execute(text("UPDATE filters SET current_value = 'yes' WHERE filter_name = :name AND filter_value = :value"), {"name": filter_name, "value": filter_value}
                )
