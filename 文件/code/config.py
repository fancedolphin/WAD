import os 
from datetime import timedelta

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'student_management_system'
USERNAME = 'root'
PASSWORD = '123456'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

class Config:
    # 表单交互时，所以要设置 secret_key，以防跨域攻击（ CSRF ）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hpc'
    # session 过期时间，没有配置此项时，默认为31天，配置后设置session.permanent=True时，以此配置项的值为准
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    # 设置静态文件缓存过期时间
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    # JSON编码格式，防止返回中文乱码
    JSON_AS_ASCII = False
    # Flask-SQLAlchemy连接数据库
    SQLALCHEMY_DATABASE_URI = DB_URI
    # 是否追踪数据库修改(开启后会触发一些钩子函数)  一般不开启, 会影响性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否显示底层执行的SQL语句
    SQLALCHEMY_ECHO = False
    # 隐藏未登录跳转携带消息的参数
    USE_SESSION_FOR_NEXT =True 

    @staticmethod
    def init_app(app):
        pass

