from datetime import datetime
from utils.helpers import generate_charges_id

class Charges:
    def __init__(self, bank_id, same_bank_rtgs, same_bank_imps, other_bank_rtgs, other_bank_imps, created_at=None, is_active=True):
        self.charges_id = generate_charges_id(bank_id)
        self.bank_id = bank_id
        self.same_bank_rtgs = same_bank_rtgs
        self.same_bank_imps = same_bank_imps
        self.other_bank_rtgs = other_bank_rtgs
        self.other_bank_imps = other_bank_imps
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = is_active

    def to_dict(self):
        return {
            "charges_id": self.charges_id,
            "bank_id": self.bank_id,
            "same_bank_rtgs": self.same_bank_rtgs,
            "same_bank_imps": self.same_bank_imps,
            "other_bank_rtgs": self.other_bank_rtgs,
            "other_bank_imps": self.other_bank_imps,
            "created_at": self.created_at,
            "is_active": self.is_active
        }
