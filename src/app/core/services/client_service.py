from typing import List, Optional
from app.core.database.models import Client
from app.core.services.base_service import BaseService


class ClientService(BaseService):
    def get_all_clients(self) -> List[Client]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, first_name, last_name, passport_number, 
                           phone_number, email, created_at, updated_at 
                    FROM clients 
                    ORDER BY last_name, first_name
                """
                )
                return [Client(*row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении клиентов: {e}")
            return []

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, first_name, last_name, passport_number, 
                           phone_number, email, created_at, updated_at 
                    FROM clients 
                    WHERE id = %s
                """,
                    (client_id,),
                )
                result = cursor.fetchone()
                return Client(*result) if result else None
        except Exception as e:
            print(f"Ошибка при получении клиента {client_id}: {e}")
            return None

    def client_exists(self, client_id: int) -> bool:
        return self._exists("clients", client_id)

    def add_client(self, **data) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM clients WHERE passport_number = %s",
                    (data["passport_number"],),
                )
                if cursor.fetchone():
                    raise Exception("Клиент с таким паспортом уже существует")

                cursor.execute(
                    """
                    INSERT INTO clients 
                    (first_name, last_name, passport_number, phone_number, email) 
                    VALUES (%s, %s, %s, %s, %s) 
                    RETURNING id
                    """,
                    (
                        data["first_name"],
                        data["last_name"],
                        data["passport_number"],
                        data.get("phone_number"),
                        data.get("email"),
                    ),
                )
                self.db.connection.commit()
                return True
        except Exception as e:
            self.db.connection.rollback()
            raise Exception(f"Ошибка добавления клиента: {str(e)}")

    def update_client(self, client_id: int, **data) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE clients 
                    SET first_name = %s, last_name = %s, passport_number = %s, 
                        phone_number = %s, email = %s, updated_at = NOW() 
                    WHERE id = %s
                """,
                    (
                        data["first_name"],
                        data["last_name"],
                        data["passport_number"],
                        data.get("phone_number"),
                        data.get("email"),
                        client_id,
                    ),
                )
                self.db.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка при обновлении клиента {client_id}: {e}")
            self.db.connection.rollback()
            return False

    def delete_client(self, client_id: int) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
                self.db.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка при удалении клиента {client_id}: {e}")
            self.db.connection.rollback()
            return False

    def get_client_by_email(self, email: str) -> Optional[Client]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, first_name, last_name, passport_number, 
                           phone_number, email, created_at, updated_at 
                    FROM clients 
                    WHERE email = %s
                    """,
                    (email,),
                )
                result = cursor.fetchone()
                return Client(*result) if result else None
        except Exception as e:
            print(f"Ошибка при получении клиента по email: {e}")
            return None
