# expense_tracker.py
# Author: Zainab Sohail
# Week 1 - Basic Expense Tracker

from tabulate import tabulate #for clean table
from datetime import datetime #to add accurate dates 
import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt #for graphs

FILENAME = "expenses.json" #Make your program remember data between runs
CATEGORIES = ["Food", "Transport", "Tuition", "Entertainment", "Utilities", "Other"]

# -----------------------------
# CHART FUNCTION
# -----------------------------

def show_chart(data, overspend_percent=20):
    """
    Display a bar chart of total spending per category.
    Categories that exceed 'overspend_percent' of the total budget are colored red.
    
    Parameters:
    - data: dict containing 'expenses' list and 'budget'
    - overspend_percent: int, percentage of budget considered "overspending"
    """
    expenses = data.get("expenses", [])
    budget = data.get("budget", 0)
    
    if not expenses:
        print("No expenses to display in chart.")
        return
    
    from collections import defaultdict
    totals = defaultdict(float)
    for e in expenses:
        category = e.get("category", "Other")
        totals[category] += e["amount"]
    
    categories = list(totals.keys())
    amounts = list(totals.values())
    
    # Calculate per-category threshold from budget
    threshold = (overspend_percent / 100) * budget if budget > 0 else float('inf')
    
    # Color bars based on overspending
    colors = ['red' if amt > threshold else 'skyblue' for amt in amounts]
    
    total_spent = sum(amounts)
    plt.figure(figsize=(8,5))
    plt.bar(categories, amounts, color=colors)
    plt.title(f"Total Spending per Category\nTotal: ${total_spent:.2f}, Budget: ${budget:.2f}, Overspend Threshold: {overspend_percent}%")
    plt.xlabel("Category")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()



# -----------------------------
# Helper functions for JSON
# -----------------------------

# Checks if the file expenses.json exists.
# If yes, json.load(file) reads the file and converts JSON back into Python objects (list of dictionaries).
# If no, returns an empty list — your program starts with no expenses.
def load_expenses():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return {"expenses": data, "budget": 0, "goal": 0}
            return data
    else:
        return {"expenses":[], "budget": 0, "Goal": 0}
    
def save_data(data):
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
 
# -----------------------------
# Core functions
# -----------------------------

def add_expense(data):
    """Add a new expense with date, name, and amount."""
    expenses = data["expenses"]
    date = datetime.now().strftime("%Y-%m-%d")
    
    print("Select a category: ")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")

    while True:
        choice = input("Enter the number of the category: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(CATEGORIES):
                category = CATEGORIES[choice - 1]
                break
            else:
                print("Invalid choice, try again.")
        except ValueError:
            print("Please enter a valid.")


    name = input("Enter expance name/type: ")


     # Validate amount
    while True:
        amount = input("Enter amount: ")
        try:
            amount = float(amount)
            break
        except ValueError:
            print(" Amount must be a number. Try again.")
            
    # Add to list and save
    expenses.append({"date": date,"category": category ,"name": name, "amount": amount})
    save_data(expenses)
    print(f"Saved: {date} -{category}-{name} (${amount})")


def delete_expense(data):
     """Delete an expense by number and save changes."""
     expenses = data["expenses"]
     if not expenses:
         print("Nor Expenses to delete.")

    # Display all expenses with index
     table = [(i + 1, e["date"], e.get("category", "Other"), e["name"], e["amount"])
             for i, e in enumerate(expenses)]
     headers = ["#", "Date", "Category", "Name", "Amount ($)"]
     print("\n--- Delete an Expense ---")
     print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    
     try:
        choice = int(input("Enter the number of the expense to delete: "))
        if 1 <= choice <= len(expenses):
            removed = expenses.pop(choice - 1)
            save_data(expenses)
            print(f"Deleted: {removed['name']}(${removed['amount']}")
        else:
            print("INVALID CHOICE NUMBER")
     except ValueError:
        print("Please enter a valid number. ")

    

    
def view_expenses(data):
    """Display all expenses in a clean table."""
    expenses = data["expenses"]
    if not expenses:
        print("No expenses recorded yet.")
        return

    table = [(e["date"], e.get("category", "Other"), e["name"], e["amount"]) for e in expenses]
    headers = ["Date", "Category", "Name", "Amount ($)"]
    print("\n--- Your Expenses ---")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))



