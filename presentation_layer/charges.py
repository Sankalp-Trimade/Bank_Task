# charges.py
from business_layer.services.charges_services import ChargesService

service = ChargesService()

def view_charges(bank_id):
    charge = service.get_charges_for_bank(bank_id)
    if charge:
        print("\n--- Charges Details ---")
        for key, value in charge.items():
            print(f"{key}: {value}")
    else:
        print("No charges found for this bank.")

def update_charges(bank_id):
    current = service.get_charges_for_bank(bank_id)
    if not current:
        print("No existing charges to update.")
        return

    print("Leave field blank to keep existing value.")
    updated_data = {}

    same_bank_rtgs = input(f"Same Bank RTGS ({current['same_bank_rtgs']}): ")
    if same_bank_rtgs:
        updated_data["same_bank_rtgs"] = float(same_bank_rtgs)

    same_bank_imps = input(f"Same Bank IMPS ({current['same_bank_imps']}): ")
    if same_bank_imps:
        updated_data["same_bank_imps"] = float(same_bank_imps)

    other_bank_rtgs = input(f"Other Bank RTGS ({current['other_bank_rtgs']}): ")
    if other_bank_rtgs:
        updated_data["other_bank_rtgs"] = float(other_bank_rtgs)

    other_bank_imps = input(f"Other Bank IMPS ({current['other_bank_imps']}): ")
    if other_bank_imps:
        updated_data["other_bank_imps"] = float(other_bank_imps)

    updated = service.update_charges_for_bank(bank_id, updated_data)
    if updated:
        print("Charges updated successfully.")
    else:
        print("Failed to update charges.")
