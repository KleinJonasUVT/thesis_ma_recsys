from flask import Flask, render_template, jsonify
from database import load_courses_from_db, load_course_from_db, load_courselist_from_db, get_max_courselist_pages
from sqlalchemy import create_engine
from sqlalchemy import text
import os

app = Flask(__name__)

filters = {
    'Degree': ['Bachelor', 'Master', 'Pre-master'],
    'Block': [1, 2, 3, 4]
}

@app.route("/")
def show_courselist_first():
  courselist = load_courselist_from_db('1')
  max_pages = get_max_courselist_pages()
  next_page_number = 2
  next_courselist = load_courselist_from_db(str(2))
  show_next_button = bool(next_courselist)
  return render_template('home.html', courselist=courselist, filters=filters, show_next_button=show_next_button, next_page = '2', max_pages=max_pages)

@app.route("/api/courses")
def list_courses():
  courses = load_courses_from_db()
  return jsonify(courses)

@app.route("/<courselist_page_number>")
def show_courselist(courselist_page_number):
  courselist = load_courselist_from_db(courselist_page_number)
  max_pages = get_max_courselist_pages()
  next_page = int(courselist_page_number) + 1
  next_courselist = load_courselist_from_db(str(next_page))
  show_next_button = bool(next_courselist)
  prev_page = int(courselist_page_number) - 1
  prev_courselist = load_courselist_from_db(prev_page)
  show_prev_button = bool(prev_courselist)
  if not courselist:
    return "Not Found", 404
  else:
    return render_template('home.html', courselist=courselist, filters=filters, show_next_button=show_next_button, show_prev_button=show_prev_button, next_page=next_page, prev_page=prev_page, max_pages=max_pages)

@app.route("/course/<course_code>")
def show_course(course_code):
  course = load_course_from_db(course_code)
  if not course:
    return "Not Found", 404
  else:
    return render_template('coursepage.html',
                        course=course)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)