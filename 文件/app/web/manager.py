from . import web
from flask import jsonify,render_template,redirect,session,url_for ,request,flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Student,Teacher,Manager,College,Major,Course_select_table,Course,Course_Teacher
from app import db
from app.utils import query 

# 用户管理页
@web.route('/managing_users',methods=['GET','POST'])
@login_required
def managing_users():
    if isinstance(current_user._get_current_object(), Manager):
        return render_template('managing_users.html')

# 获取所有学生信息
@web.route('/managing_users/getAllStudents',methods=['GET','POST'])
@login_required
def getAllStudents():
    if isinstance(current_user._get_current_object(), Manager):
        students =  Student.query.all()
        data = []
        index = 0
        for key in students:
            obj = {}
            arr = []
            index = index + 1
            for course in key.COURSES:
                arr.append({'course_no':course.COURSE_NO,'course_name':course.COURSE_NAME})
            obj['number'] = index
            obj['user_no'] = key.STU_NO
            obj['user_name'] = key.STU_NAME
            obj['user_sex'] = key.STU_SEX
            obj['college'] = key.college.COLLEGE_NAME
            obj['major'] = key.major.MAJOR_NAME
            obj['in_year'] = key.IN_YEAR
            obj['courses'] = arr
            data.append(obj)
        return jsonify(data)

# 取消学生选课
@web.route('/managing_users/cancelChoose',methods=['GET','POST'])
@login_required
def ManagerCancelChooseCourse():
    if isinstance(current_user._get_current_object(), Manager):
        stu_no = request.values.get('stu_no')
        course_no = request.values.get('course_no')
        
        try:
            arr = []
            res = Student.query.filter_by(STU_NO=stu_no).first()
            res.drop_course(course_no)
            choose_course = Course_Teacher.query.filter_by(COURSE_NO=course_no).first()
            choose_course.COURSE_CAPACITY = int(choose_course.COURSE_CAPACITY) + 1
            db.session.commit()
            student = Student.query.filter_by(STU_NO=stu_no).first()
            for course in student.COURSES:
                arr.append({'course_no':course.COURSE_NO,'course_name':course.COURSE_NAME})
            return jsonify({'msg':stu_no + '取消选课成功','code':200,'courses':arr})
        except Exception as e:
            return  jsonify({'msg':'取消选课失败','code':400})
        
# 删除用户
@web.route('/managing_users/deleteUser',methods=['GET','POST'])
@login_required
def deleteUser():
    if isinstance(current_user._get_current_object(), Manager):
        user_no = request.values.get('user_no')
        user_type = request.values.get('user_type')
        try:
            if user_type == 'student':
                delete_stu = Student.query.filter_by(STU_NO=user_no).first()
                course_tables = Course_select_table.query.filter_by(STU_NO=user_no).all()
                for course in course_tables:
                    db.session.delete(course)
                db.session.commit()
                db.session.delete(delete_stu)
                db.session.commit()
            elif user_type == 'teacher':
                delete_teacher = Teacher.query.filter_by(TEACHER_NO=user_no).first()
                course_teacher = Course_Teacher.query.filter_by(TEACHER_NO=user_no).all()
                for course in course_teacher:
                    db.session.delete(course)
                db.session.commit()
                course_tables = Course_select_table.query.filter_by(TEACHER_NO=user_no).all()
                for course in course_tables:
                    db.session.delete(course)
                db.session.commit()
                db.session.delete(delete_teacher)
                db.session.commit()
            return jsonify({'msg':'删除成功,正在刷新列表','code':200})
        except Exception as e:
            print(e)
            return  jsonify({'msg':'删除用户失败','code':400})

# 获取所有教师信息
@web.route('/managing_users/getAllTeachers',methods=['GET'])
@login_required
def getTeachersInfo():
    if isinstance(current_user._get_current_object(), Manager):
        teachers =  Teacher.query.all()
        data = []
        index = 0
        for key in teachers:
            obj = {}
            arr = []
            index = index + 1
            for course in key.COURSES:
                arr.append({'course_no':course.COURSE_NO,'course_name':course.COURSE_NAME})
            obj['number'] = index
            obj['user_no'] = key.TEACHER_NO
            obj['user_name'] = key.TEACHER_NAME
            obj['user_sex'] = key.TEACHER_SEX
            obj['college'] = key.college.COLLEGE_NAME
            obj['title'] = key.TEACHER_TITLE
            obj['in_year'] = key.IN_YEAR
            obj['courses'] = arr
            data.append(obj)
        return jsonify(data)

