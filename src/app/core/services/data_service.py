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

    def search_clients_by_name(self, full_name: str):
        return self.client_service.search_clients_by_name(full_name)

    def account_exists(self, account_id: int) -> bool:
        return self.account_service.account_exists(account_id)

    def get_all_accounts(self):
        return self.account_service.get_all_accounts()

    def get_client_accounts(self, client_id: int, account_type: str = None):
        return self.account_service.get_client_accounts(client_id, account_type)

    def get_account_transactions(self, account_id: int):
        return self.transaction_service.get_account_transactions(account_id)

    def get_client_transactions(self, client_id: int = None, account_id: int = None, transaction_type: str = None):
        return self.transaction_service.get_client_transactions(client_id, account_id, transaction_type)

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
            if not self.account_service._exists("clients", client_id):
                raise ValueError(f"Клиент с ID {client_id} не найден")

            with self.db.get_cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM accounts WHERE account_number = %s",
                    (account_number,),
                )
                if cursor.fetchone():
                    raise ValueError("Счёт с таким номером уже существует")

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
                print("Сумма пополнения должна быть положительной")
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

            success_from = self.account_service.update_balance(from_account_id, -amount)
            success_to = self.account_service.update_balance(to_account_id, amount)

            if success_from and success_to:
                self.transaction_service.add_transaction(
                    from_account_id=from_account_id,
                    to_account_id=to_account_id,
                    amount=amount,
                    transaction_type="transfer",
                    description=description,
                )
                return True
            else:
                print("Ошибка обновления баланса")
                return False

        except Exception as e:
            print(f"Ошибка при переводе: {e}")
            return False

    def make_manual_transaction(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: float,
        description: str = "",
        transaction_type: str = "manual",
    ):
        try:
            if from_account_id and to_account_id:
                from_acc = self.account_service.get_account_by_id(from_account_id)
                to_acc = self.account_service.get_account_by_id(to_account_id)

                if not from_acc or not to_acc:
                    print("Один из счетов не найден")
                    return False
                if amount <= 0:
                    print("Сумма должна быть положительной")
                    return False

                success_from = self.account_service.update_balance(
                    from_account_id, -amount
                )
                success_to = self.account_service.update_balance(to_account_id, amount)

                if success_from and success_to:
                    self.transaction_service.add_transaction(
                        from_account_id=from_account_id,
                        to_account_id=to_account_id,
                        amount=amount,
                        transaction_type=transaction_type,
                        description=description,
                    )
                return success_from and success_to

            elif to_account_id:
                success = self.account_service.update_balance(to_account_id, amount)
                if success:
                    self.transaction_service.add_transaction(
                        from_account_id=None,
                        to_account_id=to_account_id,
                        amount=amount,
                        transaction_type=transaction_type,
                        description=description,
                    )
                return success

            elif from_account_id:
                success = self.account_service.update_balance(from_account_id, -amount)
                if success:
                    self.transaction_service.add_transaction(
                        from_account_id=from_account_id,
                        to_account_id=None,
                        amount=amount,
                        transaction_type=transaction_type,
                        description=description,
                    )
                return success

            else:
                print("Не указаны ни один счёт")
                return False

        except Exception as e:
            print(f"Ошибка при добавлении ручной транзакции: {e}")
            return False

    def get_all_transactions(self):
        return self.transaction_service.get_all_transactions()

    def get_client_transactions(
        self, client_id: int, account_id: int = None, transaction_type: str = None
    ):
        return self.transaction_service.get_client_transactions(
            client_id, account_id, transaction_type
        )

    def get_monthly_summary(
        self, client_id: int, account_id: int = None, transaction_type: str = None
    ):
        try:
            transactions = self.transaction_service.get_client_transactions(
                client_id, account_id, transaction_type
            )

            income_by_month = {}
            expense_by_month = {}

            for t in transactions:
                month = t.transaction_date.strftime("%Y-%m")

                if t.transaction_type == "deposit":
                    income_by_month[month] = income_by_month.get(month, 0) + t.amount
                elif t.transaction_type == "transfer" and t.from_account_id:
                    expense_by_month[month] = expense_by_month.get(month, 0) + t.amount

            months = sorted(set(income_by_month.keys()) | set(expense_by_month.keys()))
            incomes = [income_by_month.get(m, 0) for m in months]
            expenses = [expense_by_month.get(m, 0) for m in months]

            return {"months": months, "incomes": incomes, "expenses": expenses}
        except Exception as e:
            print(f"Ошибка при загрузке данных по месяцам: {e}")
            return {"months": [], "incomes": [], "expenses": []}

    def get_transaction_type_summary(
        self, client_id: int, account_id: int = None, transaction_type: str = None
    ):
        try:
            transactions = self.transaction_service.get_client_transactions(
                client_id, account_id, transaction_type
            )
            summary = {"deposit": 0, "transfer": 0, "withdrawal": 0}

            for t in transactions:
                if t.transaction_type in summary:
                    summary[t.transaction_type] += 1

            return summary
        except Exception as e:
            print(f"Ошибка при распределении транзакций: {e}")
            return {"deposit": 0, "transfer": 0, "withdrawal": 0}

    def delete_transaction(self, transaction_id: int):
        return self.transaction_service.delete_transaction(transaction_id)
