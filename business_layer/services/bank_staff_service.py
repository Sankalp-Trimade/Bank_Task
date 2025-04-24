from business_layer.models.bank_staff_model import BankStaffMember
from data_access_layer.bank_staff_repository import BankStaffRepository

class BankStaffService:
    def __init__(self):
        self.repo = BankStaffRepository()

    def signup_staff(self, bank_id, name, email, username, password, role):
        staff = BankStaffMember(
            bank_id=bank_id,
            staff_name=name,
            staff_email=email,
            staff_username=username,
            staff_password=password,
            staff_role=role
        )
        self.repo.add_staff(staff.to_dict())
        return staff.to_dict()

    def update_staff(self, bank_id, staff_id, updated_data):
        staff = self.repo.get_staff_by_id(staff_id)
        if staff and staff['bank_id'] == bank_id:
            return self.repo.update_staff(staff_id, updated_data)
        return False

    def delete_staff(self, bank_id, staff_id):
        staff = self.repo.get_staff_by_id(staff_id)
        if staff and staff['bank_id'] == bank_id:
            return self.repo.delete_staff(staff_id)
        return False

    def get_all_staff_for_bank(self, bank_id):
        all_staff = self.repo.get_all_staff()
        return [staff for staff in all_staff if staff['bank_id'] == bank_id]

    def get_staff_by_id(self, bank_id, staff_id):
        staff = self.repo.get_staff_by_id(staff_id)
        if staff and staff['bank_id'] == bank_id:
            return staff
        return None

    def login_staff(self, bank_id, username, password):
        return self.repo.get_staff_by_credentials(bank_id, username, password)