# 添加用户页
@web.route('/add_user',methods=['GET','POST'])
@login_required
def addUser():
    if isinstance(current_user._get_current_object(), Manager):
        user_type = request.args.get('user_type')
        Text = '添加'
        action = '/manager_add_user'
        return render_template('add_edit_user.html',Text=Text,user_type=user_type,action=action)

# 修改用户信息页
@web.route('/edit_user',methods=['GET','POST'])
@login_required
def editUser():
    if isinstance(current_user._get_current_object(), Manager):
        user_type = request.args.get('user_type')
        Text = '修改'
        action = '/edit_current_user_info'
        return render_template('add_edit_user.html',Text=Text,user_type=user_type,action=action)

# 取消教师课程
@web.route('/managing_users/cancel_teacher_course',methods=['GET','POST'])
@login_required
def cancelTeacherCourse():
    if isinstance(current_user._get_current_object(), Manager):
        teacher_no = request.values.get('teacher_no')
        course_no = request.values.get('course_no')
        try:
            arr = []
            course_tables = Course_select_table.query.filter_by(TEACHER_NO=teacher_no).all()
            for course in course_tables:
                db.session.delete(course)
            db.session.commit()
            course_teacher =  Course_Teacher.query.filter_by(TEACHER_NO=teacher_no,COURSE_NO=course_no).all()
            for course in course_teacher:
                db.session.delete(course)
            db.session.commit()
            teacher = Teacher.query.filter_by(TEACHER_NO=teacher_no).first()
            if not teacher.COURSES:
                for course in teacher.COURSES:
                    db.session.delete(course)
                    db.session.commit()
            for course in teacher.COURSES:
                arr.append({'course_no':course.COURSE_NO,'course_name':course.COURSE_NAME})
            return jsonify({'msg':teacher_no + '取消课程成功','code':200,'courses':arr})
        except Exception as e:
            return  jsonify({'msg':'取消课程失败','code':400})

# 获取当前用户信息
@web.route('/get_current_user_info',methods=['GET'])
def get_current_user_info():
    if isinstance(current_user._get_current_object(), Manager):
        user_no = request.args.get('user_no')
        user_type = request.args.get('user_type')
        data = []
        if user_type == 'student':
            student =  Student.query.filter_by(STU_NO=user_no).first()
            obj = {}
            obj['user_no'] = student.STU_NO
            obj['user_name'] = student.STU_NAME
            obj['user_sex'] = student.STU_SEX
            obj['college'] = student.college.COLLEGE_NAME
            obj['college_no'] = student.college.COLLEGE_NO
            obj['major'] = student.major.MAJOR_NAME
            obj['major_no'] = student.major.MAJOR_NO
            obj['in_year'] = student.IN_YEAR
            data.append(obj)
        elif user_type == 'teacher':
            teacher = Teacher.query.filter_by(TEACHER_NO=user_no).first()
            obj = {}
            obj['user_no'] = teacher.TEACHER_NO
            obj['user_name'] = teacher.TEACHER_NAME
            obj['user_sex'] = teacher.TEACHER_SEX
            obj['college'] = teacher.college.COLLEGE_NAME
            obj['college_no'] = teacher.college.COLLEGE_NO
            obj['teacher_title'] = teacher.TEACHER_TITLE
            obj['in_year'] = teacher.IN_YEAR
            data.append(obj)
        return jsonify({'data':data,'user_type':user_type,'code':200})

# 编辑用户信息
@web.route('/edit_current_user_info',methods=['POST'])
def edit_current_user_info():
    if isinstance(current_user._get_current_object(), Manager):
        user_type = request.values.get('user_type')
        user_no = request.values.get('user_no')
        user_name = request.values.get('name')
        user_sex = request.values.get('sex')
        in_year = request.values.get('in_year')
        college_no = request.values.get('college')
        major_no = request.values.get('major')
        teacher_title = request.values.get('teacher_title')
        if user_type == 'student':
            user = Student.query.filter_by(STU_NO=user_no).update({'STU_NAME':user_name,"STU_SEX":user_sex,'IN_YEAR':in_year,'MAJOR_NO':major_no,'COLLEGE_NO':college_no})
        else:
            user = Teacher.query.filter_by(TEACHER_NO=user_no).update({'TEACHER_NAME':user_name,"TEACHER_SEX":user_sex,'IN_YEAR':in_year,'TEACHER_TITLE':teacher_title,'COLLEGE_NO':college_no})
        db.session.commit()
        if int(user) == 1:
            return redirect(url_for('web.managing_users'))
        
