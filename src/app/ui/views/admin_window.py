from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableView,
    QTabWidget,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QFormLayout,
    QGroupBox,
    QMessageBox,
    QLineEdit,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtCharts import (
    QChartView,
    QBarSeries,
    QPieSeries,
    QBarSet,
    QValueAxis,
    QBarCategoryAxis,
)
from app.ui.controllers.admin_controller import AdminController
from app.ui.utils.base_table_model import BaseTableModel
from app.core.database.models import Client, Account, Transaction


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель Администратора")
        self.resize(1200, 900)
        self.admin_controller = AdminController()
        self.clients = []
        self.accounts = []
        self.transactions = []
        self.init_ui()

    def switch_to_other_version(self):
        from app.ui.views.main_window import MainWindow

        if isinstance(self, AdminWindow):
            self.close()
            self.main_window = MainWindow()
            self.main_window.show()
        elif isinstance(self, MainWindow):
            self.close()
            self.admin_window = AdminWindow()
            self.admin_window.show()

    def init_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()

        switch_button = QPushButton("Старая версия Панели")
        switch_button.clicked.connect(self.switch_to_other_version)
        switch_button.setStyleSheet(
            """
            QPushButton {
                background-color: #A0A0A0;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 150px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: #3498DB;
            }
            """
        )
        switch_button.setFlat(False)
        header_layout.addWidget(switch_button)

        title_label = QLabel("Панель администратора")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2C3E50;")
        header_layout.addStretch()
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.close)
        logout_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #A0A0A0;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 100px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: #E74C3C;
            }
            """
        )
        header_layout.addWidget(logout_btn)

        main_layout.addLayout(header_layout)

        tab_widget = QTabWidget()

        # --- Вкладка Клиенты ---
        clients_tab = QWidget()
        clients_layout = QVBoxLayout(clients_tab)

        search_client_layout = QHBoxLayout()
        self.client_search_input = QLineEdit()
        self.client_search_input.setPlaceholderText("Поиск по имени или фамилии...")
        self.client_search_input.textChanged.connect(self._on_client_search_changed)
        search_client_layout.addWidget(QLabel("Поиск клиента:"))
        search_client_layout.addWidget(self.client_search_input)
        clients_layout.addLayout(search_client_layout)

        self.client_table = QTableView()
        self.client_table.setSortingEnabled(True)
        self.client_table.setStyleSheet("QTableView::item { text-align: center; }")
        clients_layout.addWidget(self.client_table)

        create_client_group = QGroupBox("Добавить клиента")
        create_client_form = QFormLayout()
        self.client_first_name_input = QLineEdit()
        self.client_last_name_input = QLineEdit()
        self.client_passport_input = QLineEdit()
        self.client_phone_input = QLineEdit()
        self.client_email_input = QLineEdit()
        add_client_btn = QPushButton("Добавить клиента")
        add_client_btn.clicked.connect(self.add_client)

        create_client_form.addRow("Имя:", self.client_first_name_input)
        create_client_form.addRow("Фамилия:", self.client_last_name_input)
        create_client_form.addRow("Паспорт:", self.client_passport_input)
        create_client_form.addRow("Телефон:", self.client_phone_input)
        create_client_form.addRow("Email:", self.client_email_input)
        create_client_form.addRow(add_client_btn)
        create_client_group.setLayout(create_client_form)
        clients_layout.addWidget(create_client_group)

        tab_widget.addTab(clients_tab, "Клиенты")

        # --- Вкладка Счета ---
        accounts_tab = QWidget()
        accounts_layout = QVBoxLayout(accounts_tab)

        account_filter_layout = QHBoxLayout()
        self.account_client_combo = QComboBox()
        self.account_type_filter_combo = QComboBox()
        self.account_type_filter_combo.addItems(
            ["Все", "checking", "savings", "credit"]
        )

        account_filter_layout.addWidget(QLabel("Фильтр по клиенту:"))
        account_filter_layout.addWidget(self.account_client_combo)
        account_filter_layout.addWidget(QLabel("Фильтр по типу:"))
        account_filter_layout.addWidget(self.account_type_filter_combo)
        account_filter_layout.addStretch()
        accounts_layout.addLayout(account_filter_layout)

        self.account_table = QTableView()
        self.account_table.setSortingEnabled(True)
        self.account_table.setStyleSheet("QTableView::item { text-align: center; }")
        accounts_layout.addWidget(self.account_table)

        create_account_group = QGroupBox("Создать счёт")
        create_account_form = QFormLayout()
        self.account_number_input = QLineEdit()
        self.account_type_input = QComboBox()
        self.account_type_input.addItems(["checking", "savings", "credit"])
        self.account_client_id_input = QLineEdit()
        create_account_btn = QPushButton("Создать счёт")
        create_account_btn.clicked.connect(self.create_account)

        create_account_form.addRow("Номер счёта:", self.account_number_input)
        create_account_form.addRow("Тип счёта:", self.account_type_input)
        create_account_form.addRow("ID клиента:", self.account_client_id_input)
        create_account_form.addRow(create_account_btn)
        create_account_group.setLayout(create_account_form)
        accounts_layout.addWidget(create_account_group)

        tab_widget.addTab(accounts_tab, "Счета")

        # --- Вкладка Транзакции ---
        transactions_tab = QWidget()
        transactions_layout = QVBoxLayout(transactions_tab)

        transaction_filter_layout = QHBoxLayout()
        self.transaction_client_combo = QComboBox()
        self.transaction_account_combo = QComboBox()
        self.transaction_type_combo = QComboBox()
        self.transaction_type_combo.addItems(
            ["Все", "transfer", "deposit", "withdrawal"]
        )

        transaction_filter_layout.addWidget(QLabel("Фильтр по клиенту:"))
        transaction_filter_layout.addWidget(self.transaction_client_combo)
        transaction_filter_layout.addWidget(QLabel("Фильтр по счёту:"))
        transaction_filter_layout.addWidget(self.transaction_account_combo)
        transaction_filter_layout.addWidget(QLabel("Тип операции:"))
        transaction_filter_layout.addWidget(self.transaction_type_combo)
        transactions_layout.addLayout(transaction_filter_layout)

        self.transaction_table = QTableView()
        self.transaction_table.setSortingEnabled(True)
        self.transaction_table.setStyleSheet("QTableView::item { text-align: center; }")
        transactions_layout.addWidget(self.transaction_table)

        tab_widget.addTab(transactions_tab, "Транзакции")

        # --- Вкладка Статистика ---
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)

        filter_layout = QHBoxLayout()
        self.stats_client_combo = QComboBox()
        self.stats_account_combo = QComboBox()
        self.stats_transaction_type_combo = QComboBox()
        self.stats_transaction_type_combo.addItems(
            ["Все", "transfer", "deposit", "withdrawal"]
        )

        filter_layout.addWidget(QLabel("Фильтр по клиенту:"))
        filter_layout.addWidget(self.stats_client_combo)
        filter_layout.addWidget(QLabel("Фильтр по счёту:"))
        filter_layout.addWidget(self.stats_account_combo)
        filter_layout.addWidget(QLabel("Тип операции:"))
        filter_layout.addWidget(self.stats_transaction_type_combo)
        stats_layout.addLayout(filter_layout)

        self.income_expense_chart_view = QChartView()
        self.distribution_pie_chart_view = QChartView()
        stats_layout.addWidget(QLabel("Доходы / Расходы"))
        stats_layout.addWidget(self.income_expense_chart_view)
        stats_layout.addWidget(QLabel("Распределение по типам"))
        stats_layout.addWidget(self.distribution_pie_chart_view)
        tab_widget.addTab(stats_tab, "Статистика")

        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        self.account_client_combo.currentIndexChanged.connect(
            self._on_account_filter_changed
        )
        self.account_type_filter_combo.currentIndexChanged.connect(
            self._on_account_filter_changed
        )
        self.transaction_client_combo.currentIndexChanged.connect(
            self._on_transaction_filter_changed
        )
        self.transaction_account_combo.currentIndexChanged.connect(
            self._on_transaction_filter_changed
        )
        self.transaction_type_combo.currentIndexChanged.connect(
            self._on_transaction_filter_changed
        )
        self.stats_client_combo.currentIndexChanged.connect(
            self._on_stats_filter_changed
        )
        self.stats_account_combo.currentIndexChanged.connect(
            self._on_stats_filter_changed
        )
        self.stats_transaction_type_combo.currentIndexChanged.connect(
            self._on_stats_filter_changed
        )

        self.load_clients()
        self.load_all_accounts()
        self.load_all_transactions()
        self.load_stats_data()

    def load_clients(self):
        try:
            self.clients = self.admin_controller.get_all_clients()
            self._update_client_combos()
            self._load_client_table(self.clients)
        except Exception as e:
            self.show_error(f"Ошибка при загрузке клиентов: {e}")

    def _update_client_combos(self):
        for combo in [
            self.transaction_client_combo,
            self.account_client_combo,
            self.stats_client_combo,
        ]:
            combo.blockSignals(True)
            combo.clear()
            combo.addItem("Все", None)
            for client in self.clients:
                full_name = f"{client.first_name} {client.last_name}"
                combo.addItem(full_name, client.id)
            combo.blockSignals(False)

    def _load_client_table(self, clients=None):
        if clients is None:
            clients = self.clients
        data = []
        for client in clients:
            data.append(
                [
                    client.id,
                    f"{client.first_name} {client.last_name}",
                    client.passport_number,
                    client.phone_number or "—",
                    client.email or "—",
                ]
            )
        headers = ["ID", "ФИО", "Паспорт", "Телефон", "Email"]
        self.client_table.setModel(BaseTableModel(data, headers))

    def _on_client_search_changed(self, text: str):
        if not text.strip():
            self.load_clients()
            return

        filtered = self.admin_controller.search_clients_by_name(text)
        self._load_client_table(filtered)

    def load_all_accounts(self):
        try:
            self.accounts = self.admin_controller.get_all_accounts()
            self._update_account_combo()
            self._load_account_table(self.accounts)
        except Exception as e:
            self.show_error(f"Ошибка при загрузке счетов: {e}")

    def _update_account_combo(self):
        self.transaction_account_combo.blockSignals(True)
        self.stats_account_combo.blockSignals(True)
        self.transaction_account_combo.clear()
        self.stats_account_combo.clear()
        self.transaction_account_combo.addItem("Все", None)
        self.stats_account_combo.addItem("Все", None)
        for acc in self.accounts:
            item_text = f"{acc.account_number} ({acc.account_type})"
            self.transaction_account_combo.addItem(item_text, acc.id)
            self.stats_account_combo.addItem(item_text, acc.id)
        self.transaction_account_combo.blockSignals(False)
        self.stats_account_combo.blockSignals(False)

    def _load_account_table(self, accounts=None):
        if accounts is None:
            accounts = self.accounts
        data = []
        for acc in accounts:
            client_info = self.admin_controller.data_service.get_client_by_id(
                acc.client_id
            )
            client_name = (
                f"{client_info.first_name} {client_info.last_name}"
                if client_info
                else "—"
            )

            data.append(
                [
                    acc.account_number,
                    acc.account_type,
                    f"{acc.balance:.2f} {acc.currency}",
                    "Активен" if acc.is_active else "Заблокирован",
                    acc.opened_date.strftime("%Y-%m-%d"),
                    client_name,
                ]
            )

        headers = ["Номер", "Тип", "Баланс", "Статус", "Дата открытия", "Клиент"]
        self.account_table.setModel(BaseTableModel(data, headers))

    def _on_account_filter_changed(self):
        client_id = self.account_client_combo.currentData()
        account_type = self.account_type_filter_combo.currentText()
        account_type = None if account_type == "Все" else account_type

        accounts = self.admin_controller.get_filtered_accounts(client_id, account_type)
        self._load_account_table(accounts)

    def load_all_transactions(self):
        try:
            self.transactions = self.admin_controller.get_all_transactions()
            self._load_transaction_table(self.transactions)
        except Exception as e:
            self.show_error(f"Ошибка при загрузке транзакций: {e}")

    def _load_transaction_table(self, transactions):
        data = []
        for t in transactions:
            from_acc = self.admin_controller.data_service.get_account_by_id(
                t.from_account_id
            )
            to_acc = self.admin_controller.data_service.get_account_by_id(
                t.to_account_id
            )

            data.append(
                [
                    t.id,
                    from_acc.account_number if from_acc else "—",
                    to_acc.account_number if to_acc else "—",
                    f"{t.amount:.2f}",
                    t.transaction_type,
                    t.description or "—",
                    t.transaction_date.strftime("%Y-%m-%d %H:%M"),
                ]
            )

        headers = [
            "Отправитель",
            "Получатель",
            "Сумма",
            "Тип",
            "Описание",
            "Дата",
        ]
        self.transaction_table.setModel(BaseTableModel(data, headers))

    def _on_transaction_filter_changed(self):
        client_id = self.transaction_client_combo.currentData()
        account_id = self.transaction_account_combo.currentData()
        transaction_type = self.transaction_type_combo.currentText()
        transaction_type = None if transaction_type == "Все" else transaction_type

        transactions = self.admin_controller.get_filtered_transactions(
            client_id, account_id, transaction_type
        )
        self._load_transaction_table(transactions)

    def load_stats_data(self):
        self._on_stats_filter_changed()

    def _on_stats_filter_changed(self):
        client_id = self.stats_client_combo.currentData()
        account_id = self.stats_account_combo.currentData()
        transaction_type = self.stats_transaction_type_combo.currentText()
        transaction_type = None if transaction_type == "Все" else transaction_type

        summary = self.admin_controller.get_monthly_summary(
            client_id, account_id, transaction_type
        )
        self.update_income_expense_chart(
            summary["months"], summary["incomes"], summary["expenses"]
        )

        summary_types = self.admin_controller.get_transaction_type_summary(
            client_id, account_id, transaction_type
        )
        self.update_distribution_chart(summary_types)

    def update_income_expense_chart(self, months, incomes, expenses):
        chart = self.income_expense_chart_view.chart()
        if chart:
            chart.removeAllSeries()
            chart.axes().clear()

        series_income = QBarSet("Пополнения")
        series_expense = QBarSet("Переводы")
        series_income.setColor(Qt.GlobalColor.green)
        series_expense.setColor(Qt.GlobalColor.red)

        series_income.append(incomes)
        series_expense.append(expenses)

        bar_series = QBarSeries()
        bar_series.append(series_income)
        bar_series.append(series_expense)

        axis_x = QBarCategoryAxis()
        axis_x.setTitleText("Месяцы")
        axis_x.append(months)

        axis_y = QValueAxis()
        axis_y.setTitleText("Сумма (RUB)")

        chart = self.income_expense_chart_view.chart()
        chart.removeAllSeries()
        chart.addSeries(bar_series)
        chart.createDefaultAxes()
        for ax in chart.axes():
            chart.removeAxis(ax)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        bar_series.attachAxis(axis_x)
        bar_series.attachAxis(axis_y)
        chart.setTitle("Доходы и расходы по месяцам")

    def update_distribution_chart(self, summary):
        chart = self.distribution_pie_chart_view.chart()
        if chart:
            chart.removeAllSeries()

        pie_series = QPieSeries()
        pie_series.append("Пополнения", summary["deposit"])
        pie_series.append("Переводы", summary["transfer"])
        pie_series.append("Снятия", summary["withdrawal"])

        slice_1 = pie_series.slices()[0]
        slice_1.setExploded()
        slice_1.setLabelVisible()
        slice_1.setPen(Qt.GlobalColor.darkGreen)
        slice_1.setBrush(Qt.GlobalColor.green)

        slice_2 = pie_series.slices()[1]
        slice_2.setLabelVisible()
        slice_2.setPen(Qt.GlobalColor.darkRed)
        slice_2.setBrush(Qt.GlobalColor.red)

        slice_3 = pie_series.slices()[2]
        slice_3.setLabelVisible()
        slice_3.setPen(Qt.GlobalColor.darkBlue)
        slice_3.setBrush(Qt.GlobalColor.blue)

        chart = self.distribution_pie_chart_view.chart()
        chart.removeAllSeries()
        chart.addSeries(pie_series)
        chart.setTitle("Распределение транзакций по типам")

    def add_client(self):
        first_name = self.client_first_name_input.text().strip()
        last_name = self.client_last_name_input.text().strip()
        passport_number = self.client_passport_input.text().strip()
        phone_number = self.client_phone_input.text().strip()
        email = self.client_email_input.text().strip()

        if not all([first_name, last_name, passport_number]):
            self.show_error("Заполните обязательные поля: Имя, Фамилия, Паспорт")
            return

        success = self.admin_controller.add_client(
            first_name, last_name, passport_number, phone_number, email
        )
        if success:
            self.client_first_name_input.clear()
            self.client_last_name_input.clear()
            self.client_passport_input.clear()
            self.client_phone_input.clear()
            self.client_email_input.clear()
            self.load_clients()

    def create_account(self):
        account_number = self.account_number_input.text().strip()
        account_type = self.account_type_input.currentText()
        client_id_text = self.account_client_id_input.text().strip()

        if not account_number or not account_type or not client_id_text:
            self.show_error("Заполните все поля")
            return

        try:
            client_id = int(client_id_text)
            if not self.admin_controller.data_service.client_exists(client_id):
                raise ValueError("Клиент не найден")

            success = self.admin_controller.create_account(
                client_id, account_number, account_type
            )
            if success:
                self.account_number_input.clear()
                self.account_client_id_input.clear()
                self.show_success("Счёт успешно создан")
                self.load_all_accounts()
        except ValueError as ve:
            self.show_error(str(ve))
        except Exception as e:
            self.show_error(f"Ошибка при создании счёта: {str(e)}")

    def show_success(self, message: str):
        QMessageBox.information(None, "Успех", message)

    def show_error(self, message: str):
        QMessageBox.critical(None, "Ошибка", message)
