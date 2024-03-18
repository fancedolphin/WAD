from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

app = Flask(__name__,template_folder='./templates',static_folder='./static')
app.config.from_object(Config)
bootstrap = Bootstrap(app)

# 初始化SQLAlchemy对象
db = SQLAlchemy(app)

# migrate 迁移组件初始化
migrate = Migrate(app, db)
#启动CSRF保护
csrf=CSRFProtect(app)
WTF_CSRF_SECRET_KEY='salt' #设置token 生成salt

# 自定义没有通过CSRF验证错误响应
@app.errorhandler(400)
def csrf_error(reason):
    return render_template('400.html', reason=reason),400

# 配置用户会话管理
login_manager = LoginManager()
login_manager.login_view = 'web.login' # 设置登陆视图，用于未授权操作的跳转
# login_manager.login_message_category = 'info' # 设置未登录跳转,携带到登陆请求的参数
login_manager.login_message = u'对不起，您还没有登录' # 设置快闪消息，用于提示用户
login_manager.init_app(app)

# 错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def secial_exception_handler(e):
    return render_template('500.html'),500

from app.web.views import web
# 注册蓝图
app.register_blueprint(web)

