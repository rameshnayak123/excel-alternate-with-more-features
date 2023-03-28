import re
import bcrypt
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify, redirect,url_for,session, after_this_request
from app import app, db
from models import User

app.secret_key = 'RameshNayakyouneedtochange'


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

# Set response headers to prevent caching
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

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
    # Store user information in session
    session['user_id'] = user.id
    session['logged_in'] = True

    # Redirect user to dashboard
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if not session.get('logged_in'):
        # Redirect user to index page if not logged in
        return redirect(url_for('index'))

    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    # Clear user information from session
    session.pop('logged_in', None)
    session.clear()

    # Redirect user to index page
    return redirect(url_for('index'))

@app.route('/home')
def home():
    return "hello world123"




@app.route('/hirenow')
def hirenow():
    return "hello world"
