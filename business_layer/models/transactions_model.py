from datetime import datetime
from utils.helpers import generate_transaction_id

class Transaction:
    def __init__(self, bank_id, sender_account_id, sender_account_name, transfer_type, amount, charge, is_same_bank,
                 receiver_account_id=None, receiver_account_name=None, receiver_bank_id=None, receiver_bank_name=None,
                 created_at=None, is_reverted=False):
        self.transaction_id = generate_transaction_id(bank_id, sender_account_id)
        self.bank_id = bank_id
        self.sender_account_id = sender_account_id
        self.sender_account_name = sender_account_name
        self.receiver_account_id = receiver_account_id
        self.receiver_account_name = receiver_account_name
        self.receiver_bank_id = receiver_bank_id
        self.receiver_bank_name = receiver_bank_name
        self.transfer_type = transfer_type
        self.amount = amount
        self.charge = charge
        self.is_same_bank = is_same_bank
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_reverted = is_reverted

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "bank_id": self.bank_id,
            "sender_account_id": self.sender_account_id,
            "sender_account_name": self.sender_account_name,
            "receiver_account_id": self.receiver_account_id,
            "receiver_account_name": self.receiver_account_name,
            "receiver_bank_id": self.receiver_bank_id,
            "receiver_bank_name": self.receiver_bank_name,
            "transfer_type": self.transfer_type,
            "amount": self.amount,
            "charge": self.charge,
            "is_same_bank": self.is_same_bank,
            "created_at": self.created_at,
            "is_reverted": self.is_reverted
        }
