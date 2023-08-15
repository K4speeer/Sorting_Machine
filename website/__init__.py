# Import flask Module
from flask import Flask
# Import timedelta to set the server's session lifetime
from datetime import timedelta
# Import SQLAlchemy to manipulate with SQL database
from flask_sqlalchemy import SQLAlchemy

# Create_App function to initialize Flask application for further run 
def create_app():
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
    # Creating a database model for the project  
    class sessions(db.Model):
        _id = db.Column('id', db.Integer(), primary_key=True )
        dateTime = db.Column('SessionDate', db.DateTime(), nullable=False)
        total_objects = db.Column('ObjectsQuantity', db.Integer(), nullable=False)
        gate1_params = db.Column('gate1Params', db.String(25))
        gate2_params = db.Column('gate2Params', db.String(25))
        gate3_params = db.Column('gate3Params', db.String(25))
        gate1_objects = db.Column('gate1Objects', db.Integer())
        gate2_objects = db.Column('gate2Objects', db.Integer())
        gate3_objects = db.Column('gate3Objects', db.Integer())
        # Model initialization function 
        def __init__(self, dateTime, total_objects, gate1_params, gate2_params, gate3_params, gate1_objects, gate2_objects, gate3_objects):
            self.dateTime = dateTime
            self.total_objects = total_objects
            self.gate1_params = gate1_params
            self.gate2_params = gate2_params
            self.gate3_params = gate3_params
            self.gate1_objects = gate1_objects
            self.gate2_objects = gate2_objects
            self.gate3_objects = gate3_objects
    
    # Create the database file within the app context
    with app.app_context():
        db.create_all()
    
    # Import the views to the app
    from .views import views
    # Register all used Blueprints 
    app.register_blueprint(views, url_prefix="/")
    
    # Return the app Object to run it 
    return app
