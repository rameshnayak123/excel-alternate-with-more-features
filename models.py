from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    pricing = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
