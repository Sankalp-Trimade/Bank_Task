from business_layer.services.bank_staff_service import BankStaffService

staff_service = BankStaffService()

def signup_bank_staff(bank_id):
    print("\n--- Bank Staff Signup ---")
    name = input("Enter Staff Name: ")
    email = input("Enter Staff Email: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    role = input("Enter Role (e.g., Manager, Teller): ")

    created_staff = staff_service.signup_staff(
        bank_id=bank_id,
        name=name,
        email=email,
        username=username,
        password=password,
        role=role
    )

    if created_staff:
        print("\nBank staff created successfully:")
        print(f"Staff Name: {created_staff['staff_name']}")
        print(f"Staff ID: {created_staff['staff_id']}")
    else:
        print("Failed to create bank staff.")

def update_bank_staff(bank_id):
    print("\n--- Update Bank Staff ---")
    staff_id = input("Enter Staff ID to update: ")
    existing_staff = staff_service.get_staff_by_id(bank_id, staff_id)

    if not existing_staff:
        print("Staff not found or doesn't belong to your bank.")
        return

    print("Leave fields blank to skip updating them.")
    name = input("Enter new Staff Name: ")
    email = input("Enter new Staff Email: ")
    username = input("Enter new Username: ")
    password = input("Enter new Password: ")
    role = input("Enter new Role: ")

    updated_data = {}
    if name: updated_data["staff_name"] = name
    if email: updated_data["staff_email"] = email
    if username: updated_data["staff_username"] = username
    if password: updated_data["staff_password"] = password
    if role: updated_data["staff_role"] = role

    success = staff_service.update_staff(bank_id, staff_id, updated_data)
    if success:
        print("Staff updated successfully.")
    else:
        print("Failed to update staff.")

def delete_bank_staff(bank_id):
    print("\n--- Delete Bank Staff ---")
    staff_id = input("Enter Staff ID to delete: ")
    existing_staff = staff_service.get_staff_by_id(bank_id, staff_id)

    if not existing_staff:
        print("Staff not found or doesn't belong to your bank.")
        return

    success = staff_service.delete_staff(bank_id, staff_id)
    if success:
        print("Staff deleted successfully.")
    else:
        print("Failed to delete staff.")

def list_all_staff(bank_id):
    print("\n--- All Staff for Logged-in Bank ---")
    all_staff = staff_service.get_all_staff_for_bank(bank_id)

    if not all_staff:
        print("No staff found for this bank.")
        return

    for staff in all_staff:
        print("-" * 40)
        print(f"Staff ID: {staff['staff_id']}")
        print(f"Name: {staff['staff_name']}")
        print(f"Email: {staff['staff_email']}")
        print(f"Username: {staff['staff_username']}")
        print(f"Role: {staff['staff_role']}")
        print(f"Created At: {staff['staff_created_at']}")
        print(f"Active: {staff['is_active']}")

def get_staff_by_id(bank_id):
    print("\n--- Get Staff by ID ---")
    staff_id = input("Enter Staff ID: ")
    staff = staff_service.get_staff_by_id(bank_id, staff_id)

    if not staff:
        print("Staff not found or doesn't belong to your bank.")
        return

    print("-" * 40)
    print(f"Staff ID: {staff['staff_id']}")
    print(f"Name: {staff['staff_name']}")
    print(f"Email: {staff['staff_email']}")
    print(f"Username: {staff['staff_username']}")
    print(f"Role: {staff['staff_role']}")
    print(f"Created At: {staff['staff_created_at']}")
    print(f"Active: {staff['is_active']}")

def login_bank_staff(bank_id):
    username = input("Username: ")
    password = input("Password: ")

    staff_service = BankStaffService()
    staff_member = staff_service.login_staff(bank_id, username, password)

    return staff_member
