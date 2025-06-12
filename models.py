from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Component(db.Model):
    __tablename__ = 'components'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    current_min = db.Column(db.Float)
    current_max = db.Column(db.Float)
    voltage_min = db.Column(db.Float)
    voltage_max = db.Column(db.Float)
    power = db.Column(db.String)
    capacitance_min = db.Column(db.Float)
    capacitance_max = db.Column(db.Float)
    tolerance = db.Column(db.String)
    datasheet_link = db.Column(db.String)
    notes = db.Column(db.String)
