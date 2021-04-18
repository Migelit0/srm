from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class AddPaymentForm(FlaskForm):
    days_number = IntegerField('Количество дней')
    submit = SubmitField('Добавить')
