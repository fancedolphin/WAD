from . import web
from flask import jsonify,render_template,request
from app.utils import query,function


# 学生查询成绩页，分页
@web.route('/score_query',methods=['GET','POST'])
def score_query():

    user_id = function.get_id()
    if function.student(user_id):   #isinstance(current_user._get_current_object(), Student)
        user_no = user_id                  #current_user.get_id()
        page = request.args.get("page")
        is_page = request.args.get("is_page")
        #print(page,is_page)
        if page is None:
            page = 1
        page = int(page)
        pageSize = 5
        page = (page-1)*pageSize
        #print(page,pageSize,user_no)
        #tableList = Course_select_table.query.filter_by(STU_NO=user_no).offset(page).limit(pageSize).all()
        sql = f"SELECT * FROM `course_select_table` where  STU_NO='{user_no}' LIMIT {page},{pageSize};"
        tableList = query.query_dic(sql)
        data = []
        index = 0
        #print(tableList)
        try:
            for key in tableList:
                obj = {}
                if index == 0:
                    index = page + index + 1
                else:
                    index = index + 1
                #teacher = Teacher.query.filter_by(TEACHER_NO=key['TEACHER_NO']).first()
                sq2 = f"SELECT * FROM `teacher` WHERE TEACHER_NO='{key['TEACHER_NO']}'"
                teacher = query.query_dic(sq2)
                teacher_name = teacher[0]['TEACHER_NAME']
                #course = Course.query.filter_by(COURSE_NO=key['COURSE_NO']).first()
                sq3 = f"SELECT *FROM `course` WHERE COURSE_NO='{key['COURSE_NO']}';"
                course = query.query_dic(sq3)
                obj['number'] = index
                obj['course_no'] = key['COURSE_NO']
                obj['stu_no'] = key['STU_NO']
                obj['grade'] = key['GRADE']
                obj['teacher_name'] = teacher_name
                obj['course_name'] = course[0]['COURSE_NAME']
                obj['credit'] = course[0]['COURSE_CREDIT']
                obj['course_hour'] = course[0]['COURSE_HOUR']
                data.append(obj)
        except:
            data = []
        if is_page is not None:
            return jsonify(data)
        else:
            return render_template('score_query.html',tableList=data)

# 获取所有学生选课的成绩列表
@web.route('/score_query/getTable',methods=['GET'])
#@login_required
def getScoreTable():
    user_no = function.get_id()
    if function.student(user_no):      #isinstance(current_user._get_current_object(), Student)
        #user_no = current_user.get_id()
        try:
            #tableList = Course_select_table.query.filter_by(STU_NO=user_no).all()
            sql = f"SELECT * FROM `course_select_table` where  STU_NO='{user_no}';"
            tableList = query.query_dic(sql)
            data = []
            index = 0
            for key in tableList:
                # print(key)
                obj = {}
                index = index + 1 
                #teacher = Teacher.query.filter_by(TEACHER_NO=key['TEACHER_NO']).first()
                #teacher_name = teacher.TEACHER_NAME
                sq2 = f"SELECT * FROM `teacher` WHERE TEACHER_NO='{key['TEACHER_NO']}'"
                teacher = query.query_dic(sq2)
                teacher_name = teacher[0]['TEACHER_NAME']

                #course = Course.query.filter_by(COURSE_NO=key['COURSE_NO']).first()
                sq3 = f"SELECT * FROM `course` WHERE COURSE_NO='{key['COURSE_NO']}';"
                course = query.query_dic(sq3)
                obj['number'] = index
                obj['course_no'] = key['COURSE_NO']
                obj['stu_no'] = key['STU_NO']
                obj['grade'] = key['GRADE']
                obj['teacher_name'] = teacher_name
                obj['course_name'] = course[0]['COURSE_NAME']
                obj['credit'] = course[0]['COURSE_CREDIT']
                obj['course_hour'] = course[0]['COURSE_HOUR']
                data.append(obj)
            return jsonify(data)
        except Exception as e:
            return jsonify(None)
    
