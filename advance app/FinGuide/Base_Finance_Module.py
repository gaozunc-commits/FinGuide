import tkinter as tk
from tkinter import messagebox

class BaseFinanceModule:
    
    def __init__(self, parent, data_manager, colors, title, categories=None):
        self.parent = parent
        self.dm = data_manager
        self.COLORS = colors
        self.title = title
        self.categories = ['Food', 'Transport', 'Shopping', 'Bills', 
                                       'Entertainment', 'Healthcare', 'Other']
        self.create_title()
        self.content_area = tk.Frame(self.parent, bg=self.COLORS['primary'])
        
    
    def create_title(self):
        tk.Label(self.parent, text=self.title, font=('Arial', 20, 'bold'),
                fg=self.COLORS['accent'], bg=self.COLORS['primary']).pack(anchor='w', pady=20)
    
    
    def validate_amount(self, amount, field_name="Amount", min_value=0, max_value=99999):
        if amount < min_value:
            messagebox.showerror("Error", f"{field_name} must be at least {min_value}")
            return False
        if amount > max_value:
            messagebox.showerror("Error", f"{field_name} cannot exceed {max_value}")
            return False
        return True
    

    def create_input_field(self, parent, label_text, default_value=""):
        tk.Label(parent, text=label_text, font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(10, 5))
        
        entry = tk.Entry(parent, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        if default_value:
            entry.insert(0, default_value)
        entry.pack(fill='x', padx=20, pady=5)
        
        return entry
