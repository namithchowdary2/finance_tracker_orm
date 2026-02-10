#importing necessary libraries
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,text,Float
from sqlalchemy.orm import sessionmaker, declarative_base,relationship
#database connection
engine=create_engine('sqlite:///finance_tracker.db')
#creating a base class for our models
Base=declarative_base() 
#creating a session class and binding it to our engine
Session = sessionmaker(bind=engine)
#creating a session object
session = Session()
# NOW creating the tables
#category table:
class Category(Base):
    __tablename__='categories'
    id=Column(Integer, primary_key=True) #unique category id
    name=Column(String) #category name
    #one category can have many transactions
    transactions=relationship('Transaction', back_populates='category')
    #one category can have many budgets
    budgets=relationship('Budget', back_populates='category')
#transaction table:
class Transaction(Base):
    __tablename__='transactions'
    id=Column(Integer, primary_key=True) #unique transaction id
    amount=Column(Float) #transaction amount
    description=Column(String) #transaction description
    date=Column(String) #transaction date
    category_id=Column(Integer, ForeignKey('categories.id')) #foreign key to link transaction to category
    #many transactions belong to one category
    category=relationship('Category', back_populates='transactions')
    #subscription table:
class Subscription(Base):
    __tablename__='subscriptions'
    id=Column(Integer, primary_key=True) #unique subscription id
    name=Column(String) #subscription name
    amount=Column(Float) #subscription amount
    start_date=Column(String) #subscription start date
    end_date=Column(String) #subscription end date
#budget table:
class Budget(Base):
    __tablename__='budgets'
    id=Column(Integer, primary_key=True) #unique budget id
    category_id=Column(Integer, ForeignKey('categories.id')) #foreign key to link budget to category
    #many budgets belong to one category
    category=relationship('Category', back_populates='budgets') #relationship to access category details
    month=Column(String) #budget month
    budget_limit=Column(Float) #budget limit for the month
    #creating the tables in the database
Base.metadata.create_all(engine)
def add_category():
    #ask user for cateory name
    name=input("Category name: ")
    #create category object and save to database
    session.add(Category(name=name))
    session.commit()
    print("Category added")
def add_transaction():
    amount=float(input("Transaction amount: "))
    description=input("Transaction description: ")
    date=input("Transaction date (YYYY-MM-DD): ")
    category_id=int(input("Category ID: "))
    #create transaction object and save to database
    session.add(Transaction(amount=amount, description=description, date=date, category_id=category_id))
    session.commit()
    print("Transaction added")
def update_transaction():
    transaction_id=int(input("Transaction ID to update: "))
    #find transaction record by ID 
    transaction=session.query(Transaction).filter(Transaction.id==transaction_id).first()
    if transaction:
        transaction.amount=float(input("New amount: "))
        transaction.description=input("New description: ")
        transaction.date=input("New date (YYYY-MM-DD): ")
        transaction.category_id=int(input("New category ID: "))
        session.commit()
        print("Transaction updated")
    else:
        print("Transaction not found")
def delete_transaction():
    transaction_id=int(input("Transaction ID to delete: "))
    #find transaction record by ID
    transaction=session.query(Transaction).filter(Transaction.id==transaction_id).first()
    if transaction:
        session.delete(transaction)
        session.commit()
        print("Transaction deleted")
    else:
        print("Transaction not found")
def search_by_date():
    date=input("Enter date (YYYY-MM-DD): ")
    transactions=session.query(Transaction).filter(Transaction.date==date).all()
    for t in transactions:
        print(f"ID: {t.id}, Amount: {t.amount}, Description: {t.description}, Category ID: {t.category_id}")
def category_summary():
    sql=text("SELECT c.name, SUM(t.amount) FROM categories c JOIN transactions t ON c.id = t.category_id GROUP BY c.id")
    result=session.execute(sql)
    for row in result:
        print(f"Category: {row[0]}, Total Amount: {row[1]}")
def set_budget():
    category_id=int(input("Category ID for budget: "))
    month=input("Budget month (YYYY-MM): ")
    limit=float(input("Budget limit: "))
    #create budget object and save to database
    session.add(Budget(category_id=category_id, month=month, budget_limit=limit))
    session.commit()
    print("Budget set")
def budget_alert():
    month=input("Enter month for budget alert (YYYY-MM): ")
    #caluculate total spent for each category in the given month and compare with budget limit
    sql=text("""
    SELECT c.name, b.budget_limit, SUM(t.amount) as total_spent
    FROM budgets b
    JOIN categories c ON b.category_id = c.id
    LEFT JOIN transactions t ON c.id = t.category_id AND t.date LIKE :month || '-%'
    WHERE b.month = :month
    GROUP BY c.id, b.budget_limit
    """)
    result=session.execute(sql, {'month': month})
    for row in result:
        category_name=row[0]
        budget_limit=row[1]
        total_spent=row[2]
        if total_spent > budget_limit:
            print(f"Alert: Category '{category_name}' has exceeded the budget limit! Spent: {total_spent}, Limit: {budget_limit}")
        else:
            print(f"Category '{category_name}': Spent {total_spent}, Limit {budget_limit} - Within budget.")
def add_subscription():
    name = input("Subscription name: ") #ask user for subscription name
    amount = float(input("Subscription amount: ")) #ask user for subscription amount
    start_date = input("Start date (YYYY-MM-DD): ") #ask user for subscription start date
    end_date = input("End date (YYYY-MM-DD): ") #ask user for subscription end date
    #create subscription object and save to database
    session.add(Subscription(name=name, amount=amount, start_date=start_date, end_date=end_date))
    session.commit()
    print("Subscription added")
#CLI for user interaction
while True:
    print("\n1. Add Category\n2. Add Transaction\n3. Update Transaction\n4. Delete Transaction\n5. Search Transaction by Date\n6. Category Summary\n7. Set Budget\n8. Budget Alert\n9. Add Subscription\n0. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        add_category()
    elif choice == '2':
        add_transaction()
    elif choice == '3':
        update_transaction()
    elif choice == '4':
        delete_transaction()
    elif choice == '5':
        search_by_date()
    elif choice == '6':
        category_summary()
    elif choice == '7':
        set_budget()
    elif choice == '8':
        budget_alert()
    elif choice == '9':
        add_subscription()
    elif choice == '0':
        break
    else:
        print("Invalid option, try again.")