# 添加用户
@web.route('/manager_add_user',methods=['POST'])
def manager_add_user():
    if isinstance(current_user._get_current_object(), Manager):
        error = None
        Text = '添加'
        action = '/manager_add_user'
        user_type = request.values.get('user_type')
        user_no = request.values.get('user_no')
        user_name = request.values.get('name')
        user_sex = request.values.get('sex')
        in_year = request.values.get('in_year')
        college_no = request.values.get('college')
        major_no = request.values.get('major')
        teacher_title = request.values.get('teacher_title')
        if len(user_no) != 8:
            error = u'用户编号需为8位'
            flash(error)
            return render_template('add_edit_user.html',user_type=user_type,head_text='学生', error=error,Text=Text,action=action)
        if user_type == 'student':
            user = Student.query.filter_by(STU_NO=user_no).first()
            if user is not None:
                error = u'该用户已存在！'
                flash(error)
                return render_template('add_edit_user.html',user_type=user_type,head_text='学生', error=error,Text=Text,action=action)
            else:
                user = Student(STU_NO=user_no,STU_NAME=user_name,STU_SEX=user_sex,IN_YEAR=in_year,MAJOR_NO=major_no)
                user.COLLEGE_NO = college_no
        else:
            user = Teacher.query.filter_by(TEACHER_NO=user_no).first()
            if user is not None:
                error = u'该用户已存在！'
                flash(error)
                return render_template('add_edit_user.html',user_type=user_type, head_text='教师',error=error,Text=Text,action=action)
            else:
                user = Teacher(TEACHER_NO=user_no,TEACHER_NAME=user_name,TEACHER_SEX=user_sex,IN_YEAR=in_year,TEACHER_TITLE=teacher_title)
                user.COLLEGE_NO = college_no
        db.session.add(user)
        db.session.commit()
        # print(user)
        if user is not None:
            return redirect(url_for('web.managing_users'))

# 修改密码页    
@web.route('/edit_password',methods=['GET'])
def edit_password():
    if isinstance(current_user._get_current_object(), Manager):
        return render_template('edit_password.html')
    
# 修改密码
@web.route('/set_user_password',methods=['POST'])
def set_user_password():
    if isinstance(current_user._get_current_object(), Manager):
        user_type = request.values.get('user_type')
        user_no = request.values.get('user_no')
        password = request.values.get('password')
        error = None
        try:
            if user_type == 'student':
                student = Student.query.filter_by(STU_NO=user_no).first()
                student.set_password(password)
            else:
                teacher = Teacher.query.filter_by(TEACHER_NO=user_no).first()
                teacher.set_password(password)
            db.session.commit()
            error = u'修改密码成功'
            flash(error)
            return render_template('edit_password.html',error=error)
        except Exception as e:
            error = u'修改密码失败'
            flash(error)
            return render_template('edit_password.html',error=error)

# 学院管理页
@web.route('/managing_college',methods=['GET'])
def managing_college():
    if isinstance(current_user._get_current_object(), Manager):
       return render_template('managing_college.html',type=0)

# 专业管理页
@web.route('/managing_major',methods=['GET'])
def managing_major():
    if isinstance(current_user._get_current_object(), Manager):
       return render_template('managing_major.html',type=1)
    
# 课程管理页
@web.route('/managing_course',methods=['GET'])
def managing_course():
    if isinstance(current_user._get_current_object(), Manager):
       return render_template('managing_course.html',type=2)

