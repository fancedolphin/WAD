from . import web
from flask import jsonify,render_template,redirect,session,url_for ,request,flash
from app.utils import query,function



# 录入成绩页
@web.route('/add_score',methods=['GET','POST'])
#@login_required
def add_score():
    user_id = function.get_id()
    if function.teacher(user_id):
        return render_template('add_score.html')

# 获取所有课程
@web.route('/getTeacherCourses',methods=['GET'])
#@login_required
def getCourses():
    user_id = function.get_id()
    if function.teacher(user_id):
        user_no = user_id
        #courses = Course_Teacher.query.filter_by(TEACHER_NO=user_no).all()
        sq1 = f"SELECT * FROM `course_teacher` WHERE TEACHER_NO='{user_no}';"
        courses = query.query_dic(sq1)
        data = []
        for key in courses:
            obj = {}
            #c = Course.query.filter_by(COURSE_NO=key['COURSE_NO']).first()
            sq2 = f"SELECT * FROM `course` WHERE COURSE_NO='{key['COURSE_NO']}';"
            c = query.query_dic(sq2)
            obj['course_no'] = c[0]['COURSE_NO']
            obj['course_name'] = c[0]['COURSE_NAME']
            obj['course_credit'] = c[0]['COURSE_CREDIT']
            obj['course_hour'] = c[0]['COURSE_HOUR']
            data.append(obj)
        return jsonify(data)

# 获取当前课程的所有已选课学生
@web.route('/add_score/getCourseAll/<course_no>',methods=['GET'])
#@login_required
def getCourseAll(course_no):
    user_id = function.get_id()
    if function.teacher(user_id):
        user_no = user_id
        #print(user_no,course_no)
        #tableList = Course_select_table.query.filter_by(TEACHER_NO=user_no,COURSE_NO=course_no).all()
        sq1 = f"SELECT * FROM `course_select_table` WHERE TEACHER_NO='{user_no}' and COURSE_NO='{course_no}';"
        tableList = query.query_dic(sq1)

        data = []
        index = 0
        #print(tableList)
        try:
            for key in tableList:
                obj = {}
                index = index + 1

                #course = Course.query.filter_by(COURSE_NO=key['COURSE_NO']).first()
                sq2 = f"SELECT * FROM `course` WHERE COURSE_NO='{key['COURSE_NO']}';"
                course = query.query_dic(sq2)

                #student = Student.query.filter_by(STU_NO=key['STU_NO']).first()
                sq3 = f"SELECT * FROM `student` WHERE STU_NO='{key['STU_NO']}';"
                student1 = query.query_dic(sq3)

                sq4 = f"SELECT * FROM `college` WHERE COLLEGE_NO='{student1[0]['COLLEGE_NO']}';"
                stu_college = query.query_dic(sq4)[0]['COLLEGE_NAME']

                sq5 = f"SELECT * FROM `major` WHERE MAJOR_NO='{student1[0]['MAJOR_NO']}';"
                stu_major = query.query_dic(sq5)[0]['MAJOR_NAME']

                obj['number'] = index
                obj['course_name'] = course[0]['COURSE_NAME']
                obj['stu_no'] = key['STU_NO']
                obj['stu_name'] = student1[0]['STU_NAME']
                obj['stu_college'] = stu_college
                obj['stu_major'] = stu_major
                obj['in_year'] = student1[0]['IN_YEAR']
                obj['grade'] = key['GRADE']
                data.append(obj)
        except:
            data = []
        return jsonify(data)

# 录入成绩
@web.route('/add_score/inputGrade',methods=['POST'])
#@login_required
def inputGrade():
    user_id = function.get_id()
    if function.teacher(user_id):
        user_no = user_id
        stu_no = request.values.get('stu_no')
        course_no = request.values.get('course_no')
        grade = request.values.get('grade')

        sq1 = f"UPDATE `course_select_table` set GRADE={int(grade)} where TEACHER_NO='{user_no}' and COURSE_NO='{course_no}' and STU_NO='{stu_no}';"
        query.update(sq1)

        return jsonify({'msg':'录入成功','code':200})

# 课程设置页
@web.route('/course_setup',methods=['GET'])
#@login_required
def course_setup():
    user_id = function.get_id()
    if function.teacher(user_id):
        return render_template('course_setup.html')
    
