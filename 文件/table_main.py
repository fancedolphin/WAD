from flask import Flask, request, redirect, url_for, render_template, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


users = {}

connection = create_connection("localhost", "root", "1111", "learning_system")
cursor = connection.cursor()
try:
    select_users = """SELECT * FROM users"""
    cursor.execute(select_users)
    rows = cursor.fetchall()
    for user in rows:
        username = user[1]
        password = user[2]
        identity = user[3]
        users[username] = {'password': password, 'identity': identity}
except Error as e:
    print(f"The error '{e}' occurred")
# finally:
#     cursor.close()
#     connection.close()

print(users)

student_info = {}
Instructor_info = {}
Admin_info = {}


@app.route('/')
def toLogin():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        identity = request.form['identity']

        if username in users and users[username]['password'] == password and users[username]['identity'] == identity:
            select_user_query = """SELECT * FROM users WHERE username = %s """
            cursor.execute(select_user_query, (username,))
            user_data = cursor.fetchall()
            user_tuple = user_data[0]
            print(user_data)
            if identity == 'S':
                student_info['name'] = user_tuple[1]
                student_info['student_id'] = user_tuple[0]
                student_info['level'] = user_tuple[4]
                student_info['class'] = user_tuple[10]
                student_info['major'] = user_tuple[9]
                return redirect(url_for('stu_home'))
            if identity == 'I':
                Instructor_info['name'] = user_tuple[1]
                Instructor_info['Instructor_id'] = user_tuple[0]
                return redirect(url_for('ins_home'))
            if identity == 'A':
                return redirect(url_for('adm_home'))
        else:
            # login fail
            return redirect(url_for('error'))
    else:
        return render_template('login.html')


# --------------------------------------------------------------------------------------------------------------
@app.route('/api/course-table')
def get_all_courses():
    stud_courses = []
    cursor.execute("SELECT enrollments.course_id FROM enrollments WHERE  student_id = %s", [student_info['student_id']])
    rows = cursor.fetchall()
    for courses_id in rows:
        number = courses_id[0]
        cursor.execute("SELECT * FROM course WHERE course_id = %s", [number])
        stu_courses = cursor.fetchall()
        for course in stu_courses:
            cursor.execute("SELECT username FROM users WHERE user_id = %s", [course[2]])
            InsName = cursor.fetchall()
            stud_course = {
                'course_id': course[0],
                'course_name': course[1],
                'level': course[4],
                'class': course[6],
                'instructor': InsName,
                'semester': course[5],
                'day': course[-2],
                'section': course[-1],
            }
            stud_courses.append(stud_course)
    return jsonify(stud_courses)


# --------------------------------------------------------------------------------------------------------------
cursor.execute("SELECT * FROM course ")
all_course = cursor.fetchall()
allCourses = []
for course in all_course:
    cursor.execute(
        "SELECT users.username FROM course JOIN users ON course.instructor_id = users.user_id ORDER BY course.course_id ASC;")
    usernames = cursor.fetchall()
    courses = {
        'id': course[0],
        'category': course[-4],
        'level': course[4],
        'semester': course[5],
        'course_name': course[1],
        'instructor': usernames[course[0] - 1],
        'selected': False
    }
    allCourses.append(courses)
print(allCourses)


@app.route('/courses', methods=['GET'])
def get_courses():
    # 获取查询参数 category
    category = request.args.get('category')
    print(category)
    # 如果没有提供 category 参数，则返回所有课程
    if not category:
        return jsonify(courses)

    # 根据 category 过滤课程
    cursor.execute("SELECT course_id FROM enrollments")
    enrollments = cursor.fetchall()
    connection.commit()
    filtered_courses = [course1 for course1 in allCourses if course1['category'] == category and course1['id'] not in [enrollment[0] for enrollment in enrollments]]

    if category == 'Selected':
        filtered_courses = []
        for course2 in allCourses:
            for enrollment in enrollments:
                if enrollment[0] == course2['id']:
                    course2['selected'] = True
                    course2['category'] = 'Selected'
                    filtered_courses.append(course2)
    return jsonify(filtered_courses)


@app.route('/select-course', methods=['POST'])
def select_course():
    course_id = request.args.get('courseId')
    category = request.args.get('category')
    print(category)
    for course in allCourses:
        if str(course['id']) == course_id:
            course['selected'] = True
            course['category'] = category
            add_enrollment = ("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)")
            data_enrollment = (student_info['student_id'], course_id)
            cursor.execute(add_enrollment, data_enrollment)
            connection.commit()
            print(category)
            return jsonify({'message': 'Course selected successfully.'})
    return jsonify({'error': 'Course not found.'}), 404


@app.route('/cancel-course', methods=['POST'])
def cancel_course():
    course_id = request.args.get('courseId')
    original_category = request.args.get('originalCategory')
    for course in allCourses:
        if str(course['id']) == course_id and course.get('selected'):
            course['selected'] = False
            delete_enrollment = ("DELETE FROM enrollments WHERE student_id = %s AND course_id = %s")
            data_enrollment = (student_info['student_id'], course_id)
            cursor.execute(delete_enrollment, data_enrollment)
            connection.commit()
            print(original_category)
            course['category'] = original_category if original_category in ['Required', 'Optional'] else 'Selected'
            return jsonify({'message': 'Course cancelled successfully.'})

    return jsonify({'error': 'Course not found or not selected.'}), 404


# --------------------------------------------------------------------------------------
@app.route('/api/student-info')
def get_student_info():
    print(student_info)
    return jsonify(student_info)


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/stu_home')
def stu_home():
    return render_template('student/stu_home.html')


@app.route('/ins_home')
def ins_home():
    return render_template('instructor/ins_home.html')


@app.route('/adm_home')
def adm_home():
    return render_template('admin/adm_home.html')


@app.route('/stu_course', methods=['GET', 'POST'])
def stu_course():
    return render_template('student/stu_course.html')


@app.route('/grade', methods=['GET', 'POST'])
def stu_Grade():
    return render_template('student/grade.html')


@app.route('/StuInformation', methods=['GET', 'POST'])
def stuInformation():
    return render_template('student/stuInformation.html')


@app.route('/homework', methods=['GET', 'POST'])
def homework():
    return render_template('student/homework.html')


@app.route('/Lecture', methods=['GET', 'POST'])
def lecture():
    return render_template('student/lecture.html')


@app.route('/Submission', methods=['GET', 'POST'])
def submission():
    return render_template('student/submission.html')


@app.route('/Email', methods=['GET', 'POST'])
def email():
    return render_template('student/Email.html')


if __name__ == '__main__':
    app.run()