# 搜索已选课程成绩
@web.route('/score_query/getSearch/<course_no>',methods=['GET'])
#@login_required
def getScoreSearchList(course_no):
    user_id = function.get_id()
    if function.student(user_id):
        user_no = user_id
        try:
            print(user_no,course_no)
            #tableList = Course_select_table.query.filter_by(STU_NO=user_no,COURSE_NO=course_no).first()
            sq1 = f"SELECT * FROM `course_select_table` WHERE STU_NO='{user_no}' and COURSE_NO='{course_no}';"
            tableList = query.query_dic(sq1)
            if tableList is None:
                return jsonify({'msg':'搜索失败','code':400})
            else:
                data = []
                index = 0
                # print(key)
                key = tableList
                obj = {}
                index = index + 1 
                #teacher = Teacher.query.filter_by(TEACHER_NO=key[0]['TEACHER_NO']).first()
                #teacher_name = teacher.TEACHER_NAME
                sq2 = f"SELECT * FROM `teacher` WHERE TEACHER_NO='{key[0]['TEACHER_NO']}'"
                teacher = query.query_dic(sq2)
                teacher_name = teacher[0]['TEACHER_NAME']
                #course = Course.query.filter_by(COURSE_NO=key[0]['COURSE_NO']).first()
                sq3 = f"SELECT * FROM `course` WHERE COURSE_NO='{key[0]['COURSE_NO']}';"
                course = query.query_dic(sq3)
                obj['number'] = index
                obj['course_no'] = key[0]['COURSE_NO']
                obj['stu_no'] = key[0]['STU_NO']
                obj['grade'] = key[0]['GRADE']
                obj['teacher_name'] = teacher_name
                obj['course_name'] = course[0]['COURSE_NAME']
                obj['credit'] = course[0]['COURSE_CREDIT']
                obj['course_hour'] = course[0]['COURSE_HOUR']
                data.append(obj)
                return jsonify(data)
        except Exception as e:
            return jsonify({'msg':'搜索失败','code':400})

# 选课页，分页
@web.route('/choose_course',methods=['GET','POST'])
def choose_course():
    user_id = function.get_id()
    if function.student(user_id):
        user_no = user_id
        page = request.args.get("page")
        is_page = request.args.get("is_page")
        if page is None:
            page = 1
        page = int(page)
        pageSize = 5
        page = (page-1)*pageSize
        sql = "select * from COURSE a where not exists(select * from COURSE_SELECT_TABLE b where a.COURSE_NO=b.COURSE_NO and STU_NO=%s) limit %d,%d" % (user_no,page,pageSize)
        tableList = query.query(sql)
        #print(tableList)
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
            #print(course_teacher)
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
            #print(data)
            return jsonify(data)
        else:
            #print('data数据',data)
            return render_template('choose_course.html',tableList=data)

# 获取所有学生未选课程列表
@web.route('/choose_course/getTable',methods=['GET'])
#@login_required
def getChooseTable():
    user_id = function.get_id()
    if function.student(user_id):
        user_no = user_id
        sql = "select * from COURSE a where not exists(select * from COURSE_SELECT_TABLE b where a.COURSE_NO=b.COURSE_NO and STU_NO=%s)" % user_no 
        tableList = query.query(sql)
        data2 = []
        index = 0
        #print('tablelist：',tableList)
        for key in tableList:
            # print(key)
            obj = {}
            index = index + 1 
            sql2 = "select * from COURSE_TEACHER where COURSE_NO = '%s'" % key[0]
            course_teacher = query.query(sql2)

            if course_teacher == None:
                pass
            else:
                sql3 = "select * from TEACHER where TEACHER_NO = '%s'" % course_teacher[0][0]
                teacher = query.query(sql3)
                obj['number'] = index
                obj['course_no'] = key[0]
                obj['course_capacity'] = course_teacher[0][2]
                obj['teacher_name'] = teacher[0][1]
                obj['course_name'] = key[1]
                obj['credit'] = key[2]
                obj['course_hour'] = key[3]
                data2.append(obj)
        return jsonify(data2)

# 搜索未选课程
@web.route('/choose_course/getSearch/<course_no>',methods=['GET'])
#@login_required
def getChooseSearchList(course_no):
    user_id = function.get_id()
    if function.student(user_id):
        user_no = user_id
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
            return jsonify(data)
        except Exception as e:
            return jsonify({'msg':'搜索失败','code':400})

