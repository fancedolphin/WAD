from . import web
from app.utils import query,function
from flask import jsonify,render_template,redirect,url_for ,request,flash



# 用户管理页
@web.route('/managing_users',methods=['GET','POST'])
#@login_required
def managing_users():
    user_id = function.get_id()
    if function.manager(user_id):
        return render_template('managing_users.html')

# 获取所有学生信息
@web.route('/managing_users/getAllStudents',methods=['GET','POST'])
#@login_required
def getAllStudents():
    user_id = function.get_id()
    if function.manager(user_id):

        #students =  Student.query.all()

        sq1 = f"SELECT * FROM `student`;"
        students = query.query_dic(sq1)
        data = []
        index = 0
        for key in students:
            obj = {}
            arr = []
            index = index + 1
            sq2 =f"SELECT * FROM `college` WHERE COLLEGE_NO='{key['COLLEGE_NO']}';"
            college_data = query.query_dic(sq2)
            sq3 = f"SELECT * FROM `major` WHERE MAJOR_NO='{key['MAJOR_NO']}';"
            major_data = query.query_dic(sq3)
            sq4 = f"SELECT * FROM `course_select_table` WHERE STU_NO='{key['STU_NO']}';"
            course_select_table_data = query.query_dic(sq4)

            if course_select_table_data == None:
                arr = []
            elif len(course_select_table_data) > 1:
                for key2 in course_select_table_data:
                    sq5 = f"SELECT * FROM `course` WHERE COURSE_NO='{key2['COURSE_NO']}';"
                    course_data = query.query_dic(sq5)
                    arr.append({'course_no': course_data[0]['COURSE_NO'], 'course_name': course_data[0]['COURSE_NAME']})
            elif len(course_select_table_data) == 1:
                sq5 = f"SELECT * FROM `course` WHERE COURSE_NO='{course_select_table_data[0]['COURSE_NO']}';"
                course_data = query.query_dic(sq5)
                arr.append({'course_no': course_data[0]['COURSE_NO'], 'course_name': course_data[0]['COURSE_NAME']})
            obj['number'] = index
            obj['user_no'] = key['STU_NO']
            obj['user_name'] = key['STU_NAME']
            obj['user_sex'] = key['STU_SEX']
            obj['college'] =  college_data[0]['COLLEGE_NAME']                          #key.college.COLLEGE_NAME
            obj['major'] =  major_data[0]['MAJOR_NAME']                                      #key.major.MAJOR_NAME
            obj['in_year'] = key['IN_YEAR']
            obj['courses'] = arr
            data.append(obj)
        return jsonify(data)

# 取消学生选课
@web.route('/managing_users/cancelChoose',methods=['GET','POST'])
#@login_required
def ManagerCancelChooseCourse():
    user_id = function.get_id()
    if function.manager(user_id):
        stu_no = request.values.get('stu_no')
        course_no = request.values.get('course_no')

        try:
            arr = []
            sq1 = f"DELETE FROM `course_select_table` WHERE STU_NO='{stu_no}' and COURSE_NO='{course_no}';"
            query.update(sq1)


            sq2 = f"SELECT * FROM `course_teacher` WHERE COURSE_NO='{course_no}';"
            cour = query.query_dic(sq2)
            sq3 = f"UPDATE `course_teacher` set COURSE_CAPACITY={int(cour[0]['COURSE_CAPACITY'])+1} where COURSE_NO='{course_no}';"
            query.update(sq3)

            sq4 = f"SELECT * FROM `course_select_table` WHERE STU_NO='{stu_no}';"
            adata = query.query_dic(sq4)
            if adata == None:
                arr = []
            elif len(adata) > 1:
                for i in adata:
                    sq5 = f"SELECT * FROM `course` WHERE COURSE_NO='{i['COURSE_NO']}';"
                    sq5data = query.query_dic(sq5)
                    arr.append({'course_no': sq5data[0]['COURSE_NO'], 'course_name': sq5data[0]['COURSE_NAME']})
            elif len(adata) == 1:
                sq6 = f"SELECT * FROM `course` WHERE COURSE_NO='{adata[0]['COURSE_NO']}';"
                sq6data = query.query_dic(sq6)
                arr.append({'course_no': sq6data[0]['COURSE_NO'], 'course_name': sq6data[0]['COURSE_NAME']})

            return jsonify({'msg':stu_no + '取消选课成功','code':200,'courses':arr})
        except Exception as e:
            return  jsonify({'msg':'取消选课失败','code':400})


