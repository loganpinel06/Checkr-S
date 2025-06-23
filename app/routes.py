#routes.py will setup all routes for the checkbook app
#this file handles the following routes: dashboard, checkbook, delete, and edit
    #the dashboard route will display the dashboard page with a year selector form and a list of months as buttons to choose from
    #the checkbook route will display the checkbook page where users can enter their starting balance and log transactions for the selected month and year
    #the delete route will handle deleting a transaction from the checkbook
    #the edit route will handle editing a transaction from the checkbook
#this file uses Flask's Blueprint feature to create a modular structure for the app, ensures routes are require a user to be logged in to access them, logs
#any errors to a logger, use Flask-WTF forms for user input validation and CSRF protection, and lastly handles database interactions using SQLAlchemy.

#imports
#Core Flask imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
#flak-login for user authentication
from flask_login import login_required, current_user
#import the Transaction model from models.py
from .models import Transaction, Balance
#import the db object from __init__.py to connect to the database
from . import db, logger
#import the Flask-WTF forms from forms.py
from .forms import YearForm, StartingBalanceForm, ResetBalanceForm, UserInputForm, EditTransactionForm
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
    #create the YearForm instance
    form = YearForm()
    #call the MONTHS, SELECTED_YEAR, and CURRENT_YEAR global variables
    global MONTHS, SELECTED_YEAR, CURRENT_YEAR
    #default the year_id to the current year
    year_id = SELECTED_YEAR

    #check if the method is POST (call the form.validate_on_submit() method to check if the form is valid)
    if form.validate_on_submit():
        #get the year from the form
        year_id = int(form.year.data) #make sure the variable is an int
        #update the SELECTED_YEAR variable to the selected year
        SELECTED_YEAR = year_id
        #redirect the user back to the dashboard with the selected year
        return redirect(url_for('view.dashboard', year_id=year_id))
    #else we want to display the dashboard page
    else:
        #workaround for allowing the Flask-WTF form to auto select the SELECTED_YEAR in the select field
        #check if the method is GET and set the form data to the SELECTED_YEAR
        form.year.data = SELECTED_YEAR
        #render the dashboard template and pass the months list and enumerate python function to the template
        return render_template('main/dashboard.html', months=MONTHS, selected_year=SELECTED_YEAR, current_year=CURRENT_YEAR, year_id=year_id, enumerate=enumerate, form=form)

#route for the main checkbook page
@view.route('/checkbook/<int:year_id>/<int:month_id>', methods=["POST", "GET"])
@login_required #require a user to be logged in to access the checkbook
def checkbook(year_id:int, month_id:int):
    #create the form instance for the StartingBalanceForm, ResetBalanceForm, and UserInputForm
    starting_balance_form = StartingBalanceForm()
    reset_balance_form = ResetBalanceForm()
    user_input_form = UserInputForm()
    #use date from datetime to handle time and date features
    #create a default_month variable to use in the checkbook page so that the html date input will default to the selected month from dashboard.html
    default_month = date(year_id, month_id, 1).strftime('%Y-%m-%d')
    
    #update the default date value for the user_input_form
    user_input_form.date.data = datetime.strptime(default_month, '%Y-%m-%d') #convert the string to a datetime object
    
    #gather the forms hidden field value
    field_id = request.form.get('field_id')
    #check if the method is POST (call the form.validate_on_submit() method to check if the form is valid)
    #since we have multiple forms in this route we need to also check the submit fields data
    #STARTING BALANCE FORM
    if starting_balance_form.validate_on_submit() and field_id=="balanceForm":
        #get the starting balance from the form
        balance = starting_balance_form.starting_balance.data
        #create a new Balance object
        newBalance = Balance(user_id=current_user.id, year_id=year_id, month_id=month_id, starting_balance=float(balance), total_balance=float(balance))
        #try and except block to handle errors
        try:
            #add and commit the new starting balance to the database
            db.session.add(newBalance)
            db.session.commit()
            #redirect the user to the checkbook page
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
        #ERROR
        except Exception as e:
            #log the error to the logger
            logger.error(f"Error adding starting balance: {e}")
            #flash a message to let the user know there was an error and redirect back to the checkbook page
            flash("There was an error adding the starting balance, please try again")
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
    #RESET BALANCE FORM
    elif reset_balance_form.validate_on_submit() and field_id=="resetBalanceForm":
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
                #flash a message to let the user know there is no balance to reset
                flash("No balance to reset")
                return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
        #ERROR
        except Exception as e:
            #log the error to the logger
            logger.error(f"Error resetting balance: {e}")
            #flash a message to let the user know there was an error and redirect back to the checkbook page
            flash("There was an error resetting the balance, please try again")
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
    #USER INPUT FORM
    elif user_input_form.validate_on_submit() and field_id=="inputForm":
        #ENSURE THE STARTING BALANCE IS SET FIRST
        #get the balance object for flashing a message (OBJECT SHOULD BE NONE)
        balance_object = Balance.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).first()
        #if the object is None, we need to flash a message and redirect the user to the checkbook page
        if balance_object is None:
            flash("Please set a starting balance first.", "warning")
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
        #else there is a balance object so we can proceed with adding the transaction
        else:
            #get the data from the html form
            transaction_date_object = user_input_form.date.data #this gets the date, which is already a datetime object see line 74
            content = user_input_form.content.data
            amount = user_input_form.amount.data
            type = user_input_form.type.data
            #Handle balance logic
            #get the balance object from the Balance model
            balance_object = Balance.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).first()
            #update the total_balance based on the transaction type and the amount
            if type == '+':
                #add the amount to the balance
                balance_object.total_balance += float(amount)
            elif type == '-':
                #subtract the amount from the balance
                balance_object.total_balance -= float(amount)
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
                #log the error to the logger
                logger.error(f"Error adding transaction: {e}")
                #flash a message to let the user know there was an error and redirect back to the checkbook page
                flash("There was an error adding the transaction, please try again")
                return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
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
        return render_template('main/checkbook.html', transactions=transactions, transactionType=transactionType, year_id=year_id, month_id=month_id, month_name=month_name, default_month=default_month, enumerate=enumerate,
                               starting_balance=f"{balance_object.starting_balance:,.2f}" if balance_object else None, #balance variables
                               total_balance=f"{balance_object.total_balance:,.2f}" if balance_object else None, 
                               starting_balance_form=starting_balance_form, reset_balance_form=reset_balance_form, user_input_form=user_input_form) #FlaskForms
    
