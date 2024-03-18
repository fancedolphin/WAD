from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login_manager


# 管理员
class Manager(UserMixin,db.Model):
    MANAGER_NO = db.Column(db.String(8),primary_key=True)
    MANAGER_NAME = db.Column(db.String(10),nullable=False)
    MANAGER_PASSWORD = db.Column(db.Text, nullable=False)
   

    def get_id(self):
        return self.MANAGER_NO
    
    def set_password(self, password):
        self.MANAGER_PASSWORD = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.MANAGER_PASSWORD,password)

# 学院表
class College(db.Model):
    COLLEGE_NO = db.Column(db.String(4),primary_key=True)
    COLLEGE_NAME = db.Column(db.String(10),nullable=False)
    TEACHERS = db.relationship('Teacher',backref='college',lazy='subquery') # 学院：教师 = 1:n
    STUDENTS = db.relationship('Student',backref='college',lazy='subquery') # 学院：学生 = 1:n
    MAJORS = db.relationship('Major',backref='college',lazy='subquery') # 学院：专业 = 1:n
    COURSES = db.relationship('Course',backref='college',lazy='subquery') # 学院：课程 = 1:n

# 专业表
class Major(db.Model):
    MAJOR_NO = db.Column(db.String(6),primary_key=True) 
    MAJOR_NAME = db.Column(db.String(10),nullable=False)
    COLLEGE_NO = db.Column(db.String(4),db.ForeignKey('college.COLLEGE_NO'),nullable=False) # 添加外键
    STUDENTS = db.relationship('Student',backref='major',lazy='subquery') # 专业：学生 = 1:n

# 教师-学生-课程 m:n
class Course_select_table(db.Model):
    __tablename__ = 'course_select_table' # 设置表名, 表名默认为类名小写
    STU_NO = db.Column(db.String(8),db.ForeignKey('student.STU_NO'),primary_key=True,nullable=False)
    TEACHER_NO = db.Column(db.String(8),db.ForeignKey('teacher.TEACHER_NO'),primary_key=True,nullable=False)
    COURSE_NO = db.Column(db.String(8),db.ForeignKey('course.COURSE_NO'),primary_key=True,nullable=False)
    GRADE = db.Column(db.Integer)

    def __init__(self,STU_NO,TEACHER_NO,COURSE_NO):
        self.STU_NO = STU_NO
        self.TEACHER_NO = TEACHER_NO
        self.COURSE_NO = COURSE_NO
        
    # 录入成绩
    def input_grade(self,grade):
        self.GRADE = grade

# 课程-教师 m:n
class Course_Teacher(db.Model):
    __tablename__ = "course_teacher"
    TEACHER_NO = db.Column(db.String(8),db.ForeignKey('teacher.TEACHER_NO'),primary_key=True,nullable=False)
    COURSE_NO = db.Column(db.String(8),db.ForeignKey('course.COURSE_NO'),primary_key=True,nullable=False)
    COURSE_CAPACITY = db.Column(db.Integer,nullable=False)

    def __init__(self,TEACHER_NO,COURSE_NO,COURSE_CAPACITY):
        self.COURSE_NO = COURSE_NO
        self.TEACHER_NO = TEACHER_NO
        self.COURSE_CAPACITY = COURSE_CAPACITY

# 课程表
class Course(db.Model):
    COURSE_NO = db.Column(db.String(8), primary_key=True)
    COURSE_NAME = db.Column(db.String(10), nullable=False)
    COURSE_CREDIT = db.Column(db.Integer, nullable=False)
    COURSE_HOUR = db.Column(db.Integer, nullable=False)
    TEACHERS = db.relationship('Teacher', secondary='course_teacher', backref='course', lazy='subquery') # 教师：课程 = m:n
    COLLEGE_NO = db.Column(db.String(4), db.ForeignKey('college.COLLEGE_NO'), nullable=False)

    # def __init__(self,COURSE_NO,COURSE_NAME,COURSE_CREDIT,COURSE_HOUR):
    #     self.COLLEGE_NO = COLLEGE_NO
    #     self.COURSE_NAME = COLLEGE_NO
    #     self.COURSE_CREDIT = COURSE_CREDIT
    #     self.COURSE_HOUR = COURSE_HOUR

# 学生表
class Student(UserMixin,db.Model):
    STU_NO = db.Column(db.String(8),primary_key=True)
    STU_NAME = db.Column(db.String(10),nullable=False)
    STU_SEX = db.Column(db.String(10),nullable=False)
    IN_YEAR = db.Column(db.String(4),nullable=False)
    STU_PASSWORD = db.Column(db.Text, nullable=False)
    COLLEGE_NO = db.Column(db.String(4), db.ForeignKey('college.COLLEGE_NO'), nullable=False)
    COURSES = db.relationship('Course', secondary='course_select_table', backref='student', lazy='subquery') # 学生：课程 = m:n
    MAJOR_NO = db.Column(db.String(16), db.ForeignKey('major.MAJOR_NO'), nullable=False)

    def __init__(self,STU_NO,STU_NAME,STU_SEX,IN_YEAR,MAJOR_NO):
        self.STU_NO = STU_NO
        self.STU_NAME = STU_NAME
        self.STU_SEX = STU_SEX
        self.IN_YEAR = IN_YEAR
        self.MAJOR_NO = MAJOR_NO
        self.set_password('123456')
    
    def get_id(self):
        return self.STU_NO
    
    def set_password(self,password):
        self.STU_PASSWORD = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.STU_PASSWORD,password)
    
    # 取消选课
    def drop_course(self,COURSE_NO):
        course_drop = [course for course in self.COURSES if course.COURSE_NO==COURSE_NO][0]
        self.COURSES.remove(course_drop)

# 教师表
class Teacher(UserMixin,db.Model):
    TEACHER_NO = db.Column(db.String(8), primary_key=True)
    TEACHER_NAME = db.Column(db.String(10), nullable=False)
    TEACHER_SEX = db.Column(db.String(2), nullable=False)
    IN_YEAR = db.Column(db.String(4), nullable=False)
    TEACHER_TITLE = db.Column(db.String(10))
    TEACHER_PASSWORD = db.Column(db.Text, nullable=False)
    COLLEGE_NO = db.Column(db.String(4), db.ForeignKey('college.COLLEGE_NO'), nullable=False)
    STUDENTS = db.relationship('Student', secondary='course_select_table', backref='teacher', lazy='subquery')
    COURSES = db.relationship('Course', secondary='course_teacher', backref='teacher', lazy='subquery')

    def __init__(self,TEACHER_NO,TEACHER_NAME,TEACHER_SEX,IN_YEAR,TEACHER_TITLE):
        self.TEACHER_NO = TEACHER_NO
        self.TEACHER_NAME = TEACHER_NAME
        self.TEACHER_SEX = TEACHER_SEX 
        self.IN_YEAR = IN_YEAR
        self.TEACHER_TITLE = TEACHER_TITLE
        self.set_password('123456')

    def get_id(self):
        return self.TEACHER_NO
    
    def set_password(self,password):
        self.TEACHER_PASSWORD = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.TEACHER_PASSWORD,password)
