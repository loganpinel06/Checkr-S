#models.py will setup the main model for the apps Transactions

#imports
from . import db
from datetime import datetime

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