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