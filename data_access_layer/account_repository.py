import json
import datetime
from data_access_layer.bank_repository import BankRepository


DATA_FILE = "data/banks.json"

class AccountRepository:
    def __init__(self):
        self.file_path = DATA_FILE
        self.bank_repository = BankRepository()

    def _load_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def save_account(self, bank_id, account_data):
        data = self._load_data()
        for bank in data:
            if bank["id"] == bank_id:
                if "accounts" not in bank:
                    bank["accounts"] = []
                bank["accounts"].append(account_data)
        self._save_data(data)

    def update_account(self, bank_id, account_id, updated_data):
        data = self._load_data()
        for bank in data:
            if bank["id"] == bank_id:
                for account in bank.get("accounts", []):
                    if account["id"] == account_id:
                        account.update(updated_data)
        self._save_data(data)

    def delete_account(self, bank_id, account_id):
        data = self._load_data()
        for bank in data:
            if bank["id"] == bank_id:
                bank["accounts"] = [acc for acc in bank.get("accounts", []) if acc["id"] != account_id]
        self._save_data(data)

    def get_all_accounts(self, bank_id):
        data = self._load_data()
        for bank in data:
            if bank["id"] == bank_id:
                return bank.get("accounts", [])
        return []

    def authenticate_account(self, bank_id, username, password):
        data = self._load_data()
        for bank in data:  
            if bank["id"] == bank_id:
                for account in bank.get("accounts", []):
                    if account["username"] == username and account["password"] == password:
                        return account
        return None
    
    def add_transaction(self, bank_id, transaction):
        data = self._load_data()
        for bank in data:
            if bank["id"] == bank_id:
                if "transactions" not in bank:
                    bank["transactions"] = []
                bank["transactions"].append(transaction)
                self._save_data(data)
                return True
        return False
    
    def get_account(self, bank_id, account_id):
        with open(self.file_path, "r") as file:
            data = json.load(file)  
            
            for bank in data:
                if bank["id"] == bank_id:
                    for account in bank["accounts"]:
                        if account["id"] == account_id:
                            return account  
        return None  
    
    def update_balance(self, bank_id, account_id, new_balance):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        updated = False  
        for bank in data:
            if bank["id"] == bank_id:
                for account in bank.get("accounts", []):
                    if account["id"] == account_id:
                        account["balance"] = new_balance
                        updated = True
                        break

        if updated:
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
            return True

        return False

    def get_bank_by_id(self, bank_id):
        data = self._load_data()
        for bank in data:
            if bank["id"] == bank_id:
                return bank
        return None

    def get_transactions_by_account(self, bank_id, username):
        banks_data = self.bank_repository.load_banks()
        bank = next((b for b in banks_data if b["id"] == bank_id), None)

        if not bank:
            print("❌ Bank not found.")
            return []

        all_txns = bank.get("transactions", [])
        user_txns = []

        for txn in all_txns:
            if txn["type"] == "deposit" or txn["type"] == "withdraw":
                if txn.get("username", "").strip().lower() == username:
                    user_txns.append(txn)
            elif txn["type"] == "transfer":
                if txn.get("sender", "").strip().lower() == username or txn.get("receiver", "").strip().lower() == username:
                    user_txns.append(txn)

        return user_txns

