from app.utils import query


#获取用户id
def get_id():
    with open('id.txt', "r") as f:
        userid = f.read()
    return userid


#根据id查找用户信息
def student(id):
    sql = f"SELECT * FROM `student` where  STU_NO = '{str(id)}' "
    da = query.query(sql)
    return da
def teacher(id):
    sql = f"SELECT * FROM `teacher` where  TEACHER_NO = '{str(id)}' "
    da2 = query.query(sql)
    return da2
def manager(id):
    sql = f"SELECT * FROM `manager` where  MANAGER_NO = '{str(id)}' "
    da3 = query.query(sql)
    return da3

#密码验证
def stuhash(id,password):
    sql = f"SELECT * FROM `student` where  STU_NO = '{str(id)}' "
    dahash = query.query(sql)
    if dahash == None:
        return dahash
    else:
        #msg = check_password_hash(dahash[0][4],password)
        if dahash[0][4] == password:
            msg = True
        else:
            msg = False
        return msg
def teahash(id,password):
    sql = f"SELECT * FROM `teacher` where  TEACHER_NO = '{str(id)}' "
    dahash = query.query(sql)
    if dahash == None:
        return dahash
    else:
        #msg = check_password_hash(dahash[0][5],password)
        if dahash[0][5] == password:
            msg = True
        else:
            msg = False
        return msg
def manhash(id,password):
    sql = f"SELECT * FROM `manager` where  MANAGER_NO = '{str(id)}' "
    dahash = query.query(sql)
    if dahash == None:
        return dahash
    else:
        #msg = check_password_hash(dahash[0][2],password)
        if dahash[0][2] == password:
            msg = True
        else:
            msg = False
        return msg


#学生功能页函数
#1、学生信息显示
def student_data(id):
    sql1 = f"SELECT * FROM `student` where  STU_NO = '{str(id)}' "
    data1 = query.query_dic(sql1)
    sql2 = f"SELECT * FROM `college` where  COLLEGE_NO = '{data1[0]['COLLEGE_NO']}' "
    data2 = query.query_dic(sql2)
    sql3 = f"SELECT * FROM `major` where  MAJOR_NO = '{data1[0]['MAJOR_NO']}' "
    data3 = query.query_dic(sql3)
    data = {'STU_NAME': data1[0]['STU_NAME'], 'STU_SEX': data1[0]['STU_SEX'], 'STU_NO': data1[0]['STU_NO'],
            'college': {'COLLEGE_NAME': data2[0]['COLLEGE_NAME']}, 'major': {'MAJOR_NAME': data3[0]['MAJOR_NAME']}, 'IN_YEAR': data1[0]['IN_YEAR']}
    return data





#教师功能函数
#1、教师信息显示
def teacher_data(id):
    sql1 = f"SELECT * FROM `teacher` where  TEACHER_NO = '{str(id)}' "
    da1 = query.query_dic(sql1)

    sql2 = f"SELECT * FROM `college` where  COLLEGE_NO = '{da1[0]['COLLEGE_NO']}' "
    da2 = query.query_dic(sql2)
    data = {'TEACHER_NAME':da1[0]['TEACHER_NAME'],'TEACHER_SEX':da1[0]['TEACHER_SEX'],'TEACHER_NO':da1[0]['TEACHER_NO'],
            'college':{'COLLEGE_NAME':da2[0]['COLLEGE_NAME']},'TEACHER_TITLE':da1[0]['TEACHER_TITLE'],'IN_YEAR':da1[0]['IN_YEAR']}

    return data







