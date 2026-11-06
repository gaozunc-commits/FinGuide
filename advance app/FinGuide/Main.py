import tkinter as tk
from tkinter import *
from pathlib import Path

from Budget_Planner import BudgetPlanner
from Expense_Tracker import ExpenseTracker
from Tax_Estimator import TaxEstimator
from Saving_Goal_Tracker import SavingGoalTracker
from Data_Manager import DataManager


# Colour Palette
COLORS = {
    'primary': '#DCD7D0',
    'secondary': '#f6f5f4', 
    'text': '#5C4742',
    'accent': '#391B18',
    'success': '#DFCD95'
}

# GUI
class FinanceAssistantGUI:
    def __init__(self):
        # 1. Setup Data and Window
        self.dm = DataManager(r"FinGuide\Data\finance_data.txt")
        self.root = Tk()
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['primary'])
        self.root.title("FinGuide")
        
        # 3. Create Layout Frames
        self.sidebar = tk.Frame(self.root, bg=COLORS['primary'], width=200)
        self.sidebar.pack(side='left', fill='y', padx=10, pady=10)
        
        self.content_area = tk.Frame(self.root, bg=COLORS['primary'])
        self.content_area.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # 4. Create UI Elements
        self.create_sidebar()
        self.show_dashboard()

    # Sidebar
    def create_sidebar(self):
        try:
            logo = tk.PhotoImage(file="FinGuide/Images/logo.png")
        except:
            try:
                logo = tk.PhotoImage(file=f"{Path.cwd()}/FinGuide/Images/logo.png")
            except:
                logo = tk.PhotoImage(file="FinGuide\\Images\\logo.png")
        
        logo = logo.subsample(5, 5)
        
        self.logo_image = logo
        
        # Create label with image
        title_label = tk.Label(self.sidebar, image=self.logo_image, bg=COLORS['primary'])
        title_label.pack(pady=(10,20), anchor='w', padx=(20,10))

        # Navigation Buttons
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Expense Tracker", self.show_expense_tracker),
            ("Budget Planner", self.show_budget_planner),
            ("Savings Goals", self.show_savings_goals),
            ("Tax Estimator", self.show_tax_estimator)
        ]
        
        for text, command in nav_items:
            btn = tk.Button(self.sidebar, text=text, command=command,
                           font=('Arial', 11), fg=COLORS['text'], bg=COLORS['secondary'],
                           cursor='hand2', anchor='w', padx=15, pady=12, 
                           relief='flat', borderwidth=0)
            btn.pack(fill='x', pady=2)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=COLORS['secondary'], width=180, height=120)
        card.pack_propagate(False)
        
        tk.Label(card, text=title, font=('Arial', 10), fg=COLORS['text'],
                bg=COLORS['secondary']).pack(pady=(20, 5))
        tk.Label(card, text=value, font=('Arial', 20, 'bold'), fg=color,
                bg=COLORS['secondary']).pack()
        
        return card
    
    def create_action_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command,
                        font=('Arial', 11), bg=COLORS['success'],
                        fg=COLORS['accent'], width=12, height=2)
    
    def show_dashboard(self):
        self.clear_content()
        
        welcome = tk.Label(self.content_area, text="💸 Manage Your Money Now ! 💸",
                          font=('Courier', 14, 'bold'), fg=COLORS['text'], bg=COLORS['primary'])
        welcome.pack(anchor='w', pady=(45,50), padx=6)
        
        stats_frame = tk.Frame(self.content_area, bg=COLORS['primary'])
        stats_frame.pack(fill='x', pady=10)
        
        try:
            expenses = self.dm.load_expenses()
            total_expenses = sum(exp['amount'] for exp in expenses)
            
            budgets = self.dm.load_budgets()
            total_budget = sum(budgets.values())
            
            goals = self.dm.load_goals()
            total_savings = sum(goal['current'] for goal in goals)
        except Exception:
            total_expenses = 0.0
            total_budget = 0.0
            total_savings = 0.0

        expense_card = self.create_stat_card(stats_frame, "Total Expenses", 
                                            f"RM{total_expenses:.2f}",'#CD6868')
        expense_card.pack(side='left', padx=10)
        
        budget_card = self.create_stat_card(stats_frame, "Total Budget",
                                           f"RM{total_budget:.2f}", '#4BC37D')
        budget_card.pack(side='left', padx=10)
        
        savings_card = self.create_stat_card(stats_frame, "Total Savings",
                                            f"RM{total_savings:.2f}", '#E1C526')
        savings_card.pack(side='left', padx=10)
        
        quick_label = tk.Label(self.content_area, text="Shortcut:",
                              font=('Arial', 16, 'bold'), fg=COLORS['text'],
                              bg=COLORS['primary'])
        quick_label.pack(anchor='w', pady=(15, 15), padx=6)
        
        actions_frame = tk.Frame(self.content_area, bg=COLORS['primary'])
        actions_frame.pack(fill='x')
        
        self.create_action_button(actions_frame, "Add Expense", 
                                self.show_expense_tracker).pack(side='left', padx=10)
        self.create_action_button(actions_frame, "Set Budget",
                                self.show_budget_planner).pack(side='left', padx=10)
        self.create_action_button(actions_frame, "Add Goal",
                                self.show_savings_goals).pack(side='left', padx=10)
    
    def show_expense_tracker(self):
        self.clear_content()
        ExpenseTracker(self.content_area, self.dm, COLORS)
    
    def show_budget_planner(self):
        self.clear_content()
        BudgetPlanner(self.content_area, self.dm, COLORS)
    
    def show_savings_goals(self):
        self.clear_content()
        SavingGoalTracker(self.content_area, self.dm, COLORS)
    
    def show_tax_estimator(self):
        self.clear_content()
        TaxEstimator(self.content_area, COLORS)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FinanceAssistantGUI()
    app.run()