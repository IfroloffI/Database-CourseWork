from app.core.services.client_service import ClientService
from app.core.services.account_service import AccountService
from app.core.services.transaction_service import TransactionService


class DataService:
    def __init__(self):
        self.client_service = ClientService()
        self.account_service = AccountService()
        self.transaction_service = TransactionService()

    def client_exists(self, client_id: int) -> bool:
        return self.client_service.client_exists(client_id)

    def get_all_clients(self):
        return self.client_service.get_all_clients()

    def get_client_by_id(self, client_id: int):
        return self.client_service.get_client_by_id(client_id)

    def add_client(self, **data):
        return self.client_service.add_client(**data)

    def update_client(self, client_id: int, **data):
        return self.client_service.update_client(client_id, **data)

    def delete_client(self, client_id: int):
        return self.client_service.delete_client(client_id)

    def account_exists(self, account_id: int) -> bool:
        return self.account_service.account_exists(account_id)

    def get_client_accounts(self, client_id: int):
        return self.account_service.get_client_accounts(client_id)

    def get_account_by_id(self, account_id: int):
        return self.account_service.get_account_by_id(account_id)

    def add_account(self, client_id: int, **data):
        return self.account_service.add_account(client_id, **data)

    def update_account(self, account_id: int, **data):
        return self.account_service.update_account(account_id, **data)

    def delete_account(self, account_id: int):
        return self.account_service.delete_account(account_id)

    def get_account_transactions(self, account_id: int):
        return self.transaction_service.get_account_transactions(account_id)

    def get_client_transactions(self, client_id: int):
        return self.transaction_service.get_client_transactions(client_id)

    def get_all_transactions(self):
        return self.transaction_service.get_all_transactions()

    def get_transaction_by_id(self, transaction_id: int):
        return self.transaction_service.get_transaction_by_id(transaction_id)

    def add_transaction(self, **data):
        return self.transaction_service.add_transaction(**data)

    def update_transaction(self, transaction_id: int, **data):
        return self.transaction_service.update_transaction(transaction_id, **data)

    def delete_transaction(self, transaction_id: int):
        return self.transaction_service.delete_transaction(transaction_id)
