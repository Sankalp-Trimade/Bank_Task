from data_access_layer.charges_repository import ChargesRepository
from business_layer.models.charges_model import Charges

class ChargesService:
    def __init__(self):
        self.repo = ChargesRepository()

    def create_default_charges_for_bank(self, bank_id):
        charges = Charges(
            bank_id=bank_id,
            same_bank_rtgs=0,
            same_bank_imps=5,
            other_bank_rtgs=2,
            other_bank_imps=6
        )
        self.repo.add_charge(charges.to_dict())
        return charges.to_dict()

    def get_charges_for_bank(self, bank_id):
        all_charges = self.repo.get_all_charges()
        for charge in all_charges:
            if charge['bank_id'] == bank_id:
                return charge
        return None

    def update_charges_for_bank(self, bank_id, updated_data):
        all_charges = self.repo.get_all_charges()
        for charge in all_charges:
            if charge['bank_id'] == bank_id:
                charge.update(updated_data)
                self.repo.save_all_charges(all_charges)
                return charge
        return None
