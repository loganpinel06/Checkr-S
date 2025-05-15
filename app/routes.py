#routes.py will setup all routes for the web app and handle logic for using the database model

#imports
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Transaction
from . import db

#create the blueprint for the routes
view = Blueprint('view', __name__)

