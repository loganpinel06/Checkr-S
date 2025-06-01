#__init__.py initializes the app package to be used in main.py
#this script will setup the flask app and database, register the blueprints, and configure the app / database

#imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#initialize the database
db = SQLAlchemy()

#create a login manager for user authentication
login_manager = LoginManager()

#function to create the app and return it
def createApp():
    #create the app
    app = Flask(__name__)
    #configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable modification tracking for performance inhancement

    #secret key for the app (used for session management and CSRF protection)
    app.config['SECRET_KEY'] = 'secret_key' # change this to a secure key in production

    #initialize the database
    db.init_app(app)

    #initialize the login manager
    login_manager.init_app(app)

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
        #make sure the correct model is being imported
        from .models import Transaction
        #create the database
        db.create_all()

    #return the app
    return app

