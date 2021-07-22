from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route("/sname", methods = ["POST"])
def search_name():
    name = request.form.get("search_name")
    conn = create_connection(r"products.db")
    items = select_product_by_name(conn, name)
    print(items)
    return render_template("sname.html", items = items)

@app.route("/sprice", methods = ["POST"])
def search_price():
    price = request.form.get("search_price")
    conn = create_connection(r"products.db")
    items = select_product_by_price(conn, price)
    return render_template("sprice.html", items = items)

@app.route("/view")
def view():
    conn = create_connection(r"products.db")
    items= select_all_products(conn)
    print(items)
    return render_template("viewall.html", items = items)

@app.route("/insert", methods=["POST"])
def insert():
    name = request.form.get("name")
    price = request.form.get("price")
    conn = create_connection(r"products.db")
    insert_product(conn, (name, price))
    return render_template("home.html")


@app.route("/", methods=["GET"])
def home():
    
    table = """ CREATE TABLE IF NOT EXISTS products (
                                    id integer PRIMARY KEY,
                                    name text,
                                    price integer
                                ); """

    conn = create_connection(r"products.db")
    
    if conn is not None:
        create_tables(conn, table)
    else:
        print("Error! cannot create the database connection.")

        

    
    return render_template("home.html")


def create_connection(db_file):
    conn = None

    try:
        conn=sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        if conn:
            conn.close()

def create_tables(conn, table):
    try:
        c = conn.cursor()
        c.execute(table)
    except Error as e:
        print(e)

def insert_product(conn, product):
    sql = """ INSERT INTO products(name,price)
              VALUES(?,?) """

    cur = conn.cursor()
    cur.execute(sql, product)
    conn.commit()
    return cur.lastrowid

def select_all_products(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")

    rows = cur.fetchall()

    return rows

def select_product_by_price(conn, price):

    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE price=?", (price,))

    rows = cur.fetchall()

    return rows

def select_product_by_name(conn, name):

    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE name=?", (name,))

    rows = cur.fetchall()

    return rows
        


if __name__ == '__main__':
    app.run(debug=True)
 
