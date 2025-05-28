#routes.py will setup all routes for the web app and handle logic for using the database model

#imports
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Transaction
from . import db
from datetime import date

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
    #use date from datetime to handle time and date features
    #create a currentYear variable so that the checkbook page will always default to the current year
    #create a defaultMonth variable to use in the checkbook page so that the html date input will default to the selected month from dashboard.html
    currentYear = date.today().year
    defaultMonth = date(currentYear, month_id, 1).strftime('%Y-%m-%d')
    #add a task to the checkbook
    #make sure the method is "POST"
    if request.method == "POST":
        #get the data from the html form
        content = request.form['content']
        amount = request.form['amount']
        type = request.form['type']
        #create a new transaction object
        newTransaction = Transaction(content=content, amount=amount, type=type, month_id=month_id, year_id=1)
        #add the transaction to the database
        #try and except block to handle errors
        try:
            #connect to the db and add the transaction
            db.session.add(newTransaction)
            #commit the transaction to the db
            db.session.commit()
            #redirect the user to the checkbook page
            return redirect(url_for('view.checkbook', month_id=month_id))
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
        return render_template('checkbook.html', transactions=transactions, transactionType=transactionType, month_id=month_id, month_name=month_name, defaultMonth=defaultMonth, enumerate=enumerate)
    
#route to delete a transaction
@view.route('/checkbook/delete/<int:month_id>/<int:id>')
def delete(month_id:int, id:int):
    #query the transaction we need to delete
    deleteTransaction = Transaction.query.get_or_404(id)
    #try, except block to handle errors
    try:
        #connect to the db and delete the transaction
        db.session.delete(deleteTransaction)
        #commit the transaction to the db
        db.session.commit()
        #redirect the user to the checkbook page
        return redirect(url_for('view.checkbook', month_id=month_id))
    #ERROR
    except Exception as e:
        #return an ERROR and its error type
        return "ERROR:{}".format(e)
    
#route to edit a transaction
@view.route('/checkbook/edit/<int:month_id>/<int:id>', methods=["POST", "GET"])
def edit(month_id:int, id:int):
    #query the transaction we need to edit by the id
    transaction = Transaction.query.get_or_404(id)
    #check if the method is POST
    if request.method == "POST":
        #update the attributes fo the transaction
        transaction.content = request.form['content']
        transaction.amount = request.form['amount']
        transaction.type = request.form['type']
        #try, except block to handle errors
        try:
            #connect to the db and update the transaction
            db.session.commit()
            #redirect the user to the checkbook page
            return redirect(url_for('view.checkbook', month_id=month_id))
        #ERROR
        except Exception as e:
            #return an ERROR and its error type
            return "ERROR:{}".format(e)
    #otherwise we want to display a page where the user can edit their transaction
    else:
        #pass the transaction model to use its id in the edit.html page
        return render_template('edit.html', transaction=transaction, month_id=month_id)
