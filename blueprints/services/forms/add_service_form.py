from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, Regexp


class AddServiceForm(FlaskForm):
    regex = '(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]'
    host = StringField('хост сервера', validators=[DataRequired(),
                                                   Regexp(regex=regex)])
    kuznechik_key = StringField('ключ алгоритма "кузнечик"',
                                   validators=[DataRequired(), Length(min=32, max=32,
                                                                      message="Длина ключа должна быть 32"),
                                               Regexp(regex='[A-Za-z0-9]')])
    access_type = SelectField('Выберете тип доступа данных', choices=[(1, 'Только id'),
                                                                      (2, 'ФИО и класс учащегося')])
    submit = SubmitField('Добавить Сервис')