# 选课
@web.route('/choose_course/choose',methods=['POST'])
#@login_required
def chooseCourse():
    #print('进入选课页面')
    user_id = function.get_id()
    if function.student(user_id):
        user_no = user_id
        course_no = request.values.get('course_no')


        sq2 =f"SELECT * FROM `course_teacher` WHERE COURSE_NO='{course_no}';"
        sounum = query.query_dic(sq2)
        sq1 = f"UPDATE `course_teacher` set COURSE_CAPACITY='{int(sounum[0]['COURSE_CAPACITY'])-1}' where COURSE_NO='{course_no}';"
        query.update(sq1)

        sq3 = f"INSERT into course_select_table(STU_NO,TEACHER_NO,COURSE_NO) VALUES('{user_no}','{sounum[0]['TEACHER_NO']}','{course_no}');"
        res = query.update(sq3)
        #print(res)
        if res == None:
            return jsonify({'msg':'选课成功,正在重新获取列表','code':200})
        else:
            return jsonify({'msg':'选课失败,正在重新获取列表','code':400})

# 已选课页
@web.route('/isChoosed_course',methods=['GET'])
#@login_required
def isChoosed_course():
    user_id = function.get_id()
    if function.student(user_id):     #isinstance(current_user._get_current_object(), Student)
        user_no = user_id
        page = request.args.get("page")
        is_page = request.args.get("is_page")
        if page is None:
            page = 1
        page = int(page)
        pageSize = 5
        page = (page-1)*pageSize


        sql = f"SELECT * FROM `course_select_table` where  STU_NO='{user_no}' LIMIT {page},{pageSize};"
        tableList = query.query_dic(sql)

        data = []
        index = 0
        try:
            for key in tableList:
                # print(key)
                obj = {}
                if index == 0:
                    index = page + index + 1
                else:
                    index = index + 1
                #teacher = Teacher.query.filter_by(TEACHER_NO=key['TEACHER_NO']).first()
                #teacher_name = teacher.TEACHER_NAME
                sq2 = f"SELECT * FROM `teacher` WHERE TEACHER_NO='{key['TEACHER_NO']}'"
                teacher = query.query_dic(sq2)
                teacher_name = teacher[0]['TEACHER_NAME']

                #course = Course.query.filter_by(COURSE_NO=key['COURSE_NO']).first()
                sq3 = f"SELECT * FROM `course` WHERE COURSE_NO='{key['COURSE_NO']}';"
                course = query.query_dic(sq3)

                #course_teacher = Course_Teacher.query.filter_by(COURSE_NO=key['COURSE_NO']).first()
                sq4 =f"SELECT * FROM `course_teacher` WHERE COURSE_NO='{key['COURSE_NO']}';"
                course_teacher = query.query_dic(sq4)

                obj['number'] = index
                obj['course_no'] = key['COURSE_NO']
                obj['course_capacity'] = course_teacher[0]['COURSE_CAPACITY']
                obj['teacher_name'] = teacher_name
                obj['course_name'] = course[0]['COURSE_NAME']
                obj['credit'] = course[0]['COURSE_CREDIT']
                obj['course_hour'] = course[0]['COURSE_HOUR']
                data.append(obj)
        except:
            data = []
        if is_page is not None:
            return jsonify(data)
        else:
            return render_template('isChoosed_course.html',tableList=data)

