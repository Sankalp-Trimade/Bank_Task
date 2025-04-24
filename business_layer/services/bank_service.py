from business_layer.models.bank_model import Bank
from data_access_layer.bank_repository import BankRepository
from utils.helpers import get_current_datetime

class BankService:
    def __init__(self):
        self.repo = BankRepository()

    def create_bank(self, name, branch_code, ifsc_code, address, city, state, pincode, phone):
        bank = Bank(
            bank_name=name,
            branch_code=branch_code,
            ifsc_code=ifsc_code,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            created_at=get_current_datetime(),
            is_active=True
        )
        self.repo.add_bank(bank.to_dict())
        return bank.to_dict()  

    def update_bank(self, bank_id, updated_data):
        existing_bank = self.repo.get_bank_by_id(bank_id)
        if not existing_bank:
            return False

        for key, value in updated_data.items():
            if key in existing_bank:
                existing_bank[key] = value

        return self.repo.update_bank(bank_id, existing_bank)

    def get_all_banks(self):
        return self.repo.get_all_banks()

    def get_bank_by_id(self, bank_id):
        return self.repo.get_bank_by_id(bank_id)

    def delete_bank(self, bank_id):
        existing_bank = self.repo.get_bank_by_id(bank_id)
        if not existing_bank:
            return False

        self.repo.delete_bank(bank_id)
        return True
