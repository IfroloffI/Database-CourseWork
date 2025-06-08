from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from app.core.services.data_service import DataService
from app.ui.utils.base_table_model import BaseTableModel


class UserController(QObject):
    data_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.data_service = DataService()
        self.selected_account_id = None

    @pyqtSlot()
    def show_error(self, message: str):
        QMessageBox.critical(None, "Ошибка", message)

    @pyqtSlot()
    def show_success(self, message: str):
        QMessageBox.information(None, "Успех", message)

    @pyqtSlot()
    def create_account(
        self, client_id: int, account_number: str, account_type: str
    ) -> bool:
        try:
            success = self.data_service.create_account(
                client_id, account_number, account_type
            )
            if success:
                self.data_updated.emit()
            else:
                self.show_error("Не удалось создать счёт")
            return success
        except ValueError as ve:
            self.show_error(str(ve))
            return False
        except Exception as e:
            self.show_error(f"Ошибка при создании счёта: {str(e)}")
            return False

    @pyqtSlot()
    def get_client_accounts(self, client_id: int):
        try:
            accounts = self.data_service.get_client_accounts(client_id)
            self.data_updated.emit()
            return accounts
        except Exception as e:
            self.show_error(f"Ошибка загрузки счетов: {str(e)}")
            return []

    @pyqtSlot()
    def get_selected_account_balance(self, account_id: int) -> float:
        try:
            account = self.data_service.get_account_by_id(account_id)
            if account:
                return account.balance
            else:
                self.show_error("Счёт не найден")
                return 0.0
        except Exception as e:
            self.show_error(f"Ошибка получения баланса: {str(e)}")
            return 0.0

    @pyqtSlot()
    def transfer_funds(
        self,
        from_account_id: int,
        to_account_number: str,
        amount: float,
        description: str = "",
    ) -> bool:
        if amount <= 0:
            self.show_error("Сумма перевода должна быть положительной")
            return False

        try:
            to_account = self.data_service.get_account_by_number(to_account_number)
            if not to_account:
                self.show_error("Счёт получателя не найден")
                return False

            success = self.data_service.make_transfer(
                from_account_id, to_account.id, amount, description
            )

            if success:
                self.data_updated.emit()

            return success

        except ValueError as ve:
            self.show_error(str(ve))
            return False
        except Exception as e:
            self.show_error(f"Ошибка при переводе: {str(e)}")
            return False

    @pyqtSlot()
    def deposit_balance(self, account_id: int, amount: float) -> bool:
        if amount <= 0:
            self.show_error("Сумма пополнения должна быть положительной")
            return False

        try:
            success = self.data_service.deposit_to_account(account_id, amount)
            if success:
                self.data_updated.emit()
            return success
        except Exception as e:
            self.show_error(f"Ошибка при пополнении: {str(e)}")
            return False

    @pyqtSlot()
    def load_transactions(self, table_view, client_id: int = None):
        try:
            transactions = self.data_service.get_client_transactions(client_id)
            seen_ids = set()
            data = []

            for t in transactions:
                if t.id in seen_ids:
                    continue
                seen_ids.add(t.id)

                from_acc = self.data_service.get_account_by_id(t.from_account_id)
                to_acc = self.data_service.get_account_by_id(t.to_account_id)

                data.append(
                    [
                        t.id,
                        from_acc.account_number if from_acc else "—",
                        to_acc.account_number if to_acc else "—",
                        f"{t.amount:.2f}",
                        t.transaction_type,
                        t.description or "",
                        t.transaction_date.strftime("%Y-%m-%d %H:%M"),
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
            ]
            table_view.setModel(BaseTableModel(data, headers))
        except Exception as e:
            self.show_error(f"Ошибка при загрузке транзакций: {str(e)}")

    @pyqtSlot()
    def get_transaction_summary(self, client_id: int) -> dict:
        try:
            transactions = self.data_service.get_client_transactions(client_id)
            total_income = sum(
                t.amount
                for t in transactions
                if t.to_account_id and t.transaction_type == "deposit"
            )
            total_expense = sum(
                t.amount
                for t in transactions
                if t.from_account_id and t.transaction_type == "transfer"
            )
            total_transfers = len(
                [t for t in transactions if t.transaction_type == "transfer"]
            )
            total_deposits = len(
                [t for t in transactions if t.transaction_type == "deposit"]
            )

            return {
                "total_income": total_income,
                "total_expense": total_expense,
                "total_transfers": total_transfers,
                "total_deposits": total_deposits,
            }
        except Exception as e:
            self.show_error(f"Ошибка при формировании статистики: {str(e)}")
            return {}

    @pyqtSlot()
    def get_client_accounts_for_combo(self, client_id: int) -> list[tuple]:
        try:
            accounts = self.data_service.get_client_accounts(client_id)
            return [(acc.account_number, acc.id) for acc in accounts]
        except Exception as e:
            self.show_error(f"Ошибка при загрузке счетов: {str(e)}")
            return []
