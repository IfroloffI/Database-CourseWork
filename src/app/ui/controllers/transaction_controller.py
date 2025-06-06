from PyQt6.QtWidgets import QTableView
from app.ui.utils.base_table_model import BaseTableModel
from app.ui.controllers.base_controller import BaseController
from app.core.database.models import Transaction, Account
from typing import Optional, List


class TransactionController(BaseController):
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        return self.data_service.get_transaction_by_id(transaction_id)

    def add_transaction(self, **data) -> bool:
        try:
            success = self.data_service.add_transaction(**data)
            if success:
                self.data_updated.emit()
            return success
        except Exception as e:
            self.show_error(f"Ошибка при добавлении транзакции: {str(e)}")
            return False

    def update_transaction(self, transaction_id: int, **data) -> bool:
        success = self.data_service.update_transaction(transaction_id, **data)
        if success:
            self.data_updated.emit()
        return success

    def delete_transaction(self, transaction_id: int) -> bool:
        success = self.data_service.delete_transaction(transaction_id)
        if success:
            self.data_updated.emit()
        return success

    def load_transactions(
        self,
        table_view: QTableView,
        client_id: int = None,
        account_id: int = None,
        accounts: List[Account] = None,
    ) -> str:
        if account_id:
            transactions = self.data_service.get_account_transactions(account_id)
            account = next((a for a in accounts if a.id == account_id), None)
            description = (
                f"Транзакции счета: {account.account_number}"
                if account
                else "Транзакции счета"
            )
        elif client_id:
            transactions = self.data_service.get_client_transactions(client_id)
            description = "Все транзакции клиента"
        else:
            transactions = self.data_service.get_all_transactions()
            description = "Все транзакции"

        if not accounts:
            accounts = (
                self.data_service.get_client_accounts(client_id) if client_id else []
            )

        data = []
        for t in transactions:
            from_acc = next(
                (a for a in accounts if a and a.id == t.from_account_id), None
            )
            to_acc = next((a for a in accounts if a and a.id == t.to_account_id), None)

            data.append(
                [
                    t.id,
                    from_acc.account_number if from_acc else "Внесение",
                    to_acc.account_number if to_acc else "",
                    f"{t.amount:.2f}",
                    t.transaction_type,
                    t.description or "",
                    t.transaction_date.strftime("%Y-%m-%d %H:%M"),
                    t.status,
                    t.created_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )

        headers = [
            "ID",
            "Отправитель",
            "Получатель",
            "Сумма",
            "Тип",
            "Описание",
            "Дата",
            "Статус",
            "Создана",
        ]
        table_view.setModel(BaseTableModel(data, headers))

        return description
