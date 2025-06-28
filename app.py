from flask import Flask, render_template, request, redirect
import mysql.connector
from config import DB_CONFIG
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def list_expenses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    current_month = datetime.now().month
    current_year = datetime.now().year

    # Get all expenses for current month
    cursor.execute("""
        SELECT * FROM expenses
        WHERE MONTH(date) = %s AND YEAR(date) = %s
        ORDER BY date DESC
    """, (current_month, current_year))
    rows = cursor.fetchall()

    # Total income
    cursor.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE type='Income' AND MONTH(date)=%s AND YEAR(date)=%s
    """, (current_month, current_year))
    income = cursor.fetchone()['SUM(amount)'] or 0

    # Total expense
    cursor.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE type='Expense' AND MONTH(date)=%s AND YEAR(date)=%s
    """, (current_month, current_year))
    expense = cursor.fetchone()['SUM(amount)'] or 0

    balance = income - expense

    # Prepare chart data
    category_data = defaultdict(float)
    daily_data = defaultdict(float)

    for row in rows:
        if row['type'] == 'Expense':
            # Pie chart: by category
            category_data[row['category']] += float(row['amount'])
            # Bar chart: by date
            date_str = row['date'].strftime('%Y-%m-%d')
            daily_data[date_str] += float(row['amount'])

    cursor.close()
    conn.close()

    return render_template("list_expenses.html",
        expenses=rows,
        income=income,
        expense=expense,
        balance=balance,
        category_data=dict(category_data),  # convert defaultdict to dict
        daily_data=dict(daily_data)
    )

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        type_ = request.form['type']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (date, type, category, amount, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (date, type_, category, amount, description))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')

    return render_template("add_expense.html")

if __name__ == '__main__':
    app.run(debug=True)


