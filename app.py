from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    pricing = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

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

    new_user = User(organization=organization, company=company, fullname=fullname, pricing=pricing, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return 'User created successfully!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5050)
