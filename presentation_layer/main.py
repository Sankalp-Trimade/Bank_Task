import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from business_layer.bank_service import BankService
from business_layer.account_service import AccountService
from business_layer.currency_service import CurrencyService
from data_access_layer.bank_repository import BankRepository



def main():
    service = BankService()
    account_service = AccountService()
    bank_repo = BankRepository()
    currency_service = CurrencyService(bank_repo)

    while True:
        print("\n--- Welcome to Bank Management System ---")
        print("1. Setup a New Bank")
        print("2. Login into a Bank")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Bank Name: ")
            branch_code = input("Branch Code: ")
            ifsc_code = input("IFSC Code: ")
            address = input("Address: ")
            city = input("City: ")
            state = input("State: ")
            pincode = input("Pincode: ")
            phone = input("Phone: ")

            bank_id = service.create_bank(name, branch_code, ifsc_code, address, city, state, pincode, phone)
            print(f"\n✅ Bank '{name}' created successfully with ID: {bank_id}\n")

        elif choice == "2":
            banks = service.get_all_banks()
            if not banks:
                print("⚠️ No banks found. Please create one first.")
                continue

            print("\n--- Available Banks ---")
            for idx, bank in enumerate(banks):
                print(f"{idx + 1}. {bank['name']} (ID: {bank['id']})")

            selected = input("Select a bank by number: ")

            try:
                selected_index = int(selected) - 1
                if 0 <= selected_index < len(banks):
                    selected_bank = banks[selected_index]
                    bank_id = selected_bank['id']

                    print("=" * 50)
                    print(f"\tWelcome to {selected_bank['name']} Bank")
                    print(f"\tBank ID: {bank_id}")
                    print("=" * 50)

                    while True:
                        print("\nPlease select your role:")
                        print("1. Sign up new Bank Staff")
                        print("2. Login as Bank Staff")
                        print("3. Login as Account Holder")
                        print("4. Exit to Main Menu")
                        role_choice = input("Enter choice: ")

                        if role_choice == "1":
                            from business_layer.bank_staff_service import BankStaffService

                            print("\n--- Staff Sign Up ---")
                            name = input("Full Name: ")
                            email = input("Email: ")
                            username = input("Username: ")
                            password = input("Password: ")
                            role = input("Role (e.g., Manager, Teller): ")

                            staff_service = BankStaffService()
                            staff_id = staff_service.signup_staff(bank_id, name, email, username, password, role)

                            print(f"\n✅ Staff '{name}' signed up successfully with ID: {staff_id}")

                        elif role_choice == "2":
                            from business_layer.bank_staff_service import BankStaffService

                            print("\n--- Bank Staff Login ---")
                            username = input("Username: ")
                            password = input("Password: ")

                            staff_service = BankStaffService()
                            staff_member = staff_service.login_staff(bank_id, username, password)

                            if staff_member:
                                print(f"\n✅ Welcome, {staff_member['name']}! You are logged in as '{staff_member['role']}'.")

                                while True:
                                    print("\n========== Bank Staff Menu ==========")
                                    print("1. Create Account")
                                    print("2. Update Account")
                                    print("3. Delete Account")
                                    print("4. View Transactions")
                                    print("5. Revert Transaction")
                                    print("6. Add New Currency")
                                    print("7. View Currencies")
                                    print("8. Update Currency")
                                    print("9. Delete Currency")
                                    print("10. Update Transfer Charges")
                                    print("11. View Transfer Charges")
                                    print("12. Back to Main Menu")
                                    print("=====================================")

                                    staff_choice = input("Enter your choice: ")

                                    if staff_choice == "1":
                                        print("\n--- Create Account ---")
                                        name = input("Account Holder Name: ")
                                        email = input("Email: ")
                                        username = input("Username: ")
                                        password = input("Password: ")

                                        account_id = account_service.create_account(bank_id, name, email, username, password)
                                        print(f"✅ Account created successfully with ID: {account_id}")

                                    elif staff_choice == "2":
                                        print("\n--- Update Account ---")
                                        account_id = input("Enter Account ID: ")
                                        print("Leave fields blank to skip updating them.")
                                        updated_fields = {}
                                        name = input("New Name: ")
                                        email = input("New Email: ")
                                        if name:
                                            updated_fields["name"] = name
                                        if email:
                                            updated_fields["email"] = email

                                        if updated_fields:
                                            account_service.update_account(bank_id, account_id, updated_fields)
                                            print("✅ Account updated successfully.")
                                        else:
                                            print("⚠️ No changes provided.")

                                    elif staff_choice == "3":
                                        print("\n--- Delete Account ---")
                                        account_id = input("Enter Account ID to delete: ")
                                        confirm = input(f"Are you sure you want to delete account {account_id}? (yes/no): ")
                                        if confirm.lower() == "yes":
                                            account_service.delete_account(bank_id, account_id)
                                            print("✅ Account deleted.")
                                        else:
                                            print("❌ Deletion cancelled.")
                                        
                                    elif staff_choice == "4":
                                        username = input("🔎 Enter the account username to view transactions: ").strip()
                                        account = account_service.get_account_by_username(bank_id, username)

                                        if account:
                                            transactions = account_service.view_transactions(bank_id, username)
                                            if transactions:
                                                print("\n📜 Transaction History:")
                                                for txn in transactions:
                                                    print(f"Transaction ID: {txn['txn_id']}")
                                                    print(f"Type: {txn['type'].capitalize()}")
                                                    print(f"Amount: {txn['amount']} {txn.get('currency', 'INR')}")
                                                    print(f"Date: {txn.get('timestamp', txn.get('date', 'N/A'))}")
                                                    print("-" * 40)
                                            else:
                                                print("ℹ️ No transactions found for this account.")
                                        else:
                                            print("❌ Account not found with the given username.")

                                    elif staff_choice == "5":
                                        username = input("Enter the username for transaction revert: ")
                                        txn_id = input("Enter the Transaction ID to revert: ")
                                        result = account_service.revert_transaction(bank_id, username, txn_id)
                                        print(result)

                                    elif staff_choice == "6":
                                        currency = input("Enter Currency Code (e.g., USD, EUR): ").upper()
                                        try:
                                            rate = float(input(f"Enter Exchange Rate for {currency}: "))
                                            result = currency_service.add_currency(bank_id, currency, rate)
                                            print(result)
                                        except ValueError:
                                            print("Invalid rate. Please enter a number.")

                                    elif staff_choice == "7":
                                        currencies = currency_service.view_currencies(bank_id)
                                        if currencies:
                                            print("Accepted Currencies and Exchange Rates:")
                                            for code, rate in currencies.items():
                                                print(f"{code}: {rate}")
                                        else:
                                            print("No currencies found for this bank.")

                                    elif staff_choice == "8":
                                        currency = input("Enter Currency Code to Update: ").upper()
                                        try:
                                            new_rate = float(input(f"Enter New Exchange Rate for {currency}: "))
                                            result = currency_service.update_currency(bank_id, currency, new_rate)
                                            print(result)
                                        except ValueError:
                                            print("Invalid rate. Please enter a number.")

                                    elif staff_choice == "9":
                                        currency = input("Enter Currency Code to Delete: ").upper()
                                        result = currency_service.delete_currency(bank_id, currency)
                                        print(result)

                                    elif staff_choice == "10":
                                        service.update_transfer_charges(bank_id)

                                    elif staff_choice == "11":
                                        service.view_transfer_charges(bank_id)

                                    elif staff_choice == "12":
                                        print("🔙 Returning to Role Menu.")
                                        break
                                    else:
                                        print("❌ Invalid choice. Please try again.")
                            else:
                                print("❌ Invalid username or password. Login failed.")

                        elif role_choice == "3":
                            print("\n--- Account Holder Login ---")
                            username = input("Enter Username: ")
                            password = input("Enter Password: ")

                            account_data = account_service.login_account_holder(bank_id, username, password)

                            if account_data:
                                print(f"\n===== Welcome, {account_data['name']}! =====")
                                print(f"Account ID: {account_data['id']}")
                                print(f"Current Balance: ₹{account_data['balance']} INR")

                                account_id = account_data['id']
                                username = account_data['username']
                                while True:
                                    print("\n======= Account Holder Menu =======")
                                    print("1. Deposit")
                                    print("2. Withdraw")
                                    print("3. Transfer Funds")
                                    print("4. View Transactions")
                                    print("5. Show Balance")
                                    print("6. Logout")
                                    print("====================================")

                                    user_choice = input("Enter choice: ")

                                    if user_choice == "1":
                                        try:
                                            amount = float(input("Enter deposit amount: "))

                                            currency = input("Enter currency type (default INR): ") or "INR"

                                            updated_account = account_service.deposit(bank_id, account_id, amount, currency)

                                            if updated_account:
                                                print(f"✅ ₹{amount} deposited successfully.")
                                                print(f"💰 New Balance: ₹{updated_account['balance']}")
                                            else:
                                                print("❌ Account not found.")
                                        except ValueError:
                                            print("❌ Invalid input. Please enter a valid number.")
                                    elif user_choice == "2":
                                        try:
                                            amount = float(input("Enter amount to withdraw: "))
                                            if amount > 0:
                                                result = account_service.withdraw(bank_id, account_id, amount)  
                                                if result == "insufficient":
                                                    print("❌ Insufficient balance.")
                                                elif result:
                                                    print(f"✅ ₹{amount} withdrawn successfully.")
                                                    print(f"💰 Remaining Balance: ₹{result['balance']}")
                                                else:
                                                    print("❌ Account not found.")
                                            else:
                                                print("❌ Amount must be greater than zero.")
                                        except ValueError:
                                            print("❌ Invalid input. Please enter a valid number.")

                                    
                                    elif user_choice == "3":
                                        to_bank_type = input("Transfer to (1) Same Bank (2) Other Bank: ").strip()
                                        is_same_bank = to_bank_type == "1"

                                        receiver_bank_name = None
                                        if not is_same_bank:
                                            receiver_bank_name = input("Enter Receiver's Bank Name: ").strip()

                                        transfer_type = input("Choose Transfer Type - RTGS or IMPS: ").strip().upper()
                                        receiver_username = input("Enter receiver's username: ").strip()

                                        try:
                                            amount = float(input("Enter amount to transfer (INR): "))
                                        except ValueError:
                                            print("❌ Invalid amount.")
                                            return

                                        txn = account_service.transfer_funds(
                                            sender_bank_id=bank_id,
                                            sender_username=username,
                                            receiver_username=receiver_username,
                                            amount=amount,
                                            transfer_type=transfer_type,
                                            is_same_bank=is_same_bank,
                                            receiver_bank_name=receiver_bank_name
                                        )

                                        if txn:
                                            print("✅ Transfer successful!")
                                            print(f"Transaction ID: {txn['txn_id']}")
                                            print(f"Amount: ₹{txn['amount']}")
                                            print(f"Charge: ₹{txn['charge']}")
                                            print(f"Receiver: {txn['receiver']}")
                                            print(f"Transfer Type: {txn['transfer_type']}")
                                            print(f"Time: {txn['timestamp']}")
                                        else:
                                            print("❌ Transfer failed.")

                                    elif user_choice == "4":
                                        transactions = account_service.view_transactions(bank_id, username)
                                        if transactions:
                                            print("\n📜 Transaction History:")
                                            for txn in transactions:
                                                print(f"Transaction ID: {txn['txn_id']}")
                                                print(f"Type: {txn['type'].capitalize()}")

                                                if txn["type"] == "transfer":
                                                    direction = "Sent" if txn.get("sender") == username else "Received"
                                                    other_party = txn["receiver"] if direction == "Sent" else txn["sender"]
                                                    print(f"Transfer Direction: {direction}")
                                                    print(f"Other Party: {other_party}")
                                                    print(f"Amount: {txn['amount']}")
                                                    print(f"Transfer Type: {txn.get('transfer_type', 'N/A')}")
                                                    print(f"Charge: {txn.get('charge', 0)}")
                                                else:
                                                    print(f"Amount: {txn['amount']}")

                                                print(f"Date: {txn.get('timestamp', txn.get('date', 'N/A'))}")
                                                print("-" * 40)  
                                        else:
                                            print("ℹ️ No transactions found.")

                                    elif user_choice == "5":
                                        result = account_service.get_account_balance(bank_id, username)
                                        print(result)

                                    elif user_choice == "6":
                                        print("👋 Logging out of Account Holder menu.")
                                        break
                                    else:
                                        print("❌ Invalid option. Try again.")

                            else:
                                print("❌ Invalid credentials. Please try again.")

                        elif role_choice == "4":
                            print("🔙 Returning to main menu.")
                            break

                        else:
                            print("❌ Invalid choice. Try again.")

                else:
                    print("❌ Invalid selection.")
            except ValueError:
                print("❌ Please enter a valid number.")


        elif choice == "3":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
