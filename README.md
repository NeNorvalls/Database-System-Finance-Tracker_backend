# Database-System-Finance-Tracker_backend

## Tables:
- user – people who own accounts
- account – bank accounts or wallets per user
- category – expense/income categories
- transaction – money movements (deposits, expenses, transfers)

# 💰 Finance Database Design Documentation

## 📘 Overview
The **finance_db** database is designed to support a personal finance management system that tracks users, their accounts, income and expense categories, and all related transactions.  
It provides a structured way to record financial activities, view account balances, and categorize income and expenses.

The database is implemented in **MySQL 8**, running inside **Docker**, and is accessed through a **Python application** using the `mysql.connector` library.

---

## 🧱 Database Structure

### 1. Table: `user`
Stores information about each registered user.

| Column Name | Data Type | Constraints | Description |
|--------------|------------|-------------|--------------|
| `user_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each user |
| `first_name` | VARCHAR(50) | NOT NULL | User’s first name |
| `last_name` | VARCHAR(50) | NOT NULL | User’s last name |
| `email` | VARCHAR(100) | UNIQUE, NOT NULL | User’s email address |

**Purpose:**  
Keeps track of all users registered in the finance system.

---

### 2. Table: `account`
Stores user accounts, each belonging to a specific user.

| Column Name | Data Type | Constraints | Description |
|--------------|------------|-------------|--------------|
| `account_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each account |
| `user_id` | INT | FOREIGN KEY → `user(user_id)` | Links each account to its owner |
| `account_name` | VARCHAR(100) | NOT NULL | Name of the account (e.g., “Savings Account”) |
| `balance` | DECIMAL(12,2) | DEFAULT 0 | Current balance of the account |

**Purpose:**  
Allows each user to manage multiple financial accounts.

---

### 3. Table: `category`
Defines categories for transactions, used for budgeting and analysis.

| Column Name | Data Type | Constraints | Description |
|--------------|------------|-------------|--------------|
| `category_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique ID for each category |
| `name` | VARCHAR(100) | NOT NULL | Category name (e.g., “Salary”, “Rent”) |
| `type` | ENUM('income', 'expense') | NOT NULL | Indicates if the category adds or subtracts funds |

**Purpose:**  
Categorizes all income and expense transactions for reporting and insights.

---

### 4. Table: `transaction`
Records all account transactions with category and user linkage.

| Column Name | Data Type | Constraints | Description |
|--------------|------------|-------------|--------------|
| `transaction_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique transaction record |
| `account_id` | INT | FOREIGN KEY → `account(account_id)` | Links the transaction to an account |
| `category_id` | INT | FOREIGN KEY → `category(category_id)` | Defines whether the transaction is income or expense |
| `amount` | DECIMAL(12,2) | NOT NULL | Transaction amount |
| `transaction_date` | DATE | NOT NULL | Date of the transaction |
| `description` | VARCHAR(255) | NULL | Optional description of the transaction |

**Purpose:**  
Logs all financial activities — income, expenses, transfers, etc.

---

## 🔑 Primary Keys and Foreign Keys

| Table | Primary Key | Foreign Keys |
|--------|--------------|--------------|
| `user` | `user_id` | — |
| `account` | `account_id` | `user_id` → `user(user_id)` |
| `category` | `category_id` | — |
| `transaction` | `transaction_id` | `account_id` → `account(account_id)`<br>`category_id` → `category(category_id)` |

**Explanation:**  
Foreign keys create relationships between tables, maintaining **referential integrity**:
- Every account must belong to a valid user.  
- Every transaction must refer to a valid account and category.  
If a referenced record is deleted, MySQL prevents orphan records, ensuring data consistency.

---

## ⚙️ Constraints Used and Their Importance

| Constraint | Usage | Purpose |
|-------------|--------|----------|
| `PRIMARY KEY` | Uniquely identifies each record in a table | Ensures each row is distinct |
| `FOREIGN KEY` | Links tables (`account → user`, `transaction → account`) | Enforces referential integrity |
| `AUTO_INCREMENT` | Automatically generates IDs | Simplifies inserting new records |
| `NOT NULL` | Ensures critical fields are always filled | Prevents incomplete data |
| `UNIQUE` | Ensures no duplicate emails | Maintains data integrity for user info |
| `ENUM` | Restricts values to ‘income’ or ‘expense’ | Enforces valid category types |
| `DEFAULT` | Sets automatic initial values | Prevents missing balances on new accounts |

---

## 🧩 Example Relationships (ERD Summary)

**Relationships:**
- **One User → Many Accounts**
- **One Account → Many Transactions**
- **One Category → Many Transactions**

Diagram example (can be drawn in Draw.io):

```
USER (1) ───< ACCOUNT (∞)
ACCOUNT (1) ───< TRANSACTION (∞)
CATEGORY (1) ───< TRANSACTION (∞)
```

---

## 📊 Example Data

| User | Account | Category | Amount | Date | Description |
|------|----------|-----------|---------|------|-------------|
| Alice Morgan | Checking Account | Salary | +2500.00 | 2025-11-01 | Monthly salary |
| Alice Morgan | Checking Account | Groceries | -150.00 | 2025-11-02 | Supermarket shopping |
| Bob Lopez | Business Account | Freelance | +1200.00 | 2025-11-04 | Freelance project |
| Clara Nguyen | Personal Account | Utilities | -85.50 | 2025-11-04 | Electricity bill |

---

## 🧠 Why This Design Works
This database maintains:
- **Referential integrity** between linked tables (users → accounts → transactions).  
- **Data integrity** through proper constraints and validation rules.  
- **Flexibility** to expand with new tables (like budgets or recurring payments).  
- **Separation of concerns** — each table has a clear and unique purpose.

---

## 🧩 Technical Notes
- **Engine:** MySQL 8.0  
- **Encoding:** UTF8MB4 (for full Unicode support, including emojis 💸)  
- **Environment:** Dockerized MySQL accessible on port 3307  
- **Python Connection:** via `mysql.connector` and `.env` configuration  

### Example `.env`:
```env
DB_HOST=127.0.0.1
DB_PORT=3307
DB_USER=nenorvalls
DB_PASSWORD=Goldencow2029*
DB_NAME=finance_db

✅ Summary

The finance_db system demonstrates a well-structured relational model for managing financial transactions.
It enforces integrity, supports scalability, and integrates seamlessly with Python and Docker for modern application development.
