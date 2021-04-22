from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddNewLessonForm(FlaskForm):
    group_id = IntegerField('ID группы', validators=[DataRequired()])
    teacher_id = IntegerField('ID учителя', validators=[DataRequired()])
    date = StringField('Дата занятия (hh:mm-d)', validators=[DataRequired()])
    title = StringField('Названия занятия')
    submit = SubmitField('Добавить')
