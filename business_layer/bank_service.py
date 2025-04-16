from data_access_layer.bank_repository import BankRepository
from utils.helpers import generate_bank_id, get_current_datetime

class BankService:
    def __init__(self):
        self.repo = BankRepository()

    def create_bank(self, name, branch_code, ifsc_code, address, city, state, pincode, phone):
        bank_id = generate_bank_id(name)

        bank_data = {
            "id": bank_id,
            "name": name,
            "branch_code": branch_code,
            "ifsc_code": ifsc_code,
            "address": address,
            "city": city,
            "state": state,
            "pincode": pincode,
            "phone": phone,
            "created_at": get_current_datetime(),
            "is_active": True,
            "charges_same_bank": {
                "RTGS": "0%",
                "IMPS": "5%"
            },
            "charges_other_bank": {
                "RTGS": "2%",
                "IMPS": "6%"
            },
            "accepted_currency": "INR"
        }

        self.repo.save_bank(bank_data)
        return bank_id

    def get_all_banks(self):
        return self.repo.get_all_banks()

    def update_transfer_charges(self, bank_id):
        banks = self.repo.load_banks()
        bank = next((b for b in banks if b["id"] == bank_id), None)
        if not bank:
            print("Bank not found.")
            return

        print("\nWhich type of transfer charge would you like to update?")
        print("1. Same Bank")
        print("2. Other Bank")
        choice = input("Enter choice (1 or 2): ")

        if choice == "1":
            transfer_type = "charges_same_bank"
        elif choice == "2":
            transfer_type = "charges_other_bank"
        else:
            print("Invalid choice.")
            return

        print("\nWhich transfer mode would you like to update?")
        print("1. RTGS")
        print("2. IMPS")
        mode_choice = input("Enter choice (1 or 2): ")

        if mode_choice == "1":
            mode = "RTGS"
        elif mode_choice == "2":
            mode = "IMPS"
        else:
            print("Invalid transfer mode.")
            return

        value = input(f"Enter new charge for {mode} (e.g., 5%): ").strip()

        # Check if the user entered a number without '%' sign
        if value.isdigit():  # If it's just a number
            value = f"{value}%"  # Append the percentage symbol

        # If the value already has '%', we'll accept it as is
        elif "%" not in value:
            print("Invalid percentage format.")
            return

        bank[transfer_type][mode] = value
        self.repo.save_banks(banks)
        print(f"{mode} charge for {transfer_type.replace('_', ' ')} updated to {value}.")

    def view_transfer_charges(self, bank_id):
        banks = self.repo.load_banks()
        bank = next((b for b in banks if b["id"] == bank_id), None)
        if not bank:
            print("Bank not found.")
            return

        print(f"\nTransfer Charges for {bank['name']}:")
        print("Same Bank Transfers:")
        for k, v in bank.get("charges_same_bank", {}).items():
            print(f"  {k}: {v}")

        print("\nOther Bank Transfers:")
        for k, v in bank.get("charges_other_bank", {}).items():
            print(f"  {k}: {v}")