# 获取所有教师课程信息
@web.route('/course_setup/getTeacherAllCourses',methods=['GET'])
#@login_required
def getTeacherAllCourses():
    user_id = function.get_id()
    if function.teacher(user_id):
        user_no = user_id

        #teacher = Teacher.query.filter_by(TEACHER_NO=user_no).first()

        sq1 = f"SELECT * FROM `course` WHERE TEAC_NO='{user_no}';"
        course = query.query_dic(sq1)

        data = []
        for key in course:
            # print(key)
            obj = {}
            sq2 =f"SELECT * FROM `college` WHERE COLLEGE_NO='{key['COLLEGE_NO']}';"
            college_name = query.query_dic(sq2)

            sq3 = f"SELECT * FROM `course_teacher` WHERE COURSE_NO='{key['COURSE_NO']}';"
            course_capacity = query.query_dic(sq3)

            course_capacity = course_capacity[0]['COURSE_CAPACITY']


            obj['course_no'] = key['COURSE_NO']
            obj['course_name'] = key['COURSE_NAME']
            obj['course_credit'] = key['COURSE_CREDIT']
            obj['course_hour'] = key['COURSE_HOUR']
            obj['college'] = college_name[0]['COLLEGE_NAME']
            obj['college_no'] = key['COLLEGE_NO']
            #course_capacity = Course_Teacher.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            obj['course_capacity'] = course_capacity
            data.append(obj)

        # print(data)
        return jsonify(data)

# 修改课程容量
@web.route('/course_setup/edit_course',methods=['POST'])
#@login_required
def course_setup_edit():
    user_id = function.get_id()
    if function.teacher(user_id):
        user_no = user_id
        course_no = request.values.get('courses_no')
        course_capacity = request.values.get('course_capacity')

        sq1 = f"UPDATE `course_teacher` set COURSE_CAPACITY='{course_capacity}' where TEACHER_NO='{user_no}' and COURSE_NO='{course_no}';"
        query.update(sq1)
        return redirect(url_for('web.course_setup'))

# 添加课程页
@web.route('/add_teacher_course',methods=['GET'])
#@login_required
def add_teacher_course():
    user_id = function.get_id()
    if function.teacher(user_id):
        return render_template('add_teacher_course.html')

# 添加课程
@web.route('/add_teacher_course/add_course',methods=['POST'])
#@login_required
def course_setup_add():
    user_id = function.get_id()
    if function.teacher(user_id):
        user_no = user_id
        error = None
        course_no = request.values.get('courses_no')
        course_capacity = request.values.get('course_capacity')
        course_capacity = int(course_capacity)

        #course_teacher = Course_Teacher.query.filter_by(TEACHER_NO=user_no,COURSE_NO=course_no).first()
        sq1 =f"SELECT * FROM `course_teacher` WHERE TEACHER_NO='{user_no}' and COURSE_NO='{course_no}';"
        course_teacher = query.query(sq1)

        if not course_teacher and course_teacher is None:

            sq2 = f"INSERT into course_teacher VALUES('{user_no}','{course_no}',{course_capacity});"
            query.update(sq2)
            error = u'添加' + course_no + '课程成功'
            flash(error)

            return render_template('add_teacher_course.html', error=error)
           
        else:
            error =  u'已有' + course_no + '课程'
            flash(error)
            return render_template('add_teacher_course.html', error=error)


# 删除当前课程
@web.route('/course_setup/delete_course',methods=['POST'])
#@login_required
def course_setup_delete():
    user_id = function.get_id()
    if function.teacher(user_id):
        user_no = user_id
        course_no = request.values.get('delete_course_no')
        try:
            #course_tables = Course_select_table.query.filter_by(TEACHER_NO=user_no).all()
            sq1 = f"DELETE from course_select_table where TEACHER_NO='{user_no}';"
            cou_se_ta = query.query_dic(sq1)

            sq2 = f"DELETE from course_teacher where TEACHER_NO='{user_no}' and COURSE_NO='{course_no}';"
            cou_se_ta2 = query.update(sq2)

            if cou_se_ta and cou_se_ta2 is None:
                pass
            else:
                return jsonify({'msg':'已删除课程','code':200})
            return jsonify({'msg':'删除课程成功','code':200})

        except Exception as e:
            # print(e)
            return jsonify({'msg':'删除课程失败','code':400})