import json
import os

DATA_FILE = "data/banks.json"

class BankRepository:
    def __init__(self):
        self._ensure_data_file_exists()

    def _ensure_data_file_exists(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump([], f, indent=4)

    def save_bank(self, bank_data):
        banks = self.get_all_banks()
        banks.append(bank_data)
        with open(DATA_FILE, 'w') as f:
            json.dump(banks, f, indent=4)

    def get_all_banks(self):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)

    def save_bank_staff(self, bank_id, staff_data):
        banks = self.get_all_banks()
        for bank in banks:
            if bank["id"] == bank_id:
                if "staff" not in bank:
                    bank["staff"] = []
                bank["staff"].append(staff_data)
                break
        with open(DATA_FILE, 'w') as f:
            json.dump(banks, f, indent=4)

    def get_bank_by_id(self, bank_id):
        banks = self.get_all_banks()
        for bank in banks:
            if bank['id'] == bank_id:
                return bank
        return None
    
    def load_banks(self):
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    def save_banks(self, banks):
        with open(DATA_FILE, 'w') as file:
            json.dump(banks, file, indent=4)