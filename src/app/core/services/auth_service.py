import bcrypt
from typing import Optional
from app.core.database.models import AuthUser, Client
from app.core.services.base_service import BaseService


class AuthService(BaseService):
    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def get_user_by_login(self, login: str) -> Optional[AuthUser]:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    "SELECT id, login, password_hash, role, client_id FROM auth WHERE login = %s",
                    (login,),
                )
                row = cursor.fetchone()
                if row:
                    return AuthUser(*row)
                return None
        except Exception as e:
            print(f"Ошибка при поиске пользователя: {e}")
            return None

    def register_user(
        self, login: str, password: str, role: str = "user"
    ) -> Optional[int]:
        """Возвращает ID созданного пользователя или None"""
        try:
            pwd_hash = self.hash_password(password)
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO auth (login, password_hash, role)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (login, pwd_hash, role),
                )
                self.db.connection.commit()
                return cursor.fetchone()[0]
        except Exception as e:
            self.db.connection.rollback()
            print(f"Ошибка регистрации пользователя: {e}")
            return None

    def link_client_to_auth(self, auth_id: int, client_id: int) -> bool:
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    "UPDATE auth SET client_id = %s WHERE id = %s", (client_id, auth_id)
                )
                self.db.connection.commit()
                return True
        except Exception as e:
            self.db.connection.rollback()
            print(f"Ошибка связи пользователя с клиентом: {e}")
            return False
