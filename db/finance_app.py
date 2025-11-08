import os
from mysql.connector import connect, Error
from dotenv import load_dotenv  # pip install python-dotenv

# Load environment variables from .env file
load_dotenv()


def connect_db():
    """
    Establishes a connection to the MySQL database using environment variables.
    Sensitive credentials (username/password) are NOT stored directly in this file.
    """
    try:
        connection = connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", 3306)),  # can be 3307 if using a separate Docker container
            user=os.getenv("DB_USER"),             # pulled from .env
            password=os.getenv("DB_PASSWORD"),     # pulled from .env
            database=os.getenv("DB_NAME", "finance_db"),
        )
        return connection
    except Error as e:
        print("Connection error:", e)
        return None


def test_connection():
    """Checks that Python can connect to the database and prints DB + version info."""
    conn = connect_db()
    if not conn:
        print("❌ Python could NOT connect to MySQL.")
        return

    cur = conn.cursor()
    cur.execute("SELECT DATABASE(), VERSION();")
    db_name, version = cur.fetchone()
    print("✅ Python is connected!")
    print(f"Current database: {db_name}")
    print(f"MySQL version: {version}")
    cur.close()
    conn.close()


def show_transactions():
    """Displays all transactions in the database."""
    conn = connect_db()
    if not conn:
        return

    cur = conn.cursor()
    cur.execute("""
        SELECT t.transaction_id,
               u.first_name,
               u.last_name,
               c.name,
               t.amount,
               t.transaction_date
        FROM `transaction` t
        JOIN account a ON t.account_id = a.account_id
        JOIN `user` u ON a.user_id = u.user_id
        JOIN category c ON t.category_id = c.category_id
        ORDER BY t.transaction_date DESC
    """)
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def add_transaction(account_id, category_id, amount, date, description):
    """Adds a new transaction to the database."""
    conn = connect_db()
    if not conn:
        return

    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO `transaction` (account_id, category_id, amount, transaction_date, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (account_id, category_id, amount, date, description))
        conn.commit()
        print("✅ Transaction added.")
    except Error as e:
        print("Error adding transaction:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def show_user_summary(user_id):
    """Displays account summary and balance for a given user."""
    conn = connect_db()
    if not conn:
        return

    cur = conn.cursor()
    cur.execute("""
        SELECT u.first_name, u.last_name, a.account_name, a.balance
        FROM account a
        JOIN `user` u ON u.user_id = a.user_id
        WHERE u.user_id = %s
    """, (user_id,))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    # Optional test on startup
    test_connection()
    show_transactions()
