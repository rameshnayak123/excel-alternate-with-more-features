from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Define the Organization model
class Organization(db.Model):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    companies = relationship('Company', backref='organization', lazy=True)

# Define the Company model
class Company(db.Model):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    name = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    pricing_option = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

# Define a function to save the password in md5 format
def save_password(password):
    md5_password = hashlib.md5(password.encode())
    return md5_password.hexdigest()
