import pymysql
from config import HOST,DATABASE,USERNAME,PASSWORD
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'student_management_system'
USERNAME = 'root'
PASSWORD = '123456'
# 查询
def query(sql):
    # 创建与数据库连接对象
    db = pymysql.connect(host=HOST, user=USERNAME, password=PASSWORD, db=DATABASE, charset='utf8')
    # 利用db方法创建游标对象
    cur = db.cursor()
    try:
        # 利用游标对象execute()方法执行SQL命令
        cur.execute(sql)
        # 获取所有记录
        result = cur.fetchall()
        # 提交到数据库执行
        db.commit()
        #print('query success!')
        #查询不到返回None
        if len(result) == 0:
            result = None
        return result
    except:
        # 回滚：恢复对数据库所做的最后更改或提交
        print('查询错误')
        db.rollback()
    # 关闭游标对象
    cur.close()
    # 断开数据库连接
    db.close()

# 查询,返回字典格式数据
def query_dic(sql):
    # 创建与数据库连接对象
    db = pymysql.connect(host=HOST, user=USERNAME, password=PASSWORD, db=DATABASE, charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    # 利用db方法创建游标对象
    cur = db.cursor()
    try:
        # 利用游标对象execute()方法执行SQL命令
        cur.execute(sql)
        # 获取所有记录
        result = cur.fetchall()
        # 提交到数据库执行
        db.commit()
        #print('query success!')
        #查询不到返回None
        if len(result) == 0:
            result = None
        return result
    except:
        # 回滚：恢复对数据库所做的最后更改或提交
        print('查询错误')
        db.rollback()
    # 关闭游标对象
    cur.close()
    # 断开数据库连接
    db.close()


def model(sql):
    # 1.链接mysql数据库
    db = pymysql.connect(host='localhost',
                         user='ad',
                         password='password',
                         database='data',
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        # 2.创建游标对象
        cursor = db.cursor()
        # 3.执行sql语句
        res = cursor.execute(sql)
        db.commit()  # 在执行sql语句时，注意进行提交
        # 4.提取结果
        data = cursor.fetchall()
        if data:
            return data
        else:
            return res
    except:
        db.rollback()  # 当代码出现错误时，进行回滚
    finally:
        # 6.关闭数据库连接
        db.close()
# 修改，添加，删除
def update(sql):
    db = pymysql.connect(host=HOST, user=USERNAME, password=PASSWORD, db=DATABASE, charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
        #print('update success')
    except:
        return None
        print('修改/添加错误')
        db.rollback()
    cur.close()
    db.close()
