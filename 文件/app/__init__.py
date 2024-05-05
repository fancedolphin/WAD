from flask import Flask,render_template
from config import Config



app = Flask(__name__,template_folder='./templates',static_folder='./static')
app.config.from_object(Config)


# 自定义没有通过CSRF验证错误响应
@app.errorhandler(400)
def csrf_error(reason):
    return render_template('400.html', reason=reason),400


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

