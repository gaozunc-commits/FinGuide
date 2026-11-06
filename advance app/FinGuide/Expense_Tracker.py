import tkinter as tk
from tkinter import messagebox

from Base_Finance_Module import BaseFinanceModule

# EXPENSE TRACKER CLASS
class ExpenseTracker(BaseFinanceModule):

    def __init__(self, parent, data_manager, colors):
        super().__init__(parent, data_manager, colors, "Expense Tracker")
        self.create_tabs()
        self.expense_content = tk.Frame(self.parent, bg=self.COLORS['primary'])
        self.expense_content.pack(fill='both', expand=True, pady=10)
        self.show_add_expense_form()


    # TABS
    def create_tabs(self):
        # Frame
        tabs_frame = tk.Frame(self.parent, bg=self.COLORS['primary'])
        tabs_frame.pack(fill='x', pady=10)
        
        # Add Expense 
        add_tab = tk.Label(tabs_frame, text="Add Expense", font=('Arial', 11),
                          fg=self.COLORS['accent'], bg=self.COLORS['secondary'],
                          padx=20, pady=10, cursor='hand2')
        add_tab.pack(side='left', padx=5)
        add_tab.bind('<Button-1>', lambda e: self.switch_tab('add'))
        
        # View Expenses 
        view_tab = tk.Label(tabs_frame, text="View Expenses", font=('Arial', 11),
                           fg=self.COLORS['text'], bg=self.COLORS['primary'],
                           padx=20, pady=10, cursor='hand2')
        view_tab.pack(side='left', padx=5)
        view_tab.bind('<Button-1>', lambda e: self.switch_tab('view'))
        
        # Edit/Delete 
        edit_tab = tk.Label(tabs_frame, text="Edit/Delete", font=('Arial', 11),
                           fg=self.COLORS['text'], bg=self.COLORS['primary'],
                           padx=20, pady=10, cursor='hand2')
        edit_tab.pack(side='left', padx=5)
        edit_tab.bind('<Button-1>', lambda e: self.switch_tab('edit'))
        
        # View by Category 
        category_tab = tk.Label(tabs_frame, text="View by Category", font=('Arial', 11),
                               fg=self.COLORS['text'], bg=self.COLORS['primary'],
                               padx=20, pady=10, cursor='hand2')
        category_tab.pack(side='left', padx=5)
        category_tab.bind('<Button-1>', lambda e: self.switch_tab('category'))
        
        # Monthly Summary 
        monthly_tab = tk.Label(tabs_frame, text="Monthly Summary", font=('Arial', 11),
                              fg=self.COLORS['text'], bg=self.COLORS['primary'],
                              padx=20, pady=10, cursor='hand2')
        monthly_tab.pack(side='left', padx=5)
        monthly_tab.bind('<Button-1>', lambda e: self.switch_tab('monthly'))
        
        self.tabs = {'add': add_tab, 'view': view_tab, 'edit': edit_tab, 'category': category_tab, 'monthly': monthly_tab}


    def switch_tab(self, tab_name):
        for name, tab in self.tabs.items():
            if name == tab_name:
                tab.config(fg=self.COLORS['accent'], bg=self.COLORS['secondary'])
            else:
                tab.config(fg=self.COLORS['text'], bg=self.COLORS['primary'])
        

        for widget in self.expense_content.winfo_children():
            widget.destroy()
        

        if tab_name == 'add':
            self.show_add_expense_form()
        elif tab_name == 'view':
            self.show_all_expenses()
        elif tab_name == 'edit':
            self.show_edit_expense()
        elif tab_name == 'category':
            self.show_expenses_by_category()
        elif tab_name == 'monthly':
            self.show_monthly_summary()

    
    # GUI
    
    def create_card(self, title, width=400, height=500):
        card = tk.Frame(self.expense_content, bg=self.COLORS['secondary'], width=width, height=height)
        card.pack_propagate(False)
        
        title_label = tk.Label(card, text=title, font=('Arial', 14, 'bold'),
                              fg=self.COLORS['accent'], bg=self.COLORS['secondary'])
        title_label.pack(anchor='w', padx=20, pady=15)
        
        return card


    def get_current_date(self):
        return "2001-09-11"  # Default date

    # ADD EXPENSE 
    def show_add_expense_form(self):
        form_card = self.create_card("Add Expense")
        form_card.pack(pady=20)
        
        # Date input field
        tk.Label(form_card, text="Date (YYYY-MM-DD)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(10, 5))
        self.expense_date = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.expense_date.insert(0, self.get_current_date())
        self.expense_date.pack(fill='x', padx=20, pady=5)
        
        # Amount input field
        tk.Label(form_card, text="Amount (RM)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.expense_amount = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.expense_amount.pack(fill='x', padx=20, pady=5)
        
        # Category dropdown
        tk.Label(form_card, text="Category", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.expense_category = tk.StringVar(value=self.categories[0])
        category_menu = tk.OptionMenu(form_card, self.expense_category, *self.categories)
        category_menu.config(bg=self.COLORS['primary'], fg=self.COLORS['text'])
        category_menu.pack(fill='x', padx=20, pady=5)
        
        # Description input field
        tk.Label(form_card, text="Description", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.expense_desc = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.expense_desc.pack(fill='x', padx=20, pady=5)
        
        # Add Expense button
        tk.Button(form_card, text="Add Expense", command=self.add_expense,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(pady=20)


    def add_expense(self):
        try:
            amount = float(self.expense_amount.get())
            if not self.validate_amount(amount, "Amount", min_value=0.01):
                return
            
            expense = {
                'date': self.expense_date.get(),
                'amount': amount,
                'category': self.expense_category.get(),
                'description': self.expense_desc.get()
            }
            
            self.dm.save_expense(expense)
            messagebox.showinfo("Success", "Expense added successfully!")
            
            self.expense_amount.delete(0, tk.END)
            self.expense_desc.delete(0, tk.END)
            self.expense_date.delete(0, tk.END)
            self.expense_date.insert(0, self.get_current_date())
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    # VIEW ALL EXPENSES
    def show_all_expenses(self):
        expenses_card = tk.Frame(self.expense_content, bg=self.COLORS['secondary'])
        expenses_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(expenses_card, text="All Expenses", font=('Arial', 16, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', pady=10)
        
        expenses = self.dm.load_expenses()
        
        if not expenses:
            tk.Label(expenses_card, text="No expenses recorded yet.", 
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Display expense
        for i in range(len(expenses)):
            exp = expenses[i]
            expense_frame = tk.Frame(expenses_card, bg=self.COLORS['secondary'])
            expense_frame.pack(fill='x', pady=5, padx=20)
            
            if i % 2 == 0:
                expense_frame.config(bg='#e8e4dd')
            
            info_text = f"{exp['date']} - RM{exp['amount']:.2f} - {exp['category']} - {exp['description']}"
            tk.Label(expense_frame, text=info_text, font=('Arial', 10),
                    fg=self.COLORS['text'], bg=expense_frame['bg']).pack(anchor='w')
        
        # Calculate and display total
        total = 0
        for exp in expenses:
            total += exp['amount']
        
        total_frame = tk.Frame(expenses_card, bg=self.COLORS['secondary'])
        total_frame.pack(fill='x', pady=10)
        tk.Label(total_frame, text=f"Total Expenses: RM{total:.2f}", 
                font=('Arial', 12, 'bold'), fg=self.COLORS['accent'], 
                bg=self.COLORS['secondary']).pack()

    # EDIT/DELETE EXPENSE
    def show_edit_expense(self):
        edit_card = tk.Frame(self.expense_content, bg=self.COLORS['secondary'])
        edit_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(edit_card, text="Edit/Delete Expense", font=('Arial', 16, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', pady=15)
        
        expenses = self.dm.load_expenses()
        
        if not expenses:
            tk.Label(edit_card, text="No expenses recorded yet.", 
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Expense selection dropdown
        input_frame = tk.Frame(edit_card, bg=self.COLORS['secondary'])
        input_frame.pack(fill='x', pady=10)
        
        tk.Label(input_frame, text="Select Expense:", fg=self.COLORS['text'], 
                bg=self.COLORS['secondary'], font=('Arial', 11)).pack(side='left')
        
        expense_options = []
        for i in range(len(expenses)):
            exp = expenses[i]
            expense_options.append(f"{i}: {exp['date']} - RM{exp['amount']:.2f} - {exp['category']}")
        
        self.selected_expense_index = tk.StringVar(value=expense_options[0])
        expense_menu = tk.OptionMenu(input_frame, self.selected_expense_index, *expense_options)
        expense_menu.config(bg=self.COLORS['primary'], fg=self.COLORS['text'], font=('Arial', 9))
        expense_menu.pack(side='left', padx=10)
        
        tk.Button(input_frame, text="Load", command=self.load_expense_for_edit,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(side='left', padx=5)
        
        # Edit form
        form_frame = tk.Frame(edit_card, bg=self.COLORS['secondary'])
        form_frame.pack(fill='x', pady=10, padx=20)
        
        # Amount field
        tk.Label(form_frame, text="Amount (RM)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', pady=(10, 5))
        self.edit_expense_amount = tk.Entry(form_frame, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.edit_expense_amount.pack(fill='x', pady=5)
        
        # Category dropdown
        tk.Label(form_frame, text="Category", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', pady=(15, 5))
        self.edit_expense_category = tk.StringVar(value=self.categories[0])
        category_menu = tk.OptionMenu(form_frame, self.edit_expense_category, *self.categories)
        category_menu.config(bg=self.COLORS['primary'], fg=self.COLORS['text'])
        category_menu.pack(fill='x', pady=5)
        
        # Description field
        tk.Label(form_frame, text="Description", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', pady=(15, 5))
        self.edit_expense_desc = tk.Entry(form_frame, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.edit_expense_desc.pack(fill='x', pady=5)
        
        # Date field
        tk.Label(form_frame, text="Date (YYYY-MM-DD)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', pady=(15, 5))
        self.edit_expense_date = tk.Entry(form_frame, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.edit_expense_date.pack(fill='x', pady=5)
        
        # Action buttons
        button_frame = tk.Frame(edit_card, bg=self.COLORS['secondary'])
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Update Expense", command=self.update_expense,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(side='left', padx=10)
        tk.Button(button_frame, text="Delete Expense", command=self.delete_expense,
                 bg='#DE8383', fg=self.COLORS['accent']).pack(side='left', padx=10)
        
        self.load_expense_for_edit()


    def load_expense_for_edit(self):
        expenses = self.dm.load_expenses()
        if not expenses:
            return
        
        selected = self.selected_expense_index.get()
        index = int(selected.split(':')[0])
        
        expense = expenses[index]
        self.edit_expense_amount.delete(0, tk.END)
        self.edit_expense_amount.insert(0, str(expense['amount']))
        
        self.edit_expense_category.set(expense['category'])
        
        self.edit_expense_desc.delete(0, tk.END)
        self.edit_expense_desc.insert(0, expense['description'])
        
        self.edit_expense_date.delete(0, tk.END)
        self.edit_expense_date.insert(0, expense['date'])


    def update_expense(self):
        try:
            amount = float(self.edit_expense_amount.get())
            if not self.validate_amount(amount, "Amount", min_value=0.01):
                return
            
            expenses = self.dm.load_expenses()
            selected = self.selected_expense_index.get()
            index = int(selected.split(':')[0])
            
            expenses[index] = {
                'date': self.edit_expense_date.get(),
                'amount': amount,
                'category': self.edit_expense_category.get(),
                'description': self.edit_expense_desc.get()
            }
            
            self.dm.save_all_expenses(expenses)
            messagebox.showinfo("Success", "Expense updated successfully!")
            self.show_edit_expense()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")


    def delete_expense(self):
        expenses = self.dm.load_expenses()
        selected = self.selected_expense_index.get()
        index = int(selected.split(':')[0])
        
        deleted = expenses.pop(index)
        self.dm.save_all_expenses(expenses)
        messagebox.showinfo("Success", f"Deleted expense: {deleted['description']}")
        self.show_edit_expense()

    # CATEGORY VIEW FUNCTIONALITY
    def show_expenses_by_category(self):
        category_card = tk.Frame(self.expense_content, bg=self.COLORS['secondary'])
        category_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(category_card, text="Expenses by Category", font=('Arial', 16, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', pady=15)
        
        expenses = self.dm.load_expenses()
        
        if not expenses:
            tk.Label(category_card, text="No expenses recorded yet.", 
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        categories = []
        for exp in expenses:
            if exp['category'] not in categories:
                categories.append(exp['category'])
        
        # Category selection
        input_frame = tk.Frame(category_card, bg=self.COLORS['secondary'])
        input_frame.pack(fill='x', pady=10)
        
        tk.Label(input_frame, text="Select Category:", fg=self.COLORS['text'], 
                bg=self.COLORS['secondary'], font=('Arial', 11)).pack(side='left')
        
        self.selected_category = tk.StringVar(value=categories[0])
        category_menu = tk.OptionMenu(input_frame, self.selected_category, *categories)
        category_menu.config(bg=self.COLORS['primary'], fg=self.COLORS['text'], font=('Arial', 10))
        category_menu.pack(side='left', padx=10)
        
        tk.Button(input_frame, text="Show Expenses", 
                 command=self.display_category_expenses,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(side='left', padx=10)
        
        self.category_results = tk.Frame(category_card, bg=self.COLORS['secondary'])
        self.category_results.pack(fill='both', expand=True, pady=10)
        
        self.display_category_expenses()


    def display_category_expenses(self):
        for widget in self.category_results.winfo_children():
            widget.destroy()
        
        expenses = self.dm.load_expenses()
        category = self.selected_category.get()
        
        # Filter expenses by category
        filtered = []
        for exp in expenses:
            if exp['category'] == category:
                filtered.append(exp)
        
        if not filtered:
            tk.Label(self.category_results, text=f"No expenses found for category: {category}",
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        total = 0
        for i in range(len(filtered)):
            exp = filtered[i]
            expense_frame = tk.Frame(self.category_results, bg=self.COLORS['secondary'])
            expense_frame.pack(fill='x', pady=2, padx=20)
            
            if i % 2 == 0:
                expense_frame.config(bg='#e8e4dd')
            
            info_text = f"{exp['date']} - RM{exp['amount']:.2f} - {exp['description']}"
            tk.Label(expense_frame, text=info_text, font=('Arial', 10),
                    fg=self.COLORS['text'], bg=expense_frame['bg']).pack(anchor='w')
            
            total += exp['amount']
        
        total_frame = tk.Frame(self.category_results, bg=self.COLORS['secondary'])
        total_frame.pack(fill='x', pady=10)
        tk.Label(total_frame, text=f"Total for {category}: RM{total:.2f}", 
                font=('Arial', 12, 'bold'), fg=self.COLORS['accent'], 
                bg=self.COLORS['secondary']).pack()

    # MONTHLY SUMMARY FUNCTIONALITY
    def show_monthly_summary(self):
        monthly_card = tk.Frame(self.expense_content, bg=self.COLORS['secondary'])
        monthly_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(monthly_card, text="Monthly Summary", font=('Arial', 16, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', pady=15)
        
        # Month input
        input_frame = tk.Frame(monthly_card, bg=self.COLORS['secondary'])
        input_frame.pack(fill='x', pady=10)
        
        tk.Label(input_frame, text="Year-Month (YYYY-MM):", fg=self.COLORS['text'], 
                bg=self.COLORS['secondary'], font=('Arial', 11)).pack(side='left')
        
        self.month_input = tk.Entry(input_frame, bg=self.COLORS['primary'], fg=self.COLORS['text'], font=('Arial', 10))
        self.month_input.insert(0, "2001-09-11")  # Default date
        self.month_input.pack(side='left', padx=10)
        
        tk.Button(input_frame, text="Show Summary", 
                 command=self.display_monthly_summary,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(side='left', padx=10)
        
        self.monthly_results = tk.Frame(monthly_card, bg=self.COLORS['secondary'])
        self.monthly_results.pack(fill='both', expand=True, pady=10)
        
        self.display_monthly_summary()


    def display_monthly_summary(self):
        for widget in self.monthly_results.winfo_children():
            widget.destroy()
        
        expenses = self.dm.load_expenses()
        year_month = self.month_input.get()
        
        # Filter monthly expenses
        monthly = []
        for exp in expenses:
            if exp['date'].startswith(year_month):
                monthly.append(exp)
        
        if not monthly:
            tk.Label(self.monthly_results, text=f"No expenses found for {year_month}",
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Calculate category totals
        category_totals = {}
        for exp in monthly:
            category = exp['category']
            if category in category_totals:
                category_totals[category] += exp['amount']
            else:
                category_totals[category] = exp['amount']
        
        # Sort categories manually (bubble sort)
        total = 0
        categories_sorted = list(category_totals.keys())
        for i in range(len(categories_sorted)):
            for j in range(i + 1, len(categories_sorted)):
                if categories_sorted[i] > categories_sorted[j]:
                    categories_sorted[i], categories_sorted[j] = categories_sorted[j], categories_sorted[i]
        
        # Display category totals
        for i in range(len(categories_sorted)):
            cat = categories_sorted[i]
            amount = category_totals[cat]
            row_frame = tk.Frame(self.monthly_results, bg=self.COLORS['secondary'])
            row_frame.pack(fill='x', pady=2, padx=20)
            
            if i % 2 == 0:
                row_frame.config(bg='#e8e4dd')
            
            info_text = f"{cat}: RM{amount:.2f}"
            tk.Label(row_frame, text=info_text, font=('Arial', 10),
                    fg=self.COLORS['text'], bg=row_frame['bg']).pack(anchor='w')
            
            total += amount
        
        # Display total
        total_frame = tk.Frame(self.monthly_results, bg=self.COLORS['secondary'])
        total_frame.pack(fill='x', pady=10)
        tk.Label(total_frame, text=f"TOTAL: RM{total:.2f}", 
                font=('Arial', 12, 'bold'), fg=self.COLORS['accent'], 
                bg=self.COLORS['secondary']).pack()