# 删除用户
@web.route('/managing_users/deleteUser',methods=['GET','POST'])
#@login_required
def deleteUser():
    user_id = function.get_id()
    if function.manager(user_id):
        user_no = request.values.get('user_no')
        user_type = request.values.get('user_type')
        try:
            if user_type == 'student':
                sq1 = f"DELETE from `course_select_table` where STU_NO='{user_no}';"
                query.update(sq1)
                sq2 = f"DELETE from `student` where STU_NO='{user_no}';"
                query.update(sq2)

            elif user_type == 'teacher':
                sq1 = f"DELETE from `course_select_table` where TEACHER_NO='{user_no}';"
                query.update(sq1)
                sq2 = f"DELETE from `course_teacher` where TEACHER_NO='{user_no}';"
                query.update(sq2)
                sq3 = f"DELETE from `teacher` where TEACHER_NO='{user_no}';"
                query.update(sq3)
            return jsonify({'msg':'删除成功,正在刷新列表','code':200})
        except Exception as e:
            print(e)
            return  jsonify({'msg':'删除用户失败','code':400})

# 获取所有教师信息
@web.route('/managing_users/getAllTeachers',methods=['GET'])
#@login_required
def getTeachersInfo():
    user_id = function.get_id()
    if function.manager(user_id):
        #teachers =  Teacher.query.all()
        #print(teachers)
        sq1 = f"SELECT * FROM `teacher`;"
        teachers_data = query.query_dic(sq1)

        data = []
        index = 0
        for key in teachers_data:
            obj = {}
            arr = []
            index = index + 1
            sq2 = f"SELECT * FROM `college` WHERE COLLEGE_NO='{key['COLLEGE_NO']}';"
            college_data = query.query_dic(sq2)
            sq3 = f"SELECT * FROM `course` WHERE TEAC_NO='{key['TEACHER_NO']}';"
            course_data = query.query_dic(sq3)

            if course_data == None:
                arr = []
            elif len(course_data) > 1:
                for i in course_data:
                    arr.append({'course_no': i['COURSE_NO'], 'course_name': i['COURSE_NAME']})
            elif len(course_data) == 1:
                arr.append({'course_no': course_data[0]['COURSE_NO'], 'course_name': course_data[0]['COURSE_NAME']})
            obj['number'] = index
            obj['user_no'] = key['TEACHER_NO']
            obj['user_name'] = key['TEACHER_NAME']
            obj['user_sex'] = key['TEACHER_SEX']
            obj['college'] = college_data[0]['COLLEGE_NAME']
            obj['title'] = key['TEACHER_TITLE']
            obj['in_year'] = key['IN_YEAR']
            obj['courses'] = arr
            data.append(obj)
            #print(obj)
        return jsonify(data)

# 添加用户页
@web.route('/add_user',methods=['GET','POST'])
#@login_required
def addUser():
    user_id = function.get_id()
    if function.manager(user_id):
        user_type = request.args.get('user_type')
        Text = '添加'
        action = '/manager_add_user'
        return render_template('add_edit_user.html',Text=Text,user_type=user_type,action=action)

# 修改用户信息页
@web.route('/edit_user',methods=['GET','POST'])
#@login_required
def editUser():
    user_id = function.get_id()
    if function.manager(user_id):
        user_type = request.args.get('user_type')
        Text = '修改'
        action = '/edit_current_user_info'
        return render_template('add_edit_user.html',Text=Text,user_type=user_type,action=action)

# 取消教师课程
@web.route('/managing_users/cancel_teacher_course',methods=['GET','POST'])
#@login_required
def cancelTeacherCourse():
    user_id = function.get_id()
    if function.manager(user_id):
        teacher_no = request.values.get('teacher_no')
        course_no = request.values.get('course_no')
        try:
            arr = []
            sq1 = f"DELETE from `course_select_table` where TEAC_NO='{teacher_no}';"
            query.update(sq1)

            sq2 = f"DELETE from `course_teacher` where TEAC_NO='{teacher_no}' and COURSE_NO='{course_no}';"
            query.update(sq2)

            sq3 = f"SELECT * FROM `course` WHERE TEAC_NO='{teacher_no}';"
            ourse_data = query.query_dic(sq3)
            if ourse_data == None:
                arr =[]
            elif len(ourse_data) > 1:
                for i in ourse_data:
                    arr.append({'course_no': i['COURSE_NO'], 'course_name': i['COURSE_NAME']})
            elif len(ourse_data) == 1:
                arr.append({'course_no': ourse_data[0]['COURSE_NO'], 'course_name': ourse_data[0]['COURSE_NAME']})
            return jsonify({'msg':teacher_no + '取消课程成功','code':200,'courses':arr})

        except Exception as e:
            return  jsonify({'msg':'取消课程失败','code':400})

