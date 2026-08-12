import csv
import json
from datetime import date

class Expense:
    def __init__(self, id, amount, category, description, date):
        self.id = id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def to_dict(self):
        return {"id":self.id,"amount":self.amount ,"category": self.category,"description": self.description,"date": self.date}

def load_expenses():
    try:
        with open('expenses.json','r') as f:
            expense = json.load(f)

        return expense
    except FileNotFoundError:
        return []   

def save_expenses(expenses):
    with open('expenses.json','w') as f:
        json.dump(expenses,f) 

def add_expense(expenses):
    amount = int(input("Enter the amount: "))
    category = input("Enter the category: ")
    description = input("Enter the description: ")
    today = str(date.today())
    new_id = max(e["id"] for e in expenses) + 1 if expenses else 1
    expense = Expense(id= new_id, amount= amount, category=category, description=description,date=today)
    expenses.append(expense.to_dict())
    save_expenses(expenses)
    print("Expense Added")

def export_csv(expenses):
    with open("expenses_report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "amount", "category", "description", "date"])
        for expense in expenses:
            writer.writerow([expense["id"], expense["amount"], expense["category"],expense["description"], expense["date"]])
        print("DONE")

def load_budgets():
    try:
        with open("budgets.json", "r") as f:
            expense = json.load(f)

        return expense 
    except FileNotFoundError:
        return {}

def save_budgets(budgets):
    with open("budgets.json", "w") as f:
        json.dump(budgets, f)

def set_budget(budgets):
    category = input("Enter the category: ")
    amount = int(input("Enter the amount: "))
    budgets[category] = amount
    save_budgets(budgets)
    print("DONE")


def monthly_summary(expenses, budgets):
    date = input("Enter the month(YYYY-MM): ")
    totals = {}
    for expense in expenses:
        if expense['date'].startswith(date):
            totals[expense['category']] = totals.get(expense['category'], 0) + expense['amount'] 
    print(f"----{date}---")
    for category, total in totals.items():
        if category in budgets and total > budgets[category]:
            print(f"{category} : {total} OVER BUDGET (limit {budgets[category]})")
        else:
            print(f"{category} : {total}")
    print(f"Total : {sum(totals.values())}")

def main():
    expenses = load_expenses()
    budgets = load_budgets()
    while(True):
        
        print("1. Add expense\n2. Set budget for category\n3. View monthly summary (with alerts)\n4. Export to CSV\n5. Quit")
        choice = int(input("Enter your choice(1 - 5): "))
        if choice == 1:
            add_expense(expenses)
        elif choice == 2:
            set_budget(budgets)
        elif choice == 3:
            monthly_summary(expenses, budgets)
        elif choice == 4:
            export_csv(expenses)
        elif choice == 5:
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":main()