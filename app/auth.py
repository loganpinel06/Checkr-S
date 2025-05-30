#auth.py will handle user authentication using Flask-Login by managing the routes necessary for login and registration
#the User model which handles data for users can be found in models.py
#finally, the auth blueprint will be registered in the __init__.py file of the app package

#imports
#Core Flask imports
from flask import Blueprint, render_template, request, redirect, url_for
#import Flask-Login for authentication

#import password hasing fucntions from werkzeug.security
from werkzeug.security import generate_password_hash, check_password_hash