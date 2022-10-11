import sqlite3
from turtle import st
from flask import Flask, render_template, url_for, request, redirect, session, flash
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gnt07311;PWD=UhulCAYn7uydIC4p",'','')
print(conn)
print("connection successful...")


app = Flask(__name__)       #The variable __name__ is passed as first argument when creating an instance of the Flask object
'''app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'     #database initialization
db = SQLAlchemy(app) #object creation for DB'''

app.secret_key = "abc"

@app.route('/')
def index():
    return render_template('signUp.html')

@app.route('/signUp', methods = ['POST', 'GET']) 
def signUp():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user_type = "Admin"
        
        sql = "SELECT * FROM User WHERE FirstName = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, first_name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print("signup")
        if account:
            print("account")
            flash("You are already a member, Please login using your details")  
            return render_template('logIn.html', msg = "You are already a member, Please login using your details")
        else:
            insert_sql = "INSERT INTO User VALUES(?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, first_name)
            ibm_db.bind_param(prep_stmt, 2, last_name)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.bind_param(prep_stmt, 5, user_type)
            ibm_db.execute(prep_stmt)
            print("Inserted")
            flash("you are successfuly signed in")  
            return render_template('home.html')
    else:
        return render_template('logIn.html', msg = "You are already a member, Please login using your details")
        

@app.route('/logIn', methods = ['POST', 'GET'])
def logIn():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM User WHERE Email = ? AND Password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if(account):
            flash("You are successfuly logged in") 
            return render_template('home.html')
        else:
            flash("Email or password entered is incorrect") 
            return render_template('logIn.html', msg = "Incorrect email or password")
    else:
        return render_template('logIn.html', msg = "You are already a member, Please login using your details")


@app.route('/emp')
def emp():
    return render_template('emp.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutUs.html')

if __name__ == "__main__":
    app.run(debug=True)