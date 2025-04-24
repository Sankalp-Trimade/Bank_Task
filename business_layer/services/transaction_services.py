import business_layer.models.transactions_model as Transaction
import business_layer.models.depositwithdrawtransaction_model as DepositWithdrawTransaction
from data_access_layer.transaction_repository import TransactionsRepository
from data_access_layer.account_repository import AccountRepository
from data_access_layer.charges_repository import ChargesRepository
from data_access_layer.bank_repository import BankRepository
from data_access_layer.currencies_repository import CurrencyRepository

class TransactionService:
    def __init__(self):
        self.transaction_repo = TransactionsRepository()
        self.account_repo = AccountRepository()
        self.charges_repo = ChargesRepository()
        self.bank_repo = BankRepository()
        self.currency_repo = CurrencyRepository()

    def perform_transfer(self, sender_account_id, amount, transfer_type, is_same_bank, bank_id,
                         receiver_account_id=None, receiver_bank_name=None, receiver_account_name=None):
        sender = self.account_repo.get_account_by_id(bank_id, sender_account_id)
        if not sender:
            return None

        charges = self.charges_repo.get_charges_by_bank_id(bank_id)
        if not charges:
            return None

        charge_percent = (
            charges["same_bank_rtgs"] if transfer_type == "RTGS" else charges["same_bank_imps"]
        ) if is_same_bank else (
            charges["other_bank_rtgs"] if transfer_type == "RTGS" else charges["other_bank_imps"]
        )

        charge = float(amount) * float(charge_percent) / 100
        total_deduction = float(amount) + charge

        if float(sender["account_balance"]) < total_deduction:
            return None

        sender["account_balance"] -= total_deduction
        self.account_repo.update_account(bank_id, sender_account_id, sender)

        receiver_account = None
        receiver_bank_id = None

        if is_same_bank:
            all_accounts = self.account_repo.get_accounts_by_bank_id(bank_id)
            receiver_account = None
            receiver_account_id = None
            for acc in all_accounts:
                if acc["account_name"].lower() == receiver_account_name.lower():
                    receiver_account = acc
                    receiver_account_id = acc["account_id"]
                    break

            if not receiver_account:
                return None
            receiver_account["account_balance"] += float(amount)
            self.account_repo.update_account(bank_id, receiver_account_id, receiver_account)

        else:
            receiver_bank = self.bank_repo.get_bank_by_name(receiver_bank_name)
            if not receiver_bank:
                return None
            receiver_bank_id = receiver_bank["bank_id"]
            
            all_accounts = self.account_repo.get_accounts_by_bank_id(receiver_bank_id)
            receiver_account = None
            receiver_account_id = None
            for acc in all_accounts:
                if acc["account_name"].lower() == receiver_account_name.lower():
                    receiver_account = acc
                    receiver_account_id = acc["account_id"]
                    break

            if not receiver_account:
                return None

            receiver_account["account_balance"] += float(amount)
            self.account_repo.update_account(receiver_bank_id, receiver_account_id, receiver_account)

        transaction = Transaction.Transaction(
            bank_id=bank_id,
            sender_account_id=sender_account_id,
            sender_account_name=sender["account_name"],
            receiver_account_id = receiver_account["account_id"] if receiver_account else receiver_account_id,
            receiver_account_name = receiver_account["account_name"] if receiver_account else receiver_account_name,
            receiver_bank_id=bank_id if is_same_bank else receiver_bank_id,
            receiver_bank_name=self.bank_repo.get_bank_by_id(bank_id)["bank_name"] if is_same_bank else receiver_bank_name,
            transfer_type=transfer_type,
            amount=float(amount),
            charge=round(charge, 2),
            is_same_bank=is_same_bank
        )
        self.transaction_repo.add_transaction(transaction.to_dict())
        return transaction

    def deposit_money(self, bank_id, account_id, currency_name, amount):
        account = self.account_repo.get_account_by_id(bank_id, account_id)
        if not account:
            return None

        if currency_name == "INR":
            amount_in_inr = amount
        else:
            currencies = self.currency_repo.get_all_currencies_by_bank(bank_id)
            currency_obj = next((c for c in currencies if c["currency_name"] == currency_name), None)
            if not currency_obj:
                return None
            amount_in_inr = amount * currency_obj["currency_price"]

        new_balance = account["account_balance"] + amount_in_inr
        update_success = self.account_repo.update_account(bank_id, account_id, {"account_balance": new_balance})
        if not update_success:
            return None

        transaction = DepositWithdrawTransaction.DepositWithdrawTransaction(
            bank_id, account_id, account["account_name"], "DEPOSIT", amount_in_inr
        )
        self.transaction_repo.add_transaction(transaction.to_dict())
        return transaction

    def withdraw_money(self, bank_id, account_id, amount):
        account = self.account_repo.get_account_by_id(bank_id, account_id)
        if not account:
            return None

        if account["account_balance"] < amount:
            return None

        new_balance = account["account_balance"] - amount
        update_success = self.account_repo.update_account(bank_id, account_id, {"account_balance": new_balance})
        if not update_success:
            return None

        transaction = DepositWithdrawTransaction.DepositWithdrawTransaction(
            bank_id, account_id, account["account_name"], "WITHDRAW", amount
        )
        self.transaction_repo.add_transaction(transaction.to_dict())
        return transaction

    def revert_transaction(self, transaction_id, bank_id):
        transactions = self.transaction_repo.load_data()
        transaction_found = False

        for index, txn in enumerate(transactions):
            if txn["transaction_id"] == transaction_id:
                if txn["is_reverted"] or txn["bank_id"] != bank_id:
                    return False

                if txn["transfer_type"] in ["DEPOSIT", "WITHDRAW"]:
                    account = self.account_repo.get_account_by_id(bank_id, txn["account_id"])
                    if not account:
                        return False

                    if txn["transfer_type"] == "DEPOSIT":
                        new_balance = account["account_balance"] - txn["amount"]
                    elif txn["transfer_type"] == "WITHDRAW":
                        new_balance = account["account_balance"] + txn["amount"]
                    else:
                        return False

                    update_success = self.account_repo.update_account(bank_id, txn["account_id"], {"account_balance": new_balance})
                    if not update_success:
                        return False

                    txn["is_reverted"] = True
                    transactions[index] = txn
                    transaction_found = True
                    break

                elif txn["transfer_type"] in ["RTGS", "IMPS"]:
                    sender_account = self.account_repo.get_account_by_id(bank_id, txn["sender_account_id"])
                    receiver_account = self.account_repo.get_account_by_id(txn["receiver_bank_id"], txn["receiver_account_id"])

                    if not sender_account or not receiver_account:
                        return False

                    sender_account["account_balance"] += txn["amount"]
                    receiver_account["account_balance"] -= txn["amount"]

                    if txn.get("charge", 0) > 0:
                        sender_account["account_balance"] += txn["charge"]

                    sender_update = self.account_repo.update_account(bank_id, sender_account["account_id"], {"account_balance": sender_account["account_balance"]})
                    receiver_update = self.account_repo.update_account(txn["receiver_bank_id"], receiver_account["account_id"], {"account_balance": receiver_account["account_balance"]})

                    if not sender_update or not receiver_update:
                        return False

                    txn["is_reverted"] = True
                    transactions[index] = txn
                    transaction_found = True
                    break

        if transaction_found:
            self.transaction_repo.save_data(transactions)
            return txn
        else:
            return False