#route to delete a transaction
@view.route('/checkbook/delete/<int:year_id>/<int:month_id>/<int:id>')
@login_required #require a user to be logged in to access the delete route
def delete(year_id:int, month_id:int, id:int):
    #we need to have a balance_object in order to delete a transaction so we need to check if it exists
    #and if it doesn't exist, we need to flash a message and redirect the user to the checkbook page
    balance_object = Balance.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).first()
    if balance_object is None:
        flash("Please set a starting balance first.", "warning")
        return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
    #else we can proceed with deleting the transaction
    else:
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
                #subtract the amount to the total_balance
                balance_object.total_balance -= float(deleteTransaction.amount)
            elif deleteTransaction.type == '-':
                #add the amount from the total_balance
                balance_object.total_balance += float(deleteTransaction.amount)
            #delete the transaction from database
            #connect to the db and delete the transaction
            db.session.delete(deleteTransaction)
            #commit the transaction to the db
            db.session.commit()
            #redirect the user to the checkbook page
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
        #ERROR
        except Exception as e:
            #log the error to the logger
            logger.error(f"Error deleting transaction: {e}")
            #flash a message to let the user know there was an error and redirect back to the checkbook page
            flash("There was an error deleting the transaction, please try again")
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
    
#route to edit a transaction
@view.route('/checkbook/edit/<int:year_id>/<int:month_id>/<int:id>', methods=["POST", "GET"])
@login_required #require a user to be logged in to access the edit route
def edit(year_id:int, month_id:int, id:int):
    #create the UserInputForm instance
    form = EditTransactionForm()
    #query the transaction we need to edit by the id
    transaction = Transaction.query.get_or_404(id)
    #store the original amount in a variable for balance logic later
    original_amount = transaction.amount
    #store the original type incase it is changed (for balance logic later)
    original_type = transaction.type

    #make sure the tranasction belongs to the current user
    if transaction.user_id != current_user.id:
        return "Unauthorized", 403
    #check if the method is POST (call the form.validate_on_submit() method to check if the form is valid)
    if form.validate_on_submit():
        #update the attributes for the transaction
        transaction_date_object = form.date.data #this gets the date as a string
        transaction.date = transaction_date_object #update the date
        transaction.content = form.content.data
        transaction.amount = form.amount.data
        transaction.type = form.type.data

        #Handle balance logic
        #get the balance object from the Balance model
        balance_object = Balance.query.filter_by(year_id=year_id, month_id=month_id, user_id=current_user.id).first()
        #update the total_balance based on the transaction type and the amount
        if transaction.type == '+':
            #check if the type was changed from the original
            if transaction.type != original_type:
                #we need to add the original amount back to the balance
                balance_object.total_balance += float(original_amount)
            #else is only changing the amount
            else:
                #remove the original amount from the balance
                balance_object.total_balance -= float(original_amount)
            #add the NEW amount to the balance
            balance_object.total_balance += float(transaction.amount)
        elif transaction.type == '-':
            #check if the type was changed from the original
            if transaction.type != original_type:
                #we need to subtract the original amount back from the balance
                balance_object.total_balance -= float(original_amount)
            #else is only changing the amount
            else:
                #remove the original amount from the balance
                balance_object.total_balance += float(original_amount)
            #subtract the NEW amount from the balance
            balance_object.total_balance -= float(transaction.amount)

        #try, except block to handle errors
        try:
            #connect to the db and update the transaction
            db.session.commit()
            #redirect the user to the checkbook page
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
        #ERROR
        except Exception as e:
            #log the error to the logger
            logger.error(f"Error editing transaction: {e}")
            #flash a message to let the user know there was an error and redirect back to the checkbook page
            flash("There was an error editing the transaction, please try again")
            return redirect(url_for('view.checkbook', year_id=year_id, month_id=month_id))
    #otherwise we want to display a page where the user can edit their transaction
    else:
        #check if the method is GET so we can prepopulate the form with the transaction data
        if request.method == 'GET':
            #use the queried transaction to set default values for the form fields so the form will display the transactions original values
            form.date.data = transaction.date
            form.content.data = transaction.content
            form.amount.data = transaction.amount
            form.type.data = transaction.type
        #pass the transaction model to use its id in the edit.html page
        return render_template('main/edit.html', transaction=transaction, year_id=year_id, month_id=month_id, form=form)