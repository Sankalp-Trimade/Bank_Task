import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from presentation_layer.bank import (
    create_bank,
    update_bank,
    delete_bank,
    get_all_banks,
    get_bank_by_id
)
from presentation_layer.bank_staff import (
    signup_bank_staff,
    update_bank_staff,
    delete_bank_staff,
    list_all_staff,
    get_staff_by_id,
    login_bank_staff
)
from presentation_layer.account import (
    create_account,
    update_account,
    delete_account,
    list_all_accounts,
    get_account_by_id,
    login_account,
    view_balance
)
from presentation_layer.currencies import (
    create_currency,
    view_currencies,
    update_currency,
    delete_currency
)
from presentation_layer.charges import (
    view_charges,
    update_charges
)
from presentation_layer.transactions import (
    transfer_money, 
    revert_transaction, 
    view_transaction_history,
    deposit_money,
    withdraw_money,
    view_transaction_history_by_account
)


def main():
    while True:
        print("\n--- Welcome to Bank Management System ---")
        print("1. Setup a New Bank")
        print("2. Update Bank Details")
        print("3. List All Banks")
        print("4. View a Bank by ID")
        print("5. Delete a Bank")
        print("6. Login to a Bank")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n--- Setup a New Bank ---")
            result = create_bank()
            if result:
                print(f"Bank '{result['bank_name']}' created successfully with ID: {result['bank_id']}")
            else:
                print("Failed to create the bank.")

        elif choice == '2':
            print("\n--- Update Bank ---")
            success = update_bank()
            if success:
                print("Bank updated successfully.")
            else:
                print("Failed to update the bank.")

        elif choice == '3':
            banks = get_all_banks()
            if banks:
                print("\n--- List of All Banks ---")
                for bank in banks:
                    for key, value in bank.items():
                        print(f"{key}: {value}")
                    print("-" * 40)
            else:
                print("No banks found.")

        elif choice == '4':
            print("\n--- View Bank By ID ---")
            bank = get_bank_by_id()
            if bank:
                print("\n--- Bank Details ---")
                for key, value in bank.items():
                    print(f"{key}: {value}")
            else:
                print("Bank not found.")

        elif choice == '5':
            print("\n--- Delete Bank ---")
            success = delete_bank()
            if success:
                print("Bank deleted successfully.")
            else:
                print("Failed to delete the bank.")

        elif choice == '6':
            banks = get_all_banks()
            if not banks:
                print("No banks available to login.")
                continue

            print("\nAvailable Banks:")
            for idx, bank in enumerate(banks, start=1):
                print(f"{idx}. {bank['bank_name']}")

            try:
                selection = int(input("Select a bank number to login: "))
                if 1 <= selection <= len(banks):
                    selected_bank = banks[selection - 1]
                    bank_id = selected_bank['bank_id']
                    print("=" * 50)
                    print(f"\tWelcome to {selected_bank['bank_name']}")
                    print(f"\tBank ID: {bank_id}")
                    print("=" * 50)

                    while True:
                        print("\nPlease select your role:")
                        print("1. Sign up new Bank Staff")
                        print("2. Update Bank Staff")
                        print("3. Delete Bank Staff")
                        print("4. List All Bank Staff")
                        print("5. Get Staff by ID")
                        print("6. Login as a bank staff")
                        print("7. Login as an account holder")
                        print("8. Exit to Main Menu")
                        role_choice = input("Enter choice: ")

                        if role_choice == '1':
                            signup_bank_staff(bank_id)

                        elif role_choice == '2':
                            update_bank_staff(bank_id)

                        elif role_choice == '3':
                            delete_bank_staff(bank_id)

                        elif role_choice == '4':
                            list_all_staff(bank_id)

                        elif role_choice == '5':
                            get_staff_by_id(bank_id)

                        elif role_choice == '6':
                            print("\n--- Bank Staff Login ---")
                            staff_member = login_bank_staff(bank_id)

                            if staff_member:
                                print(f"\nWelcome, {staff_member['staff_name']}! You are logged in as '{staff_member['staff_role']}'.")

                                while True:
                                    print("\n========== Bank Staff Menu ==========")
                                    print("1. Create Account")
                                    print("2. Update Account")
                                    print("3. Delete Account")
                                    print("4. List all Account")
                                    print("5. Get Account by ID")
                                    print("6. Add New Currency")
                                    print("7. View Currencies")
                                    print("8. Update Currency")
                                    print("9. Delete Currency")
                                    print("10. Update Transfer Charges")
                                    print("11. View Transfer Charges")
                                    print("12. Revert Transaction")
                                    print("13. View Transaction History of an Account")
                                    print("14. Back to Main Menu")
                                    print("=====================================")

                                    staff_choice = input("Enter your choice: ")
                                    if staff_choice == '1':
                                        if create_account(bank_id):
                                            print("Account created successfully.")
                                        else:
                                            print("Failed to create account.")

                                    elif staff_choice == '2':
                                        if update_account(bank_id):
                                            print("Account updated successfully.")
                                        else:
                                            print("Failed to update account.")

                                    elif staff_choice == '3':
                                        if delete_account(bank_id):
                                            print("Account deleted successfully.")
                                        else:
                                            print("Failed to delete account.")

                                    elif staff_choice == '4':
                                        list_all_accounts(bank_id)

                                    elif staff_choice == '5':
                                        get_account_by_id(bank_id)

                                    elif staff_choice == "6":
                                        create_currency(bank_id)

                                    elif staff_choice == "7":
                                        view_currencies(bank_id)

                                    elif staff_choice == "8":
                                        update_currency(bank_id)

                                    elif staff_choice == "9":
                                        delete_currency(bank_id)
                                    
                                    elif staff_choice == "10":
                                        update_charges(bank_id)

                                    elif staff_choice == "11":
                                        view_charges(bank_id)

                                    elif staff_choice == "12":
                                        revert_transaction(bank_id)

                                    elif staff_choice == '13':
                                        account_name = input("Enter Account Holder Name: ")
                                        view_transaction_history_by_account(bank_id, account_name)

                                    elif staff_choice == '14':
                                        break

                                    else:
                                        print("Functionality coming soon...")
                            else:
                                print("Invalid credentials or you do not belong to this bank.")

                        elif role_choice == '7':
                            account_holder = login_account(bank_id)
                            if not account_holder:
                                print("Invalid username or password.")
                                break
                            account_id = account_holder['account_id']


                            if account_holder:
                                while True:
                                    print("\n========== Account Holder Menu ==========")
                                    print("1. Deposit Money")
                                    print("2. Withdraw Money")
                                    print("3. Transfer Money")
                                    print("4. View Balance")
                                    print("5. View Transaction History")
                                    print("6. Logout")
                                    print("=========================================")

                                    account_choice = input("Enter your choice: ")

                                    if account_choice == '1':
                                        deposit_money(bank_id, account_id)
                                        
                                    elif account_choice == '2':
                                        withdraw_money(bank_id, account_id)
                                        
                                    elif account_choice == '3':
                                        transfer_money(bank_id, account_id)

                                    elif account_choice == '4':
                                        view_balance(bank_id, account_id)

                                    elif account_choice == '5':
                                        view_transaction_history(bank_id, account_id)

                                    elif account_choice == '6':
                                        break

                                    else:
                                        print("Invalid choice. Try again.")

                        elif role_choice == '8':
                            print("Returning to main menu...\n")
                            break

                        else:
                            print("Invalid choice. Please try again.")

                else:
                    print("Invalid selection.")

            except ValueError:
                print("Please enter a valid number.")

        elif choice == '7':
            print("Exiting... Thank you for using the system!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
