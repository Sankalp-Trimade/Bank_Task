from datetime import datetime
from utils.helpers import generate_currency_id

class Currency:
    def __init__(self, bank_id, currency_name, currency_price, created_at=None, is_active=True):
        self.currency_id = generate_currency_id(currency_name)
        self.bank_id = bank_id
        self.currency_name = currency_name
        self.currency_price = currency_price
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = is_active

    def to_dict(self):
        return {
            "currency_id": self.currency_id,
            "bank_id": self.bank_id,
            "currency_name": self.currency_name,
            "currency_price": self.currency_price,
            "created_at": self.created_at,
            "is_active": self.is_active,
        }
