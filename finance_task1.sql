-- Drop and recreate database
DROP DATABASE IF EXISTS finance_db;
CREATE DATABASE finance_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE finance_db;

-- Table: user
CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Table: account
CREATE TABLE account (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    balance DECIMAL(12,2) DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Table: category
CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('income', 'expense') NOT NULL
);

-- Table: transaction
CREATE TABLE transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_date DATE NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (account_id) REFERENCES account(account_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

-- Sample data

INSERT INTO user (first_name, last_name, email) VALUES
('Alice', 'Morgan', 'alice@example.com'),
('Bob', 'Lopez', 'bob@example.com'),
('Clara', 'Nguyen', 'clara@example.com');

INSERT INTO account (user_id, account_name, balance) VALUES
(1, 'Checking Account', 1500.00),
(1, 'Savings Account', 3000.00),
(2, 'Business Account', 5000.00),
(3, 'Personal Account', 2200.00);

INSERT INTO category (name, type) VALUES
('Salary', 'income'),
('Groceries', 'expense'),
('Rent', 'expense'),
('Utilities', 'expense'),
('Freelance', 'income'),
('Dining Out', 'expense');

INSERT INTO transaction (account_id, category_id, amount, transaction_date, description) VALUES
(1, 1, 2500.00, '2025-11-01', 'Monthly salary'),
(1, 2, -150.00, '2025-11-02', 'Supermarket shopping'),
(1, 3, -900.00, '2025-11-03', 'Monthly rent'),
(2, 5, 1200.00, '2025-11-04', 'Freelance project'),
(3, 4, -85.50, '2025-11-04', 'Electricity bill'),
(3, 6, -45.00, '2025-11-05', 'Dinner with friends');
