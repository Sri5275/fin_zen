-- FinZen Database Schema

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    merchant TEXT,
    transaction_date DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Budgets Table
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL UNIQUE,
    allocated_amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Investments Table
CREATE TABLE IF NOT EXISTS investments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    asset_type TEXT NOT NULL, -- 'STOCK' or 'MF'
    quantity REAL NOT NULL,
    purchase_price REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Goals Table
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal_name TEXT NOT NULL,
    target_amount REAL NOT NULL,
    current_amount REAL NOT NULL,
    target_date DATE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
