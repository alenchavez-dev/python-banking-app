# Banking Management System
# Author: Alen Chavez
# Description:
# A small console banking app that lets users create accounts, log in with a hashed PIN,
# make checking/savings transactions, view basic balance statistics, and log activity to CSV.
# This was built as part of a college course but cleaned up and structured for my portfolio.

import json
import random
import hashlib
import csv
import os
from datetime import datetime
import statistics

DATA_FILE = 'customers.json'
CSV_LOG = 'transactions.csv'


# -------------------- Helper Functions --------------------

def hash_pin(pin: str) -> str:
    """Hashes a 4-digit PIN using SHA-256."""
    return hashlib.sha256(pin.encode()).hexdigest()


def ensure_csv_header():
    """Makes sure the transaction log file has a header. Creates it if missing."""
    if not os.path.exists(CSV_LOG):
        with open(CSV_LOG, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "username", "account_type", "old_balance", "amount", "new_balance"])


def log_transaction(username: str, account_type: str, old_balance: float, amount: float, new_balance: float):
    """Logs a transaction to transactions.csv with a timestamp."""
    ensure_csv_header()
    with open(CSV_LOG, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(timespec='seconds'),
                         username, account_type,
                         f"{old_balance:.2f}", f"{amount:.2f}", f"{new_balance:.2f}"])


def create_pin() -> str:
    """
    Prompts user for a 4-digit PIN or generates a random one.
    Returns the hashed version. This gives users flexibility while keeping storage secure.
    """
    tries = 0
    while tries < 3:
        pin_input = input("Enter a 4-digit PIN or type 'random' to generate one: ").strip()
        if pin_input.lower() == 'random':
            generated = str(random.randint(1000, 9999))
            print(f"Your generated PIN is: {generated}")
            return hash_pin(generated)
        if pin_input.isdigit() and len(pin_input) == 4:
            return hash_pin(pin_input)
        else:
            print("Invalid PIN. It must be exactly 4 digits.")
            tries += 1

    # If they fail 3 times, just give them a random one so the flow continues
    fallback = str(random.randint(1000, 9999))
    print(f"Failed to create PIN. Your new PIN is: {fallback}")
    return hash_pin(fallback)


