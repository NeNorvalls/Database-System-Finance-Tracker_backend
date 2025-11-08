-- 1. List all transactions after November 1st, 2025
SELECT * FROM transaction WHERE transaction_date > '2025-11-01';

-- 2. List all users alphabetically
SELECT first_name, last_name, email FROM user ORDER BY last_name;

-- 3. Find all expenses over 100
SELECT * FROM transaction WHERE amount < -100;

-- 4. Add a new user
INSERT INTO user (first_name, last_name, email)
VALUES ('David', 'Kim', 'david@example.com');

-- 5. Add a new account for David
INSERT INTO account (user_id, account_name, balance)
VALUES (4, 'Vacation Fund', 200.00);

-- 6. Update account balance for Alice’s Checking Account
UPDATE account
SET balance = balance + 500
WHERE account_id = 1;

-- 7. Show all transactions with user and category
SELECT t.transaction_id, u.first_name, u.last_name,
       c.name AS category, t.amount, t.transaction_date
FROM transaction t
JOIN account a ON t.account_id = a.account_id
JOIN user u ON a.user_id = u.user_id
JOIN category c ON t.category_id = c.category_id;

-- 8. Show total spent per category
SELECT c.name AS category, SUM(t.amount) AS total
FROM transaction t
JOIN category c ON t.category_id = c.category_id
GROUP BY c.name;

-- 9. Show total income and expenses per user
SELECT u.first_name, u.last_name,
       SUM(CASE WHEN t.amount > 0 THEN t.amount ELSE 0 END) AS income,
       SUM(CASE WHEN t.amount < 0 THEN t.amount ELSE 0 END) AS expenses
FROM user u
JOIN account a ON u.user_id = a.user_id
JOIN transaction t ON a.account_id = t.account_id
GROUP BY u.user_id;

-- 10. List users who have not made any transactions
SELECT u.*
FROM user u
LEFT JOIN account a ON u.user_id = a.user_id
LEFT JOIN transaction t ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL;
