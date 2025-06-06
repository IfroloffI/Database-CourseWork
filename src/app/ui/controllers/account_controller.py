from PyQt6.QtWidgets import QTableView
from app.ui.utils.base_table_model import BaseTableModel
from app.ui.controllers.base_controller import BaseController
from app.core.database.models import Account
from typing import Optional


class AccountController(BaseController):
    def load_client_accounts(self, client_id: int, table_view: QTableView):
        accounts = self.data_service.get_client_accounts(client_id)
        data = []
        for account in accounts:
            data.append(
                [
                    account.id,
                    account.account_number,
                    account.account_type,
                    f"{account.balance:.2f}",
                    account.currency,
                    account.opened_date.strftime("%Y-%m-%d"),
                    "Да" if account.is_active else "Нет",
                    account.created_at.strftime("%Y-%m-%d %H:%M"),
                    account.updated_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )
        headers = [
            "ID",
            "Номер счета",
            "Тип",
            "Баланс",
            "Валюта",
            "Дата открытия",
            "Активен",
            "Создан",
            "Обновлен",
        ]
        table_view.setModel(BaseTableModel(data, headers))

    def select_account(self, client_id: int, account_id: int) -> Optional[Account]:
        accounts = self.data_service.get_client_accounts(client_id)
        return next((a for a in accounts if a.id == account_id), None)

    def add_account(self, client_id: int, **data) -> bool:
        try:
            success = self.data_service.add_account(client_id=client_id, **data)
            if success:
                self.data_updated.emit()
            return success
        except Exception as e:
            self.show_error(f"Ошибка при добавлении счета: {str(e)}")
            return False

    def update_account(self, account_id: int, **data) -> bool:
        success = self.data_service.update_account(account_id, **data)
        if success:
            self.data_updated.emit()
        return success

    def delete_account(self, account_id: int) -> bool:
        success = self.data_service.delete_account(account_id)
        if success:
            self.data_updated.emit()
        return success
