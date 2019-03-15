from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти')
