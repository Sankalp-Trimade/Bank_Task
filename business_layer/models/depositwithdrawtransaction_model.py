from datetime import datetime
from utils.helpers import generate_transaction_id

class DepositWithdrawTransaction:
    def __init__(self, bank_id, account_id, account_name, transfer_type, amount):
        self.transaction_id = generate_transaction_id(bank_id, account_id)
        self.bank_id = bank_id
        self.account_id = account_id
        self.account_name = account_name
        self.transfer_type = transfer_type
        self.amount = amount
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_reverted = False

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "bank_id": self.bank_id,
            "account_id": self.account_id,
            "account_name": self.account_name,
            "transfer_type": self.transfer_type,
            "amount": self.amount,
            "created_at": self.created_at,
            "is_reverted": self.is_reverted
        }
