from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MessageSendForm(FlaskForm):
    content = TextAreaField('Текст сообщения', validators=[DataRequired()])
    submit = SubmitField('Отправить')
