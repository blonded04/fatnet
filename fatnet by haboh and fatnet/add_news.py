from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[
        DataRequired()])  # if there is no data it wouldn't be sent
    content = TextAreaField('Текст новости', validators=[
        DataRequired()])  # if there is no data it wouldn't be sent
    submit = SubmitField('Добавить')
