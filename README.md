Personal Finance Manager

A Command Line Interface (CLI) based Personal Finance Tracker built using Python, SQLite, and SQLAlchemy ORM.
This project helps users manage daily expenses, track subscriptions, monitor category-wise spending, and control monthly budgets.

Features:
Add and manage expense categories
2) Record daily transactions (expenses)
3) Update entries
4) delete incorrect or extra entries
5) Search expenses by date
6) View category-wise spending summary (using Raw SQL)
7) Set monthly budgets for categories
8) Get budget alerts when spending exceeds the limit
9) Track subscriptions (Netflix, Gym, etc.)
10) Persistent storage using SQLite database

Technologies Used:

Python 3
SQLite Database
SQLAlchemy ORM
Raw SQL Queries
CLI (Command Line Interface)

Database Schema:

The application uses four relational tables with proper foreign key relationships.

Categories
Stores different types of spending categories.
Fields:
id — Integer, Primary Key
name — String, name of the category (e.g., Food, Travel)
Relationship:
One category can have many transactions
One category can have many budgets
Transactions
Stores all expense records entered by the user.
Fields:
id — Integer, Primary Key
amount — Float, money spent
description — String, expense details
date — String, date of transaction (YYYY-MM-DD)
category_id — Integer, Foreign Key referencing categories.id
Relationship:
Many transactions belong to one category
Budgets
Stores monthly spending limits for each category.
Fields:
id — Integer, Primary Key
category_id — Integer, Foreign Key referencing categories.id
month — String, month in format YYYY-MM
budget_limit — Float, maximum allowed spending
Relationship:
Many budget records can belong to one category
Used to compare actual spending vs planned budget
Subscriptions
Stores recurring expenses separately.
Fields:
id — Integer, Primary Key
name — String, subscription name (e.g., Netflix)
amount — Float, subscription cost
start_date — String, start date (YYYY-MM-DD)
end_date — String, end/renewal date
Relationship:
Independent table (not linked to categories)
Relationship Summary
Category → Transactions = One-to-Many
Category → Budgets = One-to-Many
Transactions → Category = Many-to-One
Budgets → Category = Many-to-One
Subscriptions = Standalone entity

How It Works(Workflow):

User creates categories (Food, Travel, etc.)
User records transactions under categories
System stores all data using SQLAlchemy ORM
User can:
Update or delete transactions
Search by date
View category spending summary
User sets monthly budgets
System compares spending with budget and shows alerts
Subscriptions are tracked separately for recurring expenses

FLOW CHART(workflow):

START
  |
  v
User Runs Program
  |
  v
Database Connection Established (SQLite + SQLAlchemy)
  |
  v
Tables Created (Categories, Transactions, Budgets, Subscriptions)
  |
  v
Main Menu Displayed
  |
  v
User Chooses an Option
  |                                                              
  v                                                              
Add Category (1)                                         
  |                                                              
Enter Category Name                                    
  |                                                   
Category Stored in DB                                           
  |                 
  v
Back to Menu
  |
  v
Update Transaction (3)  --> Enter Transaction ID --> Modify Details --> Save --> Back
  |
  v
Delete Transaction (4)  --> Enter Transaction ID --> Delete Record --> Back
  |
  v
Search by Date (5) --> Enter Date --> Fetch Matching Transactions --> Display --> Back
  |
  v
Category Summary (6)
  |
  v
Run RAW SQL JOIN (Categories + Transactions)
  |
  v
Calculate SUM(amount) GROUP BY Category
  |
  v
Display Category-wise Spending
  |
  v
Back to Menu
  |
  v
Set Budget (7)
  |
  v
Enter Category ID, Month (YYYY-MM), Budget Limit
  |
  v
Budget Stored in Budgets Table
  |
  v
Back to Menu
  |
  v
Budget Alert (8)
  |
  v
Enter Month (YYYY-MM)
  |
  v
System Calculates Total Spending per Category for that Month
  |
  v
Compare Spending with Budget Limit
  |
  v
If Spent > Limit → ALERT    
Else → Within Budget 
  |
  v
Back to Menu
  |
  v
Add Subscription (9)
  |
  v
Enter Name, Amount, Start Date, End Date
  |
  v
Subscription Stored in DB
  |
  v
Back to Menu
  |
  v
User Selects Exit (0)
  |
  v
Program Ends
  |
  v
END

How to Run the Project:
1)Install dependencies:
pip install sqlalchemy

2) Run the program:
python finance_tracker.py

CLI Menu Options:
1. Add Category
2. Add Transaction
3. Update Transaction
4. Delete Transaction
5. Search Transaction by Date
6. Category Summary
7. Set Budget
8. Budget Alert
9. Add Subscription
0. Exit

Learning Outcomes:

This project demonstrates:
ORM-based database interaction
SQL JOINs and aggregation
CLI application design
Budget tracking logic
Modular programming with Python

Future Enhancements:
Export reports to CSV
Flask Web Interface
User Authentication
Charts and visual analytics

Author: Namith
