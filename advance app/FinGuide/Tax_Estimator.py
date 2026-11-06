import tkinter as tk
from tkinter import messagebox

from Base_Finance_Module import BaseFinanceModule

# TAX ESTIMATOR CLASS
class TaxEstimator(BaseFinanceModule):

    def __init__(self, parent, colors):
        super().__init__(parent, None, colors, "Simple Tax Estimator")
        self.show_tax_calculator()


    # GUI COMPONENTS
    def create_card(self, title, width=500, height=500):
        card = tk.Frame(self.parent, bg=self.COLORS['secondary'], width=width, height=height)
        card.pack_propagate(False)
        
        title_label = tk.Label(card, text=title, font=('Arial', 14, 'bold'),
                              fg=self.COLORS['accent'], bg=self.COLORS['secondary'])
        title_label.pack(anchor='w', padx=20, pady=15)
        
        return card


    # TAX CALCULATOR FUNCTIONALITY
    def show_tax_calculator(self):
        tax_card = self.create_card("Tax Calculator")
        tax_card.pack(pady=20)
        
        # Annual income input field
        tk.Label(tax_card, text="Annual Income (RM)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(10, 5))
        self.tax_income = tk.Entry(tax_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.tax_income.pack(fill='x', padx=20, pady=5)
        
        # Deductions input field
        tk.Label(tax_card, text="Total Deductions (RM)", font=('Arial', 10),
                fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(anchor='w', padx=20, pady=(15, 5))
        self.tax_deductions = tk.Entry(tax_card, bg=self.COLORS['primary'], fg=self.COLORS['text'])
        self.tax_deductions.insert(0, "0")
        self.tax_deductions.pack(fill='x', padx=20, pady=5)
        
        # Calculate Tax button
        tk.Button(tax_card, text="Calculate Tax", command=self.calculate_tax,
                 bg=self.COLORS['success'], fg=self.COLORS['accent']).pack(pady=20)
        
        # Results display area
        self.tax_results = tk.Frame(tax_card, bg=self.COLORS['secondary'])
        self.tax_results.pack(fill='both', expand=True, padx=20, pady=10)


    def calculate_tax(self):
        try:
            annual_income = float(self.tax_income.get())
            deductions = float(self.tax_deductions.get())
            
            if not self.validate_amount(annual_income, "Annual Income", min_value=0):
                return
            if not self.validate_amount(deductions, "Deductions", min_value=0):
                return

            if annual_income < deductions:
                messagebox.showerror("Error", "Tax Deduction cannot be lower than Annual Income")
                return False

            # Calculate taxable income
            taxable_income = max(0, annual_income - deductions)
            
            # Progressive tax calculation based on tax brackets
            if taxable_income <= 10000:
                tax = taxable_income * 0.10
                rate = 10
            elif taxable_income <= 40000:
                tax = 1000 + (taxable_income - 10000) * 0.15
                rate = 15
            elif taxable_income <= 85000:
                tax = 5500 + (taxable_income - 40000) * 0.22
                rate = 22
            else:
                tax = 15400 + (taxable_income - 85000) * 0.28
                rate = 28
            
            # Calculate effective tax rate
            effective_rate = (tax / annual_income * 100) if annual_income > 0 else 0

            for widget in self.tax_results.winfo_children():
                widget.destroy()
            
            # Results data
            results = [
                ("Annual Income", f"RM{annual_income:,.2f}"),
                ("Deductions", f"RM{deductions:,.2f}"),
                ("Taxable Income", f"RM{taxable_income:,.2f}"),
                ("Marginal Tax Rate", f"{rate}%"),
                ("Estimated Tax", f"RM{tax:,.2f}"),
                ("Effective Rate", f"{effective_rate:.2f}%"),
                ("After-Tax Income", f"RM{annual_income - tax:,.2f}")
            ]
            
            # Display results header
            tk.Label(self.tax_results, text="=== Tax Estimation Summary ===", 
                    font=('Arial', 12, 'bold'), fg=self.COLORS['accent'], 
                    bg=self.COLORS['secondary']).pack(anchor='w', pady=5)
            
            # Display each result row
            for label, value in results:
                row_frame = tk.Frame(self.tax_results, bg=self.COLORS['secondary'])
                row_frame.pack(fill='x', pady=2)
                
                tk.Label(row_frame, text=label + ":", font=('Arial', 10),
                        fg=self.COLORS['text'], bg=self.COLORS['secondary']).pack(side='left')
                tk.Label(row_frame, text=value, font=('Arial', 10, 'bold'),
                        fg=self.COLORS['accent'], bg=self.COLORS['secondary']).pack(side='right')
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")