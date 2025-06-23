#forms.py uses the Flask-WTF extension to create forms that will be used inside the applications templates.
#this is designed to create stronger more secure forms compared to a traditional HTML form and protect agains CSRF attacks.

#imports
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, PasswordField, DateField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
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
    #see message parameter in validators to see what is required for username and password
    username = StringField('Username: ', validators=[DataRequired(), Length(min=6, max=30, message='Username must be between 6 and 30 characters long'), 
                                                     Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', message='Username must contain upper and lower case letters, and at least one number')])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long'), 
                                                       Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).+$', message='Password must contain upper and lower case letters, at least one number, and one special character')])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
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
