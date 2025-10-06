# 🏦 Python Banking App (SQL Edition)

A simple console-based banking application built with **Python** and **SQLite**.  
This project simulates a basic banking system with secure PIN hashing, persistent account storage, CSV transaction auditing, and built-in sample accounts for quick testing.  

Originally created for a college course, it has been **fully refactored** to demonstrate clean architecture, database integration, and practical security practices suitable for portfolio use.

---

## 🚀 Features

- 🔐 **Secure 4-digit PIN hashing** (SHA-256) — no plaintext PINs stored  
- 🧾 **Checking and Savings accounts** with deposits, withdrawals, and live balance updates  
- 🧠 **Basic statistics** — average balances and users above average  
- 📝 **CSV transaction audit logging** — secondary log for transparency  
- 🧍 **Create/Delete accounts** interactively through the console menu  
- 🧪 **Three preloaded test accounts** for instant use:
  - `alice` / PIN: `1111`  
  - `bob` / PIN: `2222`  
  - `carla` / PIN: `3333`

---

## 🧰 Tech Stack

- **Language:** Python 3  
- **Database:** SQLite (persistent `bank.db` file generated automatically)  
- **Audit Logging:** CSV (auto-generated `transactions.csv`)  
- **No external libraries** — runs entirely with the Python standard library

---

## 🧪 How to Run

```bash
git clone https://github.com/alenchavez-dev/python-banking-app.git
cd python-banking-app
python3 main.py
