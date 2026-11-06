import tkinter as tk
from tkinter import messagebox

from Base_Finance_Module import BaseFinanceModule

# SAVING GOAL TRACKER CLASS
class SavingGoalTracker(BaseFinanceModule):

    def __init__(self, parent, data_manager, colors):
        super().__init__(parent, data_manager, colors, "Savings Goal Tracker")
        self.create_tabs()
        self.goal_content = tk.Frame(self.parent, bg=self.COLORS['primary'])
        self.goal_content.pack(fill='both', expand=True, pady=10)
        self.show_add_goal_form()


    # TABS
    def create_tabs(self):
        # Frame
        tabs_frame = tk.Frame(self.parent, bg=self.COLORS['primary'])
        tabs_frame.pack(fill='x', pady=10)
        
        # Add Goal 
        add_tab = tk.Label(tabs_frame, text="Add Goal", font=('Arial', 11),
                          fg=self.COLORS['accent'], bg=self.COLORS['secondary'],
                          padx=20, pady=10, cursor='hand2')
        add_tab.pack(side='left', padx=5)
        add_tab.bind('<Button-1>', lambda e: self.switch_tab('add'))
        
        # Update Progress 
        update_tab = tk.Label(tabs_frame, text="Update Progress", font=('Arial', 11),
                             fg=self.COLORS['text'], bg=self.COLORS['primary'],
                             padx=20, pady=10, cursor='hand2')
        update_tab.pack(side='left', padx=5)
        update_tab.bind('<Button-1>', lambda e: self.switch_tab('update'))
        
        # View Goals 
        view_tab = tk.Label(tabs_frame, text="View Goals", font=('Arial', 11),
                           fg=self.COLORS['text'], bg=self.COLORS['primary'],
                           padx=20, pady=10, cursor='hand2')
        view_tab.pack(side='left', padx=5)
        view_tab.bind('<Button-1>', lambda e: self.switch_tab('view'))
        
        # Delete Goal 
        delete_tab = tk.Label(tabs_frame, text="Delete Goal", font=('Arial', 11),
                             fg=self.COLORS['text'], bg=self.COLORS['primary'],
                             padx=20, pady=10, cursor='hand2')
        delete_tab.pack(side='left', padx=5)
        delete_tab.bind('<Button-1>', lambda e: self.switch_tab('delete'))
        
        self.tabs = {'add': add_tab, 'update': update_tab, 'view': view_tab, 'delete': delete_tab}


    def switch_tab(self, tab_name):
        for name, tab in self.tabs.items():
            if name == tab_name:
                tab.config(fg=self.COLORS['accent'], bg=self.COLORS['secondary'])
            else:
                tab.config(fg=self.COLORS['text'], bg=self.COLORS['primary'])
        
        for widget in self.goal_content.winfo_children():
            widget.destroy()
        
        if tab_name == 'add':
            self.show_add_goal_form()
        elif tab_name == 'update':
            self.show_update_goal_form()
        elif tab_name == 'view':
            self.show_goals_list()
        elif tab_name == 'delete':
            self.show_delete_goal_form()


    # GUI
    
    def create_card(self, title, width=400, height=500):
        card = tk.Frame(self.goal_content, bg=self.COLORS['secondary'], width=width, height=height)
        card.pack_propagate(False)
        
        title_label = tk.Label(card, text=title, font=('Arial', 14, 'bold'),
                              fg=self.COLORS['accent'], bg=self.COLORS['secondary'])
        title_label.pack(anchor='w', padx=20, pady=15)
        
        return card


    # ADD GOAL 
    def show_add_goal_form(self):
        form_card = self.create_card("Add New Goal")
        form_card.pack(pady=20)
        
        # Goal name input field
        tk.Label(form_card, text="Goal Name", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(10, 5))
        self.goal_name = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.goal_name.pack(fill='x', padx=20, pady=5)
        
        # Target amount input field
        tk.Label(form_card, text="Target Amount (RM)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.goal_target = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.goal_target.pack(fill='x', padx=20, pady=5)
        
        # Current savings input field
        tk.Label(form_card, text="Current Savings (RM)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.goal_current = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.goal_current.insert(0, "0")
        self.goal_current.pack(fill='x', padx=20, pady=5)
        
        # Deadline input field
        tk.Label(form_card, text="Deadline (YYYY-MM-DD)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.goal_deadline = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.goal_deadline.pack(fill='x', padx=20, pady=5)
        
        # Add Goal button
        tk.Button(form_card, text="Add Goal", command=self.add_goal,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(pady=20)


    def add_goal(self):
        try:
            name = self.goal_name.get().strip()
            if not name:
                messagebox.showerror("Error", "Goal name cannot be empty")
                return
            
            target = float(self.goal_target.get())
            if not self.validate_amount(target, "Target amount", min_value=0.01):
                return
            
            current = float(self.goal_current.get())
            if not self.validate_amount(current, "Current savings", min_value=0):
                return
            
            if current > target:
                messagebox.showerror("Error", "Current savings cannot exceed target amount")
                return
            
            deadline = self.goal_deadline.get().strip()
            
            goal = {
                'name': name,
                'target': target,
                'current': current,
                'deadline': deadline
            }
            
            goals = self.dm.load_goals()
            goals.append(goal)
            self.dm.save_goals(goals)
            
            messagebox.showinfo("Success", f"Goal '{name}' added successfully!")
            
            self.goal_name.delete(0, tk.END)
            self.goal_target.delete(0, tk.END)
            self.goal_current.delete(0, tk.END)
            self.goal_current.insert(0, "0")
            self.goal_deadline.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for amounts")


    # UPDATE GOAL PROGRESS
    def show_update_goal_form(self):
        form_card = self.create_card("Update Goal Progress", 400, 300)
        form_card.pack(pady=20)
        
        goals = self.dm.load_goals()
        
        if not goals:
            tk.Label(form_card, text="No goals set yet.", 
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Goal selection dropdown
        tk.Label(form_card, text="Select Goal:", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(10, 5))
        
        goal_names = [goal['name'] for goal in goals]
        self.selected_goal = tk.StringVar(value=goal_names[0])
        goal_menu = tk.OptionMenu(form_card, self.selected_goal, *goal_names)
        goal_menu.config(bg=self.COLORS['primary'], fg=self.COLORS['text'])
        goal_menu.pack(fill='x', padx=20, pady=5)
        
        # Amount to add input field
        tk.Label(form_card, text="Amount to Add (RM):", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.update_amount = tk.Entry(form_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.update_amount.pack(fill='x', padx=20, pady=5)
        
        # Update Goal button
        tk.Button(form_card, text="Update Goal", command=self.update_goal,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(pady=20)


    def update_goal(self):
        try:
            goals = self.dm.load_goals()
            goal_name = self.selected_goal.get()
            amount = float(self.update_amount.get())
            
            if not self.validate_amount(amount, "Amount", min_value=0):
                return
            
            for goal in goals:
                if goal['name'] == goal_name:
                    new_current = goal['current'] + amount
                    if new_current > goal['target']:
                        messagebox.showerror("Error", "Cannot exceed target amount")
                        return
                    goal['current'] = new_current
                    break
            
            self.dm.save_goals(goals)
            messagebox.showinfo("Success", f"Updated! Added RM{amount:.2f} to {goal_name}")
            self.update_amount.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")


    # VIEW GOALS
    def show_goals_list(self):
        list_card = tk.Frame(self.goal_content, bg=self.COLORS['secondary'])
        list_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(list_card, text="Your Savings Goals", font=('Arial', 16, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', pady=15)
        
        goals = self.dm.load_goals()
        
        if not goals:
            tk.Label(list_card, text="No goals set yet.", 
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Display goals
        for goal in goals:
            goal_frame = tk.Frame(list_card, bg=self.COLORS['secondary'], relief='raised', bd=1)
            goal_frame.pack(fill='x', pady=10, padx=20)
            
            progress = (goal['current'] / goal['target'] * 100) if goal['target'] > 0 else 0
            remaining = goal['target'] - goal['current']
            
            tk.Label(goal_frame, text=goal['name'], font=('Arial', 14, 'bold'),
                    fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(anchor='w', padx=10, pady=(10, 5))
            
            details = f"Target: RM{goal['target']:.2f} | Current: RM{goal['current']:.2f} | Remaining: RM{remaining:.2f} | Progress: {progress:.1f}%"
            tk.Label(goal_frame, text=details, font=('Arial', 10),
                    fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=10, pady=5)
            
            tk.Label(goal_frame, text=f"Deadline: {goal['deadline']}", font=('Arial', 10),
                    fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=10, pady=(0, 10))


    # DELETE GOAL FUNCTIONALITY
    def show_delete_goal_form(self):
        form_card = self.create_card("Delete Goal", 400, 300)
        form_card.pack(pady=20)
        
        goals = self.dm.load_goals()
        
        if not goals:
            tk.Label(form_card, text="No goals set yet.", 
                    fg=self.COLORS['text'], bg=self.COLORS['secondary'], font=('Arial', 12)).pack(pady=20)
            return
        
        # Goal selection dropdown
        tk.Label(form_card, text="Select Goal to Delete:", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(10, 5))
        
        goal_names = [goal['name'] for goal in goals]
        self.delete_goal = tk.StringVar(value=goal_names[0])
        goal_menu = tk.OptionMenu(form_card, self.delete_goal, *goal_names)
        goal_menu.config(bg=self.COLORS['primary'], fg=self.COLORS['text'])
        goal_menu.pack(fill='x', padx=20, pady=5)
        
        # Delete Goal button
        tk.Button(form_card, text="Delete Goal", command=self.delete_goal_action,
                 bg='#DE8383', fg=self.COLORS['accent']).pack(pady=20)


    def delete_goal_action(self):
        goals = self.dm.load_goals()
        goal_name = self.delete_goal.get()
        
        for i, goal in enumerate(goals):
            if goal['name'] == goal_name:
                deleted_goal = goals.pop(i)
                self.dm.save_goals(goals)
                messagebox.showinfo("Success", f"Deleted goal: {deleted_goal['name']}")
                self.show_delete_goal_form()
                return