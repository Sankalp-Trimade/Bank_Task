from data_access_layer.base_repository import BaseRepository

class CurrencyRepository(BaseRepository):
    def __init__(self):
        super().__init__('currencies')

    def add_currency(self, currency_dict):
        data = self.load_data()
        data.append(currency_dict)
        self.save_data(data)
        return True

    def get_all_currencies_by_bank(self, bank_id):
        data = self.load_data()
        return [currency for currency in data if currency['bank_id'] == bank_id and currency['is_active']]

    def update_currency(self, bank_id, currency_id, updated_data):
        data = self.load_data()
        for i, currency in enumerate(data):
            if currency['currency_id'] == currency_id and currency['bank_id'] == bank_id:
                data[i].update(updated_data)
                self.save_data(data)
                return True
        return False

    def delete_currency(self, bank_id, currency_id):
        data = self.load_data()
        new_data = [currency for currency in data if not (currency['currency_id'] == currency_id and currency['bank_id'] == bank_id)]
        
        if len(new_data) != len(data):
            self.save_data(new_data)
            return True

        return False
