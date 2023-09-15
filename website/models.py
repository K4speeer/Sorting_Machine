from . import db

class sessions(db.Model):
        _id = db.Column('id', db.Integer(), primary_key=True )
        dateTime = db.Column('SessionDate', db.DateTime(), nullable=False)
        start_time = db.Column('sessionStartTime', db.String(10), nullable=False)
        end_time = db.Column('sessionEndTime', db.String(10), nullable=False)
        total_objects = db.Column('ObjectsQuantity', db.Integer(), nullable=False)
        general_parameter = db.Column('generalParameter', db.String(10), nullable=False)
        gate1_params = db.Column('gate1Params', db.String(25))
        gate1_objects = db.Column('gate1Objects', db.Integer())
        gate2_params = db.Column('gate2Params', db.String(25))
        gate2_objects = db.Column('gate2Objects', db.Integer())
        gate3_params = db.Column('gate3Params', db.String(25))
        gate3_objects = db.Column('gate3Objects', db.Integer())
        # Model initialization function 
        def __init__(self, dateTime, total_objects,start_time, end_time, general_parameter, gate1_params, gate2_params, gate3_params, gate1_objects, gate2_objects, gate3_objects):
            self.dateTime = dateTime
            self.start_time = start_time
            self.end_time = end_time
            self.total_objects = total_objects
            self.general_parameter = general_parameter
            self.gate1_params = gate1_params
            self.gate1_objects = gate1_objects
            self.gate2_params = gate2_params
            self.gate2_objects = gate2_objects
            self.gate3_params = gate3_params
            self.gate3_objects = gate3_objects
            
        