# 修改学院、专业、课程信息
@web.route('/manage_edit',methods=['POST'])
def manage_edit():
    if isinstance(current_user._get_current_object(), Manager):
        type_ = request.values.get('type')
        college_no = request.values.get('college_no')
        college_name = request.values.get('college_name')
        major_no = request.values.get('major_no')
        major_name = request.values.get('major_name')
        course_no = request.values.get('course_no')
        course_name = request.values.get('course_name')
        course_credit = request.values.get('course_credit')
        course_hour = request.values.get('course_hour')
        url = ''
        msg = ''
        manage = None
        if type_ == '0':
            url = 'managing_college.html'
            manage =College.query.filter_by(COLLEGE_NO=college_no).update({'COLLEGE_NO':college_no,"COLLEGE_NAME":college_name})
        elif type_ == '1':
            url = 'managing_major.html'
            manage = Major.query.filter_by(MAJOR_NO=major_no).update({'MAJOR_NO':major_no,'MAJOR_NAME':major_name})
        elif type_ == '2':
            url = 'managing_course.html'
            manage = Course.query.filter_by(COURSE_NO=course_no).update({'COURSE_NO':course_no,'COURSE_NAME':course_name,'COURSE_CREDIT':course_credit})
        db.session.commit()
        if int(manage) == 1:
            msg = u'修改成功'
            flash(msg)
            return render_template(url,error=msg,type=type_)
        else:
            msg = u'修改失败'
            flash(msg)
            return render_template(url,error=msg,type=type_)
            
# 添加学院、专业、课程信息
@web.route('/manage_add',methods=['POST'])
def manage_add():
    if isinstance(current_user._get_current_object(), Manager):
        type = request.values.get('type')
        college_no = request.values.get('college_no')
        college_name = request.values.get('college_name')
        major_no = request.values.get('major_no')
        major_name = request.values.get('major_name')
        course_no = request.values.get('course_no')
        course_name = request.values.get('course_name')
        course_credit = request.values.get('course_credit')
        course_hour = request.values.get('course_hour')

        if type == '0':
            manage = College.query.filter_by(COLLEGE_NO=college_no).first()
            if manage is not None:
                msg = u'学院已存在！'
                return jsonify({'msg':msg,'code':200})
            else:
                manage = College(COLLEGE_NO=college_no,COLLEGE_NAME=college_name)      
        elif type == '1':
            manage = Major.query.filter_by(MAJOR_NO=major_no).first()
            if manage is not None:
                msg = u'专业已存在！'
                return jsonify({'msg':msg,'code':200})
            else:
                manage = Major(MAJOR_NO=major_no,MAJOR_NAME=major_name)
                manage.COLLEGE_NO = college_no
        elif type == '2':
            manage = Course.query.filter_by(COURSE_NO=course_no).first()
            if manage is not None:
                msg = u'课程已存在！'
                return jsonify({'msg':msg,'code':200})
            else:
                manage = Course(COURSE_NO=course_no,COURSE_NAME=course_name,COURSE_CREDIT=course_credit,COURSE_HOUR=course_hour)
                manage.COLLEGE_NO = college_no
        db.session.add(manage)
        db.session.commit()
        if manage is not None:
            msg = u'添加成功！'
            return jsonify({'msg':msg,'code':200})
        
# 删除学院、专业、课程
@web.route('/manage_delete',methods=['POST'])
def manage_delete():
    if isinstance(current_user._get_current_object(), Manager):
        type = request.values.get('type')
        college_no = request.values.get('college_no')
        major_no = request.values.get('major_no')
        course_no = request.values.get('course_no')

        if type == '0':
            manage = College.query.filter_by(COLLEGE_NO=college_no).first()
            print(manage.TEACHERS)
            if len(manage.TEACHERS) != 0:
                msg = u'删除失败，该学院下有教师或学生信息,正在刷新数据！'
                return jsonify({'msg':msg,'code':200})
        elif type == '1':
            manage = Major.query.filter_by(MAJOR_NO=major_no).first()
            if len(manage.STUDENTS) != 0:
                msg = u'删除失败，该专业下有教师或学生信息,正在刷新数据！'
                return jsonify({'msg':msg,'code':200})
        elif type == '2':
            manage = Course.query.filter_by(COURSE_NO=course_no).first()
            if  len(manage.TEACHERS) != 0:
                msg = u'删除失败，该课程下有教师或学生信息,正在刷新数据！'
                return jsonify({'msg':msg,'code':200})
        db.session.delete(manage)
        db.session.commit()
        if manage is not None:
            msg = u'删除成功,正在刷新数据'
            return jsonify({'msg':msg,'code':200})