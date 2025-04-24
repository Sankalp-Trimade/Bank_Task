from data_access_layer.base_repository import BaseRepository

class AccountRepository(BaseRepository):
    def __init__(self):
        super().__init__('accounts')

    def add_account(self, account_dict):
        data = self.load_data()
        data.append(account_dict)
        self.save_data(data)
        return True

    def get_account_by_id(self, bank_id, account_id):
        data = self.load_data()
        return next(
            (acc for acc in data if acc['account_id'] == account_id and acc['bank_id'] == bank_id),
            None
        )

    def get_accounts_by_bank_id(self, bank_id):
        data = self.load_data()
        return [acc for acc in data if acc['bank_id'] == bank_id]

    def update_account(self, bank_id, account_id, updated_data):
        data = self.load_data()
        for i, acc in enumerate(data):
            if acc['account_id'] == account_id and acc['bank_id'] == bank_id:
                data[i].update(updated_data)
                self.save_data(data)
                return True
        return False

    def delete_account(self, bank_id, account_id):
        data = self.load_data()
        new_data = [acc for acc in data if not (acc['account_id'] == account_id and acc['bank_id'] == bank_id)]
        if len(new_data) != len(data):
            self.save_data(new_data)
            return True
        return False

    def get_account_by_credentials(self, bank_id, username, password):
        data = self.load_data()
        for acc in data:
            if (
                acc['bank_id'] == bank_id and
                acc['account_username'] == username and
                acc['account_password'] == password and
                acc['is_active']
            ):
                return acc
        return None
