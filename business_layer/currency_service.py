import json
import os

class CurrencyService:
    def __init__(self, currency_repo):
        self.currency_repo = currency_repo
        self.file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks.json')

    def add_currency(self, bank_id, currency_code, exchange_rate):
        currency_code = currency_code.strip().upper()
        bank = self.currency_repo.get_bank_by_id(bank_id)
        if not bank:
            return "Bank not found."

        if "currencies" not in bank:
            bank["currencies"] = {}

        if currency_code in bank["currencies"]:
            return f"{currency_code} already exists with rate {bank['currencies'][currency_code]}."

        bank["currencies"][currency_code] = exchange_rate
        self.update_bank(bank)
        return f"{currency_code} added with exchange rate {exchange_rate}."

    def view_currencies(self, bank_id):
        bank = self.currency_repo.get_bank_by_id(bank_id)
        return bank.get("currencies", {}) if bank else {}

    def update_currency(self, bank_id, currency_code, new_rate):
        currency_code = currency_code.strip().upper()
        bank = self.currency_repo.get_bank_by_id(bank_id)

        if not bank or "currencies" not in bank:
            return "Currency list not found."

        if currency_code not in bank["currencies"]:
            return f"{currency_code} not found."

        bank["currencies"][currency_code] = new_rate
        self.update_bank(bank)
        return f"{currency_code} updated with new rate {new_rate}."

    def delete_currency(self, bank_id, currency_code):
        currency_code = currency_code.strip().upper()
        bank = self.currency_repo.get_bank_by_id(bank_id)

        if not bank or "currencies" not in bank:
            return "Currency list not found."

        if currency_code not in bank["currencies"]:
            return f"{currency_code} not found."

        del bank["currencies"][currency_code]
        self.update_bank(bank)
        return f"{currency_code} deleted successfully."

    def update_bank(self, updated_bank):
        try:
            if not os.path.exists(self.file_path):
                print("banks.json file does not exist.")
                return False

            with open(self.file_path, "r") as file:
                banks = json.load(file)

            bank_found = False
            for i, bank in enumerate(banks):
                if bank["id"] == updated_bank["id"]:
                    banks[i] = updated_bank
                    bank_found = True
                    break

            if not bank_found:
                print("Bank not found for update.")
                return False

            with open(self.file_path, "w") as file:
                json.dump(banks, file, indent=4)
            print("✅ Bank updated successfully.")
            return True

        except Exception as e:
            print(f"❌ Error while updating bank: {e}")
            return False