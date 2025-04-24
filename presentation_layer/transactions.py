from business_layer.services.transaction_services import TransactionService
from data_access_layer.transaction_repository import TransactionsRepository


service = TransactionService()
transaction_repo = TransactionsRepository()

def transfer_money(bank_id, sender_account_id):
    is_same_bank_input = input("Transfer within same bank? (yes/no): ").lower()
    is_same_bank = is_same_bank_input == "yes"
    transfer_type = input("Transfer type (IMPS/RTGS): ").upper()
    amount = float(input("Enter amount to transfer: "))

    if is_same_bank:

        receiver_account_name = input("Enter receiver's account holder name: ")
        transaction = service.perform_transfer(
            sender_account_id,
            amount,
            transfer_type,
            is_same_bank,
            bank_id,
            receiver_account_name=receiver_account_name
        )
    else:
        receiver_bank_name = input("Enter receiver's bank name: ")
        receiver_account_name = input("Enter receiver's account holder name: ")
        transaction = service.perform_transfer(
            sender_account_id,
            amount,
            transfer_type,
            is_same_bank,
            bank_id,
            receiver_bank_name=receiver_bank_name,
            receiver_account_name=receiver_account_name
        )

    if transaction:
        print("\nTransaction completed successfully!")
        print(f"Transaction ID: {transaction.transaction_id}")
        print(f"From: {transaction.sender_account_name} (ID: {transaction.sender_account_id})")
        if transaction.is_same_bank:
            print(f"To: {transaction.receiver_account_name} (ID: {transaction.receiver_account_id})")
        else:
            print(f"To: {transaction.receiver_account_name} at {transaction.receiver_bank_name} (Bank ID: {transaction.receiver_bank_id})")
        print(f"Amount: ₹{transaction.amount}")
        print(f"Charge Applied: ₹{transaction.charge}")
        print(f"Transfer Type: {transaction.transfer_type}")
        print(f"Date: {transaction.created_at}")
    else:
        print("\nTransaction failed. Please check account details, balance, or transfer configuration.")
 
def deposit_money(bank_id, account_id):
    currency_name = input("Enter currency (leave blank for INR): ").upper() or "INR"
    amount = float(input(f"Enter amount in {currency_name}: "))
    
    transaction = service.deposit_money(bank_id, account_id, currency_name, amount)
    
    if transaction:
        print("Deposit successful.")
    else:
        print("Deposit failed.")

def withdraw_money(bank_id, account_id):
    amount = float(input("Enter amount to withdraw (in INR): "))
    
    transaction = service.withdraw_money(bank_id, account_id, amount)
    
    if transaction:
        print("Withdrawal successful.")
    else:
        print("Withdrawal failed.")

def revert_transaction(bank_id):
    transaction_id = input("Enter Transaction ID to revert: ").strip()
    result = service.revert_transaction(transaction_id, bank_id)
    if result:
        print("Transaction has been successfully reverted.")
    else:
        print("Failed to revert the transaction. Please check the transaction ID or bank permissions.")

def view_transaction_history(bank_id, account_id):
    data = transaction_repo.get_all_transactions()
    transactions_found = False

    for txn in data:
        transfer_type = txn.get("transfer_type", "").upper()

        if transfer_type in ["DEPOSIT", "WITHDRAW"]:
            if txn.get("bank_id") != bank_id or txn.get("account_id") != account_id:
                continue

        elif not (
            (txn.get("sender_account_id") == account_id and txn.get("bank_id") == bank_id) or
            (txn.get("receiver_account_id") == account_id and txn.get("receiver_bank_id") == bank_id)
        ):
            continue

        transactions_found = True
        print(f"Transaction ID: {txn.get('transaction_id')}")
        print(f"Transfer Type: {txn.get('transfer_type')}")
        print(f"Amount: {txn.get('amount')}")
        print(f"Date: {txn.get('created_at')}")
        print(f"Transaction Status: {'Reverted' if txn.get('is_reverted') else 'Completed'}")

        if transfer_type in ['DEPOSIT', 'WITHDRAW']:
            print(f"Account ID: {txn.get('account_id')}")
            print(f"Account Name: {txn.get('account_name')}")
        else:
            print(f"Charge: {txn.get('charge')}")
            print(f"Sender: {txn.get('sender_account_name')} (ID: {txn.get('sender_account_id')})")
            print(f"Receiver: {txn.get('receiver_account_name')} (ID: {txn.get('receiver_account_id')})")

            if txn.get('is_same_bank'):
                print("Transaction Type: Same Bank")
            else:
                print("Transaction Type: Other Bank")
                print(f"Sender Bank: {txn.get('bank_id')}")
                print(f"Receiver Bank: {txn.get('receiver_bank_name')}")

        print("-" * 50)

    if not transactions_found:
        print("No transactions found for this account in the given bank.")

def view_transaction_history_by_account(bank_id, account_name):
    data = transaction_repo.get_all_transactions()
    transactions_found = False

    for txn in data:
        transfer_type = txn.get("transfer_type", "").upper()

        if transfer_type in ["DEPOSIT", "WITHDRAW"]:
            if txn.get("bank_id") == bank_id and txn.get("account_name") == account_name:
                pass
            else:
                continue

        elif not (
            (txn.get("sender_account_name") == account_name and txn.get("bank_id") == bank_id) or
            (txn.get("receiver_account_name") == account_name and txn.get("receiver_bank_id") == bank_id)
        ):
            continue

        transactions_found = True
        print(f"Transaction ID: {txn.get('transaction_id')}")
        print(f"Amount: {txn.get('amount')}")
        print(f"Transfer Type: {txn.get('transfer_type')}")
        print(f"Date: {txn.get('created_at')}")
        print(f"Status: {'Reverted' if txn.get('is_reverted') else 'Completed'}")

        if transfer_type in ["DEPOSIT", "WITHDRAW"]:
            print(f"Account Name: {txn.get('account_name')}")
        else:
            print(f"Sender: {txn.get('sender_account_name')}")
            print(f"Receiver: {txn.get('receiver_account_name')}")
            print(f"Charge: {txn.get('charge')}")

        print("-" * 50)

    if not transactions_found:
        print(f"No transactions found for {account_name} in bank {bank_id}.")
