import sqlite3
from turtle import st
from flask import Flask, render_template, url_for, request, redirect, session, flash
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gnt07311;PWD=UhulCAYn7uydIC4p",'','')
print(conn)
print("connection successful...")

order_price = 0

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
        user_type = "Customer"
        
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
            flash("You are successfully Registered")  
            return render_template('logIn.html')
    else:
        return render_template('logIn.html', msg = "You are already a member, Please login using your details")
        

@app.route('/logIn', methods = ['POST', 'GET'])
def logIn():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if(email == "admin@gmail.com"):
            if(password == "12345"):
                cat_sql = "SELECT COUNT(*) FROM Category"
                stmt = ibm_db.exec_immediate(conn, cat_sql)
                catcount = ibm_db.fetch_both(stmt)
                categ = catcount[0]
                supp_sql = "SELECT COUNT(*) FROM Supplier"
                stmt1 = ibm_db.exec_immediate(conn, supp_sql)
                suppcount = ibm_db.fetch_both(stmt1)
                supple = suppcount[0]
                prod_sql = "SELECT COUNT(*) FROM Product"
                stmt2 = ibm_db.exec_immediate(conn, prod_sql)
                prodcount = ibm_db.fetch_both(stmt2)
                prod = prodcount[0]
                sales_sql = "SELECT COUNT(*) FROM UserSales"
                stmt3 = ibm_db.exec_immediate(conn, sales_sql)
                salescount = ibm_db.fetch_both(stmt3)
                sales = salescount[0]
                return render_template('home.html', categ = categ, supple = supple, prod = prod, sales = sales)
        sql = "SELECT * FROM User WHERE Email = ? AND Password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if(account):
            # flash("You are successfuly logged in") 
            sale_sql = "SELECT * FROM Product"
            stmt = ibm_db.exec_immediate(conn, sale_sql)
            dictionary = ibm_db.fetch_both(stmt)
            sales = []
            while dictionary != False:
                sales.append(dictionary)
                dictionary = ibm_db.fetch_both(stmt)

            return render_template('userSale.html', sales = sales)
        else:
            flash("Email or password entered is incorrect") 
            return render_template('logIn.html', msg = "Incorrect email or password")
    else:
        return render_template('logIn.html', msg = "You are already a member, Please login using your details")





if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8202)