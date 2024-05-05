from . import web
from flask import jsonify,render_template,redirect,url_for ,request,flash
from app.utils import query,function


@web.route('/',methods=('GET', 'POST'))
def index():
    return render_template('login.html')

# 首页
@web.route('/home',methods=('GET', 'POST'))
#@login_required
def home():
    user_no = function.get_id()
    if function.student(user_no):   #isinstance(current_user._get_current_object(), Student)
        username = function.student(user_no)[0][1] + 'Student'
    elif function.teacher(user_no):   #elif:True     isinstance(current_user._get_current_object(), Teacher)
        username = function.teacher(user_no)[0][1] + 'Teacher'
    elif function.manager(user_no):     #isinstance(current_user._get_current_object(), Manager)
        username = 'Admin'
    return render_template('index.html',user=username)


# 登录
@web.route('/login',methods=('GET','POST'))
def login():
    # 用户权限管理
    # isinstance（object，type）来判断一个对象是否是一个已知的类型
    # is_authenticated() 如果用户已经登录，必须返回 True，否则返回 False
    if request.method == 'POST':
        user_no = request.form['user_no']
        password = request.form['password']
        error = None

        user1 = function.student(user_no)
        user2 = function.teacher(user_no)
        user3 = function.manager(user_no)

        if user1:
            role = 1
            if not function.stuhash(user_no,password):
                error = u'学生账号密码错误!'
        elif user2:
            if not function.teahash(user_no,password):
                error = u'教师账号密码错误!'
            role = 2
        elif user3:
            if not function.manhash(user_no,password):
                error = u'管理员账号密码错误!'
            role = 0
        elif not user1 or user2 is None:
            error = u'该用户不存在!'


        if error is None:
            # 登录
            #login_user(user)
            next_page = request.args.get('next')
            if not next_page:
                #写入用户id
                with open('id.txt',"w+",encoding='utf-8') as f:
                    text = user_no
                    f.write(text)
                f.close()
                '''#读取用户id
                with open('id.txt',"r") as f:
                    data = f.read()'''

                next_page = url_for('web.home',user_role=role)      #跳转教师
            if role:
                return redirect(url_for('web.home',user_role=role))    #跳转学生
            else:
                return redirect(url_for('web.home',user_role=role))    #跳转管理员
        flash(error)

        return render_template('login.html', error=error)
    elif request.method == 'GET':
        return render_template('login.html')

# 退出登录
@web.route('/logout')
#@login_required
def logout():
    #logout_user()
    flash(u'already log out')
    return redirect(url_for('web.login'))


# 个人信息页
@web.route('/personal_information',methods=('GET','POST'))
#@login_required
def personal_information():
    #user_no =  current_user.get_id()
    user_no = function.get_id()

    if function.student(user_no):    #isinstance(current_user._get_current_object(), Student)
        result = function.student_data(user_no)
    elif function.teacher(user_no):   #isinstance(current_user._get_current_object(), Teacher)
        #result = Teacher.query.get(user_no)
        result = function.teacher_data(user_no)
    return render_template('personal_information.html',result=result)

# 修改个人信息页
@web.route('/revise_info',methods=['GET','POST'])
#@login_required
def revise_info():
    user_no = function.get_id()
    if function.student(user_no):   #isinstance(current_user._get_current_object(), Student)
        return render_template('revise_info.html',role=True)
    elif function.teacher(user_no):
        return render_template('revise_info.html',role=False)

# 获取学院
@web.route('/getCollege',methods=['GET','POST'])
def getCollege():
    #colleges = College.query.all()
    sq1 = f"SELECT * FROM `college`;"
    colleges = query.query_dic(sq1)
    data = []
    for key in colleges:
        obj = {}
        obj['college_no'] = key['COLLEGE_NO']
        obj['college_name'] = key['COLLEGE_NAME']
        data.append(obj)
    return jsonify(data)

# 获取专业
@web.route('/getMajor',methods=['GET','POST'])
def getMajor():
    #majors = Major.query.all()
    sq1 = f"SELECT * FROM `major`;"
    majors = query.query_dic(sq1)
    data = []
    for key in majors:
        obj = {}
        obj['major_no'] = key['MAJOR_NO']
        obj['major_name'] = key['MAJOR_NAME']
        obj['college_no'] = key['COLLEGE_NO']
        data.append(obj)
    return jsonify(data)

# 获取课程
@web.route('/getAllCourses',methods=['GET','POST'])
def getAllCourses():
    #courses = Course.query.all()
    sq1 = f"SELECT * FROM `course`;"
    courses = query.query_dic(sq1)
    data = []
    for key in courses:
        obj = {}
        obj['course_no'] = key['COURSE_NO']
        obj['course_name'] = key['COURSE_NAME']
        obj['college_no'] = key['COLLEGE_NO']
        obj['course_credit'] = key['COURSE_CREDIT']
        obj['course_hour'] = key['COURSE_HOUR']
        data.append(obj)
    #print(data)
    return jsonify(data)

# 修改个人信息
@web.route('/revise_info/revise_detail_info',methods=['GET','POST'])
#@login_required
def revise_detail_info():
    #user_no =  current_user.get_id()
    user_no = function.get_id()
    name = request.form.get('name')
    sex = request.form.get('sex')
    college_no = request.form.get('college')
    in_year = request.form.get('in_year')
    #print(name,sex,college_no,in_year)

    if function.student(user_no):   #isinstance(current_user._get_current_object(), Student)
        major_no = request.form.get('major')
        sql = f"UPDATE student SET STU_NAME='{name}',STU_SEX='{sex}',IN_YEAR='{in_year}',MAJOR_NO='{str(major_no)}',COLLEGE_NO='{str(college_no)}' WHERE STU_NO='{str(user_no)}'; "
        query.update(sql)
        #user = Student.query.filter_by(STU_NO=user_no).update({'STU_NAME':name,"STU_SEX":sex,'IN_YEAR':in_year,'MAJOR_NO':major_no,'COLLEGE_NO':college_no})
    elif function.teacher(user_no):   #isinstance(current_user._get_current_object(), Teacher)
        teacher_title = request.form.get('teacher_title')
        #print(name,sex,in_year,teacher_title,college_no,user_no)
        sqltes = f"UPDATE teacher SET TEACHER_NAME='{name}',TEACHER_SEX='{sex}',IN_YEAR='{str(in_year)}',TEACHER_TITLE='{teacher_title}',COLLEGE_NO='{str(college_no)}' WHERE TEACHER_NO='{str(user_no)}'; "
        query.update(sqltes)

    return redirect(url_for('web.personal_information'))