# 获取所有学生已选课程列表
@web.route('/isChoosed_course/getTable',methods=['GET'])
#@login_required
def getisChoosedTable():
    user_id = function.get_id()
    if function.student(user_id):     #isinstance(current_user._get_current_object(), Student)
        user_no = user_id
        #tableList = Course_select_table.query.filter_by(STU_NO=user_no).filter(Course_select_table.COURSE_NO==Course.COURSE_NO)
        sql = f"SELECT * FROM `course_select_table` where  STU_NO='{user_no}';"
        tableList = query.query_dic(sql)

        data = []
        index = 0
        for key in tableList:
            #print(key)
            obj = {}
            if index == 0:
                index = index + 1 
            #teacher = Teacher.query.filter_by(TEACHER_NO=key['TEACHER_NO']).first()
            #teacher_name = teacher.TEACHER_NAME
            sq2 = f"SELECT * FROM `teacher` WHERE TEACHER_NO='{key['TEACHER_NO']}'"
            teacher = query.query_dic(sq2)
            teacher_name = teacher[0]['TEACHER_NAME']

            #course = Course.query.filter_by(COURSE_NO=key['COURSE_NO']).first()
            sq3 = f"SELECT * FROM `course` WHERE COURSE_NO='{key['COURSE_NO']}';"
            course = query.query_dic(sq3)

            #course_teacher = Course_Teacher.query.filter_by(COURSE_NO=key['COURSE_NO']).first()
            sq4 = f"SELECT * FROM `course_teacher` WHERE COURSE_NO='{key['COURSE_NO']}';"
            course_teacher = query.query_dic(sq4)

            obj['number'] = index
            obj['course_no'] = key['COURSE_NO']
            obj['course_capacity'] = course_teacher[0]['COURSE_CAPACITY']
            obj['teacher_name'] = teacher_name
            obj['course_name'] = course[0]['COURSE_NAME']
            obj['credit'] = course[0]['COURSE_CREDIT']
            obj['course_hour'] = course[0]['COURSE_HOUR']
            data.append(obj)
        #print('getdata',data)
        return jsonify(data)

# 搜索已选课程
@web.route('/isChoosed_course/getSearch/<course_no>',methods=['GET'])
#@login_required
def getIsChoosedSearchList(course_no):
    user_id = function.get_id()
    if function.student(user_id):    #isinstance(current_user._get_current_object(), Student)
        user_no = user_id
        data = []
        index = 0
        obj = {}
        if index == 0:
            index = index +1
        try:
            #print(user_no,course_no)
            #tableList = Course_select_table.query.filter_by(STU_NO=user_no,COURSE_NO=course_no).first()
            sql = f"SELECT * FROM `course_select_table` where  STU_NO='{user_no}' and COURSE_NO='{course_no}';"
            tableList = query.query_dic(sql)

            #teacher = Teacher.query.filter_by(TEACHER_NO=tableList[0]['TEACHER_NO']).first()
            #teacher_name = teacher.TEACHER_NAME
            sq2 = f"SELECT * FROM `teacher` WHERE TEACHER_NO='{tableList[0]['TEACHER_NO']}'"
            teacher = query.query_dic(sq2)
            teacher_name = teacher[0]['TEACHER_NAME']


            #course = Course.query.filter_by(COURSE_NO=tableList[0]['COURSE_NO']).first()
            sq4 = f"SELECT * FROM `course` WHERE COURSE_NO='{tableList[0]['COURSE_NO']}';"
            course = query.query_dic(sq4)

            obj['number'] = index
            obj['course_no'] = tableList[0]['COURSE_NO']
            obj['stu_no'] = tableList[0]['STU_NO']
            obj['grade'] = tableList[0]['GRADE']
            obj['teacher_name'] = teacher_name
            obj['course_name'] = course[0]['COURSE_NAME']
            obj['credit'] = course[0]['COURSE_CREDIT']
            obj['course_hour'] = course[0]['COURSE_HOUR']
            data.append(obj)
            return jsonify(data)
        except Exception as e:
            return jsonify({'msg':'搜索失败','code':400})
        
# 取消选课
@web.route('/isChoosed_course/cancelChoose',methods=['POST'])
#@login_required
def cancelChooseCourse():
    user_id = function.get_id()
    if function.student(user_id):
        user_no = user_id
        course_no = request.values.get('course_no')
        try:
            sq2 = f"SELECT * FROM `course_teacher` WHERE COURSE_NO='{course_no}';"
            sounum = query.query_dic(sq2)
            #print(int(sounum[0]['COURSE_CAPACITY']) + 1)
            sq3 = f"UPDATE `course_teacher` set COURSE_CAPACITY='{int(sounum[0]['COURSE_CAPACITY']) + 1}' where COURSE_NO='{course_no}';"
            query.update(sq3)
            sq4 =f"DELETE from course_select_table where STU_NO='{user_no}' and COURSE_NO='{course_no}';"
            query.update(sq4)

            return jsonify({'msg':'取消选课成功,正在重新获取列表','code':200})
        except Exception as e:
            return  jsonify({'msg':'取消选课失败,正在重新获取列表','code':200})
        