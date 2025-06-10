from typing import List, Optional
from app.core.database.models import Account
from app.core.services.base_service import BaseService


class AccountService(BaseService):
    def __init__(self):
        super().__init__()

    def get_client_accounts(
        self, client_id: int, account_type: str = None
    ) -> List[Account]:
        try:
            with self.db.get_cursor() as cursor:
                query = """
                    SELECT id, client_id, account_number, account_type, balance, currency, opened_date, is_active, created_at, updated_at
                    FROM accounts
                    WHERE 1=1
                """
                params = []

                if client_id:
                    query += " AND client_id = %s"
                    params.append(client_id)

                if account_type:
                    query += " AND account_type = %s"
                    params.append(account_type)

                cursor.execute(query, tuple(params))
                return [Account(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении счетов клиента: {e}")
            return []

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, client_id, account_number, account_type, 
                           balance, currency, opened_date, is_active, created_at, updated_at 
                    FROM accounts 
                    WHERE id = %s
                """,
                    (account_id,),
                )
                result = cursor.fetchone()
                return Account(*result) if result else None
        except Exception as e:
            print(f"Ошибка при получении счета {account_id}: {e}")
            return None

    def account_exists(self, account_id: int) -> bool:
        return self._exists("accounts", account_id)

    def add_account(self, client_id: int, **data) -> bool:
        try:
            if not self._exists("clients", client_id):
                raise ValueError("Клиент не существует")

            with self.db.get_cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM accounts WHERE account_number = %s",
                    (data["account_number"],),
                )
                if cursor.fetchone():
                    raise ValueError("Счет с таким номером уже существует")

            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO accounts 
                    (client_id, account_number, account_type, balance, currency, is_active, opened_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                    """,
                    (
                        client_id,
                        data["account_number"],
                        data["account_type"],
                        data.get("balance", 0.0),
                        data.get("currency", "RUB"),
                        data.get("is_active", True),
                    ),
                )
                self.db.connection.commit()
                return True
        except ValueError as ve:
            print(f"[INFO] Ошибка добавления счёта: {ve}")
            return False
        except Exception as e:
            self.db.connection.rollback()
            print(f"[ERROR] Ошибка добавления счёта: {e}")
            return False

    def update_account(self, account_id: int, **data) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE accounts 
                    SET account_number = %s, account_type = %s, balance = %s, 
                        currency = %s, is_active = %s, updated_at = NOW() 
                    WHERE id = %s
                """,
                    (
                        data["account_number"],
                        data["account_type"],
                        data["balance"],
                        data["currency"],
                        data["is_active"],
                        account_id,
                    ),
                )
                self.db.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.db.connection.rollback()
            print(f"Ошибка при обновлении счета {account_id}: {e}")
            return False

    def delete_account(self, account_id: int) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
                self.db.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.db.connection.rollback()
            print(f"Ошибка при удалении счета {account_id}: {e}")
            return False

    def get_account_by_number(self, account_number: str) -> Optional[Account]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, client_id, account_number, account_type,
                           balance, currency, opened_date, is_active, created_at, updated_at
                    FROM accounts 
                    WHERE account_number = %s
                    """,
                    (account_number,),
                )
                result = cursor.fetchone()
                return Account(*result) if result else None
        except Exception as e:
            print(f"Ошибка при получении счёта по номеру: {e}")
            return None

    def update_balance(self, account_id: int, amount: float) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    "UPDATE accounts SET balance = balance + %s, updated_at = NOW() WHERE id = %s",
                    (amount, account_id),
                )
                self.db.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.db.connection.rollback()
            print(f"Ошибка обновления баланса: {e}")
            return False

    def get_all_accounts(self) -> List[Account]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, client_id, account_number, account_type, 
                        balance, currency, opened_date, is_active, created_at, updated_at
                    FROM accounts
                    ORDER BY opened_date DESC
                """
                )
                return [Account(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении всех счетов: {e}")
            return []
