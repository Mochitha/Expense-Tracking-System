import mysql.connector  # MySQL database connector
from contextlib import contextmanager  # Context manager for resource handling
from logging_setup import setup_logger  # Custom logger setup

# Set up a logger for debugging and tracking database operations
logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager to establish a database connection and return a cursor.
    Automatically closes the connection and commits changes if required.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )
    cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries
    yield cursor  # Provide the cursor for database operations
    if commit:
        connection.commit()  # Commit changes if required
    cursor.close()  # Close the cursor
    connection.close()  # Close the connection

def fetch_expenses_for_date(expense_date):
    """Fetch all expenses for a given date."""
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        return cursor.fetchall()  # Return all matching records

def delete_expenses_for_date(expense_date):
    """Delete all expenses for a given date."""
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def insert_expense(expense_date, amount, category, notes):
    """Insert a new expense record into the database."""
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def fetch_expense_summary(start_date, end_date):
    """Fetch a summary of expenses grouped by category for a given date range."""
    logger.info(f"fetch_expense_summary called with start: {start_date}, end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s and %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        return cursor.fetchall()  # Return summarized expense data

def fetch_monthly_expense_summary():
    """Fetch a summary of total expenses grouped by month."""
    logger.info("fetch_monthly_expense_summary called")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT 
               MONTHNAME(expense_date) as month,
               SUM(amount) as total FROM expenses
               GROUP BY month;
            '''
        )
        return cursor.fetchall()  # Return expense summary by month

if __name__ == "__main__":
    # Example usage of the functions
    # expenses = fetch_expenses_for_date("2024-09-30")
    # print(expenses)
    # delete_expenses_for_date("2024-08-25")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    # for record in summary:
    #     print(record)
    print(fetch_monthly_expense_summary())
