#__init__.py initializes the app package to be used in main.py
#this script will setup the flask app, database, login manager for auth, limiter for rate limiting, and a 
#logger for logging errors server side or to Renders console in deployment.
#this script also register the blueprints for the apps routes, and configure the app to connect to a Supabase
#PostgreSQL database, and adding session / cookie security features.

#IMPORTS
#import flask
from flask import Flask
#import flask_sqlalchemy for database management
from flask_sqlalchemy import SQLAlchemy
#import flask_login for user authentication
from flask_login import LoginManager
#import flask_limiter for rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#import os and dotenv to load environment variables
import os
from dotenv import load_dotenv
#import logging for logging errors to a .log file
import logging
#from logging.handlers import RotatingFileHandler #!!UNCOMMENT THIS LINE IF RUNNING LOCALLY AND HAVE READ COMMENT ON LINE 46!!
#import sys for logging errors to the console for Render deployment
import sys
#import datetime for session lifetime management
from datetime import timedelta

#load environment variables from .env file
load_dotenv()

#initialize the database
db = SQLAlchemy()

#create a login manager for user authentication
login_manager = LoginManager()
#customize the message displayed when a user tries to access a protected route without being logged in
login_manager.login_message = "Invalid Session. Please log in to continue."

#setup the logger for the app
logger = logging.getLogger('app_logger') #create a logger for the app
logger.setLevel(logging.ERROR) #set the logging level to ERROR

#setu a formatter for the log messages
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') #set the format for the log messages

#!!UNCOMMENT LINES 47-53 IF RUNNING LOCALLY AND WANT ERRORS LOGGED TO A FILE!!
##setup a rotating file handler to log errors to a file
##FOR LOCAL DEVELOPMENT
#file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=2) #Max file size = 10KB, and keeps 2 backups before deleting logs
#file_handler.setLevel(logging.ERROR) #set the handler level to ERROR
#file_handler.setFormatter(log_formatter)
##add the handler to the app's logger
#logger.addHandler(file_handler)

#SETUPT A StreamHadnler to log errors to the console
#THIS IS NEEDED FOR DEPLOYMENT ON REDNER
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.ERROR) #set the handler level to ERROR
stream_handler.setFormatter(log_formatter) #set the format for the log messages
#add the handler to the app's logger
logger.addHandler(stream_handler)

#setup the rate limiter for the app
#we will use deferred initialization here so we can modularize the app and import the limiter into the auth route
#the limiter wll be bound to the app in the createApp function just like the db and login_manager
limiter = Limiter(key_func=get_remote_address, 
                  storage_uri=os.getenv('REDIS_URI')) #connect to Upstash Redis to store rate limiting data in-memory

#function to create the app and return it
def createApp():
    #create the app
    app = Flask(__name__)
    #configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SUPABASE_CONNECTION_STRING') #use the environment variable for the database connection string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable modification tracking for performance inhancement

    #add session and cookie security
    app.config['SESSION_COOKIE_SECURE'] = True #Ensure cookies are only sent over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True #Prevent XSS attacks by making cookies inaccessible to JavaScript
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' #Help prevent CSRF attacks

    #configure a Session Lifetime
    #sessions will expire after 30 minutes of inactivity
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    #secret key for the app (used for session management and CSRF protection)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    #initialize the database
    db.init_app(app)

    #initialize the login manager
    login_manager.init_app(app)
    
    #initialize the rate limiter
    limiter.init_app(app)

    #set the login view for the login manager
    login_manager.login_view = 'auth.login' 

    #register the routes blueprint
    from .routes import view
    app.register_blueprint(view)

    #register the auth blueprint
    from .auth import view_auth
    app.register_blueprint(view_auth)

    #create the database using a context manager
    with app.app_context():
        #create the database
        db.create_all()

    #return the app
    return app

