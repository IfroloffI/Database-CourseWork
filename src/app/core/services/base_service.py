from typing import Optional
from app.core.database.connection import DatabaseConnection


class BaseService:
    def __init__(self):
        self.db = DatabaseConnection()

    def _exists(self, table: str, id: int) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(f"SELECT 1 FROM {table} WHERE id = %s", (id,))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Ошибка проверки существования записи в {table}: {e}")
            return False
