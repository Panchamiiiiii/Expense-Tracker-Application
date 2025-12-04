import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
DB = "expense_gui.db"
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year_month TEXT,
            category TEXT,
            budget REAL,
            UNIQUE(year_month, category)
        )
    """)
    conn.commit()
    conn.close()
def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    note = note_entry.get()
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    try:
        float(amount)
    except:
        messagebox.showerror("Error", "Enter a valid amount")
        return
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                (date, category, amount, note))
    conn.commit()
    year_month = date[:7]
    cur.execute("SELECT SUM(amount) FROM expenses WHERE category=? AND substr(date,1,7)=?",
                (category, year_month))
    total_spent = cur.fetchone()[0] or 0
    cur.execute("SELECT budget FROM budgets WHERE category=? AND year_month=?",
                (category, year_month))
    row = cur.fetchone()
    conn.close()
    if row:
        budget = row[0]
        if total_spent > budget:
            messagebox.showwarning(
                "Budget Exceeded",
                f"Budget exceeded for {category}!\nBudget: {budget}\nSpent: {total_spent}"
            )
        else:
            remaining = budget - total_spent
            messagebox.showinfo(
                "Budget Update",
                f"Expense added.\nRemaining budget for {category}: {remaining}"
            )
    else:
        messagebox.showinfo("Info", "Expense added (no budget set for category).")
def set_budget():
    month = budget_month_entry.get()
    category = budget_category_entry.get()
    amount = budget_amount_entry.get()
    if not month:
        month = datetime.today().strftime("%Y-%m")
    try:
        float(amount)
    except:
        messagebox.showerror("Error", "Invalid budget amount")
        return
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO budgets (year_month, category, budget)
        VALUES (?, ?, ?)
        ON CONFLICT(year_month, category)
        DO UPDATE SET budget=excluded.budget
    """, (month, category, amount))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Budget saved successfully!")
def show_total_spending():
    month = report_month_entry.get()
    if not month:
        month = datetime.today().strftime("%Y-%m")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expenses WHERE substr(date,1,7)=?", (month,))
    total = cur.fetchone()[0] or 0
    conn.close()
    messagebox.showinfo("Total Spending", f"Total spending in {month}: ₹{total}")
def show_spending_vs_budget():
    month = report_month_entry.get()
    if not month:
        month = datetime.today().strftime("%Y-%m")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT category, SUM(amount) 
        FROM expenses 
        WHERE substr(date,1,7)=?
        GROUP BY category
    """, (month,))
    spending = cur.fetchall()
    result = "Category      Spent     Budget     Difference\n\n"
    for cat, spent in spending:
        cur.execute("SELECT budget FROM budgets WHERE category=? AND year_month=?",
                    (cat, month))
        row = cur.fetchone()
        budget = row[0] if row else None

        if budget:
            diff = budget - spent
            result += f"{cat:<12} {spent:<8} {budget:<8} {diff:<8}\n"
        else:
            result += f"{cat:<12} {spent:<8} No Budget\n"

    conn.close()

    messagebox.showinfo("Spending vs Budget", result)
init_db()

root = tk.Tk()
root.title("Expense Tracker App")
root.geometry("600x500")
root.resizable(False, False)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Add Expense")

tk.Label(tab1, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(tab1)
date_entry.pack()

tk.Label(tab1, text="Category:").pack()
category_entry = tk.Entry(tab1)
category_entry.pack()

tk.Label(tab1, text="Amount:").pack()
amount_entry = tk.Entry(tab1)
amount_entry.pack()

tk.Label(tab1, text="Note:").pack()
note_entry = tk.Entry(tab1)
note_entry.pack()

tk.Button(tab1, text="Add Expense", command=add_expense).pack(pady=10)
tab2 = tk.Frame(notebook)
notebook.add(tab2, text="Set Budget")

tk.Label(tab2, text="Month (YYYY-MM):").pack()
budget_month_entry = tk.Entry(tab2)
budget_month_entry.pack()

tk.Label(tab2, text="Category:").pack()
budget_category_entry = tk.Entry(tab2)
budget_category_entry.pack()

tk.Label(tab2, text="Budget Amount:").pack()
budget_amount_entry = tk.Entry(tab2)
budget_amount_entry.pack()
tk.Button(tab2, text="Save Budget", command=set_budget).pack(pady=10)
tab3 = tk.Frame(notebook)
notebook.add(tab3, text="Reports")
tk.Label(tab3, text="Month (YYYY-MM):").pack()
report_month_entry = tk.Entry(tab3)
report_month_entry.pack()
tk.Button(tab3, text="Total Spending", command=show_total_spending).pack(pady=5)
tk.Button(tab3, text="Spending vs Budget", command=show_spending_vs_budget).pack(pady=5)
root.mainloop()
