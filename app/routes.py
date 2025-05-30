#routes.py will setup all routes for the web app and handle logic for using the database model

#imports
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Transaction
from . import db
from datetime import date, datetime

#create the blueprint for the routes
view = Blueprint('view', __name__)

#create a global list of months for the dashboard
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

#create a global variable to hold the current year which will be used in dashboard and checkbook routes as a default value
CURRENT_YEAR = date.today().year

#route for the dashboard
@view.route('/', methods=["POST", "GET"])
def dashboard():
    #call the MONTHS and CURRENT_YEAR global variable
    global MONTHS, CURRENT_YEAR
    #default the year_id to the current year
    year_id = CURRENT_YEAR
    #check if the method is POST (aka we are getting data from the form)
    if request.method == "POST":
        #get the year from the form
        year_id = int(request.form['year']) #make sure the variable is an int
        #update the CURRENT_YEAR variable to the selected year
        CURRENT_YEAR = year_id
        #redirect the user back to the dashboard with the selected year
        return redirect(url_for('view.dashboard', year_id=year_id))
    #else we want to display the dashboard page
    else:
        #render the dashboard template and pass the months list and enumerate python function to the template
        return render_template('dashboard.html', months=MONTHS, current_year=CURRENT_YEAR, year_id=year_id, enumerate=enumerate)

#route for the main checkbook page
@view.route('/checkbook/<int:year_id>/<int:month_id>', methods=["POST", "GET"])
def checkbook(year_id:int, month_id:int):
    #use date from datetime to handle time and date features
    #create a default_month variable to use in the checkbook page so that the html date input will default to the selected month from dashboard.html
    default_month = date(year_id, month_id, 1).strftime('%Y-%m-%d')
    #add a task to the checkbook
    #make sure the method is "POST"
    if request.method == "POST":
        #get the data from the html form
        transaction_date_string = request.form['date'] #this gets the date as a string
        transaction_date_object = datetime.strptime(transaction_date_string, '%Y-%m-%d') #convert the string to a datetime object
        content = request.form['content']
        amount = request.form['amount']
        type = request.form['type']
        #create a new transaction object
        newTransaction = Transaction(date=transaction_date_object, content=content, amount=amount, type=type, year_id=year_id, month_id=month_id)
        #add the transaction to the database
        #try and except block to handle errors
        try:
            #connect to the db and add the transaction
            db.session.add(newTransaction)
            #commit the transaction to the db
            db.session.commit()
            #redirect the user to the checkbook page
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
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
        transactions = Transaction.query.filter_by(year_id=year_id, month_id=month_id).all()
        #define the transaction type as a seperate variable so we can format it on the web page
        transactionType = Transaction.type

        #return the rendered template and pass transactions to the html page
        return render_template('checkbook.html', transactions=transactions, transactionType=transactionType, year_id=year_id, month_id=month_id, month_name=month_name, default_month=default_month, enumerate=enumerate)
    
#route to delete a transaction
@view.route('/checkbook/delete/<int:year_id>/<int:month_id>/<int:id>')
def delete(year_id:int, month_id:int, id:int):
    #query the transaction we need to delete
    deleteTransaction = Transaction.query.get_or_404(id)
    #try, except block to handle errors
    try:
        #connect to the db and delete the transaction
        db.session.delete(deleteTransaction)
        #commit the transaction to the db
        db.session.commit()
        #redirect the user to the checkbook page
        return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
    #ERROR
    except Exception as e:
        #return an ERROR and its error type
        return "ERROR:{}".format(e)
    
#route to edit a transaction
@view.route('/checkbook/edit/<int:year_id>/<int:month_id>/<int:id>', methods=["POST", "GET"])
def edit(year_id:int, month_id:int, id:int):
    #query the transaction we need to edit by the id
    transaction = Transaction.query.get_or_404(id)
    #check if the method is POST
    if request.method == "POST":
        #update the attributes fo the transaction
        transaction_date_string = request.form['date'] #this gets the date as a string
        transaction_date_object = datetime.strptime(transaction_date_string, '%Y-%m-%d') #convert the string to a datetime object
        transaction.date = transaction_date_object #update the date
        transaction.content = request.form['content']
        transaction.amount = request.form['amount']
        transaction.type = request.form['type']
        #try, except block to handle errors
        try:
            #connect to the db and update the transaction
            db.session.commit()
            #redirect the user to the checkbook page
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
        #ERROR
        except Exception as e:
            #return an ERROR and its error type
            return "ERROR:{}".format(e)
    #otherwise we want to display a page where the user can edit their transaction
    else:
        #pass the transaction model to use its id in the edit.html page
        return render_template('edit.html', transaction=transaction, year_id=year_id, month_id=month_id)
