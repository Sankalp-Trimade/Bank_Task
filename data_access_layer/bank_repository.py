from data_access_layer.base_repository import BaseRepository

class BankRepository(BaseRepository):
    def __init__(self):
        super().__init__('bank')

    def add_bank(self, bank_data):
        banks = self.load_data()
        banks.append(bank_data)
        self.save_data(banks)

    def get_all_banks(self):
        return self.load_data()

    def get_bank_by_id(self, bank_id):
        banks = self.load_data()
        for bank in banks:
            if bank['bank_id'] == bank_id:
                return bank
        return None

    def update_bank(self, bank_id, updated_data):
        banks = self.load_data()
        for idx, bank in enumerate(banks):
            if bank['bank_id'] == bank_id:
                banks[idx].update(updated_data)
                self.save_data(banks)
                return True
        return False

    def delete_bank(self, bank_id):
        banks = self.load_data()
        banks = [bank for bank in banks if bank['bank_id'] != bank_id]
        self.save_data(banks)

    def get_bank_by_name(self, bank_name):
        banks = self.load_data()
        for bank in banks:
            if bank["bank_name"].lower() == bank_name.lower():
                return bank
        return None
    
    def get_bank_name_by_id(self, bank_id):
        bank_repo = BankRepository()
        banks = bank_repo.get_all_banks()
        for bank in banks:
            if bank['bank_id'] == bank_id:
                return bank['bank_name']
        return False
    
    
