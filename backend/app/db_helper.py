import sqlite3

DB_PATH = "Food_chatbot.db"

def get_order_status(order_id: str):
    """Fetches the status of an order from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT status FROM order_tracking WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()

def get_next_order_id():
    """Fetch the next available order ID from the orders table."""
    conn = sqlite3.connect("Food_chatbot.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(order_id) FROM orders")
    result = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return 1 if result is None else result + 1

def fetch_food_item_id(food_item):
    """Fetch the item ID of a given food item."""
    conn = sqlite3.connect("Food_chatbot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT item_id FROM food_items WHERE name = ?", (food_item,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else None

def get_total_order_price(order_id):
    """Calculate total price for an order."""
    conn = sqlite3.connect("Food_chatbot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(total_price) FROM orders WHERE order_id = ?", (order_id,))
    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result if result else 0

def insert_order_item(order_id, food_id, quantity, total_price):
    """Insert an order item into the orders table."""
    conn = sqlite3.connect("Food_chatbot.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO orders (order_id, item_id, quantity, total_price) VALUES (?, ?, ?, ?)",
            (order_id, food_id, quantity, total_price),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting order item: {e}")
    finally:
        cursor.close()
        conn.close()

def insert_order_tracking(order_id, status="progress"):
    """Insert order tracking status."""
    conn = sqlite3.connect("Food_chatbot.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO order_tracking (order_id, status) VALUES (?, ?)", (order_id, status))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting order tracking: {e}")
    finally:
        cursor.close()
        conn.close()