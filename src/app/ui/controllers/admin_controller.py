from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
from app.core.services.data_service import DataService


class AdminController(QObject):
    data_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.data_service = DataService()
        self.client_id = None

    def show_error(self, message: str):
        QMessageBox.critical(None, "Ошибка", message)

    def show_success(self, message: str):
        QMessageBox.information(None, "Успех", message)

    def get_all_clients(self):
        try:
            return self.data_service.get_all_clients()
        except Exception as e:
            self.show_error(f"Ошибка при загрузке клиентов: {str(e)}")
            return []

    def add_client(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        phone_number: str,
        email: str,
    ) -> bool:
        try:
            success = self.data_service.add_client(
                first_name=first_name,
                last_name=last_name,
                passport_number=passport_number,
                phone_number=phone_number,
                email=email,
            )
            if success:
                self.data_updated.emit()
            return success
        except ValueError as ve:
            self.show_error(str(ve))
            return False
        except Exception as e:
            self.show_error(f"Ошибка при добавлении клиента: {str(e)}")
            return False

    def update_client(self, client_id: int, **data) -> bool:
        try:
            success = self.data_service.update_client(client_id, **data)
            if success:
                self.data_updated.emit()
            return success
        except Exception as e:
            self.show_error(f"Ошибка при обновлении клиента: {str(e)}")
            return False

    def delete_client(self, client_id: int) -> bool:
        try:
            success = self.data_service.delete_client(client_id)
            if success:
                self.data_updated.emit()
            return success
        except Exception as e:
            self.show_error(f"Ошибка при удалении клиента: {e}")
            return False

    def get_all_accounts(self):
        try:
            return self.data_service.get_all_accounts()
        except Exception as e:
            self.show_error(f"Ошибка при получении всех счетов: {e}")
            return []

    def get_filtered_accounts(self, client_id: int = None, account_type: str = None):
        try:
            return self.data_service.get_client_accounts(client_id, account_type)
        except Exception as e:
            self.show_error(f"Ошибка при фильтрации счетов: {e}")
            return []

    def create_account(
        self,
        client_id: int,
        account_number: str,
        account_type: str,
        currency: str = "RUB",
    ) -> bool:
        try:
            success = self.data_service.create_account(
                client_id, account_number, account_type, currency=currency
            )
            if success:
                self.data_updated.emit()
            return success
        except Exception as e:
            self.show_error(f"Ошибка при создании счёта: {e}")
            return False

    def delete_account(self, account_id: int) -> bool:
        try:
            success = self.data_service.delete_account(account_id)
            if success:
                self.data_updated.emit()
            return success
        except Exception as e:
            self.show_error(f"Ошибка при удалении счёта: {e}")
            return False

    def get_all_transactions(self):
        try:
            return self.data_service.get_all_transactions()
        except Exception as e:
            self.show_error(f"Ошибка при загрузке транзакций: {e}")
            return []

    def get_filtered_transactions(
        self,
        client_id: int = None,
        account_id: int = None,
        transaction_type: str = None,
    ):
        try:
            return self.data_service.get_client_transactions(
                client_id, account_id, transaction_type
            )
        except Exception as e:
            self.show_error(f"Ошибка при фильтрации транзакций: {e}")
            return []

    def get_monthly_summary(
        self,
        client_id: int = None,
        account_id: int = None,
        transaction_type: str = None,
    ):
        try:
            return self.data_service.get_monthly_summary(
                client_id, account_id, transaction_type
            )
        except Exception as e:
            self.show_error(f"Ошибка при формировании ежемесячной статистики: {e}")
            return {"months": [], "incomes": [], "expenses": []}

    def get_transaction_type_summary(
        self,
        client_id: int = None,
        account_id: int = None,
        transaction_type: str = None,
    ):
        try:
            return self.data_service.get_transaction_type_summary(
                client_id, account_id, transaction_type
            )
        except Exception as e:
            self.show_error(f"Ошибка при распределении транзакций: {e}")
            return {"deposit": 0, "transfer": 0, "withdrawal": 0}

    def search_clients_by_name(self, full_name: str):
        try:
            return self.data_service.search_clients_by_name(full_name)
        except Exception as e:
            self.show_error(f"Ошибка при поиске клиентов: {e}")
            return []
