#models.py will setup the main model for the apps Transactions

#imports
from . import db
from datetime import datetime
#import flask_login to create a User model for authentication
from flask_login import UserMixin
#import generate_password_hash and check_password_hash from werkzeug.security to hash passwords for security and check passwords during login
from werkzeug.security import generate_password_hash, check_password_hash

#create the User model
#this model will be used to store the users information in the database
#it will have the following fields:
#id: the id of the user
#username: the username of the user
#password_hash: the hashed password of the user
#joined_date: the date the user joined the app
class User(UserMixin, db.Model):
    #id field
    id = db.Column(db.Integer, primary_key=True)
    #username field
    username = db.Column(db.String(50), unique=True, nullable=False)
    #password field
    password_hash = db.Column(db.String(150), nullable=False)
    #joined_date field
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    #define a relationship to the Transaction model
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    #override the __repr__ method to return a string representation of the object's id
    def __repr__(self):
        #show the user id
        return "User {}".format(self.id)
    
    #create a method to set the password hash
    def set_password(self, password):
        #hash the password
        self.password_hash = generate_password_hash(password)

    #create a method to check the password hash against a password provided at login
    def check_password(self, password):
        #check the password hash against the password provided
        return check_password_hash(self.password_hash, password)

#create the Transaction model
#this model will be used to store the transactions in the database
#it will have the following fields:
#year_id: the id of the year for the transaction
#month_id: the id of the month for the transaction
#id: the id of the transaction
#content: the description of the transaction
#amount: the amount of the transaction
#type: the type of the transaction (income or expense) (measured by user input of + or -)
#date: the date of the transaction
class Transaction(db.Model):
    #create a user_id foreign key to link transactions to a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #year_id field
    year_id = db.Column(db.Integer, nullable=False)
    #month_id field
    month_id = db.Column(db.Integer, nullable=False)
    #id field
    id = db.Column(db.Integer, primary_key=True)
    #content field
    content = db.Column(db.String(100), nullable=False)
    #amount field
    amount = db.Column(db.Integer, nullable=False)
    #type field
    type = db.Column(db.String(1), nullable=False)
    #date field
    date = db.Column(db.DateTime, default=datetime.utcnow)

    #override the __repr__ method to return a string representation of the object's id
    def __repr__(self):
        #show the task id
        return "Task {}".format(self.id)

    #create a method to format transactions to have a $
    @property   #allow this method to be used as a property and called on the object
    def formatAmount(self):
        return "${}".format(self.amount)