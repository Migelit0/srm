from flask_table import Col, BoolCol
from flask_wtf import FlaskForm


class AttendanceTable(FlaskForm):  # https://github.com/SergioLlana/datatables-flask-serverside
    forms = []
    classes = ['some_class']
    # name = Col('Name')
    attendance_bool = BoolCol('Attendance_bool', yes_display='Affirmative', no_display='Negatory')


if __name__ == '__main__':
    table = AttendanceTable(items, classes=['otherclass'])
