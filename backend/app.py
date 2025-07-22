import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allows the frontend to make requests to this backend

DATABASE = 'database/finzen.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initializes the database and populates it with sample data."""
    with app.app_context():
        db = get_db()
        with open('database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        
        # --- SAMPLE DATA INSERTION ---
        # Clear existing data to avoid duplicates on re-run
        db.execute("DELETE FROM users")
        db.execute("DELETE FROM transactions")
        db.execute("DELETE FROM budgets")
        db.execute("DELETE FROM investments")
        db.execute("DELETE FROM goals")

        # Create a sample user
        db.execute("INSERT INTO users (id, email, password_hash) VALUES (?, ?, ?)",
                   (1, 'user@example.com', 'hashed_password_placeholder'))

        # Sample transactions
        transactions_data = [
            (1, 150.00, 'Food & Dining', 'Swiggy', '2025-07-21'),
            (1, 1200.00, 'Shopping', 'Myntra', '2025-07-20'),
            (1, 750.00, 'Groceries', 'Blinkit', '2025-07-19'),
            (1, 3000.00, 'Bills & Utilities', 'Airtel Bill', '2025-07-18'),
            (1, 500.00, 'Entertainment', 'BookMyShow', '2025-07-17'),
        ]
        db.executemany("INSERT INTO transactions (user_id, amount, category, merchant, transaction_date) VALUES (?, ?, ?, ?, ?)", transactions_data)

        # Sample budgets
        budgets_data = [
            (1, 'Food & Dining', 5000),
            (1, 'Shopping', 8000),
            (1, 'Groceries', 6000),
            (1, 'Entertainment', 3000),
            (1, 'Travel', 10000)
        ]
        db.executemany("INSERT INTO budgets (user_id, category, allocated_amount) VALUES (?, ?, ?)", budgets_data)

        # Sample investments
        investments_data = [
            (1, 'TCS', 'STOCK', 10, 3800.50),
            (1, 'RELIANCE', 'STOCK', 15, 2900.00),
            (1, 'HDFCBANK', 'STOCK', 20, 1650.75),
            (1, 'PARAGPARIKH', 'MF', 50, 80.20)
        ]
        db.executemany("INSERT INTO investments (user_id, symbol, asset_type, quantity, purchase_price) VALUES (?, ?, ?, ?, ?)", investments_data)

        # Sample goals
        goals_data = [
            (1, 'Goa Trip', 75000, 25000, '2025-12-31'),
            (1, 'New iPhone', 150000, 45000, '2026-09-30')
        ]
        db.executemany("INSERT INTO goals (user_id, goal_name, target_amount, current_amount, target_date) VALUES (?, ?, ?, ?, ?)", goals_data)
        
        db.commit()
        db.close()


@app.route('/api/dashboard_data')
def get_dashboard_data():
    """
    This is the main API endpoint that aggregates all data for the dashboard.
    In a real app, user_id would come from a secure authentication token (JWT).
    """
    user_id = 1 # Hardcoded for prototype
    db = get_db()

    # Fetch recent transactions
    transactions_cur = db.execute(
        "SELECT merchant, category, amount, transaction_date FROM transactions WHERE user_id = ? ORDER BY transaction_date DESC LIMIT 5", (user_id,)
    )
    transactions = [dict(row) for row in transactions_cur.fetchall()]

    # Fetch budget vs actuals
    budgets_cur = db.execute("""
        SELECT
            b.category,
            b.allocated_amount,
            COALESCE(SUM(t.amount), 0) as spent_amount
        FROM budgets b
        LEFT JOIN transactions t ON b.category = t.category AND b.user_id = t.user_id
        WHERE b.user_id = ?
        GROUP BY b.category
    """, (user_id,))
    budgets = [dict(row) for row in budgets_cur.fetchall()]
    
    # Fetch goals
    goals_cur = db.execute("SELECT * FROM goals WHERE user_id = ?", (user_id,))
    goals = [dict(row) for row in goals_cur.fetchall()]

    # --- SIMULATE PORTFOLIO DATA (in a real app, this would use a live market API) ---
    # This data is hardcoded for demonstration
    portfolio = {
        "total_invested": 120535.00,
        "current_value": 129200.00,
        "day_gain": 850.50,
        "overall_pnl": 8665.00,
        "allocation": [
            {"name": "Indian Equity", "value": 90440.00},
            {"name": "Global Equity", "value": 20360.00},
            {"name": "Debt", "value": 18400.00}
        ]
    }
    
    # Financial Health Score (Simulated)
    financial_health = {"score": 742, "max_score": 900, "assessment": "Good"}

    response_data = {
        "transactions": transactions,
        "budgets": budgets,
        "goals": goals,
        "portfolio": portfolio,
        "financial_health": financial_health
    }
    
    db.close()
    return jsonify(response_data)

if __name__ == '__main__':
    init_db() # Initialize DB with sample data on startup
    app.run(debug=True, port=5001)