# 获取当前用户信息
@web.route('/get_current_user_info',methods=['GET'])
def get_current_user_info():
    user_id = function.get_id()
    if function.manager(user_id):
        user_no = request.args.get('user_no')
        user_type = request.args.get('user_type')
        data = []
        if user_type == 'student':
            #student =  Student.query.filter_by(STU_NO=user_no).first()
            sq1 = f"SELECT * FROM `student` WHERE STU_NO='{user_no}';"
            student = query.query_dic(sq1)
            sq2 = f"SELECT * FROM `college` WHERE COLLEGE_NO='{student[0]['COLLEGE_NO']}';"
            college_data = query.query_dic(sq2)
            sq3 = f"SELECT * FROM `major` WHERE MAJOR_NO='{student[0]['MAJOR_NO']}';"
            major_data = query.query_dic(sq3)

            obj = {}
            obj['user_no'] = student[0]['STU_NO']
            obj['user_name'] = student[0]['STU_NAME']
            obj['user_sex'] = student[0]['STU_SEX']
            obj['college'] = college_data[0]['COLLEGE_NAME']
            obj['college_no'] = college_data[0]['COLLEGE_NO']
            obj['major'] = major_data[0]['MAJOR_NAME']
            obj['major_no'] = major_data[0]['MAJOR_NO']
            obj['in_year'] = student[0]['IN_YEAR']
            data.append(obj)
        elif user_type == 'teacher':
            #teacher = Teacher.query.filter_by(TEACHER_NO=user_no).first()
            sq5 = f"SELECT * FROM `teacher` WHERE TEACHER_NO='{user_no}';"
            teacher = query.query_dic(sq5)
            sq6 = f"SELECT * FROM `college` WHERE COLLEGE_NO='{teacher[0]['COLLEGE_NO']}';"
            college_data = query.query_dic(sq6)
            obj = {}
            obj['user_no'] = teacher[0]['TEACHER_NO']
            obj['user_name'] = teacher[0]['TEACHER_NAME']
            obj['user_sex'] = teacher[0]['TEACHER_SEX']
            obj['college'] = college_data[0]['COLLEGE_NAME']
            obj['college_no'] = college_data[0]['COLLEGE_NO']
            obj['teacher_title'] = teacher[0]['TEACHER_TITLE']
            obj['in_year'] = teacher[0]['IN_YEAR']
            data.append(obj)
        return jsonify({'data':data,'user_type':user_type,'code':200})

# 编辑用户信息
@web.route('/edit_current_user_info',methods=['POST'])
def edit_current_user_info():
    user_id = function.get_id()
    if function.manager(user_id):
        user_type = request.values.get('user_type')
        user_no = request.values.get('user_no')
        user_name = request.values.get('name')
        user_sex = request.values.get('sex')
        in_year = request.values.get('in_year')
        college_no = request.values.get('college')
        major_no = request.values.get('major')
        teacher_title = request.values.get('teacher_title')
        if user_type == 'student':
            #user = Student.query.filter_by(STU_NO=user_no).update({'STU_NAME':user_name,"STU_SEX":user_sex,'IN_YEAR':in_year,'MAJOR_NO':major_no,'COLLEGE_NO':college_no})
            sq1 = f"UPDATE `student` set STU_NAME='{user_name}',STU_SEX='{user_sex}',IN_YEAR='{in_year}',MAJOR_NO='{major_no}',COLLEGE_NO='{college_no}' where STU_NO='{user_no}';"
            query.update(sq1)
            user = 1
        else:
            #user = Teacher.query.filter_by(TEACHER_NO=user_no).update({'TEACHER_NAME':user_name,"TEACHER_SEX":user_sex,'IN_YEAR':in_year,'TEACHER_TITLE':teacher_title,'COLLEGE_NO':college_no})
            sq2 = f"UPDATE `teacher` set TEACHER_NAME='{user_name}',TEACHER_SEX='{user_sex}',IN_YEAR='{in_year}',TEACHER_TITLE='{teacher_title}',COLLEGE_NO='{college_no}' where TEACHER_NO='{user_no}';"
            #print(user_name,user_sex,in_year,teacher_title,college_no,user_no)
            query.update(sq2)
            user = 1
        #db.session.commit()
        if int(user) == 1:
            return redirect(url_for('web.managing_users'))
        
