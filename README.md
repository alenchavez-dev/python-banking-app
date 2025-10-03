# 🏦 Python Banking App

A simple console-based banking application built with **Python**.  
This project simulates a basic banking system with secure PIN hashing, account creation, checking/savings transactions, CSV transaction logging, and basic statistics.  

It was originally developed as part of a college course and later refactored and expanded to demonstrate clean code structure and practical security practices.

---

## 🚀 Features

- 🔐 **Secure 4-digit PIN hashing** (SHA-256) — no plaintext PINs stored  
- 🧾 **Checking and Savings accounts** with deposits & withdrawals  
- 🧠 **Basic account statistics** (average balances & above-average users)  
- 📝 **CSV transaction logging** (auto-generated file)  
- 👤 **Create/Delete accounts** interactively through the console menu

---

## 🧰 Tech Stack

- **Language:** Python 3  
- **Storage:** JSON (for accounts) + CSV (for transactions)  
- **No external libraries** required — runs out of the box

---

## 🧪 How to Run

1. **Clone the repository**  
  git clone https://github.com/alenchavez-dev/python-banking-app.git
  cd python-banking-app
  python3 main.py   # or 'python main.py' depending on your setup

2.
# Built-in test account
# Username: alen123
# PIN: 2222

The PIN is stored hashed in customers.json, but this account is provided so you can log in without creating a new one.

Alternatively, you can create your own account from the main menu to test the full account creation + hashing flow.
