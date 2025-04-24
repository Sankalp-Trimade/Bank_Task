from datetime import datetime
from utils.helpers import generate_bank_id 

class Bank:
    def __init__(self, bank_name, branch_code, ifsc_code, address, city, state, pincode, phone, created_at=None, is_active=True):
        self.bank_id = generate_bank_id(bank_name)
        self.bank_name = bank_name
        self.branch_code = branch_code
        self.ifsc_code = ifsc_code
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
        self.phone = phone
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = is_active

    def to_dict(self):
        return {
            "bank_id": self.bank_id,
            "bank_name": self.bank_name,
            "branch_code": self.branch_code,
            "ifsc_code": self.ifsc_code,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "phone": self.phone,
            "created_at": self.created_at,
            "is_active": self.is_active,
        }
