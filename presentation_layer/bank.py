from business_layer.services.bank_service import BankService
from business_layer.services.charges_services import ChargesService

charges_service = ChargesService()

def create_bank():
    name = input("Enter bank name: ")
    branch_code = input("Enter branch code: ")
    ifsc_code = input("Enter IFSC code: ")
    address = input("Enter address: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    pincode = input("Enter pincode: ")
    phone = input("Enter phone number: ")

    service = BankService()
    created_bank = service.create_bank(
        name=name,
        branch_code=branch_code,
        ifsc_code=ifsc_code,
        address=address,
        city=city,
        state=state,
        pincode=pincode,
        phone=phone
    )
    charges_service.create_default_charges_for_bank(created_bank['bank_id'])
    return created_bank

def update_bank():
    bank_id = input("Enter the bank ID to update: ")
    print("Enter updated details (leave blank to skip):")
    fields = ["bank_name", "branch_code", "ifsc_code", "address", "city", "state", "pincode", "phone"]
    updated_data = {}

    for field in fields:
        value = input(f"{field.replace('_', ' ').capitalize()}: ")
        if value:
            updated_data[field] = value

    service = BankService()
    success = service.update_bank(bank_id, updated_data)
    return success

def get_all_banks():
    service = BankService()
    return service.get_all_banks()

def get_bank_by_id():
    bank_id = input("Enter bank ID: ")
    service = BankService()
    return service.get_bank_by_id(bank_id)

def delete_bank():
    bank_id = input("Enter bank ID to delete: ")
    service = BankService()
    return service.delete_bank(bank_id)
