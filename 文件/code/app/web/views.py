from . import web
from flask import jsonify,render_template,redirect,session,url_for ,request,flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Student,Teacher,Manager,College,Major,Course_select_table,Course
from app.forms import LoginForm
from app import login_manager
from app import db

@login_manager.user_loader
def load_user(user_id):
    print(user_id)  
    user = Student.query.get(int(user_id))
    if user:
        return user
    else:
        user =  Teacher.query.get(int(user_id))
        if user:
            return user
        else:
            return Manager.query.get(int(user_id))
   
@web.route('/',methods=('GET', 'POST'))
def index():
    return render_template('login.html')

# 首页
@web.route('/home',methods=('GET', 'POST'))
@login_required
def home():
    user_no = current_user.get_id()
    if isinstance(current_user._get_current_object(), Student):
        user = Student.query.get(user_no)
        username = user.STU_NAME + '同学'
    elif isinstance(current_user._get_current_object(), Teacher):
        user = Teacher.query.get(user_no)
        username = user.TEACHER_NAME + '老师'
    elif isinstance(current_user._get_current_object(), Manager):
        username = '管理员'
    return render_template('index.html',user=username)

# 登录
@web.route('/login',methods=('GET','POST'))
def login():
    # 用户权限管理
    # isinstance（object，type）来判断一个对象是否是一个已知的类型
    # is_authenticated() 如果用户已经登录，必须返回 True，否则返回 False
    if current_user.is_authenticated:
        if isinstance(current_user._get_current_object(), Student):
            return redirect(url_for('web.home'))
        elif isinstance(current_user._get_current_object(), Teacher):
            return redirect(url_for('web.home'))
        elif isinstance(current_user._get_current_object(), Manager):
            return redirect(url_for('web.home'))
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user_no = form.user_no.data
            password = form.password.data
            # remember = request.form.get('remember')
            # remember = [True if remember=='on' else False][0]
            # print(user_no,password,remember)
            error = None 
            role = 1

            user = Student.query.filter_by(STU_NO=user_no).first()
            # 判断是否为学生
            if not user:
                # 若不是，则选取教师
                role = 2
                user = Teacher.query.filter_by(TEACHER_NO=user_no).first()
            if not user:
                # 若不是教师,则管理员
                role = 0
                user = Manager.query.filter_by(MANAGER_NO=user_no).first()

            if not user or user is None:
                error = u'该用户不存在!'
            elif not user.check_password(password):
                error = u'密码错误!'

            if error is None:
                # 登录
                login_user(user)
                next_page = request.args.get('next')
                if not next_page:
                    next_page = url_for('web.home',user_role=role)
                if role:
                    return redirect(url_for('web.home',user_role=role))
                else:
                    return redirect(url_for('web.home',user_role=role))
            flash(error)
        else:
            return render_template('login.html',form=form)
        return render_template('login.html', error=error)
    elif request.method == 'GET':
        return render_template('login.html')

# 退出登录
@web.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'用户已经登出')
    return redirect(url_for('web.login'))

# 个人信息页
@web.route('/personal_information',methods=('GET','POST'))
@login_required
def personal_information():
    user_no =  current_user.get_id()
    
    if isinstance(current_user._get_current_object(), Student):
        result = Student.query.get(user_no) 
    elif isinstance(current_user._get_current_object(), Teacher):
        result = Teacher.query.get(user_no) 

    return render_template('personal_information.html',result=result)

# 修改个人信息页
@web.route('/revise_info',methods=['GET','POST'])
@login_required
def revise_info():
    if isinstance(current_user._get_current_object(), Student):
        return render_template('revise_info.html',role=True)
    elif isinstance(current_user._get_current_object(), Teacher):
        return render_template('revise_info.html',role=False)

# 获取学院
@web.route('/getCollege',methods=['GET','POST'])
def getCollege():
    colleges = College.query.all()
    data = []
    for key in colleges:
        obj = {}
        obj['college_no'] = key.COLLEGE_NO
        obj['college_name'] = key.COLLEGE_NAME
        data.append(obj)
    return jsonify(data)

# 获取专业
@web.route('/getMajor',methods=['GET','POST'])
def getMajor():
    majors = Major.query.all()
    data = []
    for key in majors:
        obj = {}
        obj['major_no'] = key.MAJOR_NO
        obj['major_name'] = key.MAJOR_NAME
        obj['college_no'] = key.COLLEGE_NO
        data.append(obj)
    return jsonify(data)

# 获取课程
@web.route('/getAllCourses',methods=['GET','POST'])
def getAllCourses():
    courses = Course.query.all()
    data = []
    for key in courses:
        obj = {}
        obj['course_no'] = key.COURSE_NO
        obj['course_name'] = key.COURSE_NAME
        obj['college_no'] = key.COLLEGE_NO
        obj['course_credit'] = key.COURSE_CREDIT
        obj['course_hour'] = key.COURSE_HOUR
        data.append(obj)
    return jsonify(data)

# 修改个人信息
@web.route('/revise_info/revise_detail_info',methods=['GET','POST'])
@login_required
def revise_detail_info():
    user_no =  current_user.get_id()
    name = request.form.get('name')
    sex = request.form.get('sex')
    college_no = request.form.get('college')
    in_year = request.form.get('in_year')
    if isinstance(current_user._get_current_object(), Student):
        major_no = request.form.get('major')
        user = Student.query.filter_by(STU_NO=user_no).update({'STU_NAME':name,"STU_SEX":sex,'IN_YEAR':in_year,'MAJOR_NO':major_no,'COLLEGE_NO':college_no})
    elif isinstance(current_user._get_current_object(), Teacher):
        teacher_title = request.form.get('teacher_title')
       
        user = Teacher.query.filter_by(TEACHER_NO=user_no).update({'TEACHER_NAME':name,"TEACHER_SEX":sex,'IN_YEAR':in_year,'TEACHER_TITLE':teacher_title,'COLLEGE_NO':college_no})
    
    db.session.commit()
    if int(user) == 1:
        return redirect(url_for('web.personal_information'))