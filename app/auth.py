#auth.py will handle user authentication using Flask-Login by managing the routes necessary for login and registration
#this file uses the Users model from models.py to create and manage user accounts
#it will also use Flask-WTF forms from forms.py to create the login and registration forms for better security
#additionally the file uses the limiter created in __init__.py to limit the rate of requests to the login route so people cannot brute force the login
#lastly, the file sets the session to be permanent when a user is logged in so that the session will expire if the user is inactive for a certain amount of time

#imports
#Core Flask imports
from flask import Blueprint, render_template, session, redirect, url_for, flash
#import Flask-Login for authentication
from flask_login import login_user, login_required, logout_user
#import flask_limiters RateLimiterExceeded function to handle rate limiting and how it is displayed to the user
from flask_limiter.errors import RateLimitExceeded
#import the user model from models.py
from .models import User
#import the Flask-WTF forms from forms.py
from .forms import LoginForm, RegisterForm
#import the db object from __init__.py to connect to the database
#and import the login manager for user authentication
from . import db, login_manager, logger, limiter

#create the blueprint for the auth routes
view_auth = Blueprint('auth', __name__)

#create a user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    #this function will be used by Flask-Login to load the user from the database
    #it will return the user object if it exists, otherwise it will return None
    return User.query.get(int(user_id))

#create a route for the registration page
@view_auth.route('/register', methods=["GET", "POST"])
def register():
    #create the registration form
    form = RegisterForm()
    #validate the form (check to see if the form method is "POST")
    #but use the built in Flask-WTF method to also validate the form and check for CSRF token
    if form.validate_on_submit():
        #get the username and password from the form
        username = form.username.data
        password = form.password.data
        #check if the user already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            #if user exists, redirect back to registration page with an error message
            return redirect(url_for('auth.register', error='Username already exists'))
        #otherwise, create a new user
        else:
            #create a new user object
            new_user = User(username=username)
            #set the password for the new user (HASHING THE PASSWORD)
            new_user.set_password(password)
            #add the new user to the database
            #try, except block to handle any database errors
            try:
                #connect to the database and commit the new user
                db.session.add(new_user)
                db.session.commit()
                #flash a success message to the user
                flash("Registration successful! You can now log in")
                #if registration is successful, redirect to the login page
                return redirect(url_for('auth.login'))
            #ERROR
            except Exception as e:
                #log the errror to the logger
                logger.error(f"Error registering user: {e}")
                #flash a message to the user
                flash("There was an error registering your account, please try again")
                #redirect back to the registration page
                return redirect(url_for('auth.register'))
    #else we want to render the registration template
    else:
        #render the registration.html template
        return render_template('auth/register.html', form=form)

#create a route for the login page
@view_auth.route('/', methods=["GET", "POST"])
#add the decorator to limit the rate of requests to this route
@limiter.limit("3 per 5 minutes", methods=["POST"])  # Limit to 5 requests per minute, POST methods only
def login():
    #create the login form
    form = LoginForm()
    #validate the form (check to see if the form method is "POST")
    #but use the built in Flask-WTF method to also validate the form and check for CSRF token
    if form.validate_on_submit():
        #if the form is valid, get the username and password from the form
        username = form.username.data
        password = form.password.data
        #query the database for the user with the given username
        user = User.query.filter_by(username=username).first()
        #check if the user exists and if the password is correct
        if user and user.check_password(password):
            #try except block to handle any errors during login
            try:
                #log in the user
                login_user(user)
                #set the session as permanent to enable to session lifetime management
                session.permanent = True
                #redirect to the dashboard after successful login
                return redirect(url_for('view.dashboard'))
            #ERROR
            except Exception as e:
                #log the error to the logger
                logger.error(f"Error logging in user: {e}")
                #flash a message to the user
                flash("There was an error logging you in, please try again")
                #redirect back to the login page
                return redirect(url_for('auth.login'))
        #incorrect username or password
        else:
            #if login fails, redirect back to login page with an error message and flash a message saying login failed
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login', error='Invalid username or password'))
    #else we want to render the login template
    else:
        #redner the login.html tempalte
        return render_template('auth/login.html', form=form)
    
#create a route for logout
@view_auth.route('/logout', methods=["GET", "POST"])
@login_required #cant logout if not logged in
def logout():
    #log out the user
    logout_user()
    #flash a message to the user
    flash('You have been logged out!')
    #redirect to the login page
    return redirect(url_for('auth.login'))

#add a error handler for 429 errors (Rate Limiter on login route)
#this will be used to flash a message to the user when they hit the rate limit instead of rendering a basic html page
@view_auth.errorhandler(RateLimitExceeded)
def ratelimit_exceeded(e):
    #flash a message to the user
    flash('Too many login attempts. Please try again in 5 minutes', 'error')
    #redirect to the login page
    return redirect(url_for('auth.login'))