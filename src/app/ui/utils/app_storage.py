from typing import Optional
from app.core.database.models import Client, Account


class AppStorage:
    def __init__(self):
        self._current_client: Optional[Client] = None
        self._current_account: Optional[Account] = None

    @property
    def current_client(self) -> Optional[Client]:
        return self._current_client

    @current_client.setter
    def current_client(self, client: Optional[Client]):
        self._current_client = client

    @property
    def current_account(self) -> Optional[Account]:
        return self._current_account

    @current_account.setter
    def current_account(self, account: Optional[Account]):
        self._current_account = account
