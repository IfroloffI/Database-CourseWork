from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableView
from PyQt6.QtCore import Qt
from design.generated.ui_main_window import Ui_MainWindow
from app.ui.controllers.client_controller import ClientController
from app.ui.controllers.account_controller import AccountController
from app.ui.controllers.transaction_controller import TransactionController
from app.ui.utils.base_table_model import BaseTableModel
from app.ui.dialogs.client_dialog import ClientDialog
from app.ui.dialogs.account_dialog import AccountDialog
from app.ui.dialogs.transaction_dialog import TransactionDialog
from app.ui.utils.app_storage import AppStorage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.storage = AppStorage()
        self.client_controller = ClientController()
        self.account_controller = AccountController()
        self.transaction_controller = TransactionController()

        self._setup_ui()
        self._connect_signals()
        self._load_initial_data()

    def _setup_ui(self):
        for table in [
            self.ui.clientsTableView,
            self.ui.accountsTableView,
            self.ui.transactionsTableView,
        ]:
            table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
            table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
            table.hideColumn(0)

    def _connect_signals(self):
        self.ui.addClientButton.clicked.connect(self._add_client_dialog)
        self.ui.editClientButton.clicked.connect(self._edit_client_dialog)
        self.ui.deleteClientButton.clicked.connect(self._delete_client)
        self.ui.refreshClientsButton.clicked.connect(
            lambda: self._refresh_clients(True)
        )

        self.ui.addAccountButton.clicked.connect(self._add_account_dialog)
        self.ui.editAccountButton.clicked.connect(self._edit_account_dialog)
        self.ui.deleteAccountButton.clicked.connect(self._delete_account)
        self.ui.refreshAccountsButton.clicked.connect(
            lambda: self._refresh_accounts(True)
        )

        self.ui.addTransactionButton.clicked.connect(self._add_transaction_dialog)
        self.ui.editTransactionButton.clicked.connect(self._edit_transaction_dialog)
        self.ui.deleteTransactionButton.clicked.connect(self._delete_transaction)
        self.ui.refreshTransactionsButton.clicked.connect(
            lambda: self._refresh_transactions(True)
        )

        self.ui.showTransactionsButton.clicked.connect(self._show_transactions)
        self.ui.backToClientsButton.clicked.connect(self._back_to_clients)

        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self._show_about)

        self.client_controller.data_updated.connect(
            lambda: self._refresh_clients(False)
        )
        self.account_controller.data_updated.connect(
            lambda: self._refresh_accounts(False)
        )
        self.transaction_controller.data_updated.connect(
            lambda: self._refresh_transactions(False)
        )

    def _load_initial_data(self):
        self._refresh_clients(True)
        if (model := self.ui.clientsTableView.model()) and model.rowCount() > 0:
            self.ui.clientsTableView.selectRow(0)
            self._on_client_selected()

    def _on_client_selected(self):
        selected = self.ui.clientsTableView.selectionModel().selectedRows()
        if not selected:
            self.storage.current_client = None
            self.storage.current_account = None
            self.ui.accountsGroup.setTitle("Счета клиента")
            self._refresh_accounts(True)
            return

        client_id = selected[0].data()
        self.storage.current_client = self.client_controller.select_client(client_id)

        if self.storage.current_client:
            self.ui.accountsGroup.setTitle(
                f"Счета клиента: {self.storage.current_client.last_name}"
            )
            self._refresh_accounts(True)
            if self.ui.accountsTableView.model():
                self.ui.accountsTableView.selectionModel().selectionChanged.connect(
                    self._on_account_selected
                )

    def _on_account_selected(self):
        selected = self.ui.accountsTableView.selectionModel().selectedRows()
        if not selected:
            self.storage.current_account = None
            self._refresh_transactions(True)
            return

        account_id = selected[0].data()
        if self.storage.current_client:
            self.storage.current_account = self.account_controller.select_account(
                self.storage.current_client.id, account_id
            )
        self._refresh_transactions(True)

    def _refresh_clients(self, emit_signal=True):
        self.client_controller.load_clients(self.ui.clientsTableView)
        if emit_signal:
            self.client_controller.data_updated.emit()
        if self.ui.clientsTableView.model():
            self.ui.clientsTableView.selectionModel().selectionChanged.connect(
                self._on_client_selected
            )
            self._on_client_selected()

    def _refresh_accounts(self, emit_signal=True):
        if self.storage.current_client:
            self.account_controller.load_client_accounts(
                self.storage.current_client.id, self.ui.accountsTableView
            )
        else:
            self.storage.current_account = None
            self.ui.accountsTableView.setModel(None)

        if emit_signal:
            self.account_controller.data_updated.emit()

        if self.ui.accountsTableView.model():
            self.ui.accountsTableView.selectionModel().selectionChanged.connect(
                self._on_account_selected
            )
            self._on_account_selected()

    def _refresh_transactions(self, emit_signal=True):
        current_client = self.storage.current_client
        current_account = self.storage.current_account

        accounts = None
        if current_client:
            accounts = self.account_controller.data_service.get_client_accounts(
                current_client.id
            )

        if current_account:
            description = self.transaction_controller.load_transactions(
                self.ui.transactionsTableView,
                account_id=current_account.id,
                accounts=accounts,
            )
            if current_client:
                description = f"{current_client.last_name} - {description}"
        elif current_client:
            description = self.transaction_controller.load_transactions(
                self.ui.transactionsTableView,
                client_id=current_client.id,
                accounts=accounts,
            )
            description = f"{current_client.last_name} - {description}"
        else:
            description = self.transaction_controller.load_transactions(
                self.ui.transactionsTableView
            )

        self.ui.transactionsGroup.setTitle(description)

        if emit_signal:
            self.transaction_controller.data_updated.emit()

    def _show_transactions(self):
        if self.storage.current_client:
            self.ui.tabWidget.setCurrentIndex(1)
            self._refresh_transactions(True)

    def _back_to_clients(self):
        self.ui.tabWidget.setCurrentIndex(0)

    def _delete_client(self):
        selected = self.ui.clientsTableView.selectionModel().selectedRows()
        if not selected:
            self.client_controller.show_error("Выберите клиента для удаления")
            return
        client_id = selected[0].data()
        if self.client_controller.delete_client(client_id):
            self._refresh_clients(True)

    def _delete_account(self):
        if not self.storage.current_account:
            self.account_controller.show_error("Выберите счет для удаления")
            return
        if self.account_controller.delete_account(self.storage.current_account.id):
            self._refresh_accounts(True)

    def _show_about(self):
        from app.core.config import AppConfig

        QMessageBox.about(
            self,
            "О программе",
            AppConfig.get("APP_NAME") + "\nВерсия: " + AppConfig.get("APP_VERSION"),
        )

    def _add_client_dialog(self):
        dialog = ClientDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                if self.client_controller.add_client(**data):
                    self._refresh_clients(True)
            except Exception as e:
                self.client_controller.show_error(
                    f"Ошибка при добавлении клиента: {str(e)}"
                )

    def _edit_client_dialog(self):
        selected = self.ui.clientsTableView.selectionModel().selectedRows()
        if not selected:
            self.client_controller.show_error("Выберите клиента для редактирования")
            return

        client_id = selected[0].data()
        client = self.client_controller.get_client_by_id(client_id)
        if not client:
            return

        dialog = ClientDialog(self, client)
        if dialog.exec():
            data = dialog.get_data()
            if self.client_controller.update_client(client_id, **data):
                self._refresh_clients(True)

    def _add_account_dialog(self):
        if not self.storage.current_client:
            self.account_controller.show_error("Выберите клиента для добавления счета")
            return

        dialog = AccountDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                if self.account_controller.add_account(
                    self.storage.current_client.id, **data
                ):
                    self._refresh_accounts(True)
            except Exception as e:
                self.account_controller.show_error(
                    f"Ошибка при добавлении счета: {str(e)}"
                )

    def _edit_account_dialog(self):
        if not self.storage.current_account:
            self.account_controller.show_error("Выберите счет для редактирования")
            return

        dialog = AccountDialog(self, self.storage.current_account)
        if dialog.exec():
            data = dialog.get_data()
            if self.account_controller.update_account(
                self.storage.current_account.id, **data
            ):
                self._refresh_accounts(True)

    def _add_transaction_dialog(self):
        if not self.storage.current_client:
            self.transaction_controller.show_error(
                "Выберите клиента для добавления транзакции"
            )
            return

        accounts = self.account_controller.data_service.get_client_accounts(
            self.storage.current_client.id
        )
        dialog = TransactionDialog(self, accounts=accounts)
        if dialog.exec():
            data = dialog.get_data()
            try:
                if self.transaction_controller.add_transaction(**data):
                    self._refresh_transactions(True)
            except Exception as e:
                self.transaction_controller.show_error(
                    f"Ошибка при добавлении транзакции: {str(e)}"
                )

    def _edit_transaction_dialog(self):
        selected = self.ui.transactionsTableView.selectionModel().selectedRows()
        if not selected:
            self.transaction_controller.show_error(
                "Выберите транзакцию для редактирования"
            )
            return

        transaction_id = selected[0].data()
        transaction = self.transaction_controller.get_transaction_by_id(transaction_id)
        if not transaction:
            return

        accounts = self.account_controller.data_service.get_client_accounts(
            self.storage.current_client.id
        )
        dialog = TransactionDialog(self, transaction, accounts)
        if dialog.exec():
            data = dialog.get_data()
            if self.transaction_controller.update_transaction(transaction_id, **data):
                self._refresh_transactions(True)

    def _delete_transaction(self):
        selected = self.ui.transactionsTableView.selectionModel().selectedRows()
        if not selected:
            self.transaction_controller.show_error("Выберите транзакцию для удаления")
            return

        transaction_id = selected[0].data()
        if self.transaction_controller.delete_transaction(transaction_id):
            self._refresh_transactions(True)