# 添加用户
@web.route('/manager_add_user',methods=['POST'])
def manager_add_user():
    user_id = function.get_id()
    if function.manager(user_id):
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
        user_password = '123'
        teacher_passord = '123456'
        #学生默认密码123，教师默认密码123456

        if len(user_no) != 8:
            error = u'用户编号需为8位'
            flash(error)
            return render_template('add_edit_user.html',user_type=user_type,head_text='学生', error=error,Text=Text,action=action)


        if user_type == 'student':
            #user = Student.query.filter_by(STU_NO=user_no).first()
            sq1 = f"SELECT * FROM `student` WHERE STU_NO='{user_no}';"
            user = query.query_dic(sq1)
            if user is not None:
                error = u'该用户已存在！'
                flash(error)
                return render_template('add_edit_user.html',user_type=user_type,head_text='学生', error=error,Text=Text,action=action)
            else:
                sq2 = f"INSERT into student(STU_NO,STU_NAME,STU_SEX,IN_YEAR,STU_PASSWORD,MAJOR_NO,COLLEGE_NO) VALUES('{user_no}','{user_name}','{user_sex}','{in_year}','{user_password}','{major_no}','{college_no}');"
                query.update(sq2)
                user = 1
        else:
            #user = Teacher.query.filter_by(TEACHER_NO=user_no).first()
            sq3 = f"SELECT * FROM `teacher` WHERE TEACHER_NO='{user_no}';"
            user = query.query_dic(sq3)
            if user is not None:
                error = u'该用户已存在！'
                flash(error)
                return render_template('add_edit_user.html',user_type=user_type, head_text='教师',error=error,Text=Text,action=action)
            else:
                #user = Teacher(TEACHER_NO=user_no,TEACHER_NAME=user_name,TEACHER_SEX=user_sex,IN_YEAR=in_year,TEACHER_TITLE=teacher_title)
                #user.COLLEGE_NO = college_no

                sq4 = f"INSERT into teacher(TEACHER_NO,TEACHER_NAME,TEACHER_SEX,IN_YEAR,TEACHER_PASSWORD,TEACHER_TITLE,COLLEGE_NO) VALUES('{user_no}','{user_name}','{user_sex}','{in_year}','{teacher_passord}','{teacher_title}','{college_no}');"
                query.update(sq4)
                user = 1
        if user == 1:
            return redirect(url_for('web.managing_users'))

# 修改密码页    
@web.route('/edit_password',methods=['GET'])
def edit_password():
    user_id = function.get_id()
    if function.manager(user_id):     #isinstance(current_user._get_current_object(), Manager)
        return render_template('edit_password.html')
    
# 修改密码
@web.route('/set_user_password',methods=['POST'])
def set_user_password():
    user_id = function.get_id()
    if function.manager(user_id):
        user_type = request.values.get('user_type')
        user_no = request.values.get('user_no')
        password = request.values.get('password')
        new_password = str(password)
        error = None
        try:
            if user_type == 'student':
                sq1 = f"UPDATE `student` set STU_PASSWORD='{new_password}' where STU_NO='{user_no}';"
                query.update(sq1)
            else:
                sq2 = f"UPDATE `teacher` set TEACHER_PASSWORD='{new_password}' where TEACHER_NO='{user_no}';"
                query.update(sq2)

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
    user_id = function.get_id()
    if function.manager(user_id):
       return render_template('managing_college.html',type=0)

# 专业管理页
@web.route('/managing_major',methods=['GET'])
def managing_major():
    user_id = function.get_id()
    if function.manager(user_id):
       return render_template('managing_major.html',type=1)
    
# 课程管理页
@web.route('/managing_course',methods=['GET'])
def managing_course():
    user_id = function.get_id()
    if function.manager(user_id):
       return render_template('managing_course.html',type=2)

# 修改学院、专业、课程信息
@web.route('/manage_edit',methods=['POST'])
def manage_edit():
    user_id = function.get_id()
    if function.manager(user_id):
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
            #manage =College.query.filter_by(COLLEGE_NO=college_no).update({'COLLEGE_NO':college_no,"COLLEGE_NAME":college_name})
            sq1 = f"UPDATE `college` set COLLEGE_NO='{college_no}',COLLEGE_NAME='{college_name}' where COLLEGE_NO='{college_no}';"
            manage = query.update(sq1)
        elif type_ == '1':
            url = 'managing_major.html'
            #manage = Major.query.filter_by(MAJOR_NO=major_no).update({'MAJOR_NO':major_no,'MAJOR_NAME':major_name})
            sq2 = f"UPDATE `major` set MAJOR_NO='{major_no}',MAJOR_NAME='{major_name}' where MAJOR_NO='{major_no}';"
            manage = query.update(sq2)
        elif type_ == '2':
            url = 'managing_course.html'
            #manage = Course.query.filter_by(COURSE_NO=course_no).update({'COURSE_NO':course_no,'COURSE_NAME':course_name,'COURSE_CREDIT':course_credit})
            sq3 = f"UPDATE `course` set COURSE_NO='{course_no}',COURSE_NAME='{course_name}',COURSE_CREDIT='{course_credit}' where COURSE_NO='{course_no}';"
            manage = query.update(sq3)
        if not manage:
            msg = u'修改成功'
            flash(msg)
            return render_template(url,error=msg,type=type_)
        elif manage:
            msg = u'修改失败'
            flash(msg)
            return render_template(url,error=msg,type=type_)
            
