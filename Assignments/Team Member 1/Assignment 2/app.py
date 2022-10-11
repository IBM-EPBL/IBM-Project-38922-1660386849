import sqlite3
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)       #The variable __name__ is passed as first argument when creating an instance of the Flask object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'     #database initialization
db = SQLAlchemy(app) #object creation for DB

@app.route('/') 
def index():
    return render_template('signUp.html')

@app.route('/login')
def login():
    return render_template('logIn.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/emp')
def emp():
    return render_template('emp.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutUs.html')

if __name__ == "__main__":
    app.run(debug=True)