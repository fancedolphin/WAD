from . import web
from flask import jsonify,render_template,redirect,session,url_for ,request,flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Student,Teacher,Manager,College,Major,Course_select_table,Course,Course_Teacher
from app import db
from app.utils import query 

# 学生查询成绩页，分页
@web.route('/score_query',methods=['GET','POST'])
@login_required
def score_query():
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        page = request.args.get("page")
        is_page = request.args.get("is_page")
        if page is None:
            page = 1
        page = int(page)
        pageSize = 5
        page = (page-1)*pageSize
        tableList = Course_select_table.query.filter_by(STU_NO=user_no).offset(page).limit(pageSize).all()
        data = []
        index = 0
        for key in tableList:
            # print(key)
            obj = {}
            if index == 0:
                index = page + index + 1
            else:
                index = index + 1 
            teacher = Teacher.query.filter_by(TEACHER_NO=key.TEACHER_NO).first()
            teacher_name = teacher.TEACHER_NAME
            course = Course.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            obj['number'] = index
            obj['course_no'] = key.COURSE_NO
            obj['stu_no'] = key.STU_NO
            obj['grade'] = key.GRADE
            obj['teacher_name'] = teacher_name
            obj['course_name'] = course.COURSE_NAME
            obj['credit'] = course.COURSE_CREDIT
            obj['course_hour'] = course.COURSE_HOUR
            data.append(obj)

        if is_page is not None:
            return jsonify(data)
        else:
            return render_template('score_query.html',tableList=data)

# 获取所有学生选课的成绩列表
@web.route('/score_query/getTable',methods=['GET'])
@login_required
def getScoreTable():
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        try:
            tableList = Course_select_table.query.filter_by(STU_NO=user_no).all()
            data = []
            index = 0
            for key in tableList:
                # print(key)
                obj = {}
                index = index + 1 
                teacher = Teacher.query.filter_by(TEACHER_NO=key.TEACHER_NO).first()
                teacher_name = teacher.TEACHER_NAME
                course = Course.query.filter_by(COURSE_NO=key.COURSE_NO).first()
                obj['number'] = index
                obj['course_no'] = key.COURSE_NO
                obj['stu_no'] = key.STU_NO
                obj['grade'] = key.GRADE
                obj['teacher_name'] = teacher_name
                obj['course_name'] = course.COURSE_NAME
                obj['credit'] = course.COURSE_CREDIT
                obj['course_hour'] = course.COURSE_HOUR
                data.append(obj)
            return jsonify(data)
        except Exception as e:
            return jsonify(None)
    
# 搜索已选课程成绩
@web.route('/score_query/getSearch/<course_no>',methods=['GET'])
@login_required
def getScoreSearchList(course_no):
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        try:
            tableList = Course_select_table.query.filter_by(STU_NO=user_no,COURSE_NO=course_no).first()
            if tableList is None:
                return jsonify({'msg':'搜索失败','code':400})
            else:
                data = []
                index = 0
                # print(key)
                key = tableList
                obj = {}
                index = index + 1 
                teacher = Teacher.query.filter_by(TEACHER_NO=key.TEACHER_NO).first()
                teacher_name = teacher.TEACHER_NAME    
                course = Course.query.filter_by(COURSE_NO=key.COURSE_NO).first()
                obj['number'] = index
                obj['course_no'] = key.COURSE_NO
                obj['stu_no'] = key.STU_NO
                obj['grade'] = key.GRADE
                obj['teacher_name'] = teacher_name
                obj['course_name'] = course.COURSE_NAME
                obj['credit'] = course.COURSE_CREDIT
                obj['course_hour'] = course.COURSE_HOUR
                data.append(obj)
          
                return jsonify(data)
        except Exception as e:
            return jsonify({'msg':'搜索失败','code':400})

