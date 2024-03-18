from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,validators
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_no = StringField('UserNumber', validators=[DataRequired('用户编码必填!')])
    password = PasswordField('Password', validators=[DataRequired('密码必填!')])
    submit = SubmitField('登录')