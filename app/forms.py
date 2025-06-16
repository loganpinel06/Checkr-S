#forms.py will...

#imports
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, PasswordField, HiddenField
from wtforms.validators import DataRequired

#create a form class for the LoginForm
class LoginForm(FlaskForm):
    #create the fields
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')