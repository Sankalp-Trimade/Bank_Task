from business_layer.services.currencies_service import CurrencyService

currency_service = CurrencyService()

def create_currency(bank_id):
    name = input("Enter currency name: ")
    price = float(input("Enter currency price: "))
    if currency_service.create_currency(bank_id, name, price):
        print("Currency added successfully.")
    else:
        print("Failed to add currency.")

def view_currencies(bank_id):
    currencies = currency_service.get_all_currencies(bank_id)
    if currencies:
        for c in currencies:
            print(f"ID: {c['currency_id']}, Name: {c['currency_name']}, Price: {c['currency_price']}, Created: {c['created_at']}")
    else:
        print("No currencies found.")

def update_currency(bank_id):
    currency_id = input("Enter currency ID to update: ")
    name = input("New name (leave blank to skip): ")
    price_input = input("New price (leave blank to skip): ")

    updated_data = {}
    if name:
        updated_data['currency_name'] = name
    if price_input:
        updated_data['currency_price'] = float(price_input)

    if updated_data and currency_service.update_currency(bank_id, currency_id, updated_data):
        print("Currency updated successfully.")
    else:
        print("Failed to update currency.")

def delete_currency(bank_id):
    currency_id = input("Enter currency ID to delete: ")
    if currency_service.delete_currency(bank_id, currency_id):
        print("Currency deleted (marked inactive).")
    else:
        print("Failed to delete currency.")
