from data_access_layer.base_repository import BaseRepository

class ChargesRepository(BaseRepository):
    def __init__(self):
        super().__init__('charges')

    def add_charge(self, charge_data):
        data = self.load_data()
        data.append(charge_data)
        self.save_data(data)

    def get_all_charges(self):
        return self.load_data()

    def save_all_charges(self, charges_list):
        self.save_data(charges_list)

    def get_charges_by_bank_id(self, bank_id):
        charges_list = self.load_data()
        for charge in charges_list:
            if charge["bank_id"] == bank_id:
                return charge
        return None
