from datetime import datetime
from business_layer.services.account_service import AccountService
from data_access_layer.bank_repository import BankRepository

account_service = AccountService()
bank_repo = BankRepository()

def create_account(bank_id):
    print("\n--- Create Account ---")
    name = input("Account Holder Name: ")
    email = input("Email: ")
    username = input("Username: ")
    password = input("Password: ")
    balance = float(input("Initial Balance: "))

    return account_service.create_account(bank_id, name, email, username, password, balance)

def update_account(bank_id):
    print("\n--- Update Account ---")
    account_id = input("Enter Account ID to update: ")
    account = account_service.get_account_by_id(bank_id, account_id)
    if not account:
        return False

    print("Leave fields blank to skip updating them.")
    name = input("New Name: ")
    email = input("New Email: ")
    username = input("New Username: ")
    password = input("New Password: ")

    updated_data = {}
    if name: updated_data["account_name"] = name
    if email: updated_data["account_email"] = email
    if username: updated_data["account_username"] = username
    if password: updated_data["account_password"] = password

    return account_service.update_account(bank_id, account_id, updated_data)

def delete_account(bank_id):
    print("\n--- Delete Account ---")
    account_id = input("Enter Account ID to delete: ")
    return account_service.delete_account(bank_id, account_id)

def list_all_accounts(bank_id):
    print("\n--- List of All Accounts ---")
    accounts = account_service.get_all_accounts(bank_id)
    
    if accounts:
        for acc in accounts:
            print(f"ID: {acc['account_id']}, Name: {acc['account_name']}, Email: {acc['account_email']}, Balance: ₹{acc['account_balance']}")
    else:
        print("No accounts found for this bank.")
    
    return accounts

def get_account_by_id(bank_id):
    print("\n--- Get Account by ID ---")
    account_id = input("Enter Account ID: ")
    account = account_service.get_account_by_id(bank_id, account_id)

    if account:
        print(f"\nAccount Details:")
        print(f"ID: {account['account_id']}")
        print(f"Name: {account['account_name']}")
        print(f"Email: {account['account_email']}")
        print(f"Username: {account['account_username']}")
        print(f"Balance: ₹{account['account_balance']}")
        print(f"Created At: {account['account_created_at']}")
        print(f"Status: {'Active' if account['is_active'] else 'Inactive'}")
    else:
        print("Account not found or doesn't belong to your bank.")

def login_account(bank_id):
    print("\n--- Account Holder Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    bank_name = bank_repo.get_bank_name_by_id(bank_id)
    account = account_service.login_account(bank_id, username, password)
    if account:
        now = datetime.now()
        formatted_date = now.strftime("%A, %d %B %Y")
        formatted_time = now.strftime("%I:%M %p")

        print("\n" + "=" * 50)
        print(f"Welcome, {account['account_name']}!")
        print(f"Account ID: {account['account_id']}")
        print(f"Logged into Bank: {bank_name}")
        print(f"Today is: {formatted_date}")
        print(f"Time: {formatted_time}")
        print("=" * 50 + "\n")
        return account
    else:
        print("Invalid credentials or account doesn't belong to this bank.")
        return None

def view_balance(bank_id, account_id):
    balance = account_service.get_account_balance(bank_id, account_id)
    if balance is not None:
        print(f"Your current account balance is: ₹{balance:.2f}")
    else:
        print("Account not found or unable to fetch balance.")
