from business_layer.models.currency_model import Currency
from data_access_layer.currencies_repository import CurrencyRepository

class CurrencyService:
    def __init__(self):
        self.repo = CurrencyRepository()

    def create_currency(self, bank_id, name, price):
        currency = Currency(bank_id, name, price)
        return self.repo.add_currency(currency.to_dict())

    def get_all_currencies(self, bank_id):
        return self.repo.get_all_currencies_by_bank(bank_id)

    def update_currency(self, bank_id, currency_id, updated_data):
        return self.repo.update_currency(bank_id, currency_id, updated_data)

    def delete_currency(self, bank_id, currency_id):
        return self.repo.delete_currency(bank_id, currency_id)
