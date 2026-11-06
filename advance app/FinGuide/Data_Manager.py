from Base_Finance_Module import BaseFinanceModule

class DataManager:
    def __init__(self, filepath='finance_data.txt'):
        self.filepath = filepath
        try:
            with open(self.filepath, 'r') as f:
                pass
        except:
            self.initialize_file()
    
    def initialize_file(self):
        with open(self.filepath, 'w') as f:
            f.write("EXPENSES_SECTION\n")
            f.write("END_EXPENSES\n")
            f.write("BUDGETS_SECTION\n")
            f.write("END_BUDGETS\n")
            f.write("GOALS_SECTION\n")
            f.write("END_GOALS\n")
    
    def read_entire_file(self):
        try:
            with open(self.filepath, 'r') as f:
                return f.readlines()
        except:
            return []
    
    def write_entire_file(self, expenses, budgets, goals):
        with open(self.filepath, 'w') as f:
            f.write("EXPENSES_SECTION\n")
            for exp in expenses:
                f.write(f"{exp['date']}|{exp['amount']}|{exp['category']}|{exp['description']}\n")
            f.write("END_EXPENSES\n")
            f.write("BUDGETS_SECTION\n")
            for category, amount in budgets.items():
                f.write(f"{category}|{amount}\n")
            f.write("END_BUDGETS\n")
            f.write("GOALS_SECTION\n")
            for goal in goals:
                f.write(f"{goal['name']}|{goal['target']}|{goal['current']}|{goal['deadline']}\n")
            f.write("END_GOALS\n")
    
    def load_expenses(self):
        expenses = []
        try:
            lines = self.read_entire_file()
            in_expenses = False
            for line in lines:
                line = line.strip()
                if line == "EXPENSES_SECTION":
                    in_expenses = True
                    continue
                elif line == "END_EXPENSES":
                    break
                elif in_expenses and line:
                    parts = line.split('|')
                    if len(parts) == 4:
                        expense_dict = {
                            'date': parts[0],
                            'amount': float(parts[1]),
                            'category': parts[2],
                            'description': parts[3]
                        }
                        expenses.append(expense_dict)
        except:
            pass
        return expenses
    
    def load_budgets(self):
        budgets = {}
        try:
            lines = self.read_entire_file()
            in_budgets = False
            for line in lines:
                line = line.strip()
                if line == "BUDGETS_SECTION":
                    in_budgets = True
                    continue
                elif line == "END_BUDGETS":
                    break
                elif in_budgets and line:
                    parts = line.split('|')
                    if len(parts) == 2:
                        budgets[parts[0]] = float(parts[1])
        except:
            pass
        return budgets
    
    def load_goals(self):
        goals = []
        try:
            lines = self.read_entire_file()
            in_goals = False
            for line in lines:
                line = line.strip()
                if line == "GOALS_SECTION":
                    in_goals = True
                    continue
                elif line == "END_GOALS":
                    break
                elif in_goals and line:
                    parts = line.split('|')
                    if len(parts) == 4:
                        goal_dict = {
                            'name': parts[0],
                            'target': float(parts[1]),
                            'current': float(parts[2]),
                            'deadline': parts[3]
                        }
                        goals.append(goal_dict)
        except:
            pass
        return goals
    
    def save_expense(self, expense):
        expenses = self.load_expenses()
        budgets = self.load_budgets()
        goals = self.load_goals()
        expenses.append(expense)
        self.write_entire_file(expenses, budgets, goals)
    
    def save_all_expenses(self, expenses):
        budgets = self.load_budgets()
        goals = self.load_goals()
        self.write_entire_file(expenses, budgets, goals)
    
    def save_budgets(self, budgets):
        expenses = self.load_expenses()
        goals = self.load_goals()
        self.write_entire_file(expenses, budgets, goals)
    
    def save_goals(self, goals):
        expenses = self.load_expenses()
        budgets = self.load_budgets()
        self.write_entire_file(expenses, budgets, goals)