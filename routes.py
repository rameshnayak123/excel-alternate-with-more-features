import re
import bcrypt
from flask import Flask, request, render_template, jsonify
from app import app, db
from models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    organization = request.form['organization']
    company = request.form['company']
    fullname = request.form['fullname']
    pricing = request.form['pricing']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'Email address already exists'}), 409

    if len(password) < 8 or not re.search("[!@#$%^&*()_+-=\[\]{};':\"\\|,.<>/?]", password):
        return "Make sure your password is at least 8 characters long and contains at least one special character."
    elif password != confirm:
        return "Password and confirm password do not match."
    else:
        # Generate a salt
        salt = bcrypt.gensalt()

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        new_user = User(organization=organization, company=company, fullname=fullname, pricing=pricing, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    return 'User created successfully!'

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user is None:
        return 'User not found'

    # Verify password hash
    if not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return 'Incorrect password'

    # Login successful
    # Store user information in session or generate a JWT token
    # Redirect user to dashboard
    return 'Login successful'

