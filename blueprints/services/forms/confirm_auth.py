from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField


class ConfirmAuth(FlaskForm):
    submit = SubmitField('Войти')
    name = HiddenField('first_name')
    sure_name = HiddenField('sure_name')
    second_name = HiddenField('second_name')
    class_num = HiddenField('class_num')
    class_liter = HiddenField('class_liter')
    login = HiddenField('login')