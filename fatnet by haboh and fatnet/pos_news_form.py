from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()],
                        render_kw={"placeholder": "Заголовок", 'size': "20",
                                   "style": "margin-right: 10px;"})
    content = StringField('Текст новости', validators=[DataRequired()],
                          render_kw={"placeholder": "Что нового?", 'size': "50",
                                     "style": "margin-right: 10px;"})
    submit = SubmitField('Опубликовать', render_kw={'class': 'btn btn-light'})
