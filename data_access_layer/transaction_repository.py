from data_access_layer.base_repository import BaseRepository

class TransactionsRepository(BaseRepository):
    def __init__(self):
        super().__init__("transactions")

    def add_transaction(self, transaction_data):
        transactions = self.load_data()
        transactions.append(transaction_data)
        self.save_data(transactions)

    def get_transaction_by_id(self, transaction_id):
        transactions = self.load_data()
        for txn in transactions:
            if txn.get("transaction_id") == transaction_id:
                return txn
        return None

    def update_transaction(self, transaction_id, updated_transaction):
        transactions = self.load_data()

        for index, txn in enumerate(transactions):
            if txn.get("transaction_id") == transaction_id:
                transactions[index] = updated_transaction
                self.save_data(transactions)
                return True

        return False

    def get_all_transactions(self):
        return self.load_data()
