import pymysql
from config import HOST,DATABASE,USERNAME,PASSWORD

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
        print('query success!')
        return result
    except:
        # 回滚：恢复对数据库所做的最后更改或提交
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
# 修改
def update(sql):
    db = pymysql.connect(host=HOST, user=USERNAME, password=PASSWORD, db=DATABASE, charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
        print('update success')
    except:
        db.rollback()
    cur.close()
    db.close()
