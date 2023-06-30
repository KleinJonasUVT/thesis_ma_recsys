from flask import Flask, render_template, jsonify
from database import load_courses_from_db

app = Flask(__name__)

@app.route("/")
def hello_world():
  courses = load_courses_from_db()
  return render_template('home.html',
                        courses=courses)

@app.route("/api/courses")
def list_courses():
  courses = load_courses_from_db()
  return jsonify(courses)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)