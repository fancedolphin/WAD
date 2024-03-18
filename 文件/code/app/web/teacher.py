from . import web
from flask import jsonify,render_template,redirect,session,url_for ,request,flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Student,Teacher,Manager,College,Major,Course_select_table,Course,Course_Teacher
from app import db

# 录入成绩页
@web.route('/add_score',methods=['GET','POST'])
@login_required
def add_score():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('add_score.html')

# 获取所有课程
@web.route('/getTeacherCourses',methods=['GET'])
@login_required
def getCourses():
    if isinstance(current_user._get_current_object(), Teacher):
        user_no = current_user.get_id()
        courses = Course_Teacher.query.filter_by(TEACHER_NO=user_no).all()
        data = []
        for key in courses:
            obj = {}
            c = Course.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            obj['course_no'] = c.COURSE_NO
            obj['course_name'] = c.COURSE_NAME
            obj['course_credit'] = c.COURSE_CREDIT
            obj['course_hour'] = c.COURSE_HOUR
            data.append(obj)
        return jsonify(data)

# 获取当前课程的所有已选课学生
@web.route('/add_score/getCourseAll/<course_no>',methods=['GET'])
@login_required
def getCourseAll(course_no):
    if isinstance(current_user._get_current_object(), Teacher):
        user_no = current_user.get_id()
        tableList = Course_select_table.query.filter_by(TEACHER_NO=user_no,COURSE_NO=course_no).all()
        data = []
        index = 0
        for key in tableList:
            obj = {}
            index = index + 1
            course = Course.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            student = Student.query.filter_by(STU_NO=key.STU_NO).first()

            obj['number'] = index
            obj['course_name'] = course.COURSE_NAME
            obj['stu_no'] = key.STU_NO
            obj['stu_name'] = student.STU_NAME
            obj['stu_college'] = student.college.COLLEGE_NAME
            obj['stu_major'] = student.major.MAJOR_NAME
            obj['in_year'] = student.IN_YEAR
            obj['grade'] = key.GRADE
            data.append(obj)
        print(data)
        return jsonify(data)

# 录入成绩
@web.route('/add_score/inputGrade',methods=['POST'])
@login_required
def inputGrade():
    if isinstance(current_user._get_current_object(), Teacher):
        user_no = current_user.get_id()
        stu_no = request.values.get('stu_no')
        course_no = request.values.get('course_no')
        grade = request.values.get('grade')
        res = Course_select_table.query.filter_by(TEACHER_NO=user_no,COURSE_NO=course_no,STU_NO=stu_no).first()
        res.input_grade(grade)
        db.session.commit()
        return jsonify({'msg':'录入成功','code':200})

# 课程设置页
@web.route('/course_setup',methods=['GET'])
@login_required
def course_setup():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('course_setup.html')
    
# 获取所有教师课程信息
@web.route('/course_setup/getTeacherAllCourses',methods=['GET'])
@login_required
def getTeacherAllCourses():
    if isinstance(current_user._get_current_object(), Teacher):
        user_no = current_user.get_id()
        teacher = Teacher.query.filter_by(TEACHER_NO=user_no).first()
        data = []
        for key in teacher.COURSES:
            # print(key)
            obj = {}
            obj['course_no'] = key.COURSE_NO
            obj['course_name'] = key.COURSE_NAME
            obj['course_credit'] = key.COURSE_CREDIT
            obj['course_hour'] = key.COURSE_HOUR
            obj['college'] = key.college.COLLEGE_NAME
            obj['college_no'] = key.college.COLLEGE_NO
            course_capacity = Course_Teacher.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            obj['course_capacity'] = course_capacity.COURSE_CAPACITY
            data.append(obj)
        # print(data)
        return jsonify(data)

# 修改课程容量
@web.route('/course_setup/edit_course',methods=['POST'])
@login_required
def course_setup_edit():
    if isinstance(current_user._get_current_object(), Teacher):
        user_no = current_user.get_id()
        course_no = request.values.get('courses_no')
        course_capacity = request.values.get('course_capacity')
        teacher_course = Course_Teacher.query.filter_by(TEACHER_NO=user_no,COURSE_NO=course_no).first()
        teacher_course.COURSE_CAPACITY = course_capacity
        db.session.commit()
        return redirect(url_for('web.course_setup'))

# 添加课程页
@web.route('/add_teacher_course',methods=['GET'])
@login_required
def add_teacher_course():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('add_teacher_course.html')

# 添加课程
@web.route('/add_teacher_course/add_course',methods=['POST'])
@login_required
def course_setup_add():
    if isinstance(current_user._get_current_object(), Teacher):
        user_no = current_user.get_id()
        error = None
        course_no = request.values.get('courses_no')
        course_capacity = request.values.get('course_capacity')
        course_capacity = int(course_capacity)
        course_teacher = Course_Teacher.query.filter_by(TEACHER_NO=user_no,COURSE_NO=course_no).first()
       
        if not course_teacher and course_teacher is None:
            res = Course_Teacher(TEACHER_NO=user_no,COURSE_NO=course_no,COURSE_CAPACITY=course_capacity)
            db.session.add(res)
            db.session.commit()
            error = u'添加' + course_no + '课程成功'
            flash(error)
            return render_template('add_teacher_course.html', error=error)
           
        else:
            error =  u'已有' + course_no + '课程'
            flash(error)
            return render_template('add_teacher_course.html', error=error)

# 删除当前课程
@web.route('/course_setup/delete_course',methods=['POST'])
@login_required
def course_setup_delete():
    if isinstance(current_user._get_current_object(), Teacher):
        user_no = current_user.get_id()
        course_no = request.values.get('delete_course_no')
        try:
            course_tables = Course_select_table.query.filter_by(TEACHER_NO=user_no).all()
            for course in course_tables:
                db.session.delete(course)
            db.session.commit()
            course_teacher =  Course_Teacher.query.filter_by(TEACHER_NO=user_no,COURSE_NO=course_no).all()
            for course in course_teacher:
                db.session.delete(course)
            db.session.commit()
            teacher = Teacher.query.filter_by(TEACHER_NO=user_no).first()
            if not teacher.COURSES:
                for course in teacher.COURSES:
                    db.session.delete(course)
                    db.session.commit()
            else:
                return jsonify({'msg':'已删除课程','code':200})
            return jsonify({'msg':'删除课程成功','code':200})
        except Exception as e:
            # print(e)
            return jsonify({'msg':'删除课程失败','code':400})