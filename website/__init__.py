# Import flask Module
from flask import Flask
# Import timedelta to set the server's session lifetime
from datetime import timedelta
# Import SQLAlchemy to manipulate with SQL database
from flask_sqlalchemy import SQLAlchemy

# Create_App function to initialize Flask application for further run 
# Defining Flask Object 
app = Flask(__name__)
# Adding DB, Security and Session configurations 
app.config["SECRET_KEY"] = "mySecretKey" # Change the secret key 
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5) # Current session lifetime is 5 minutes
# You can change it to fit your needs

# SQL Database declartion
# Link you'r SQL DataBase with it's URI 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///SortingMachine.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Change it to True if you want to track modifications

# Defining Database Object
db = SQLAlchemy(app)

# Importing a database model from models.py file for the project  
from .models import sessions

def create_app(app=app, db=db):
    
    # Create the database file within the app context
    with app.app_context():
        db.create_all()
    
    # Import the views to the app
    from .views import views
    # Register all used Blueprints 
    app.register_blueprint(views, url_prefix="/")
    
    # Return the app Object to run it 
    return app
