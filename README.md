# 🏦 Python SQL Banking App

A simple console-based **banking system built with Python and SQLite**, designed to showcase secure data handling, database integration, and clean code structure.  
This project was originally built for a college course and later **refactored** to use SQL for persistent storage, along with CSV audit logging and preloaded test accounts for quick testing.

---

## 🚀 Features

- 🔐 **Secure 4-digit PIN hashing** (SHA-256) — no plaintext PINs stored  
- 🧾 **Checking and Savings accounts** with deposits, withdrawals, and balance updates  
- 🧠 **Basic statistics** — view average balances and users above the average  
- 📝 **CSV transaction audit logging** for transparent tracking  
- 👤 **Interactive account creation and deletion** via the console menu  
- 🧪 **Three preloaded test accounts** for instant use:
  - `alice` / PIN: `1111`  
  - `bob` / PIN: `2222`  
  - `carla` / PIN: `3333`

---

## 🧰 Tech Stack

- **Language:** Python 3  
- **Database:** SQLite (`bank.db` created automatically)  
- **Audit Logging:** CSV (`transactions.csv` auto-generated)  
- **No external libraries** — runs out of the box using only the Python standard library

---

## 🧪 How to Run

```bash
git clone https://github.com/alenchavez-dev/python-sql-banking-app.git
cd python-sql-banking-app
python3 main.py
