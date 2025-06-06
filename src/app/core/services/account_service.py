from typing import List, Optional
from app.core.database.models import Account
from app.core.services.base_service import BaseService


class AccountService(BaseService):
    def get_client_accounts(self, client_id: int) -> List[Account]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, client_id, account_number, account_type, 
                           balance, currency, opened_date, is_active, created_at, updated_at 
                    FROM accounts 
                    WHERE client_id = %s
                    ORDER BY opened_date DESC
                """,
                    (client_id,),
                )
                return [Account(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении счетов клиента {client_id}: {e}")
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
                raise Exception("Клиент не существует")

            with self.db.get_cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM accounts WHERE account_number = %s",
                    (data["account_number"],),
                )
                if cursor.fetchone():
                    raise Exception("Счет с таким номером уже существует")

                cursor.execute(
                    """
                    INSERT INTO accounts 
                    (client_id, account_number, account_type, 
                     balance, currency, is_active, opened_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                    RETURNING id
                    """,
                    (
                        client_id,
                        data["account_number"],
                        data["account_type"],
                        data["balance"],
                        data["currency"],
                        data["is_active"],
                    ),
                )
                self.db.connection.commit()
                return True
        except Exception as e:
            self.db.connection.rollback()
            raise Exception(f"Ошибка добавления счета: {str(e)}")

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
            print(f"Ошибка при обновлении счета {account_id}: {e}")
            self.db.connection.rollback()
            return False

    def delete_account(self, account_id: int) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
                self.db.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка при удалении счета {account_id}: {e}")
            self.db.connection.rollback()
            return False
