from datetime import datetime
from utils.helpers import generate_staff_id  

class BankStaffMember:
    def __init__(self, bank_id, staff_name, staff_email, staff_username, staff_password, staff_role, staff_created_at=None, is_active=True):
        self.staff_id = generate_staff_id(staff_name)  
        self.bank_id = bank_id  
        self.staff_name = staff_name
        self.staff_email = staff_email
        self.staff_username = staff_username
        self.staff_password = staff_password  
        self.staff_role = staff_role
        self.staff_created_at = staff_created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = is_active

    def to_dict(self):
        return {
            "staff_id": self.staff_id,
            "bank_id": self.bank_id,
            "staff_name": self.staff_name,
            "staff_email": self.staff_email,
            "staff_username": self.staff_username,
            "staff_password": self.staff_password,
            "staff_role": self.staff_role,
            "staff_created_at": self.staff_created_at,
            "is_active": self.is_active,
        }
