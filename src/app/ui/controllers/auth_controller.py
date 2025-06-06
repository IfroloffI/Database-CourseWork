from typing import Optional
from app.core.services.auth_service import AuthService
from app.core.services.client_service import ClientService
from app.ui.utils.app_storage import AppStorage


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
        self.client_service = ClientService()

    def authenticate(self, login: str, password: str) -> Optional[str]:
        user = self.auth_service.get_user_by_login(login)
        if user and self.auth_service.verify_password(password, user.password_hash):
            AppStorage.current_account = user
            if user.client_id:
                AppStorage.current_client = self.client_service.get_client_by_id(
                    user.client_id
                )
            return user.role
        return None

    def register(self, login: str, password: str, role: str = "user") -> Optional[int]:
        return self.auth_service.register_user(login, password, role)

    def create_client_for_user(self, auth_id: int, **client_data) -> bool:
        if self.client_service.add_client(**client_data):
            client_id = self.client_service.get_client_by_email(client_data["email"]).id
            return self.auth_service.link_client_to_auth(auth_id, client_id)
        return False
