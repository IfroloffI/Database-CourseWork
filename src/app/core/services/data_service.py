from app.core.database.connection import DatabaseConnection
from app.core.services.client_service import ClientService
from app.core.services.account_service import AccountService
from app.core.services.transaction_service import TransactionService


class DataService:
    def __init__(self):
        self.db = DatabaseConnection()
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

    def get_client_transactions(self, client_id: int):
        return self.transaction_service.get_client_transactions(client_id)

    def get_account_by_id(self, account_id: int):
        return self.account_service.get_account_by_id(account_id)

    def get_account_by_number(self, account_number: str):
        return self.account_service.get_account_by_number(account_number)

    def add_account(self, client_id: int, **data):
        return self.account_service.add_account(client_id, **data)

    def update_account(self, account_id: int, **data):
        return self.account_service.update_account(account_id, **data)

    def delete_account(self, account_id: int):
        return self.account_service.delete_account(account_id)

    def create_account(
        self,
        client_id: int,
        account_number: str,
        account_type: str,
        currency: str = "RUB",
    ) -> bool:
        try:
            success = self.account_service.add_account(
                client_id=client_id,
                account_number=account_number,
                account_type=account_type,
                currency=currency,
                balance=0.0,
                is_active=True,
            )
            return success
        except ValueError as ve:
            print(f"[INFO] Ошибка создания счёта: {ve}")
            return False
        except Exception as e:
            print(f"[ERROR] Ошибка при создании счёта: {e}")
            return False

    def deposit_to_account(self, account_id: int, amount: float) -> bool:
        try:
            account = self.account_service.get_account_by_id(account_id)
            if not account:
                print("Счёт не найден")
                return False

            if amount <= 0:
                print("Сумма должна быть положительной")
                return False

            updated = self.account_service.update_balance(account_id, amount)
            if updated:
                self.transaction_service.add_transaction(
                    from_account_id=None,
                    to_account_id=account_id,
                    amount=amount,
                    transaction_type="deposit",
                    description="Пополнение счёта",
                )
            return updated
        except Exception as e:
            print(f"Ошибка при пополнении: {e}")
            return False

    def make_transfer(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: float,
        description: str = "",
    ) -> bool:
        try:
            from_acc = self.account_service.get_account_by_id(from_account_id)
            to_acc = self.account_service.get_account_by_id(to_account_id)

            if not from_acc or not to_acc:
                print("Один из счетов не найден")
                return False
            if from_acc.balance < amount or amount <= 0:
                print("Недостаточно средств или некорректная сумма")
                return False

            balance_updated = self.account_service.update_balance(
                from_account_id, -amount
            )
            balance_updated &= self.account_service.update_balance(
                to_account_id, amount
            )

            if balance_updated:
                self.transaction_service.add_transaction(
                    from_account_id=from_account_id,
                    to_account_id=to_account_id,
                    amount=amount,
                    transaction_type="transfer",
                    description=description,
                )

            return balance_updated
        except Exception as e:
            print(f"Ошибка при переводе: {e}")
            return False
