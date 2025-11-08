import os
from mysql.connector import connect, Error
from dotenv import load_dotenv  # pip install python-dotenv

# Load .env file (DB_HOST, DB_PORT, DB_USER, etc.)
load_dotenv()


def connect_db():
    try:
        connection = connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            # change 3306 to 3307 here OR in .env if you're using mysql-finance on port 3307
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "nenorvalls"),
            password=os.getenv("DB_PASSWORD", "Goldencow2029*"),
            database=os.getenv("DB_NAME", "finance_db"),
        )
        return connection
    except Error as e:
        print("Connection error:", e)
        return None


def test_connection():
    """Simple health check: confirms Python <-> MySQL connection."""
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


# Show all transactions
def show_transactions():
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


# Add transaction
def add_transaction(account_id, category_id, amount, date, description):
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
        print("Transaction added.")
    except Error as e:
        print("Error adding transaction:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# Show account summary per user
def show_user_summary(user_id):
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
    # first check connection, then show transactions
    test_connection()
    show_transactions()
