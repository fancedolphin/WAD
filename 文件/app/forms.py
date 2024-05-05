from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,validators
from wtforms.validators import DataRequired

'''class LoginForm(FlaskForm):
    user_no = StringField('UserNumber', validators=[DataRequired('Dont miss User number!')])
    password = PasswordField('Password', validators=[DataRequired('Dont miss password!')])
    submit = SubmitField('Login')'''