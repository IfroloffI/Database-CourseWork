from typing import List, Optional
from app.core.database.models import Transaction
from app.core.services.base_service import BaseService


class TransactionService(BaseService):
    def get_account_transactions(self, account_id: int) -> List[Transaction]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, from_account_id, to_account_id, amount, 
                           transaction_type, description, transaction_date, status, created_at 
                    FROM transactions 
                    WHERE from_account_id = %s OR to_account_id = %s
                    ORDER BY transaction_date DESC
                """,
                    (account_id, account_id),
                )
                return [Transaction(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении транзакций счёта {account_id}: {e}")
            return []

    def get_client_transactions(
        self,
        client_id: int = None,
        account_id: int = None,
        transaction_type: str = None,
    ) -> List[Transaction]:
        try:
            query = """
                    SELECT t.id, t.from_account_id, t.to_account_id, t.amount,
                        t.transaction_type, t.description, t.transaction_date, t.status, t.created_at
                    FROM transactions t
                    JOIN accounts a ON a.id = t.from_account_id OR a.id = t.to_account_id
                """
            params = []

            if client_id:
                query += " WHERE a.client_id = %s"
                params.extend([client_id])

            if account_id:
                query += " AND (t.from_account_id = %s OR t.to_account_id = %s)"
                params.extend([account_id, account_id])
            if transaction_type and transaction_type != "Все":
                query += " AND t.transaction_type = %s"
                params.append(transaction_type)

            with self.db.get_cursor() as cursor:
                cursor.execute(query, tuple(params))
                return [Transaction(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении транзакций клиента: {e}")
            return []

    def get_all_transactions(self) -> List[Transaction]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, from_account_id, to_account_id, amount,
                           transaction_type, description, transaction_date, status, created_at
                    FROM transactions
                    ORDER BY transaction_date DESC
                    """
                )
                return [Transaction(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении всех транзакций: {e}")
            return []

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, from_account_id, to_account_id, amount,
                           transaction_type, description, transaction_date, status, created_at
                    FROM transactions
                    WHERE id = %s
                    """,
                    (transaction_id,),
                )
                result = cursor.fetchone()
                if result:
                    return Transaction(*result)
                else:
                    return None
        except Exception as e:
            print(f"Ошибка при получении транзакции по ID {transaction_id}: {e}")
            return None

    def add_transaction(self, **data) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO transactions 
                    (from_account_id, to_account_id, amount, transaction_type, description)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        data["from_account_id"],
                        data["to_account_id"],
                        data["amount"],
                        data["transaction_type"],
                        data.get("description", ""),
                    ),
                )
                self.db.connection.commit()
                return True
        except Exception as e:
            self.db.connection.rollback()
            print(f"Ошибка при добавлении транзакции: {e}")
            return False

    def update_transaction(self, transaction_id: int, **data) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE transactions SET
                    from_account_id = %s,
                    to_account_id = %s,
                    amount = %s,
                    transaction_type = %s,
                    description = %s
                    WHERE id = %s
                    """,
                    (
                        data["from_account_id"],
                        data["to_account_id"],
                        data["amount"],
                        data["transaction_type"],
                        data.get("description", ""),
                        transaction_id,
                    ),
                )
                self.db.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.db.connection.rollback()
            print(f"Ошибка при обновлении транзакции {transaction_id}: {e}")
            return False

    def delete_transaction(self, transaction_id: int) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM transactions WHERE id = %s",
                    (transaction_id,),
                )
                self.db.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.db.connection.rollback()
            print(f"Ошибка при удалении транзакции {transaction_id}: {e}")
            return False
