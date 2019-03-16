from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={
        "placeholder": "Логин"})  # if there is no data it wouldn't be sent
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={
                                 "placeholder": "Пароль"})  # if there is no data it wouldn't be sent
    submit = SubmitField('Войти')
