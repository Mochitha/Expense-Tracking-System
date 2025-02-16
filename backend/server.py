from fastapi import FastAPI, HTTPException  # FastAPI framework and error handling
from datetime import date  # Date handling for requests
import db_helper  # Database helper functions
from typing import List  # Type hinting for lists
from pydantic import BaseModel  # Data validation and serialization

# Initialize FastAPI app
app = FastAPI()


# Pydantic model for an expense entry
class Expense(BaseModel):
    amount: float  # Expense amount
    category: str  # Expense category
    notes: str  # Additional notes


# Pydantic model for date range request
class DateRange(BaseModel):
    start_date: date  # Start date for summary
    end_date: date  # End date for summary


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    """Retrieve all expenses for a given date."""
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    """Delete existing expenses and insert new ones for a given date."""
    db_helper.delete_expenses_for_date(expense_date)  # Remove existing records
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)  # Insert new records
    return {"message": "Expenses updated successfully"}


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    """Retrieve a summary of expenses within a date range, including category-wise breakdown."""
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total = sum([row['total'] for row in data])  # Compute total expenses
    breakdown = {}
    for row in data:
        percentage = (row['total'] / total) * 100 if total != 0 else 0  # Calculate category percentage
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }
    return breakdown


@app.get("/monthly_summary/")
def get_monthly_summary():
    """Retrieve a monthly summary of expenses."""
    monthly_summary = db_helper.fetch_monthly_expense_summary()
    if monthly_summary is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve monthly expense summary from the database.")
    return monthly_summary
