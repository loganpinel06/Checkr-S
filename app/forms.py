#forms.py will...

#imports
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, PasswordField, DateField, HiddenField
from wtforms.validators import DataRequired
from datetime import datetime

#create a variable for the current year for YearForm purposes
current_year = datetime.today().year

#create a form class for the LoginForm
class LoginForm(FlaskForm):
    #create the fields
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')

#create a form class for the RegisterForm
class RegisterForm(FlaskForm):
    #create the fields
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired()])
    submit = SubmitField('Register')

#create a form class for the YearForm
class YearForm(FlaskForm):
    #create the fields
    #coerce=int is used to convert the string value to an integer so we can set a default value in the backend
    year = SelectField('Year: ', choices=[(str(i), str(i)) for i in range(2000, current_year + 1)], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Select Year')

#create a form for the StartingBalanceForm
class StartingBalanceForm(FlaskForm):
    #hidden field
    field_id = HiddenField(id="field_id", render_kw={"value": "balanceForm"})
    #pass additional HTML keywords with render_kw
    #use to set the step to any to accept float values
    #additionally we will create a custom label in HTML since we need to inject variables
    starting_balance = FloatField(validators=[DataRequired()])
    submit = SubmitField('Submit')

#create a form for the ResetBalanceForm
class ResetBalanceForm(FlaskForm):
    #hidden field
    field_id = HiddenField(render_kw={"value": "resetBalanceForm"})
    #create the fields
    submit = SubmitField('Reset Balance')

#create a form for the UserInputForm
class UserInputForm(FlaskForm):
    #create the fields
    #hidden field
    field_id = HiddenField(render_kw={"value": "inputForm"})
    #date field
    date = DateField('Transaction Date: ', format='%Y-%m-%d', validators=[DataRequired()])
    #content field
    content = StringField('Transaction Description: ', validators=[DataRequired()])
    #amount field
    amount = FloatField('Transaction Amount: ', validators=[DataRequired()])
    #transaction type field
    type = SelectField('Transaction Type: ', choices=['+', '-'], validators=[DataRequired()])
    #submit field
    submit = SubmitField('Add Transaction')

#create a form for the EditTransactionForm
class EditTransactionForm(FlaskForm):
    #create the fields
    #date field
    date = DateField('Transaction Date: ', format='%Y-%m-%d', validators=[DataRequired()])
    #content field
    content = StringField('Transaction Description: ', validators=[DataRequired()])
    #amount field
    amount = FloatField('Transaction Amount: ', validators=[DataRequired()], render_kw={"step": "any"})
    #type field
    type = SelectField('Transaction Type: ', choices=['+', '-'], validators=[DataRequired()])
    #submit field
    submit = SubmitField('Edit Transaction')
