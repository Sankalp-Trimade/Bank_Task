from data_access_layer.account_repository import AccountRepository
from business_layer.models.account_model import Account

class AccountService:
    def __init__(self):
        self.repo = AccountRepository()

    def create_account(self, bank_id, name, email, username, password, balance):
        account = Account(
            bank_id=bank_id,
            account_name=name,
            account_email=email,
            account_username=username,
            account_password=password,
            account_balance=balance
        )
        self.repo.add_account(account.to_dict())
        return account.to_dict()

    def get_all_accounts(self, bank_id):
        return self.repo.get_accounts_by_bank_id(bank_id)

    def get_account_by_id(self, bank_id, account_id):
        account = self.repo.get_account_by_id(bank_id, account_id)
        return account if account and account['bank_id'] == bank_id else None

    def update_account(self, bank_id, account_id, updated_data):
        account = self.repo.get_account_by_id(bank_id, account_id)
        if account and account['bank_id'] == bank_id:
            return self.repo.update_account(bank_id, account_id, updated_data)
        return False

    def delete_account(self, bank_id, account_id):
        account = self.repo.get_account_by_id(bank_id, account_id)
        if account and account['bank_id'] == bank_id:
            return self.repo.delete_account(bank_id, account_id)
        return False

    def login_account(self, bank_id, username, password):
        return self.repo.get_account_by_credentials(bank_id, username, password)

    def get_account_balance(self, bank_id, account_id):
        account = self.repo.get_account_by_id(bank_id, account_id)
        if account:
            return account["account_balance"]
        return None
