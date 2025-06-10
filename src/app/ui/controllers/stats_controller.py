from typing import Optional
from PyQt6.QtWidgets import QMessageBox
from app.core.services.data_service import DataService


class StatsController:
    def __init__(self, data_service: DataService = None):
        self.data_service = data_service or DataService()
        self.error_handler = lambda msg: QMessageBox.critical(None, "Ошибка", msg)

    def show_error(self, message: str):
        self.error_handler(message)

    def get_monthly_summary(
        self,
        client_id: int,
        account_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
    ) -> dict:
        try:
            transactions = self.data_service.get_client_transactions(
                client_id, account_id, transaction_type
            )
            if account_id:
                transactions = [
                    t
                    for t in transactions
                    if t.from_account_id == account_id or t.to_account_id == account_id
                ]
            if transaction_type and transaction_type != "Все":
                transactions = [
                    t for t in transactions if t.transaction_type == transaction_type
                ]

            income_by_month = {}
            expense_by_month = {}

            for t in transactions:
                month = t.transaction_date.strftime("%Y-%m")
                if t.transaction_type == "deposit":
                    income_by_month[month] = income_by_month.get(month, 0) + t.amount
                elif t.transaction_type == "transfer" and t.from_account_id:
                    expense_by_month[month] = expense_by_month.get(month, 0) + t.amount

            months = sorted(set(income_by_month.keys()) | set(expense_by_month.keys()))
            incomes = [income_by_month.get(m, 0) for m in months]
            expenses = [expense_by_month.get(m, 0) for m in months]

            return {"months": months, "incomes": incomes, "expenses": expenses}
        except Exception as e:
            self.show_error(f"Ошибка при загрузке данных по месяцам: {str(e)}")
            return {"months": [], "incomes": [], "expenses": []}

    def get_transaction_type_summary(
        self,
        client_id: int,
        account_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
    ) -> dict:
        try:
            transactions = self.data_service.get_client_transactions(
                client_id, account_id, transaction_type
            )
            if account_id:
                transactions = [
                    t
                    for t in transactions
                    if t.from_account_id == account_id or t.to_account_id == account_id
                ]
            if transaction_type and transaction_type != "Все":
                transactions = [
                    t for t in transactions if t.transaction_type == transaction_type
                ]

            summary = {"deposit": 0, "transfer": 0, "withdrawal": 0}
            for t in transactions:
                if t.transaction_type in summary:
                    summary[t.transaction_type] += 1

            return summary
        except Exception as e:
            self.show_error(f"Ошибка при распределении транзакций: {str(e)}")
            return {"deposit": 0, "transfer": 0, "withdrawal": 0}

    def get_balance_summary(self, client_id: int) -> dict:
        try:
            accounts = self.data_service.get_client_accounts(client_id)
            account_numbers = [acc.account_number for acc in accounts]
            balances = [acc.balance for acc in accounts]
            return {"accounts": account_numbers, "balances": balances}
        except Exception as e:
            self.show_error(f"Ошибка при загрузке баланса: {str(e)}")
            return {"accounts": [], "balances": []}

    def get_monthly_summary(
        self, client_id: int, account_id: int = None, transaction_type: str = None
    ):
        return self.data_service.get_monthly_summary(
            client_id, account_id, transaction_type
        )

    def get_transaction_type_summary(
        self, client_id: int, account_id: int = None, transaction_type: str = None
    ):
        return self.data_service.get_transaction_type_summary(
            client_id, account_id, transaction_type
        )