# 选课页，分页
@web.route('/choose_course',methods=['GET','POST'])
@login_required
def choose_course():
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        page = request.args.get("page")
        is_page = request.args.get("is_page")
        if page is None:
            page = 1
        page = int(page)
        pageSize = 5
        page = (page-1)*pageSize
        sql = "select * from COURSE a where not exists(select * from COURSE_SELECT_TABLE b where a.COURSE_NO=b.COURSE_NO and STU_NO=%s) limit %d,%d" % (user_no,page,pageSize)
        tableList = query.query(sql)
        data = []
        index = 0

        for key in tableList:
            # print(key)
            obj = {}
            if index == 0:
                index = page + index + 1
            else:
                index = index + 1 
            sql2 = "select * from COURSE_TEACHER where COURSE_NO = '%s'" % key[0]
            course_teacher = query.query(sql2)
            # print(course_teacher)
            for course in course_teacher:
                sql3 = "select * from TEACHER where TEACHER_NO = '%s'" % course[0]
                teacher = query.query(sql3)
                obj['number'] = index
                obj['course_no'] = key[0]
                obj['course_capacity'] = course_teacher[0][2]
                obj['teacher_name'] = teacher[0][1]
                obj['course_name'] = key[1]
                obj['credit'] = key[2]
                obj['course_hour'] = key[3]
                data.append(obj)

        if is_page is not None:
            return jsonify(data)
        else:
            return render_template('choose_course.html',tableList=data)

# 获取所有学生未选课程列表
@web.route('/choose_course/getTable',methods=['GET'])
@login_required
def getChooseTable():
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        sql = "select * from COURSE a where not exists(select * from COURSE_SELECT_TABLE b where a.COURSE_NO=b.COURSE_NO and STU_NO=%s)" % user_no 
        tableList = query.query(sql)
        data = []
        index = 0

        for key in tableList:
            # print(key)
            obj = {}
            index = index + 1 
            sql2 = "select * from COURSE_TEACHER where COURSE_NO = '%s'" % key[0]
            course_teacher = query.query(sql2)
            # print(course_teacher)
            for course in course_teacher:
                sql3 = "select * from TEACHER where TEACHER_NO = '%s'" % course[0]
                teacher = query.query(sql3)
                obj['number'] = index
                obj['course_no'] = key[0]
                obj['course_capacity'] = course_teacher[0][2]
                obj['teacher_name'] = teacher[0][1]
                obj['course_name'] = key[1]
                obj['credit'] = key[2]
                obj['course_hour'] = key[3]
                data.append(obj)

        return jsonify(data)

# 搜索未选课程
@web.route('/choose_course/getSearch/<course_no>',methods=['GET'])
@login_required
def getChooseSearchList(course_no):
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        data = []
        index = 0
        try:
            sql = "select * from COURSE a where not exists(select * from COURSE_SELECT_TABLE b where a.COURSE_NO=b.COURSE_NO and STU_NO=%s)" % user_no 
            tableList = query.query(sql)
            for key in tableList:
                obj = {}
                index = index + 1
                if key[0] == course_no:
                    sql2 = "select * from COURSE_TEACHER where COURSE_NO = '%s'" % key[0]
                    course_teacher = query.query(sql2)
                    sql3 = "select * from TEACHER where TEACHER_NO = '%s'" % course_teacher[0][0]
                    teacher = query.query(sql3)
                    obj['number'] = index
                    obj['course_no'] = key[0]
                    obj['course_capacity'] = course_teacher[0][2]
                    obj['teacher_name'] = teacher[0][1]
                    obj['course_name'] = key[1]
                    obj['credit'] = key[2]
                    obj['course_hour'] = key[3]
                    data.append(obj)
            print(data)
            return jsonify(data)
        except Exception as e:
            return jsonify({'msg':'搜索失败','code':400})

# 选课
@web.route('/choose_course/choose',methods=['POST'])
@login_required
def chooseCourse():
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        course_no = request.values.get('course_no')
        choose_course = Course_Teacher.query.filter_by(COURSE_NO=course_no).first()
        choose_course.COURSE_CAPACITY = int(choose_course.COURSE_CAPACITY)-1
        db.session.commit()
        res = Course_select_table(STU_NO=user_no,TEACHER_NO=choose_course.TEACHER_NO,COURSE_NO=course_no)
        db.session.add(res)
        db.session.commit()
        if res:
            return jsonify({'msg':'选课成功,正在重新获取列表','code':200})
        else:
            return jsonify({'msg':'选课失败,正在重新获取列表','code':400})

