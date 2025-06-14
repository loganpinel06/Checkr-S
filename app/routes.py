#routes.py will setup all routes for the web app and handle logic for adding and retrieving data (transactions) from the database

#imports
#Core Flask imports
from flask import Blueprint, render_template, request, redirect, url_for
#flak-login for user authentication
from flask_login import login_required, current_user
#import the Transaction model from models.py
from .models import Transaction, Balance
#import the db object from __init__.py to connect to the database
from . import db 
#for handling date and time features
from datetime import date, datetime 

#create the blueprint for the routes
view = Blueprint('view', __name__)

#create a global list of months for the dashboard
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

#create a global variable SELECTED_YEAR which will be used in dashboard and checkbook routes to mark the selected year by the user
#this variable will be set to whatever the computers current year is by default until it is changed by the user in the yearSelector form on the dashboard
SELECTED_YEAR = date.today().year

#create a similar global variable to store the current year based on the computer's date just like SELECTED_YEAR but this variable will not be modified ever
#this variable will be used to set the max year in the yearSelector form on the dashboard as it doesnt make sense to allow users to select a year in the future
CURRENT_YEAR = date.today().year

#route for the dashboard
@view.route('/dashboard', methods=["POST", "GET"])
@login_required #require a user to be logged in to access the dashboard
def dashboard():
    #call the MONTHS, SELECTED_YEAR, and CURRENT_YEAR global variables
    global MONTHS, SELECTED_YEAR, CURRENT_YEAR
    #default the year_id to the current year
    year_id = SELECTED_YEAR
    #check if the method is POST (aka we are getting data from the form)
    if request.method == "POST":
        #get the year from the form
        year_id = int(request.form['year']) #make sure the variable is an int
        #update the SELECTED_YEAR variable to the selected year
        SELECTED_YEAR = year_id
        #redirect the user back to the dashboard with the selected year
        return redirect(url_for('view.dashboard', year_id=year_id))
    #else we want to display the dashboard page
    else:
        #render the dashboard template and pass the months list and enumerate python function to the template
        return render_template('main/dashboard.html', months=MONTHS, selected_year=SELECTED_YEAR, current_year=CURRENT_YEAR, year_id=year_id, enumerate=enumerate)

#route for the main checkbook page
@view.route('/checkbook/<int:year_id>/<int:month_id>', methods=["POST", "GET"])
@login_required #require a user to be logged in to access the checkbook
def checkbook(year_id:int, month_id:int):
    #use date from datetime to handle time and date features
    #create a default_month variable to use in the checkbook page so that the html date input will default to the selected month from dashboard.html
    default_month = date(year_id, month_id, 1).strftime('%Y-%m-%d')
    #add a task to the checkbook
    #make sure the method is "POST"
    if request.method == "POST":
        #check which form was submitted
        form_id = request.form.get('form_id')
        #if form_id is the starting balance form
        if form_id == 'balanceForm':
            #get the starting balance from the form
            balance = request.form['startingBalance']
            #create a new Balance object
            newBalance = Balance(user_id=current_user.id, year_id=year_id, month_id=month_id, balance=float(balance))
            #try and except block to handle errors
            try:
                #add and commit the new starting balance to the database
                db.session.add(newBalance)
                db.session.commit()
                #redirect the user to the checkbook page
                return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
            #ERROR
            except Exception as e:
                #return an ERROR and its error type
                return "ERROR:{}".format(e)
        #if the form_id is the reset balance form
        elif form_id == 'resetBalanceForm':
            #get the balance object from the Balance model
            balance_object = Balance.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).first()
            #try and except block to handle errors
            try:
                #delete the balance object if it exists
                if balance_object:
                    db.session.delete(balance_object)
                    db.session.commit()
                    #redirect the user to the checkbook page
                    return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
                else:
                    return "No balance to reset", 404
            #ERROR
            except Exception as e:
                #return an ERROR and its error type
                return "ERROR:{}".format(e)
        #if the form_id is the userInput form
        elif form_id == 'inputForm':
            #get the data from the html form
            transaction_date_string = request.form['date'] #this gets the date as a string
            transaction_date_object = datetime.strptime(transaction_date_string, '%Y-%m-%d') #convert the string to a datetime object
            content = request.form['content']
            amount = request.form['amount']
            type = request.form['type']

            #Handle balance logic
            #get the balance from the Balance model
            balance_object = Balance.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).first()
            #update the balance based on the transaction type and the amount
            if type == '+':
                #add the amount to the balance
                balance_object.balance += float(amount)
            elif type == '-':
                #subtract the amount from the balance
                balance_object.balance -= float(amount)

            #create a new transaction object
            #make sure to set the user_id to the current user id so that we can link the transaction to the user
            newTransaction = Transaction(date=transaction_date_object, content=content, amount=amount, type=type, year_id=year_id, month_id=month_id, user_id=current_user.id)
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
        #else return an error
        else:
            return "Invalid form submission"
    #else we want to display all transactions (GET method)
    else:
        #call the global MONTHS variable
        global MONTHS
        #get the name of the month based on its id so we can use the name when displaying the checkbook.html page
        month_name = MONTHS[month_id-1] #do -1 because we enumerated the months in the dashboard.html page starting at 1
        #query all transactions from the db based on the month_id
        #make sure to filter by the current users id so that we only get the transactions for the current user
        transactions = Transaction.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).all()
        #define the transaction type as a seperate variable so we can format it on the web page
        transactionType = Transaction.type 
        #get the balance from the Balance model
        balance_object = Balance.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).first()
        #return the rendered template and pass transactions to the html page
        return render_template('main/checkbook.html', transactions=transactions, transactionType=transactionType, year_id=year_id, month_id=month_id, month_name=month_name, default_month=default_month, enumerate=enumerate, balance=balance_object.balance if balance_object else None)
    
#route to delete a transaction
@view.route('/checkbook/delete/<int:year_id>/<int:month_id>/<int:id>')
@login_required #require a user to be logged in to access the delete route
def delete(year_id:int, month_id:int, id:int):
    #query the transaction we need to delete
    deleteTransaction = Transaction.query.get_or_404(id)
    #make sure the transaction belongs to the current user
    if deleteTransaction.user_id != current_user.id:
        return "Unauthorized", 403 #return a 403 error
    #try, except block to handle errors
    try:
        #update the balance for the deleted transaction
        #get the balance object from the model
        balance_object = Balance.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).first()
        #update the balance based on the transaction type and the amount
        #make sure to do the opposite operation because we are 'undoing' the transaction
        if deleteTransaction.type == '+':
            #add the amount to the balance
            balance_object.balance -= float(deleteTransaction.amount)
        elif deleteTransaction.type == '-':
            #subtract the amount from the balance
            balance_object.balance += float(deleteTransaction.amount)
        #delete the transaction from database
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
@login_required #require a user to be logged in to access the edit route
def edit(year_id:int, month_id:int, id:int):
    #query the transaction we need to edit by the id
    transaction = Transaction.query.get_or_404(id)
    #make sure the tranasction belongs to the current user
    if transaction.user_id != current_user.id:
        return "Unauthorized", 403
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
        return render_template('main/edit.html', transaction=transaction, year_id=year_id, month_id=month_id)
