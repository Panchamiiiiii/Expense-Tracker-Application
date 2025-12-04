# Expense-Tracker-Application
A simple desktop Expense Tracker built with Tkinter and SQLite. Opens as a GUI window when you run the script — log daily expenses, set monthly budgets per category, get budget alerts, view reports, and export monthly data to CSV.

#Features

1)Add daily expenses: date, category, amount, note

2)Set monthly budgets per category (YYYY-MM)

3)Automatic alert when a category's monthly spending exceeds its budget

4)View total spending for a month and a Spending vs Budget report (inline)

5)Export transactions for a month to CSV

6)Desktop GUI that pops up on run (no terminal menus)

7)Small, single-file SQLite database created automatically

Tech stack

-Python 3.8+ (no external packages required)

-GUI: Tkinter (built into Python)

-Data storage: SQLite (file-based DB inside project folder)

-CSV export via Python csv module

Files

my_expense_app.py — main application (run this)

my_expenses.db — SQLite database (auto-created when app first runs)

expenses_YYYY-MM.csv — example CSV output when you export

(If you renamed the main file in your repo, update the instructions below accordingly.)

Getting started (Run in VSCode / locally)

Install Python
Ensure Python 3.8 or newer is installed. Verify with:

python --version


#Clone this repository

git clone <your-repo-url>
cd <repo-folder>


#Open in VSCode

File → Open Folder... → select the repository folder.

Run the app
Open VSCode terminal (View → Terminal) and run:

python my_expense_app.py


The GUI window will pop up. No other dependencies or setup required.

How to use (quick)

Fill in the Date, Category, Amount, and optional Note; click Add to record a transaction.

To set a monthly budget: enter Month (YYYY-MM), Category, Limit → Save Limit.

To check reports: enter Report Month (YYYY-MM) → click Monthly Total or Spending vs Limits.

To export the month's transactions to CSV: enter the month in Report Month and click Export CSV.

To edit: double-click a row to populate the input fields for convenience (then add a new transaction). To remove a row, select it and click Delete Selected.

#Database details

Database file: my_expenses.db (created in the same folder when app runs)

#Tables:

ledger — stores transactions (uid, tx_date, category, amount, note)

monthly_limits — stores budgets (ym, category, limit_amount)

You can open the .db with any SQLite viewer to inspect or back up data.
