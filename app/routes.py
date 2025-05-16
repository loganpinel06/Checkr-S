#routes.py will setup all routes for the web app and handle logic for using the database model

#imports
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Transaction
from . import db

#create the blueprint for the routes
view = Blueprint('view', __name__)

#create a global list of months for the dashboard
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

#route for the dashboard
@view.route('/')
def dashboard():
    #call the MONTHS global variable
    global MONTHS
    #render the dashboard template and pass the months list and enumerate python function to the template
    return render_template('dashboard.html', months=MONTHS, enumerate=enumerate)

#route for the main checkbook page
@view.route('/checkbook/<int:month_id>', methods=["POST", "GET"])
def checkbook(month_id:int):
    #add a task to the checkbook
    #make sure the method is "POST"
    if request.method == "POST":
        #get the data from the html form
        content = request.form['content']
        amount = request.form['amount']
        type = request.form['type']
        #create a new transaction object
        newTransaction = Transaction(content=content, amount=amount, type=type, month_id=month_id)
        #add the transaction to the database
        #try and except block to handle errors
        try:
            #connect to the db and add the transaction
            db.session.add(newTransaction)
            #commit the transaction to the db
            db.session.commit()
        except Exception as e:
            #return an ERROR and its error type
            return "ERROR:{}".format(e)
    #else we want to display all transactions
    else:
        #call the global MONTHS variable
        global MONTHS
        #get the name of the month based on its id so we can use the name when displaying the checkbook.html page
        month_name = MONTHS[month_id-1] #do -1 because we enumerated the months in the dashboard.html page starting at 1
        #query all transactions from the db based on the month_id
        transactions = Transaction.query.filter_by(month_id=month_id).all()
        #define the transaction type as a seperate variable so we can format it on the web page
        transactionType = Transaction.type
        #return the rendered template and pass transactions to the html page
        return render_template('checkbook.html', transactions=transactions, transactionType=transactionType, month_id=month_id, month_name=month_name)
    
#add a route to delete a transaction


