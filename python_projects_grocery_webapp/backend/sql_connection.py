import sqlite3
import os
from flask import g

def get_sql_connection():
    if 'db' not in g:
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(os.path.abspath(__file__)) + '/db'
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        db_path = db_dir + '/grocery_store.db'
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        
        # Create tables if they don't exist
        create_tables(g.db)
        
        # Insert initial data if needed
        insert_initial_data(g.db)
        
    return g.db

def create_tables(connection):
    cursor = connection.cursor()
    
    # Create UOM table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uom (
            uom_id INTEGER PRIMARY KEY AUTOINCREMENT,
            uom_name TEXT NOT NULL
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            uom_id INTEGER,
            price_per_unit REAL,
            FOREIGN KEY (uom_id) REFERENCES uom (uom_id)
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            total REAL,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create order_details table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_details (
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    connection.commit()

def close_connection():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def insert_initial_data(connection):
    cursor = connection.cursor()
    
    # Check if UOM table is empty
    cursor.execute('SELECT COUNT(*) FROM uom')
    if cursor.fetchone()[0] == 0:
        # Insert initial UOM data
        cursor.execute('''
            INSERT INTO uom (uom_name) VALUES 
            ('KG'),
            ('L'),
            ('Units'),
            ('Packs')
        ''')
        connection.commit()
    
    # Check if products table is empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        # Insert sample products
        cursor.execute('''
            INSERT INTO products (name, uom_id, price_per_unit) VALUES 
            ('Rice', 1, 50.00),
            ('Milk', 2, 30.00),
            ('Bread', 3, 15.00)
        ''')
        connection.commit()

