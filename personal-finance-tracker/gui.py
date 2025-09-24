import tkinter as tk
from tkinter import ttk, messagebox
from tracker import FinanceTracker, Transaction
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime

tracker = FinanceTracker()

def add_transaction():
    try:
        amount = float(amount_entry.get())
        category = category_entry.get()
        trans_type = type_var.get()
        currency = currency_entry.get().upper()
        date = date_entry.get()

        if not category or not trans_type or not date:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format.")
            return


        converted_amount = tracker.convert_currency(amount, currency)

        if trans_type == "expense":
            current_balance = tracker.get_balance()
            if converted_amount > current_balance:
                messagebox.showerror(
                    "Insufficient Funds", 
                    f"Cannot add this expense. Available balance is only {current_balance:.2f} {tracker.BASE_CURRENCY}."
                )
                return

        transaction = Transaction(amount, category, trans_type, currency, date)
        tracker.add_transaction(transaction)
        update_tables()
        update_chart()
        clear_entries()
        messagebox.showinfo("Success", "Transaction added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")

def update_tables():
    
    for row in transactions_table.get_children():
        transactions_table.delete(row)
    
    for row in summary_table.get_children():
        summary_table.delete(row)
    
    for t in tracker.transactions:
        transactions_table.insert("", "end", values=(
            t['date'], 
            f"{t['amount']:.2f}", 
            t['currency'], 
            t['category'], 
            t['type'].capitalize()
        ))
    
    categories = tracker.get_by_category()
    expense_categories = {cat: amt for cat, amt in categories.items() 
                         if any(t['type'] == 'expense' and t['category'] == cat 
                               for t in tracker.transactions)}
    
    for category, amount in expense_categories.items():
        summary_table.insert("", "end", values=(category, f"{amount:.2f} EUR"))

    update_balance()    

def update_chart():
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    categories = tracker.get_by_category()
    expense_categories = {cat: amt for cat, amt in categories.items() 
                         if any(t['type'] == 'expense' and t['category'] == cat 
                               for t in tracker.transactions)}
    
    if not expense_categories:
        no_data_label = tk.Label(chart_frame, text="No expense data to display")
        no_data_label.pack(expand=True)
        return
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(
        expense_categories.values(), 
        labels=expense_categories.keys(), 
        autopct="%1.1f%%",
        startangle=90
    )
    
    ax.set_title("Spendings Chart")
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def update_balance():
    balance = tracker.get_balance()
    spending = tracker.get_total_expenses()
    
    balance_label.config(text=f"Available Balance: {balance:.2f} {tracker.BASE_CURRENCY}")
    spending_label.config(text=f"Total Spending: {spending:.2f} {tracker.BASE_CURRENCY}")


def clear_entries():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    currency_entry.delete(0, tk.END)
    currency_entry.insert(0, "EUR")
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    type_var.set("expense")

root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("1000x700")

main_container = tk.Frame(root, padx=10, pady=10)
main_container.pack(fill=tk.BOTH, expand=True)

header_label = tk.Label(main_container, text="Personal Finance Tracker", font=("Arial", 16, "bold"))
header_label.pack(pady=(0, 10))

balance_frame = tk.Frame(main_container)
balance_frame.pack(pady=(0, 10), fill=tk.X)

balance_label = tk.Label(balance_frame, text="", font=("Arial", 14), fg="blue")
balance_label.pack(side=tk.LEFT, padx=10)

spending_label = tk.Label(balance_frame, text="", font=("Arial", 14), fg="red")
spending_label.pack(side=tk.LEFT, padx=20)


top_section = tk.Frame(main_container)
top_section.pack(fill=tk.X, pady=(0, 10))

input_section = tk.LabelFrame(top_section, text="Add New Transaction", padx=10, pady=10, width=400)
input_section.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

fields = [
    ("Amount:", amount_entry := tk.Entry(input_section, width=15)),
    ("Category:", category_entry := tk.Entry(input_section, width=15)),
    ("Currency:", currency_entry := tk.Entry(input_section, width=15)),
    ("Date (YYYY-MM-DD):", date_entry := tk.Entry(input_section, width=15))
]

for i, (label_text, entry_widget) in enumerate(fields):
    tk.Label(input_section, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
    entry_widget.grid(row=i, column=1, padx=5, pady=5, sticky="w")
    
    if label_text == "Currency:":
        entry_widget.insert(0, "EUR")
    elif label_text == "Date (YYYY-MM-DD):":
        entry_widget.insert(0, datetime.now().strftime("%Y-%m-%d"))

tk.Label(input_section, text="Type:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
type_var = tk.StringVar(value="expense")
type_frame = tk.Frame(input_section)
type_frame.grid(row=4, column=1, padx=5, pady=5, sticky="w")
tk.Radiobutton(type_frame, text="Expense", variable=type_var, value="expense").pack(side=tk.LEFT)
tk.Radiobutton(type_frame, text="Income", variable=type_var, value="income").pack(side=tk.LEFT)

add_button = tk.Button(input_section, text="Add Transaction", command=add_transaction)
add_button.grid(row=5, column=0, columnspan=2, pady=10)


summary_frame = tk.LabelFrame(top_section, text="Expenses Summary")
summary_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


summary_table = ttk.Treeview(summary_frame, columns=("Category", "Summary"), show="headings", height=8)
summary_table.heading("Category", text="Category")
summary_table.heading("Summary", text="Summary")
summary_table.column("Category", width=150)
summary_table.column("Summary", width=100)
summary_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

scrollbar2 = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=summary_table.yview)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
summary_table.configure(yscrollcommand=scrollbar2.set)

bottom_section = tk.Frame(main_container)
bottom_section.pack(fill=tk.BOTH, expand=True)


transactions_frame = tk.LabelFrame(bottom_section, text="My Transactions")
transactions_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

transactions_table = ttk.Treeview(transactions_frame, columns=("Date", "Amount", "Currency", "Category", "Type"), 
                                 show="headings", height=12)
transactions_table.heading("Date", text="Date")
transactions_table.heading("Amount", text="Amount")
transactions_table.heading("Currency", text="Currency")
transactions_table.heading("Category", text="Category")
transactions_table.heading("Type", text="Type")

transactions_table.column("Date", width=100)
transactions_table.column("Amount", width=80)
transactions_table.column("Currency", width=70)
transactions_table.column("Category", width=120)
transactions_table.column("Type", width=100)

transactions_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

scrollbar1 = ttk.Scrollbar(transactions_frame, orient=tk.VERTICAL, command=transactions_table.yview)
scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
transactions_table.configure(yscrollcommand=scrollbar1.set)

chart_frame = tk.LabelFrame(bottom_section, text="Expenses Analytics")
chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

update_tables()
update_chart()

root.mainloop()