def show_monthly_summary(data):
    """Show total spending per month."""
    expenses = data["expenses"]
    monthly_totals = {}
    for e in expenses:
        try:
            date_obj = datetime.strptime(e["date"], "%Y-%m-%d")  #FIX: define date_obj here
            month = date_obj.strftime("%Y-%m")

            monthly_totals[month] = monthly_totals.get(month, 0) + e["amount"]

        except Exception as err:
            print(f"Skipping bad entry: {e} ({err})")

    # Print table
    print("\n--- Monthly Spending Summary ---")
    table = [(month, f"${total:.2f}") for month, total in sorted(monthly_totals.items())]
    print(tabulate(table, headers=["Month", "Total Spent"], tablefmt="fancy_grid"))

 # Plot line chart
    months = list(sorted(monthly_totals.keys()))
    totals = [monthly_totals[m] for m in months]

    plt.figure(figsize=(8, 5))
    plt.plot(months, totals, marker="o", linestyle="-", color="teal")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Spent ($)")
    plt.grid(True)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def show_summary(data):
    """Show total spending per category."""
    expenses = data["expenses"]
    from collections import defaultdict
    totals = defaultdict(float)
    total_overall = 0.0

    for e in expenses:
        # Use .get("category", "Other") to safely handle older entries
        category = e.get("category", "Other")  
        totals[category] += e["amount"]
        total_overall += e["amount"]

    print("\n--- Spending Summary ---")
    for category, total in totals.items():
        print(f"{category:<20}: ${total:.2f}")
    print("-" * 30)
    print(f"{'Total':<20}: ${total_overall:.2f}")


# -----------------------------
# Budget and Goal Tracking
# -----------------------------

def set_budget(data):
    """Set or update the user's monthly budget"""
    while True:
        try:
            amount = float(input("Enter your monthly budget($): "))
            data["budget"] = amount
            save_data(data)
            print(f"Budget set to {amount:.2f}")
            break
        except ValueError:
            print("Please enter a valid number.")

def set_goal(data):
    """Set or update the user's savings goal."""
    while True:
        try:
            amount = float(input("Enter your monthly savings goal ($): "))
            data["goal"] = amount
            save_data(data)
            print(f" Savings goal set to ${amount:.2f}")
            break
        except ValueError:
            print(" Please enter a valid number.")


def check_progress(data):
    """Check current spending vs budget and goal."""
    expenses = data.get("expenses", [])
    budget = data.get("budget", 0)
    goal = data.get("goal", 0)
    total_spent = sum(e["amount"]for e in expenses)

    print("\n--- Budget Progress ---")
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Budget Limit: ${budget:.2f}")
    print(f"Savings Goal: ${goal:.2f}")

    if budget > 0:
        percent = (total_spent/budget) * 100
        print(f"Used {percent:.1f}% of your budget.")
        if total_spent > budget:
            print("You’ve exceeded your budget!")
        elif total_spent >= 0.8 * budget:
            print("You’re nearing your budget limit!")
        else:
            print("You’re within your budget.")

    if goal > 0:
            remaining = budget - total_spent
            if remaining >= goal:
                print(f"You’re on track to meet your savings goal! (${remaining:.2f} left)")
            else:
                print(f"You’re below your savings target by ${goal - remaining:.2f}")





# -----------------------------
# Main program
# -----------------------------
  

def main():
    """"Main Program Map"""
    data = load_expenses()
    

    while True:
        print("\n***Expense Tracker***")
        print("--------------------------")
        print("1. Add Expence")
        print("2. View expences")
        print("3. View Summary")
        print("4. Show Chart")
        print("5. Delete Expense")
        print("6. Monthly Summary")
        print("7. Set Monthly Budget")
        print("8. Set Savings Goal")
        print("9. Check Progress")
        print("10. Exit")
        


        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(data)
        elif choice == "2":
            view_expenses(data)
        elif choice == "3":
            show_summary(data)
        elif choice == "4":
            show_chart(data)
        elif choice == "5":
            delete_expense(data)
        elif choice == "6":
            show_monthly_summary(data)
        elif choice == "7":
            set_budget(data)
        elif choice == "8":
            set_goal(data)
        elif choice == "9":
            check_progress(data)
        elif choice == "10":
            print("Goodbye:)")
            break
        else:
            print("Invalid choice, please try again!")

if __name__ == "__main__":
    main()



