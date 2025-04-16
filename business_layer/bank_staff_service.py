# import uuid
# from data_access_layer.bank_repository import BankRepository
# from utils.helpers import get_current_datetime

# class BankStaffService:
#     def __init__(self):
#         self.repo = BankRepository()

#     def generate_staff_id(self):
#         return f"STAFF-{uuid.uuid4().hex[:6].upper()}"

#     def signup_staff(self, bank_id, name, email, username, password, role):
#         staff_id = self.generate_staff_id()

#         staff_data = {
#             "id": staff_id,
#             "name": name,
#             "email": email,
#             "username": username,
#             "password": password,
#             "role": role,
#             "created_at": get_current_datetime()
#         }

#         self.repo.save_bank_staff(bank_id, staff_data)
#         return staff_id


import json
from utils.helpers import generate_staff_id
from data_access_layer.bank_repository import BankRepository
from utils.helpers import get_current_datetime

class BankStaffService:
    def __init__(self):
        self.repo = BankRepository()

    # Use the helper function from utils/helpers.py
    def signup_staff(self, bank_id, name, email, username, password, role):
        # Generate staff ID using the new logic
        staff_id = generate_staff_id(name, bank_id)  # Using bank_id for the bank name

        staff_data = {
            "id": staff_id,
            "name": name,
            "email": email,
            "username": username,
            "password": password,
            "role": role,
            "created_at": get_current_datetime()
        }

        # Save staff data into the repository (bank_staff)
        self.repo.save_bank_staff(bank_id, staff_data)
        return staff_id


    def login_staff(self, bank_id, username, password):
            # Get all bank staff from the bank data
            bank_data = self.repo.get_bank_by_id(bank_id)
            if not bank_data:
                return None  # Bank not found

            staff_members = bank_data.get("staff", [])
            for staff in staff_members:
                if staff["username"] == username and staff["password"] == password:
                    return staff  # Successful login
            return None  # Invalid credentials