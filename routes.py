import re
import datetime
import bcrypt
import json
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify, redirect,url_for,session, after_this_request
from app import app, db
from models import User

app.secret_key = 'RameshNayakyouneedtochange'
url_data = {}

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
    return render_template('hirenow.html')

@app.route('/generate-url', methods=['POST'])
def generate_url():
    # Get form data
    title = request.form['title']
    bond_years = request.form['bond_years']
    ctc = request.form['ctc']
    description = request.form['description']

    # Generate URL and store data
    url = f'{datetime.datetime.now().timestamp()}'
    url_data = {
        'title': title,
        'bond_years': bond_years,
        'ctc': ctc,
        'description': description,
        'timestamp': datetime.datetime.now().timestamp()
    }
    with open('data.json', 'a') as file:
        json.dump({url: url_data}, file)

    # Render result template with URL
    return render_template('hirenow.html', url=url)

@app.route('/register/<url_id>', methods=['GET', 'POST'])
def register(url_id):
    # Check if URL is valid and not expired
    url_info = get_url_data(url_id)
    if url_info is None:
        return 'Invalid URL'

    expiration_time = 3600  # 1 hour
    if datetime.datetime.now().timestamp() - url_info['timestamp'] > expiration_time:
        return 'URL has expired'

    # Handle form submissions
    if request.method == 'POST':
        # Process form data
        # ...

        # Render success template
        return render_template('success.html')

    # Render form template
    return render_template('form.html', url_id=url_id, title=url_info['title'], bond_years=url_info['bond_years'], ctc=url_info['ctc'], description=url_info['description'])

