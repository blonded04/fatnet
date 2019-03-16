from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()],
                           render_kw={"id": "login",
                                      "class": "form-control"})  # if there is no data it wouldn't be sent
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"id": "password",
                                        "class": "form-control"})  # if there is no data it wouldn't be sent
    fileName = FileField("Аватар", validators=[DataRequired()],
                         render_kw={"class": "form-control-file",
                                    "id": "uploadFile"})  # if there is no data it wouldn't be sent
    submit = SubmitField('Зарегистрироваться')
