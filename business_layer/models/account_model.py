from datetime import datetime
from utils.helpers import generate_account_id


class Account:
    def __init__(self, bank_id, account_name, account_email, account_username, account_password, account_balance, account_created_at=None, is_active=True):
        self.account_id = generate_account_id(account_name)
        self.bank_id = bank_id
        self.account_name = account_name
        self.account_email = account_email
        self.account_username = account_username
        self.account_password = account_password
        self.account_balance = account_balance
        self.account_created_at = account_created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = is_active

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "bank_id": self.bank_id,
            "account_name": self.account_name,
            "account_email": self.account_email,
            "account_username": self.account_username,
            "account_password": self.account_password,
            "account_balance": self.account_balance,
            "account_created_at": self.account_created_at,
            "is_active": self.is_active,
        }
