from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import load_courses_from_db, load_course_from_db, load_courselist_from_db, get_max_courselist_pages, add_rating_to_db, get_rating_from_db, add_filter_to_db, get_filter_from_db

app = Flask(__name__)

filters = {
    'Degree': ['Bachelor', 'Master', 'Pre-master'],
    'Block': [1, 2, 3, 4]
}

@app.route("/")
def show_courselist_first():
  courselist = load_courselist_from_db('1')
  max_pages = get_max_courselist_pages()
  rating_db = {}

  for course in courselist:
    course_code = course['course_code']
    rating_db[course_code] = get_rating_from_db(course_code)
  
  next_page_number = 2
  filter_db = get_filter_from_db()
  next_courselist = load_courselist_from_db(str(2))
  show_next_button = bool(next_courselist)
  courselist_page_number=1
  is_less_than_5 = int(courselist_page_number) < 5
  return render_template('home.html', courselist=courselist, filters=filters, show_next_button=show_next_button, next_page = '2', max_pages=max_pages, courselist_page_number=courselist_page_number, is_less_than_5=is_less_than_5, rating_db = rating_db, filter_db=filter_db)

@app.route("/api/courses")
def list_courses():
  courses = load_courses_from_db()
  return jsonify(courses)

@app.route("/<courselist_page_number>")
def show_courselist(courselist_page_number):
  courselist = load_courselist_from_db(courselist_page_number)
  max_pages = get_max_courselist_pages()
  rating_db = {}

  for course in courselist:
    course_code = course['course_code']
    rating_db[course_code] = get_rating_from_db(course_code)
    
  next_page = int(courselist_page_number) + 1
  filter_db = get_filter_from_db()
  next_courselist = load_courselist_from_db(str(next_page))
  show_next_button = bool(next_courselist)
  prev_page = int(courselist_page_number) - 1
  prev_courselist = load_courselist_from_db(prev_page)
  show_prev_button = bool(prev_courselist)
  courselist_page_number=int(courselist_page_number)
  is_less_than_5 = int(courselist_page_number) < 5
  is_more_than_4 = int(courselist_page_number) > 4
  is_more_than_3_to_end = int(max_pages - courselist_page_number) > 3
  is_less_than_4_to_end = int(max_pages - courselist_page_number) < 4
  if not courselist:
    return "Not Found", 404
  else:
    return render_template('home.html', courselist=courselist, filters=filters, show_next_button=show_next_button, show_prev_button=show_prev_button, next_page=next_page, prev_page=prev_page, max_pages=max_pages, courselist_page_number=courselist_page_number, is_less_than_5=is_less_than_5, is_more_than_4=is_more_than_4, is_more_than_3_to_end=is_more_than_3_to_end, is_less_than_4_to_end=is_less_than_4_to_end, rating_db=rating_db, filter_db=filter_db)

@app.route("/course/<course_code>")
def show_course(course_code):
  course = load_course_from_db(course_code)
  if not course:
    return "Not Found", 404
  else:
    return render_template('coursepage.html',
                        course=course)

@app.route("/course/<course_code>/rating", methods=['POST'])
def rating_course(course_code):
    data = request.form
    add_rating_to_db(course_code, data)
    previous_page = request.referrer
    return redirect(previous_page)

@app.route("/filter", methods=['POST'])
def filter():
    filter_name = request.form['filter_name']
    filter_value = request.form[filter_name]
    add_filter_to_db(filter_name, filter_value)
    return jsonify(filter_value)

#redirect(url_for('show_courselist_first'))

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)