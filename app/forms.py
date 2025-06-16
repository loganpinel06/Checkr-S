#forms.py will...

#imports
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, PasswordField, HiddenField
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

#creat a form class for the YearForm
class YearForm(FlaskForm):
    #create the fields
    #coerce=int is used to convert the string value to an integer so we can set a default value in the backend
    year = SelectField('Year: ', choices=[(str(i), str(i)) for i in range(2000, current_year + 1)], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')