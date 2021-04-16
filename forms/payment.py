from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class AddPaymentForm(FlaskForm):  # https://github.com/SergioLlana/datatables-flask-serverside
    student_id = IntegerField('ID ученика', validators=[DataRequired()])
    # TODO: НУ ДОДЕЛАТЬ ФОРМУ
