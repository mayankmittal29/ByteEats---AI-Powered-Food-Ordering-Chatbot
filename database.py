import sqlite3

# Connect or create a database
conn = sqlite3.connect("Food_chatbot.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS food_items (
    item_id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS order_tracking (
    order_id INTEGER PRIMARY KEY,
    status TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (item_id) REFERENCES food_items (item_id)
)
''')

# Insert data into food_items
cursor.executemany('''
INSERT INTO food_items (item_id, name, price)
VALUES (?, ?, ?)
''', [
    (1, 'Pav Bhaji', 6.00),
    (2, 'Chole Bhature', 7.00),
    (3, 'Pizza', 8.00),
    (4, 'Mango Lassi', 5.00),
    (5, 'Masala Dosa', 6.00),
    (6, 'Vegetable Biryani', 9.00),
    (7, 'Vada Pav', 4.00),
    (8, 'Rava Dosa', 7.00),
    (9, 'Samosa', 5.00),
])

# Insert data into order_tracking
cursor.executemany('''
INSERT INTO order_tracking (order_id, status)
VALUES (?, ?)
''', [
    (40, 'delivered'),
    (41, 'in transit'),
])

# Insert data into orders
cursor.executemany('''
INSERT INTO orders (order_id, item_id, quantity, total_price)
VALUES (?, ?, ?, ?)
''', [
    (40, 1, 2, 12.00),
    (40, 3, 1, 8.00),
    (41, 4, 3, 15.00),
    (41, 6, 2, 18.00),
    (41, 9, 4, 20.00),
])

# Commit and close
conn.commit()
conn.close()

print("Database and tables created successfully!")