# 添加学院、专业、课程信息
@web.route('/manage_add',methods=['POST'])
def manage_add():
    user_id = function.get_id()
    if function.manager(user_id):
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
            #manage = College.query.filter_by(COLLEGE_NO=college_no).first()
            sq1 = f"SELECT * FROM `college` WHERE COLLEGE_NO='{college_no}';"
            manage = query.query_dic(sq1)
            if manage is not None:
                msg = u'学院已存在！'
                return jsonify({'msg':msg,'code':200})
            else:
                #manage = College(COLLEGE_NO=college_no,COLLEGE_NAME=college_name)
                sq2 = f"INSERT into `college` VALUES('{college_no}','{college_name}');"
                manage = query.update(sq2)
                #print(manage)

        elif type == '1':
            sq1 = f"SELECT * FROM `major` WHERE MAJOR_NO='{major_no}';"
            manage = query.query_dic(sq1)
            if manage is not None:
                msg = u'专业已存在！'
                return jsonify({'msg':msg,'code':200})
            else:
                sq2 = f"INSERT into `major` VALUES('{major_no}','{major_name}','{college_no}');"
                manage = query.update(sq2)

        elif type == '2':
            #manage = Course.query.filter_by(COURSE_NO=course_no).first()
            sq1 = f"SELECT * FROM `course` WHERE COURSE_NO='{course_no}';"
            manage = query.query_dic(sq1)
            if manage is not None:
                msg = u'课程已存在！'
                return jsonify({'msg':msg,'code':200})
            else:
                sq2 = f"INSERT into `course`(COURSE_NO,COURSE_NAME,COURSE_CREDIT,COURSE_HOUR,COLLEGE_NO) VALUES('{course_no}','{course_name}',{course_credit},{course_hour},'{college_no}');"
                manage = query.update(sq2)
        if manage is  None:
            msg = u'添加成功！'
            return jsonify({'msg':msg,'code':200})
        
# 删除学院、专业、课程
@web.route('/manage_delete',methods=['POST'])
def manage_delete():
    user_id = function.get_id()
    if function.manager(user_id):
        type = request.values.get('type')
        college_no = request.values.get('college_no')
        major_no = request.values.get('major_no')
        course_no = request.values.get('course_no')

        if type == '0':
            #manage = College.query.filter_by(COLLEGE_NO=college_no).first()
            sq1 = f"SELECT * FROM `student` WHERE COLLEGE_NO='{college_no}';"
            sq2 = f"SELECT * FROM `teacher` WHERE COLLEGE_NO='{college_no}';"
            stdata = query.query_dic(sq1)
            teadata = query.query_dic(sq2)
            if stdata and teadata is None:
                msg = u'删除失败，该学院下有教师或学生信息,正在刷新数据！'
                return jsonify({'msg': msg, 'code': 200})
            else:
                sq3 = f"DELETE from `college` where COLLEGE_NO='{college_no}';"
                manage = query.update(sq3)

        elif type == '1':
            sq1 = f"SELECT * FROM `student` WHERE MAJOR_NO='{major_no}';"
            manage = query.query_dic(sq1)
            if manage:
                msg = u'删除失败，该专业下有教师或学生信息,正在刷新数据！'
                return jsonify({'msg': msg, 'code': 200})
            else:
                sq2 = f"DELETE from `major` where MAJOR_NO='{major_no}';"
                manage = query.update(sq2)

        elif type == '2':
            #manage = Course.query.filter_by(COURSE_NO=course_no).first()
            sq1 = f"SELECT * FROM `course` WHERE COURSE_NO='{course_no}';"
            data = query.query_dic(sq1)
            manage = data[0]['TEAC_NO']
            if manage:
                msg = u'删除失败，该课程下有教师或学生信息,正在刷新数据！'
                return jsonify({'msg': msg, 'code': 200})
            else:
                sq2 = f"DELETE from `course` where COURSE_NO='{course_no}';"
                manage = query.update(sq2)

        if manage is  None:
            msg = u'删除成功,正在刷新数据'
            return jsonify({'msg':msg,'code':200})