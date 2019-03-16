from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MessageSendForm(FlaskForm):
    content = TextAreaField('Текст сообщения', validators=[
        DataRequired()])  # if there is no data it wouldn't be sent
    submit = SubmitField('Отправить')
