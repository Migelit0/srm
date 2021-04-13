from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField
from wtforms.validators import DataRequired


class Stundent(FlaskForm):
    student = BooleanField('')


class AttendanceForm(FlaskForm):  # https://github.com/SergioLlana/datatables-flask-serverside
    # forms = []
    # classes = ['some_class']
    # name = Col('Name')
    # attendance_bool = BoolCol('Attendance_bool', yes_display='Affirmative', no_display='Negatory')
    #   student_0 = BooleanField('test', validators=[DataRequired()])
    #   student_1 = BooleanField('test', validators=[DataRequired()])
    #   student_2 = BooleanField('test', validators=[DataRequired()])
    #   student_3 = BooleanField('test', validators=[DataRequired()])
    #   student_4 = BooleanField('test', validators=[DataRequired()])
    #   student_5 = BooleanField('test', validators=[DataRequired()])
    # all = [student_0, student_1, student_2, student_3, student_4, student_5]
    all = FieldList(FormField(Stundent))
