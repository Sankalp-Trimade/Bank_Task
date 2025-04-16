import datetime
from data_access_layer.account_repository import AccountRepository
from utils.helpers import generate_account_id, get_current_datetime, generate_transaction_id
from data_access_layer.bank_repository import BankRepository

class AccountService:
    def __init__(self):
        self.repo = AccountRepository()
        self.bank_repository = BankRepository()

    def create_account(self, bank_id, name, email, username, password):
        account_id = generate_account_id(name)
        account_data = {
            "id": account_id,
            "name": name,
            "email": email,
            "username": username,
            "password": password,
            "balance": 5000,
            "created_at": get_current_datetime()
        }
        username = username.strip().lower()
        self.repo.save_account(bank_id, account_data)
        return account_id

    def update_account(self, bank_id, account_id, updated_data):
        self.repo.update_account(bank_id, account_id, updated_data)

    def delete_account(self, bank_id, account_id):
        self.repo.delete_account(bank_id, account_id)

    def list_accounts(self, bank_id):
        return self.repo.get_all_accounts(bank_id)
    
    def login_account_holder(self, bank_id, username, password):
        return self.repo.authenticate_account(bank_id, username, password)

    def get_account_by_username(self, bank_id, username):
        username = username.strip().lower()
        bank_data = self.bank_repository.get_bank_by_id(bank_id)
        if not bank_data:
            return None

        for account in bank_data.get("accounts", []):
            if account["username"].strip().lower() == username:
                return account
        return None

    def deposit(self, bank_id, account_id, amount, currency="INR"):
        account = self.repo.get_account(bank_id, account_id)
        if not account:
            return None

        if amount <= 0:
            print("Invalid deposit amount!")
            return
        
        original_amount = amount  
        bank = self.bank_repository.get_bank_by_id(bank_id)  

        if not bank:
            print("❌ Bank not found!")
            return None
        
        if currency == "":
            currency = "INR"

        if currency != "INR" and currency not in bank["currencies"]:
            print(f"❌ Currency '{currency}' is not supported by this bank!")
            return None
        
        if currency != "INR":
            exchange_rate = bank["currencies"].get(currency)
            if exchange_rate:
                amount *= exchange_rate  
                print(f"\nCurrency Conversion:")
                print(f"Original Amount: {original_amount} {currency}")
                print(f"Converted Amount: {amount:.2f} INR\n")
            else:
                print(f"❌ Exchange rate not found for {currency}!")
                return None
        else:
            print("\nUsing INR as currency.")
        
        new_balance = account["balance"] + amount
        updated = self.repo.update_balance(bank_id, account_id, new_balance)
        if not updated:
            return None

        transaction_id = generate_transaction_id(bank_id, account_id)
        
        txn = {
            "txn_id": transaction_id,
            "username": account["username"],
            "type": "deposit",
            "amount": amount,
            "currency": currency,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.repo.add_transaction(bank_id, txn)
        
        account["balance"] = new_balance  
        
        print("\nTransaction Details:")
        print(f"Transaction ID: {transaction_id}")
        print(f"Account ID: {account['id']}")
        print(f"Amount Deposited: {amount:.2f} INR")
        print(f"New Balance: {new_balance:.2f} INR")
        print("Deposit Successful!\n")
        
        return account

    def withdraw(self, bank_id, account_id, amount):
        account = self.repo.get_account(bank_id, account_id)
        if not account:
            return None

        if account["balance"] < amount:
            return "insufficient"

        new_balance = account["balance"] - amount
        updated = self.repo.update_balance(bank_id, account_id, new_balance)
        if not updated:
            return None

        transaction_id = generate_transaction_id(bank_id, account_id)
        txn = {
            "txn_id": transaction_id,
            "username": account["username"],
            "type": "withdraw",
            "amount": amount,
            "currency": "INR",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.repo.add_transaction(bank_id, txn)

        account["balance"] = new_balance
        print("\nTransaction Details:")
        print(f"Transaction ID: {transaction_id}")
        print(f"Account ID: {account['id']}")
        print(f"Amount Withdrawn: {amount:.2f} INR")
        print(f"New Balance: {new_balance:.2f} INR")
        print("Withdrawal Successful!\n")
        return account  # Return the updated account

    def view_transactions(self, bank_id, username):
        all_txns = self.bank_repository.load_banks()
        bank = next((b for b in all_txns if b["id"] == bank_id), None)
        if not bank:
            return []

        transactions = bank.get("transactions", [])
        user_transactions = [
            txn for txn in transactions
            if txn.get("username") == username or
            txn.get("sender") == username or
            txn.get("receiver") == username
        ]
        return user_transactions

    def revert_transaction(self, bank_id, username, txn_id):
        banks_data = self.bank_repository.load_banks()
        bank = next((b for b in banks_data if b["id"] == bank_id), None)

        if not bank:
            return "❌ Bank not found."

        account = next((acc for acc in bank.get("accounts", []) if acc["username"] == username), None)
        transactions = bank.get("transactions", [])
        if not account or not transactions:
            return "❌ Account or transactions not found."

        original_txn = next((txn for txn in transactions if txn["txn_id"] == txn_id), None)
        if not original_txn:
            return "❌ Transaction not found."

        amount = original_txn["amount"]
        txn_type = original_txn["type"]
        charge = original_txn.get("charge", 0)

        revert_type = None
        note = ""

        if txn_type == "deposit":
            if account["balance"] < amount:
                return "❌ Cannot revert. Insufficient balance for withdrawal."
            account["balance"] -= amount
            revert_type = "revert_deposit"
            note = "Reverted a deposit transaction."

        elif txn_type == "withdraw":
            account["balance"] += amount
            revert_type = "revert_withdraw"
            note = "Reverted a withdrawal transaction."

        elif txn_type == "transfer":
            receiver_username = original_txn["receiver"]

            receiver_account = next((acc for acc in bank.get("accounts", []) if acc["username"] == receiver_username), None)
            receiver_bank = bank

            if not receiver_account:
                for b in banks_data:
                    if b["id"] != bank_id:
                        receiver_account = next((acc for acc in b.get("accounts", []) if acc["username"] == receiver_username), None)
                        if receiver_account:
                            receiver_bank = b
                            break

            if not receiver_account:
                return "❌ Receiver account not found."

            if receiver_account["balance"] < amount:
                return "❌ Cannot revert. Receiver has insufficient balance."

            account["balance"] += amount + charge
            receiver_account["balance"] -= amount
            revert_type = "revert_transfer"
            note = f"Reverted a transfer to {receiver_username}."

            if receiver_bank["id"] != bank_id:
                receiver_revert_txn = {
                    "txn_id": generate_transaction_id(receiver_bank["id"], receiver_account["id"]),
                    "username": receiver_username,
                    "type": "revert_receive_transfer",
                    "amount": amount,
                    "timestamp": get_current_datetime(),
                    "balance": receiver_account["balance"],
                    "note": f"Transfer from {username} was reverted."
                }
                receiver_bank.setdefault("transactions", []).append(receiver_revert_txn)

        else:
            return "❌ Unsupported transaction type for revert."

        revert_txn = {
            "txn_id": generate_transaction_id(bank_id, account["id"]),
            "username": username,
            "type": revert_type,
            "amount": amount,
            "timestamp": get_current_datetime(),
            "balance": account["balance"],
            "note": note
        }

        bank.setdefault("transactions", []).append(revert_txn)

        self.bank_repository.save_banks(banks_data)

        return f"✅ {revert_type.replace('_', ' ').capitalize()} recorded successfully."

    def transfer_funds(self, sender_bank_id, sender_username, receiver_username, amount, transfer_type, is_same_bank, receiver_bank_name=None):
        banks_data = self.bank_repository.load_banks()

        sender_bank = next((bank for bank in banks_data if bank["id"] == sender_bank_id), None)
        if not sender_bank:
            print("❌ Sender bank not found.")
            return None

        sender_account = next((acc for acc in sender_bank.get("accounts", []) if acc["username"] == sender_username), None)
        if not sender_account:
            print("❌ Sender account not found.")
            return None

        receiver_bank = None
        receiver_account = None

        if is_same_bank:
            receiver_bank = sender_bank
            receiver_account = next((acc for acc in receiver_bank.get("accounts", []) if acc["username"] == receiver_username), None)
        else:
            if not receiver_bank_name:
                print("❌ Receiver bank name is required for other bank transfers.")
                return None

            receiver_bank = next((bank for bank in banks_data if bank["name"].lower() == receiver_bank_name.lower()), None)
            if not receiver_bank:
                print(f"❌ No bank found with name '{receiver_bank_name}'.")
                return None

            receiver_account = next((acc for acc in receiver_bank.get("accounts", []) if acc["username"] == receiver_username), None)

        if not receiver_account:
            print("❌ Receiver account not found in the selected bank.")
            return None

        if sender_username == receiver_username and is_same_bank:
            print("❌ Cannot transfer to your own account.")
            return None

        charge_key = "charges_same_bank" if is_same_bank else "charges_other_bank"
        charge_str = sender_bank.get(charge_key, {}).get(transfer_type, "0%").replace("%", "")
        try:
            charge_percent = float(charge_str)
        except ValueError:
            print("❌ Invalid charge format.")
            return None

        charge_amount = round(amount * (charge_percent / 100), 2)
        total_debit = round(amount + charge_amount, 2)

        if sender_account["balance"] < total_debit:
            print(f"❌ Insufficient balance. Required: ₹{total_debit}, Available: ₹{sender_account['balance']}")
            return None

        sender_account["balance"] -= total_debit
        receiver_account["balance"] += amount

        txn_id = generate_transaction_id(sender_bank_id, sender_account["id"])
        txn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        txn_data = {
            "txn_id": txn_id,
            "type": "transfer",
            "sender": sender_username,
            "receiver": receiver_username,
            "amount": amount,
            "currency": "INR",
            "charge": charge_amount,
            "transfer_type": transfer_type,
            "timestamp": txn_time
        }

        sender_bank.setdefault("transactions", []).append(txn_data)

        if sender_bank != receiver_bank:
            receiver_bank.setdefault("transactions", []).append(txn_data.copy())

        self.bank_repository.save_banks(banks_data)

        return txn_data

    def get_account_balance(self, bank_id, username):
        account = self.get_account_by_username(bank_id, username)
        if not account:
            return "❌ Account not found."
        
        return f"💰 Current Balance for '{username}': ₹{account['balance']}"