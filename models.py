from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    marketer = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(20), default="user")

class Barname(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    waybill = db.Column(db.String(50))
    sender = db.Column(db.String(200))
    marketer = db.Column(db.String(200))
    weight = db.Column(db.Float)
    service = db.Column(db.String(100))
    upload_date = db.Column(db.String(50))
