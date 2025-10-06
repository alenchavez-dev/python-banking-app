# 🏦 Banking App (SQL Version with CSV Audit + Test Accounts)
# Author: Alen Chavez
# Description:
# A console-based banking application using SQLite as the primary datastore
# and CSV as a secondary audit trail. Includes 3 auto-loaded test accounts
# for easier testing.

import sqlite3
import hashlib
import csv
import os
from datetime import datetime

DB_FILE = "bank.db"
CSV_LOG = "transactions.csv"


# -------------------- Database Setup --------------------

def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        pin_hash TEXT NOT NULL,
        name TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        user_id INTEGER PRIMARY KEY,
        checking REAL DEFAULT 0,
        savings REAL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        account_type TEXT NOT NULL,
        old_balance REAL NOT NULL,
        amount REAL NOT NULL,
        new_balance REAL NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # ---- Add sample test accounts if database is empty ----
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]

    if user_count == 0:
        print("🧪 Adding 3 sample test accounts...")

        sample_users = [
            ("alice", hashlib.sha256("1111".encode()).hexdigest(), "Alice Smith", 1500.00, 500.00),
            ("bob", hashlib.sha256("2222".encode()).hexdigest(), "Bob Johnson", 2500.00, 1000.00),
            ("carla", hashlib.sha256("3333".encode()).hexdigest(), "Carla Gomez", 300.00, 700.00),
        ]

        for username, pin_hash, name, checking, savings in sample_users:
            cur.execute("INSERT INTO users (username, pin_hash, name) VALUES (?, ?, ?)", (username, pin_hash, name))
            user_id = cur.lastrowid
            cur.execute("INSERT INTO accounts (user_id, checking, savings) VALUES (?, ?, ?)",
                        (user_id, checking, savings))

        print("✅ Sample accounts created: alice (1111), bob (2222), carla (3333)")

    conn.commit()
    conn.close()


# -------------------- Helper Functions --------------------

def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()


def get_user(username):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, username, pin_hash, name FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, username, pin_hash, name FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row


def create_user(username, name, pin_hash, checking, savings):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, pin_hash, name) VALUES (?, ?, ?)", (username, pin_hash, name))
    user_id = cur.lastrowid
    cur.execute("INSERT INTO accounts (user_id, checking, savings) VALUES (?, ?, ?)",
                (user_id, checking, savings))
    conn.commit()
    conn.close()
    return user_id


def get_balance(user_id, account_type):
    column = "checking" if account_type == "C" else "savings"
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"SELECT {column} FROM accounts WHERE user_id = ?", (user_id,))
    balance = cur.fetchone()[0]
    conn.close()
    return balance


def update_balance(user_id, account_type, new_balance):
    column = "checking" if account_type == "C" else "savings"
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"UPDATE accounts SET {column} = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()


def ensure_csv_header():
    if not os.path.exists(CSV_LOG):
        with open(CSV_LOG, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "username", "account_type", "old_balance", "amount", "new_balance"])


def log_to_csv(username, account_type, old_balance, amount, new_balance):
    ensure_csv_header()
    with open(CSV_LOG, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(timespec='seconds'),
                         username, account_type,
                         f"{old_balance:.2f}", f"{amount:.2f}", f"{new_balance:.2f}"])


def record_transaction(user_id, account_type, old_balance, amount, new_balance):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions (user_id, account_type, old_balance, amount, new_balance, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, account_type, old_balance, amount, new_balance, datetime.now().isoformat(timespec='seconds')))
    conn.commit()
    conn.close()

    user = get_user_by_id(user_id)
    if user:
        log_to_csv(user[1], account_type, old_balance, amount, new_balance)


# -------------------- Core Features --------------------

def create_account():
    username = input("Enter new username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    if get_user(username):
        print("Username already exists.")
        return

    pin_input = input("Enter a 4-digit PIN: ").strip()
    if not (pin_input.isdigit() and len(pin_input) == 4):
        print("Invalid PIN format.")
        return

    name = input("Enter your name: ").strip()
    try:
        checking = float(input("Initial deposit for Checking: "))
    except ValueError:
        checking = 0.0
    try:
        savings = float(input("Initial deposit for Savings: "))
    except ValueError:
        savings = 0.0

    create_user(username, name, hash_pin(pin_input), checking, savings)
    print("✅ Account created successfully.")


def delete_account():
    username = input("Enter username to delete: ").strip()
    user = get_user(username)
    if not user:
        print("User not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE user_id = ?", (user[0],))
    cur.execute("DELETE FROM accounts WHERE user_id = ?", (user[0],))
    cur.execute("DELETE FROM users WHERE id = ?", (user[0],))
    conn.commit()
    conn.close()

    print("🗑 Account deleted successfully.")


def make_transaction():
    username = input("Enter your username: ").strip()
    user = get_user(username)
    if not user:
        print("No such user.")
        return

    pin = input("Enter your 4-digit PIN: ").strip()
    if hash_pin(pin) != user[2]:
        print("Invalid PIN.")
        return

    account_type = input("Enter C for Checking or S for Savings: ").strip().upper()
    if account_type not in ["C", "S"]:
        print("Invalid account type.")
        return

    old_balance = get_balance(user[0], account_type)
    print(f"Current balance: ${old_balance:,.2f}")

    try:
        amount = float(input("Enter transaction amount (negative for withdrawal): "))
    except ValueError:
        print("Invalid amount.")
        return

    if old_balance + amount < 0:
        print("❌ Insufficient funds.")
        return

    new_balance = old_balance + amount
    update_balance(user[0], account_type, new_balance)
    record_transaction(user[0], account_type, old_balance, amount, new_balance)

    print(f"✅ Transaction complete. New balance: ${new_balance:,.2f}")


def view_statistics():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT AVG(checking), AVG(savings) FROM accounts")
    avg_checking, avg_savings = cur.fetchone()

    print(f"\n📊 Average Checking: ${avg_checking or 0:,.2f}")
    print(f"📊 Average Savings:  ${avg_savings or 0:,.2f}")

    cur.execute("""
        SELECT u.username FROM users u
        JOIN accounts a ON u.id = a.user_id
        WHERE a.checking > ?
    """, (avg_checking,))
    above_checking = [row[0] for row in cur.fetchall()]

    cur.execute("""
        SELECT u.username FROM users u
        JOIN accounts a ON u.id = a.user_id
        WHERE a.savings > ?
    """, (avg_savings,))
    above_savings = [row[0] for row in cur.fetchall()]

    print("\nUsers above average (Checking):", ", ".join(above_checking) or "None")
    print("Users above average (Savings):", ", ".join(above_savings) or "None")

    conn.close()


# -------------------- Main Menu --------------------

def main_menu():
    print("\n===== Cactus Bank (SQL Edition) =====")
    print("[1] Create Account")
    print("[2] Delete Account")
    print("[3] Make Transaction")
    print("[4] View Statistics")
    print("[5] Exit")
    return input("Enter your choice: ").strip()


def main():
    init_db()
    while True:
        choice = main_menu()
        if choice == '1':
            create_account()
        elif choice == '2':
            delete_account()
        elif choice == '3':
            make_transaction()
        elif choice == '4':
            view_statistics()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
