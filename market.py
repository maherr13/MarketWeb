import sqlite3
from sqlite3 import Error


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

    for row in rows:
        print(row)

def select_product_by_name(conn, price):

    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE price=?", (price,))

    rows = cur.fetchall()

    for row in rows:
        print(row)
        

def main():   
    table = """ CREATE TABLE IF NOT EXISTS products (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        price integer
                                    ); """
    
    conn = create_connection(r"products.db")
    
    if conn is not None:
        create_tables(conn, table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        
        product1 = ('product three', 1000)
        product2 = ('product four', 2000)

        product_id = insert_product(conn, product1)
        product_id = insert_product(conn, product2)

        print("1. Query products by name:")
        select_product_by_name(conn, 2000)


        print("2. Query all products")
        select_all_products(conn)

if __name__ == '__main__':
    main()