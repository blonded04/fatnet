from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()],
                           render_kw={"id": "login", "class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"id": "password", "class": "form-control"})
    fileName = FileField("Аватар", validators=[DataRequired()],
                         render_kw={"class": "form-control-file", "id": "uploadFile"})
    submit = SubmitField('Зарегистрироваться')
