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
        
    else:
        return render_template('logIn.html', msg = "You are already a member, Please login using your details")


@app.route('/aboutus')
def aboutus():
    return render_template('aboutUs.html')

@app.route('/supplier', methods = ['POST', 'GET'])
def supplier():
    if request.method == 'POST':
        invoice_no = request.form['invoice_no']
        supplier_name = request.form['supplier_name']
        contact = request.form['contact']
        description = request.form['description']

        sql = "SELECT * FROM Supplier WHERE InvoiceNo = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, invoice_no)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if(account):
            flash("") 
        else:
            insert_sql = "INSERT INTO Supplier VALUES(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, invoice_no)
            ibm_db.bind_param(prep_stmt, 2, supplier_name)
            ibm_db.bind_param(prep_stmt, 3, contact)
            ibm_db.bind_param(prep_stmt, 4, description)
            ibm_db.execute(prep_stmt)
            print("Inserted")
            flash("Supplier information added sucessfully")  
    return render_template('supplier.html')

@app.route('/category', methods = ['POST', 'GET'])
def category():
    if request.method == 'POST':
        category_name = request.form['category_name']

        sql = "SELECT * FROM Category WHERE Category = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, category_name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        
        if(not account):
            if request.form['btt'] == 'Add':
                insert_sql = "INSERT INTO Category VALUES(?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, category_name)
                ibm_db.execute(prep_stmt)
                print("Inserted")
                flash("Category information added successfully")
            elif request.form['btt'] == 'Delete':
                delete_sql = "DELETE FROM Category WHERE Category = ?"
                prep_stmt = ibm_db.prepare(conn, delete_sql)
                ibm_db.bind_param(prep_stmt, 1, category_name)
                ibm_db.execute(prep_stmt)
                flash("Category information deleted successfully")
        elif request.form['btt'] == 'Delete':
            delete_sql = "DELETE FROM Category WHERE Category = ?"
            prep_stmt = ibm_db.prepare(conn, delete_sql)
            ibm_db.bind_param(prep_stmt, 1, category_name)
            ibm_db.execute(prep_stmt)
            flash("Category information deleted successfully")
    return render_template('category.html')

@app.route('/product', methods = ['POST', 'GET'])
def product():
    sql = "SELECT * FROM Category"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    categ = []
    while dictionary != False:
        categ.append(dictionary[0])
        dictionary = ibm_db.fetch_both(stmt)
    
    supp_sql = "SELECT * FROM Supplier"
    stmt = ibm_db.exec_immediate(conn, supp_sql)
    dictionary = ibm_db.fetch_both(stmt)
    supp = []
    while dictionary != False:
        supp.append(dictionary[1])
        dictionary = ibm_db.fetch_both(stmt)

    if request.method == 'POST':
        prod_id = request.form['prod_id']
        cate = request.form['cate']
        supple = request.form['supple']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        st = request.form['st']

        if request.form['btt'] == 'Save':
            insert_sql = "INSERT INTO Product VALUES(?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, prod_id)
            ibm_db.bind_param(prep_stmt, 2, cate)
            ibm_db.bind_param(prep_stmt, 3, supple)
            ibm_db.bind_param(prep_stmt, 4, name)
            ibm_db.bind_param(prep_stmt, 5, price)
            ibm_db.bind_param(prep_stmt, 6, quantity)
            ibm_db.bind_param(prep_stmt, 7, st)
            ibm_db.execute(prep_stmt)
            print("Inserted")
            flash("Product information added successfully")
        elif request.form['btt'] == 'Update':
            update_sql = "UPDATE Product SET Category = ?, Supplier = ?, ProductName = ?, Price = ?, Quantity = ?, Status = ? WHERE ProductId = ?"
            prep_stmt = ibm_db.prepare(conn, update_sql)
            ibm_db.bind_param(prep_stmt, 1, cate)
            ibm_db.bind_param(prep_stmt, 2, supple)
            ibm_db.bind_param(prep_stmt, 3, name)
            ibm_db.bind_param(prep_stmt, 4, price)
            ibm_db.bind_param(prep_stmt, 5, quantity)
            ibm_db.bind_param(prep_stmt, 6, st)
            ibm_db.bind_param(prep_stmt, 7, prod_id)
            ibm_db.execute(prep_stmt)
            flash("Product information updated successfully")

    return render_template('product.html', supp = supp, categ = categ)

@app.route('/userSale', methods = ['POST', 'GET'])
def userSale():
    sales = []
    order_price = 0
    if request.method == 'POST':
        cust_id = request.form['cust_id']
        prod_id = request.form['prod_id']
        quantity = request.form['quantity']
        insert_sql = "INSERT INTO UserSales VALUES(?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, cust_id)
        ibm_db.bind_param(prep_stmt, 2, prod_id)
        ibm_db.bind_param(prep_stmt, 3, quantity)
        ibm_db.execute(prep_stmt)

        s_sql = "SELECT Quantity FROM Product WHERE ProductId = ?"
        s_stmt = ibm_db.prepare(conn, s_sql)
        ibm_db.bind_param(s_stmt, 1, prod_id)
        ibm_db.execute(s_stmt)
        s_dictionary = ibm_db.fetch_both(s_stmt)
        if(int(s_dictionary[0]) <= 0):
            flash("Product available: ")
        else:
            sql = "UPDATE Product SET Quantity = Quantity-? WHERE ProductId = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, int(quantity))
            ibm_db.bind_param(stmt, 2, prod_id)
            ibm_db.execute(stmt)


            p_sql = "SELECT Price, Quantity FROM Product WHERE ProductId = ?"
            stmt = ibm_db.prepare(conn, p_sql)
            ibm_db.bind_param(stmt, 1, prod_id)
            ibm_db.execute(stmt)
            dictionary = ibm_db.fetch_both(stmt)
            order_price = int(dictionary[0])*int(quantity)
            flash("Thank you for ordering. Your total price is Rs. ")

        sale_sql = "SELECT * FROM Product"
        stmt = ibm_db.exec_immediate(conn, sale_sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            sales.append(dictionary)
            dictionary = ibm_db.fetch_both(stmt)

    return render_template('userSale.html', sales = sales, order_price = order_price)

@app.route('/manage')
def manage():
    sale_sql = "SELECT * FROM Product"
    stmt = ibm_db.exec_immediate(conn, sale_sql)
    dictionary = ibm_db.fetch_both(stmt)
    sales = []
    while dictionary != False:
        sales.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    return render_template('manage.html', sales = sales) 

@app.route('/adminSale')
def adminSale():
    sale_sql = "SELECT * FROM UserSales"
    stmt = ibm_db.exec_immediate(conn, sale_sql)
    dictionary = ibm_db.fetch_both(stmt)
    sales = []
    while dictionary != False:
        sales.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    return render_template('adminSale.html', sales = sales)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8202)