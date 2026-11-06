import tkinter as tk
from tkinter import messagebox

from Base_Finance_Module import BaseFinanceModule

# BUDGET PLANNER CLASS
class BudgetPlanner(BaseFinanceModule):

    def __init__(self, parent, data_manager, colors):
        super().__init__(parent, data_manager, colors, "Budget Planner")
        self.create_tabs()
        self.budget_content = tk.Frame(self.parent, bg=self.COLORS['primary'])
        self.budget_content.pack(fill='both', expand=True, pady=10)
        self.show_set_budget_form()


    # TABS
    def create_tabs(self):
        # Frame
        tabs_frame = tk.Frame(self.parent, bg=self.COLORS['primary'])
        tabs_frame.pack(fill='x', pady=10)
        
        # Set Budget Tab
        set_tab = tk.Label(tabs_frame, text="Set Budget", font=('Arial', 11),
                          fg=self.COLORS['accent'], bg=self.COLORS['secondary'],
                          padx=20, pady=10, cursor='hand2')
        set_tab.pack(side='left', padx=5)
        set_tab.bind('<Button-1>', lambda e: self.switch_tab('set'))
        
        # View Budgets Tab
        view_tab = tk.Label(tabs_frame, text="View Budgets", font=('Arial', 11),
                           fg=self.COLORS['text'], bg=self.COLORS['primary'],
                           padx=20, pady=10, cursor='hand2')
        view_tab.pack(side='left', padx=5)
        view_tab.bind('<Button-1>', lambda e: self.switch_tab('view'))
        
        # Edit/Delete Tab
        edit_tab = tk.Label(tabs_frame, text="Edit/Delete", font=('Arial', 11),
                           fg=self.COLORS['text'], bg=self.COLORS['primary'],
                           padx=20, pady=10, cursor='hand2')
        edit_tab.pack(side='left', padx=5)
        edit_tab.bind('<Button-1>', lambda e: self.switch_tab('edit'))
        
        # Budget vs Actual Tab
        compare_tab = tk.Label(tabs_frame, text="Budget vs Actual", font=('Arial', 11),
                              fg=self.COLORS['text'], bg=self.COLORS['primary'],
                              padx=20, pady=10, cursor='hand2')
        compare_tab.pack(side='left', padx=5)
        compare_tab.bind('<Button-1>', lambda e: self.switch_tab('compare'))
        
        self.tabs = {'set': set_tab, 'view': view_tab, 'edit': edit_tab, 'compare': compare_tab}


    def switch_tab(self, tab_name):
        # Update tab colors to show active state
        for name, tab in self.tabs.items():
            if name == tab_name:
                tab.config(fg=self.COLORS['accent'], bg=self.COLORS['secondary'])
            else:
                tab.config(fg=self.COLORS['text'], bg=self.COLORS['primary'])
        
        for widget in self.budget_content.winfo_children():
            widget.destroy()
        
        # Show selected tab (content)
        if tab_name == 'set':
            self.show_set_budget_form()
        elif tab_name == 'view':
            self.show_budget_status()
        elif tab_name == 'edit':
            self.show_edit_budget()
        elif tab_name == 'compare':
            self.show_budget_vs_actual()


    # GUI COMPONENTS
    def create_card(self, title, width=400, height=300):
        card = tk.Frame(self.budget_content, bg=self.COLORS['secondary'], width=width, height=height)
        card.pack_propagate(False)
        
        title_label = tk.Label(card, text=title, font=('Arial', 14, 'bold'),
                              fg=self.COLORS['accent'], bg=self.COLORS['secondary'])
        title_label.pack(anchor='w', padx=20, pady=15)
        
        return card


    def get_current_month(self):
        return "2001-09-11"  # Default date


    # SET BUDGET FUNCTIONALITY
    def show_set_budget_form(self):
        form_card = self.create_card("Set/Update Budget")
        form_card.pack(pady=20)
        
        # Category dropdown
        tk.Label(form_card, text="Category", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(10, 5))
        self.budget_category = tk.StringVar(value=self.categories[0])
        category_menu = tk.OptionMenu(form_card, self.budget_category, *self.categories)
        category_menu.config(bg=self.COLORS['primary'], fg=self.COLORS['text'])
        category_menu.pack(fill='x', padx=20, pady=5)
        
        # Budget amount input
        tk.Label(form_card, text="Monthly Budget (RM)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.budget_amount = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.budget_amount.pack(fill='x', padx=20, pady=5)
        
        # Set Budget button
        tk.Button(form_card, text="Set Budget", command=self.set_budget,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(pady=20)


    def set_budget(self):
        try:
            amount = float(self.budget_amount.get())

            if not self.validate_amount(amount, "Budget", min_value=0):
                return
            
            budgets = self.dm.load_budgets()
            budgets[self.budget_category.get()] = amount
            self.dm.save_budgets(budgets)
            
            messagebox.showinfo("Success", f"Budget for {self.budget_category.get()} set to RM{amount:.2f}")
            self.budget_amount.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")


    # VIEW BUDGETS FUNCTIONALITY
    def show_budget_status(self):
        status_card = tk.Frame(self.budget_content, bg=self.COLORS['secondary'])
        status_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(status_card, text="Current Budget Settings", font=('Arial', 16, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', pady=15)
        
        budgets = self.dm.load_budgets()
        
        if not budgets:
            tk.Label(status_card, text="No budgets set yet.", 
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Display all budgets with alternating row colors
        total = 0
        for i, (category, amount) in enumerate(sorted(budgets.items())):
            row_frame = tk.Frame(status_card, bg=self.COLORS['secondary'])
            row_frame.pack(fill='x', pady=2, padx=20)
            
            if i % 2 == 0:
                row_frame.config(bg='#e8e4dd')
            
            info_text = f"{category}: RM{amount:.2f}"
            tk.Label(row_frame, text=info_text, font=('Arial', 10),
                    fg=self.COLORS['text'], bg=row_frame['bg']).pack(anchor='w')
            
            total += amount
        
        # Display total budget
        total_frame = tk.Frame(status_card, bg=self.COLORS['secondary'])
        total_frame.pack(fill='x', pady=10)
        tk.Label(total_frame, text=f"TOTAL: RM{total:.2f}", 
                font=('Arial', 12, 'bold'), fg=self.COLORS['accent'], 
                bg=self.COLORS['secondary']).pack()


    # EDIT/DELETE BUDGET FUNCTIONALITY
    def show_edit_budget(self):
        edit_card = tk.Frame(self.budget_content, bg=self.COLORS['secondary'])
        edit_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(edit_card, text="Edit/Delete Budget", font=('Arial', 16, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', pady=15)
        
        budgets = self.dm.load_budgets()
        
        if not budgets:
            tk.Label(edit_card, text="No budgets set yet.", 
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Category selection
        input_frame = tk.Frame(edit_card, bg=self.COLORS['secondary'])
        input_frame.pack(fill='x', pady=10)
        
        tk.Label(input_frame, text="Select Category:", fg=self.COLORS['text'], 
                bg=self.COLORS['secondary'], font=('Arial', 11)).pack(side='left')
        
        categories = list(budgets.keys())
        self.selected_budget_category = tk.StringVar(value=categories[0])
        category_menu = tk.OptionMenu(input_frame, self.selected_budget_category, *categories)
        category_menu.config(bg=self.COLORS['primary'], fg=self.COLORS['text'], font=('Arial', 10))
        category_menu.pack(side='left', padx=10)
        
        tk.Button(input_frame, text="Load", command=self.load_budget_for_edit,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(side='left', padx=5)
        
        # Edit form
        form_frame = tk.Frame(edit_card, bg=self.COLORS['secondary'])
        form_frame.pack(fill='x', pady=10, padx=20)
        
        tk.Label(form_frame, text="Monthly Budget (RM)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', pady=(10, 5))
        self.edit_budget_amount = tk.Entry(form_frame, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.edit_budget_amount.pack(fill='x', pady=5)
        
        # Action buttons
        button_frame = tk.Frame(edit_card, bg=self.COLORS['secondary'])
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Update Budget", command=self.update_budget,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(side='left', padx=10)
        tk.Button(button_frame, text="Delete Budget", command=self.delete_budget,
                 bg='#DE8383', fg=self.COLORS['accent']).pack(side='left', padx=10)
        
        self.load_budget_for_edit()


    def load_budget_for_edit(self):
        budgets = self.dm.load_budgets()
        if not budgets:
            return
        
        category = self.selected_budget_category.get()
        amount = budgets.get(category, 0)
        
        self.edit_budget_amount.delete(0, tk.END)
        self.edit_budget_amount.insert(0, str(amount))


    def update_budget(self):
        try:
            amount = float(self.edit_budget_amount.get())
            if not self.validate_amount(amount, "Budget", min_value=0):
                return
            
            budgets = self.dm.load_budgets()
            category = self.selected_budget_category.get()
            budgets[category] = amount
            
            self.dm.save_budgets(budgets)
            messagebox.showinfo("Success", f"Budget for {category} updated to RM{amount:.2f}")
            self.show_edit_budget()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")


    def delete_budget(self):
        budgets = self.dm.load_budgets()
        category = self.selected_budget_category.get()
        
        if category in budgets:
            del budgets[category]
            self.dm.save_budgets(budgets)
            messagebox.showinfo("Success", f"Deleted budget for {category}")
            self.show_edit_budget()


    # BUDGET VS ACTUAL FUNCTIONALITY
    def show_budget_vs_actual(self):
        compare_card = tk.Frame(self.budget_content, bg=self.COLORS['secondary'])
        compare_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(compare_card, text="Budget vs Actual", font=('Arial', 16, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', pady=15)
        
        # Month input
        input_frame = tk.Frame(compare_card, bg=self.COLORS['secondary'])
        input_frame.pack(fill='x', pady=10)
        
        tk.Label(input_frame, text="Year-Month (YYYY-MM):", fg=self.COLORS['text'], 
                bg=self.COLORS['secondary'], font=('Arial', 11)).pack(side='left')
        
        self.budget_month_input = tk.Entry(input_frame, bg=self.COLORS['primary'], fg=self.COLORS['text'], font=('Arial', 10))
        self.budget_month_input.insert(0, self.get_current_month())
        self.budget_month_input.pack(side='left', padx=10)
        
        tk.Button(input_frame, text="Show Comparison", 
                 command=self.display_budget_comparison,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(side='left', padx=10)
        
        self.comparison_results = tk.Frame(compare_card, bg=self.COLORS['secondary'])
        self.comparison_results.pack(fill='both', expand=True, pady=10)
        
        self.display_budget_comparison()


    def display_budget_comparison(self):
        for widget in self.comparison_results.winfo_children():
            widget.destroy()
        
        budgets = self.dm.load_budgets()
        year_month = self.budget_month_input.get()
        expenses = self.dm.load_expenses()
        
        # Filter expenses for selected month
        monthly = []
        for exp in expenses:
            if exp['date'].startswith(year_month):
                monthly.append(exp)
        
        if not budgets:
            tk.Label(self.comparison_results, text="No budgets set yet.",
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Calculate spent amounts by category
        spent = {}
        for exp in monthly:
            spent[exp['category']] = spent.get(exp['category'], 0) + exp['amount']
        
        # Visual indicators
        for i, (category, budget) in enumerate(budgets.items()):
            row_frame = tk.Frame(self.comparison_results, bg=self.COLORS['secondary'])
            row_frame.pack(fill='x', pady=8, padx=20)
            
            if i % 2 == 0:
                row_frame.config(bg='#e8e4dd')
            
            actual = spent.get(category, 0)
            remaining = budget - actual
            percentage = (actual / budget * 100) if budget > 0 else 0

            self.create_budget_progress_bar(row_frame, category, budget, actual, percentage)
            self.create_budget_text_info(row_frame, category, budget, actual, remaining, percentage)


    def create_budget_progress_bar(self, parent, category, budget, actual, percentage):
        # Progress bar room
        bar_container = tk.Frame(parent, bg=parent['bg'])
        bar_container.pack(fill='x', pady=5)
        
        # Category label
        cat_label = tk.Label(bar_container, text=category, font=('Arial', 10, 'bold'),
                           fg=self.COLORS['text'], bg=parent['bg'], width=12, anchor='w')
        cat_label.pack(side='left')
        
        # Progress bar background 
        bar_bg = tk.Frame(bar_container, bg='#e0e0e0', height=20, width=200)
        bar_bg.pack(side='left', padx=10)
        bar_bg.pack_propagate(False)
        
        # Progress bar fill 
        fill_width = min(int((percentage / 100) * 200), 200)  
        fill_color = self.get_progress_color(percentage)
        
        bar_fill = tk.Frame(bar_bg, bg=fill_color, height=20, width=fill_width)
        bar_fill.pack(side='left', anchor='w')
        
        # Percentage label
        percent_label = tk.Label(bar_container, text=f"{percentage:.1f}%", 
                               font=('Arial', 9), fg=self.COLORS['text'], bg=parent['bg'], width=8)
        percent_label.pack(side='left', padx=5)


    def create_budget_text_info(self, parent, category, budget, actual, remaining, percentage):
        # Text info container
        text_container = tk.Frame(parent, bg=parent['bg'])
        text_container.pack(fill='x', pady=2)
        
        # Budget info
        budget_text = f"Budget: RM{budget:.2f} | Spent: RM{actual:.2f} | Remaining: RM{remaining:.2f}"
        budget_label = tk.Label(text_container, text=budget_text, font=('Arial', 9),
                              fg=self.COLORS['text'], bg=parent['bg'])
        budget_label.pack(anchor='w', padx=(120, 0))  
        
        # Status indicator with color
        status_frame = tk.Frame(parent, bg=parent['bg'])
        status_frame.pack(fill='x', pady=2)
        
        status_text, status_color = self.get_status_info(percentage)
        status_indicator = tk.Frame(status_frame, bg=status_color, width=10, height=10)
        status_indicator.pack(side='left', padx=(120, 5))
        status_indicator.pack_propagate(False)
        
        status_label = tk.Label(status_frame, text=status_text, font=('Arial', 9, 'bold'),
                              fg=status_color, bg=parent['bg'])
        status_label.pack(side='left')


    def get_progress_color(self, percentage):
        if percentage <= 60:
            return '#4CAF50'  # Good
        elif percentage <= 80:
            return '#FFC107'  # Warning
        elif percentage <= 100:
            return '#FF9800'  # Caution
        else:
            return '#F44336'  # Over budget


    def get_status_info(self, percentage):
        # Determine status text and color
        if percentage <= 60:
            return "Within Budget", '#4CAF50'
        elif percentage <= 80:
            return "Approaching Limit", '#FFC107'
        elif percentage <= 100:
            return "Close to Budget", '#FF9800'
        else:
            return "OVER BUDGET!", '#F44336'


    def get_current_month(self):
        return "2001-09-11"  # Default date