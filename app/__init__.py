
__author__ = "Mohiuddin Shovon"
__date__ = "30 th July,2022"
__email__ = "shovon.du86@gmail.com"

# Import flask
from flask import Flask,make_response,jsonify
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# Import CORS
from flask_cors import CORS,cross_origin
#Import os For File Manipulations like get paths, rename
import os
# Define the WSGI application object
app = Flask(__name__,static_folder='static')

#CORS Enabled 
CORS(app)

#Get Path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

# Configurations
app.config.from_object('config')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #It will allow below 50MB contents only
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

#app.register_blueprint(blueprint)
# Import a module / component using its blueprint handler variable (mod_da)

from app.mod_da.controllers import mod_da as da_module
app.register_blueprint(da_module)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()


# Sample HTTP error handling
@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)