def load_accounts():
    """Loads all accounts from customers.json, or returns an empty dict if the file doesn't exist."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_accounts(accounts):
    """Saves all account data to customers.json."""
    with open(DATA_FILE, 'w') as file:
        json.dump(accounts, file, indent=4, sort_keys=True)
    print("\nData Saved.")


def print_accounts_data(accounts):
    """Used during testing to quickly see current accounts (PINs are masked)."""
    print("\nCurrent Accounts Data:")
    for username, details in accounts.items():
        display = {**details}
        display['Pin'] = "<HASHED>"
        print(username, ":", display)


# -------------------- Core Features --------------------

def create_account(accounts):
    """Handles the entire account creation flow."""
    username = input("Enter new username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    if username in accounts:
        print("Username already exists.")
        return

    hashed_pin = create_pin()
    name = input("Enter your name: ").strip()

    # Basic validation on deposits
    try:
        checking_amount = float(input("Enter initial deposit for checking: "))
    except ValueError:
        print("Invalid amount. Defaulting to $0.00")
        checking_amount = 0.0

    try:
        savings_amount = float(input("Enter initial deposit for savings: "))
    except ValueError:
        print("Invalid amount. Defaulting to $0.00")
        savings_amount = 0.0

    accounts[username] = {
        'Pin': hashed_pin,
        'Name': name,
        'C': checking_amount,
        'S': savings_amount
    }

    save_accounts(accounts)
    print("Account created successfully.")


def delete_account(accounts):
    """Removes an account from the system."""
    username = input("Enter username to delete: ").strip()
    if username in accounts:
        del accounts[username]
        save_accounts(accounts)
        print("Account deleted successfully.")
    else:
        print("Username does not exist.")


def handle_transaction(accounts, username):
    """Performs a single deposit or withdrawal on either checking or savings."""
    print(f"Welcome {accounts[username]['Name']}")

    account_type = input('Enter C or S for Checking or Savings: ').upper().strip()
    if account_type not in ['C', 'S']:
        print("Invalid account type selected.")
        return

    print(f'Opening {account_type} Account...')
    old_balance = accounts[username][account_type]
    print(f'Balance: ${old_balance:,.2f}')

    try:
        amount = float(input('Enter transaction amount (negative for withdrawal): '))
        if old_balance + amount < 0:
            raise ValueError("Insufficient funds. Transaction cancelled.")
        new_balance = old_balance + amount
        accounts[username][account_type] = new_balance
        save_accounts(accounts)
        log_transaction(username, account_type, old_balance, amount, new_balance)
        print(f'Transaction complete. New balance is ${new_balance:,.2f}')
    except ValueError as e:
        print(f"Transaction error: {e}")


def reset_pin(accounts, username):
    """Called if the user fails their PIN 3 times. Lets them set a new one."""
    print("You have exceeded the maximum number of PIN attempts.")
    choice = input("Would you like to reset your PIN? (yes/no): ").strip().lower()
    if choice == 'yes':
        accounts[username]['Pin'] = create_pin()
        save_accounts(accounts)
        print("Your PIN has been reset. Please log in again to continue.")
    else:
        print("PIN not reset. Returning to menu.")


def make_transaction(accounts):
    """Authenticates the user and allows up to 4 transactions in one session."""
    username = input('Enter your username: ').strip()
    if username not in accounts:
        print("No such user exists.")
        return

    tries = 1
    while tries <= 3:
        pin_input = input('Enter your 4-digit PIN or 0 to exit: ').strip()
        if pin_input == '0':
            return
        if hash_pin(pin_input) != accounts[username]['Pin']:
            print(f'Invalid PIN. Attempt {tries} of 3.')
            if tries == 3:
                reset_pin(accounts, username)
            tries += 1
            continue

        # Logged in - allow multiple transactions
        for _ in range(4):
            handle_transaction(accounts, username)
        break


def view_statistics(accounts):
    """
    Shows average checking/savings balances across all users,
    and lists which users are above average. Just a simple reporting feature.
    """
    if not accounts:
        print("No accounts available.")
        return

    checking_balances = [details['C'] for details in accounts.values()]
    savings_balances = [details['S'] for details in accounts.values()]

    avg_checking = statistics.mean(checking_balances) if checking_balances else 0.0
    avg_savings = statistics.mean(savings_balances) if savings_balances else 0.0

    print(f"\nAverage Checking Account Balance: ${avg_checking:,.2f}")
    print(f"Average Savings Account Balance:  ${avg_savings:,.2f}")

    print("\nUsers above average (Checking):")
    above_checking = [u for u, d in accounts.items() if d['C'] > avg_checking]
    print(" - " + ", ".join(above_checking) if above_checking else " - None")

    print("\nUsers above average (Savings):")
    above_savings = [u for u, d in accounts.items() if d['S'] > avg_savings]
    print(" - " + ", ".join(above_savings) if above_savings else " - None")


# -------------------- Main Menu --------------------

def main_menu():
    """Main menu that runs in a loop until the user chooses to exit."""
    print("\n===== Cactus Bank =====")
    print("[1] Create Account")
    print("[2] Delete Account")
    print("[3] Make Transaction")
    print("[4] View Statistics")
    print("[5] Exit")
    return input("Enter your choice: ").strip()


def main():
    """Loads data and runs the main loop."""
    accounts = load_accounts()
    print("Welcome to Cactus Bank!")

    actions = {
        '1': create_account,
        '2': delete_account,
        '3': make_transaction,
        '4': view_statistics
    }

    while True:
        choice = main_menu()
        if choice == '5':
            break
        action = actions.get(choice)
        if action:
            action(accounts)
        else:
            print("Invalid choice. Please try again.")

    print("Goodbye!")


if __name__ == "__main__":
    main()
