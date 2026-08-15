from datetime import date
import json

class Expense:
    def __init__(self, id, amount, category, description, date):
        self.id = id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def to_dict(self):
        return {"id": self.id, "amount": self.amount, "category": self.category, "description": self.description, "date": self.date}

    def __str__(self):
        pass

def load_expenses():
    try:
        with open('expenses.json', 'r') as f:
            expense = json.load(f)
        return expense
    except FileNotFoundError:
        return []

def save_expenses(expenses, filename="expenses.json"):
    with open(filename, "w") as f:
        json.dump(expenses, f)

def add_expense(expenses):
    amount = int(input("Enter the amount: "))
    category = input("Enter the category: ")
    description = input("Enter the description: ")
    today = str(date.today())
    new_id = max(e["id"] for e in expenses) + 1 if expenses else 1
    expense = Expense(id=new_id, amount=amount, category=category, description=description, date=today)
    expenses.append(expense.to_dict())
    save_expenses(expenses)
    print("Expense Added")

def build_expense(expenses, amount, category, description):
    if amount < 0:
        raise ValueError("You cannot input negitive values")
    today = str(date.today())
    new_id = max(e["id"] for e in expenses) + 1 if expenses else 1
    expense = Expense(id=new_id, amount=amount, category=category, description=description, date=today)
    expenses.append(expense.to_dict())
    return expenses

def view_all(expenses):
    for expense in expenses:
        print(f"{expense['id']} : {expense['amount']} : {expense['category']} : {expense['description']} : {expense['date']}")

def view_by_category(expenses):
    category = input("Enter the category: ").lower()
    for expense in expenses:
        if expense['category'].lower() == category:
            print(f"{expense['id']} : {expense['amount']} : {expense['category']} : {expense['description']} : {expense['date']}")

def del_by_id(expenses, expenses_id):
    found = False
    for expense in expenses:
        if expense['id'] == expenses_id:
            expenses.remove(expense)
            save_expenses(expenses)
            found = True
            break
    if not found:
        print("Invalid ID")

def edit_by_id(expenses, expenses_id):
    found = False
    for expense in expenses:
        if expense['id'] == expenses_id:
            amount = int(input("Enter the new amount: "))
            description = input("Enter the new description: ")
            expense['amount'], expense['description'] = amount, description
            found = True
            break
    if found:
        save_expenses(expenses)
    else:
        print("invalid ID")

def summary_by_category(expenses):
    month = input("Enter the month(YYYY-MM): ")
    totals = {}
    for expense in expenses:
        if expense['date'].startswith(month):
            totals[expense['category']] = totals.get(expense['category'], 0) + expense['amount']
    print(f"---{month}---")
    for category, total in totals.items():
        print(f"{category} : {total}")
    print(f"Total : {sum(totals.values())}")

def main():
    expenses = load_expenses()
    while True:
        print("1. Add expense\n2. View all expenses\n3. view by category\n4. Delete by expenses\n5. Edit expense\n6. Mnthly summary\n7. quit")
        choice = int(input("Enter your choice (1-7): "))
        if choice == 1:
            add_expense(expenses)
        elif choice == 2:
            view_all(expenses)
        elif choice == 3:
            view_by_category(expenses)
        elif choice == 4:
            expenses_id = int(input("Enter the ID to delete: "))
            del_by_id(expenses, expenses_id)
        elif choice == 5:
            expenses_id = int(input("Enter the ID to edit: "))
            edit_by_id(expenses, expenses_id)
        elif choice == 6:
            summary_by_category(expenses)
        elif choice == 7:
            print("THANK YOU")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()