# 已选课页
@web.route('/isChoosed_course',methods=['GET'])
@login_required
def isChoosed_course():
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        page = request.args.get("page")
        is_page = request.args.get("is_page")
        if page is None:
            page = 1
        page = int(page)
        pageSize = 5
        page = (page-1)*pageSize
        tableList = Course_select_table.query.filter_by(STU_NO=user_no).filter(Course_select_table.COURSE_NO==Course.COURSE_NO).offset(page).limit(pageSize).all()
        data = []
        index = 0
        for key in tableList:
            # print(key)
            obj = {}
            if index == 0:
                index = page + index + 1
            else:
                index = index + 1 
            teacher = Teacher.query.filter_by(TEACHER_NO=key.TEACHER_NO).first()
            teacher_name = teacher.TEACHER_NAME
            course = Course.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            course_teacher = Course_Teacher.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            obj['number'] = index
            obj['course_no'] = key.COURSE_NO
            obj['course_capacity'] = course_teacher.COURSE_CAPACITY
            obj['teacher_name'] = teacher_name
            obj['course_name'] = course.COURSE_NAME
            obj['credit'] = course.COURSE_CREDIT
            obj['course_hour'] = course.COURSE_HOUR
            data.append(obj)
        print(tableList)
        if is_page is not None:
            return jsonify(data)
        else:
            return render_template('isChoosed_course.html',tableList=data)

# 获取所有学生已选课程列表
@web.route('/isChoosed_course/getTable',methods=['GET'])
@login_required
def getisChoosedTable():
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        tableList = Course_select_table.query.filter_by(STU_NO=user_no).filter(Course_select_table.COURSE_NO==Course.COURSE_NO)
        data = []
        index = 0
        for key in tableList:
            # print(key)
            obj = {}
            if index == 0:
                index = index + 1 
            teacher = Teacher.query.filter_by(TEACHER_NO=key.TEACHER_NO).first()
            teacher_name = teacher.TEACHER_NAME
            course = Course.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            course_teacher = Course_Teacher.query.filter_by(COURSE_NO=key.COURSE_NO).first()
            obj['number'] = index
            obj['course_no'] = key.COURSE_NO
            obj['course_capacity'] = course_teacher.COURSE_CAPACITY
            obj['teacher_name'] = teacher_name
            obj['course_name'] = course.COURSE_NAME
            obj['credit'] = course.COURSE_CREDIT
            obj['course_hour'] = course.COURSE_HOUR
            data.append(obj)
        print(data)

        return jsonify(data)

# 搜索已选课程
@web.route('/isChoosed_course/getSearch/<course_no>',methods=['GET'])
@login_required
def getIsChoosedSearchList(course_no):
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        data = []
        index = 0
        obj = {}
        if index == 0:
            index = index +1
        try:
            tableList = Course_select_table.query.filter_by(STU_NO=user_no,COURSE_NO=course_no).first()
            teacher = Teacher.query.filter_by(TEACHER_NO=tableList.TEACHER_NO).first()
            teacher_name = teacher.TEACHER_NAME
            course = Course.query.filter_by(COURSE_NO=tableList.COURSE_NO).first()
            obj['number'] = index
            obj['course_no'] = tableList.COURSE_NO
            obj['stu_no'] = tableList.STU_NO
            obj['grade'] = tableList.GRADE
            obj['teacher_name'] = teacher_name
            obj['course_name'] = course.COURSE_NAME
            obj['credit'] = course.COURSE_CREDIT
            obj['course_hour'] = course.COURSE_HOUR
            data.append(obj)
            return jsonify(data)
        except Exception as e:
            return jsonify({'msg':'搜索失败','code':400})
        
# 取消选课
@web.route('/isChoosed_course/cancelChoose',methods=['POST'])
@login_required
def cancelChooseCourse():
    if isinstance(current_user._get_current_object(), Student):
        user_no = current_user.get_id()
        course_no = request.values.get('course_no')
        try:
            res = Student.query.filter_by(STU_NO=user_no).first()
            res.drop_course(course_no)
            choose_course = Course_Teacher.query.filter_by(COURSE_NO=course_no).first()
            choose_course.COURSE_CAPACITY = int(choose_course.COURSE_CAPACITY) + 1
            db.session.commit()
            return jsonify({'msg':'取消选课成功,正在重新获取列表','code':200})
        except Exception as e:
            return  jsonify({'msg':'取消选课失败,正在重新获取列表','code':200})
        