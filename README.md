# Banking Management System

A console-based banking app that supports:

- Create and delete accounts
- Login with **hashed 4-digit PINs** (SHA-256)
- Deposits and withdrawals for Checking (C) and Savings (S)
- Persistent storage via `customers.json`
- Optional **PIN reset** after 3 failed attempts
- **Transaction logging to CSV** (`transactions.csv`)
- **Statistics view** (averages & above-average users)
- Clean, modular structure

## How to Run
1. Ensure `main.py` and `customers.json` are in the same folder.
2. Run:
   ```bash
   python main.py
