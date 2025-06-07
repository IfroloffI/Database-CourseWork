from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
    QTableView,
    QTabWidget,
    QFormLayout,
    QGroupBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtCharts import (
    QChartView,
    QBarSeries,
    QBarSet,
    QBarCategoryAxis,
    QValueAxis,
    QPieSeries,
)
from app.ui.controllers.user_controller import UserController
from app.ui.controllers.stats_controller import StatsController
from app.ui.utils.base_table_model import BaseTableModel
from app.ui.utils.app_storage import AppStorage


class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Личный кабинет")
        self.resize(1200, 850)
        self.user_controller = UserController()
        self.stats_controller = StatsController(self.user_controller.data_service)
        self.accounts = []
        self.selected_account_id = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Личный кабинет")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #34495E;")
        main_layout.addWidget(title_label)

        self.client_label = QLabel("Вы вошли как пользователь")
        self.client_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.client_label.setStyleSheet("font-size: 14px; font-style: italic;")
        main_layout.addWidget(self.client_label)

        top_right_layout = QHBoxLayout()
        logout_btn = QPushButton("Выйти")
        logout_btn.setFixedWidth(100)
        logout_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #A0A0A0;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #E74C3C;
            }
        """
        )
        logout_btn.clicked.connect(self.close)
        top_right_layout.addStretch()
        top_right_layout.addWidget(logout_btn)
        main_layout.addLayout(top_right_layout)

        tab_widget = QTabWidget()

        # --- Вкладка Счета ---
        account_tab = QWidget()
        account_layout = QVBoxLayout(account_tab)

        self.account_table = QTableView()
        self.account_table.setSortingEnabled(True)
        account_layout.addWidget(self.account_table)

        create_group = QGroupBox("Создать новый счёт")
        create_form = QFormLayout()
        self.account_number_input = QLineEdit()
        self.account_type_combo = QComboBox()
        self.account_type_combo.addItems(["checking", "savings", "credit"])
        create_btn = QPushButton("Создать счёт")
        create_btn.clicked.connect(self.create_account)

        create_form.addRow("Номер счёта:", self.account_number_input)
        create_form.addRow("Тип счёта:", self.account_type_combo)
        create_form.addRow(create_btn)
        create_group.setLayout(create_form)
        account_layout.addWidget(create_group)

        tab_widget.addTab(account_tab, "Счета")

        # --- Вкладка Пополнение ---
        deposit_tab = QWidget()
        deposit_layout = QVBoxLayout(deposit_tab)

        deposit_group = QGroupBox("Пополнить счёт")
        deposit_form = QFormLayout()
        self.deposit_account_combo = QComboBox()
        self.deposit_amount_input = QLineEdit()
        deposit_btn = QPushButton("Пополнить")
        deposit_btn.clicked.connect(self.deposit_balance)

        deposit_form.addRow("Выберите счёт:", self.deposit_account_combo)
        deposit_form.addRow("Сумма пополнения:", self.deposit_amount_input)
        deposit_form.addRow(deposit_btn)
        deposit_group.setLayout(deposit_form)
        deposit_layout.addWidget(deposit_group)

        tab_widget.addTab(deposit_tab, "Пополнение")

        # --- Вкладка Переводы ---
        transfer_tab = QWidget()
        transfer_layout = QVBoxLayout(transfer_tab)

        transfer_group = QGroupBox("Выполнить перевод")
        form_layout = QFormLayout()
        self.transfer_from_combo = QComboBox()
        self.balance_label = QLabel("Баланс: 0.0 RUB")
        self.to_account_input = QLineEdit()
        self.transfer_amount_input = QLineEdit()
        transfer_btn = QPushButton("Перевести")
        transfer_btn.clicked.connect(self.make_transfer)

        form_layout.addRow("С какого счёта:", self.transfer_from_combo)
        form_layout.addRow("", self.balance_label)
        form_layout.addRow("Номер получателя:", self.to_account_input)
        form_layout.addRow("Сумма перевода:", self.transfer_amount_input)
        form_layout.addRow(transfer_btn)
        transfer_group.setLayout(form_layout)
        transfer_layout.addWidget(transfer_group)

        tab_widget.addTab(transfer_tab, "Переводы")

        # --- Вкладка История и статистика ---
        history_stats_tab = QWidget()
        history_stats_layout = QVBoxLayout(history_stats_tab)

        filter_layout = QHBoxLayout()
        self.filter_account_combo = QComboBox()
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(["Все", "transfer", "deposit", "withdrawal"])

        filter_layout.addWidget(QLabel("Фильтр по счёту:"))
        filter_layout.addWidget(self.filter_account_combo)
        filter_layout.addWidget(QLabel("Тип операции:"))
        filter_layout.addWidget(self.filter_type_combo)

        history_stats_layout.addLayout(filter_layout)

        self.transaction_table = QTableView()
        self.transaction_table.setSortingEnabled(True)
        history_stats_layout.addWidget(self.transaction_table)

        stats_inner_tabs = QTabWidget()

        income_expense_tab = QWidget()
        income_expense_layout = QVBoxLayout(income_expense_tab)
        self.income_expense_chart_view = QChartView()
        self.income_expense_chart_view.setRenderHint(
            self.income_expense_chart_view.renderHints().Antialiasing
        )
        income_expense_layout.addWidget(self.income_expense_chart_view)
        income_expense_tab.setLayout(income_expense_layout)
        stats_inner_tabs.addTab(income_expense_tab, "Доходы / Расходы")

        distribution_tab = QWidget()
        distribution_layout = QVBoxLayout(distribution_tab)
        self.distribution_pie_chart_view = QChartView()
        self.distribution_pie_chart_view.setRenderHint(
            self.distribution_pie_chart_view.renderHints().Antialiasing
        )
        distribution_layout.addWidget(self.distribution_pie_chart_view)
        distribution_tab.setLayout(distribution_layout)
        stats_inner_tabs.addTab(distribution_tab, "Распределение по типам")

        history_stats_layout.addWidget(stats_inner_tabs)
        tab_widget.addTab(history_stats_tab, "История и статистика")

        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        # Подключаем сигналы фильтрации
        self.transfer_from_combo.currentIndexChanged.connect(self._on_account_selected)
        self.filter_account_combo.currentIndexChanged.connect(self._on_filter_changed)
        self.filter_type_combo.currentIndexChanged.connect(self._on_filter_changed)

        self.load_user_data()
        self.update_income_expense_chart()
        self.update_distribution_chart()

    def _on_account_selected(self):
        current_index = self.transfer_from_combo.currentIndex()
        account_id = self.transfer_from_combo.itemData(current_index)
        balance = self.user_controller.get_selected_account_balance(account_id)
        self.balance_label.setText(f"Баланс: {balance:.2f} RUB")

    def _on_filter_changed(self):
        client = AppStorage.current_client
        if not client:
            return
        self._load_transactions(client.id)
        self.update_income_expense_chart()
        self.update_distribution_chart()

    def load_user_data(self):
        client = AppStorage.current_client
        if not client:
            return

        self.client_label.setText(f"Клиент: {client.first_name} {client.last_name}")
        self.accounts = self.user_controller.get_client_accounts(client.id)

        account_data = []
        for acc in self.accounts:
            account_data.append([
                acc.account_number,
                acc.account_type,
                f"{acc.balance:.2f} {acc.currency}",
                acc.opened_date.strftime("%Y-%m-%d"),
                "Активен" if acc.is_active else "Заблокирован"
            ])
        headers = ["Номер", "Тип", "Баланс", "Дата открытия", "Статус"]
        self.account_table.setModel(BaseTableModel(account_data, headers))

        self.transfer_from_combo.blockSignals(True)
        self.deposit_account_combo.blockSignals(True)
        self.filter_account_combo.blockSignals(True)

        self.transfer_from_combo.clear()
        self.deposit_account_combo.clear()
        self.filter_account_combo.clear()
        self.filter_account_combo.addItem("Все", None)

        for acc in self.accounts:
            item_text = f"{acc.account_number} ({acc.account_type})"
            self.transfer_from_combo.addItem(item_text, acc.id)
            self.deposit_account_combo.addItem(item_text, acc.id)
            self.filter_account_combo.addItem(item_text, acc.id)

        self.transfer_from_combo.blockSignals(False)
        self.deposit_account_combo.blockSignals(False)
        self.filter_account_combo.blockSignals(False)

        self._on_account_selected()
        self._on_filter_changed()

    def _load_transactions(self, client_id: int):
        account_id = self.filter_account_combo.currentData()
        transaction_type = self.filter_type_combo.currentText()
        transaction_type = None if transaction_type == "Все" else transaction_type

        transactions = self.user_controller.data_service.get_client_transactions(
            client_id
        )
        seen_ids = set()
        data = []

        for t in transactions:
            if t.id in seen_ids:
                continue
            seen_ids.add(t.id)

            from_acc = self.user_controller.data_service.get_account_by_id(
                t.from_account_id
            )
            to_acc = self.user_controller.data_service.get_account_by_id(
                t.to_account_id
            )

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
        self.transaction_table.setModel(BaseTableModel(data, headers))

    def update_income_expense_chart(self):
        chart = self.income_expense_chart_view.chart()
        if chart:
            chart.removeAllSeries()
            chart.axes().clear()

        client = AppStorage.current_client
        if not client:
            return

        summary = self.stats_controller.get_monthly_summary(client.id)
        months = summary["months"]
        incomes = summary["incomes"]
        expenses = summary["expenses"]

        series_income = QBarSet("Пополнения")
        series_expense = QBarSet("Расходы")
        series_income.append(incomes)
        series_expense.append(expenses)
        series_income.setColor(Qt.GlobalColor.green)
        series_expense.setColor(Qt.GlobalColor.red)

        bar_series = QBarSeries()
        bar_series.append(series_income)
        bar_series.append(series_expense)

        axis_x = QBarCategoryAxis()
        axis_x.setTitleText("Месяцы")
        axis_x.append(months)

        axis_y = QValueAxis()
        axis_y.setTitleText("Сумма (RUB)")

        chart = self.income_expense_chart_view.chart()
        chart.addSeries(bar_series)
        chart.createDefaultAxes()

        for ax in chart.axes():
            chart.removeAxis(ax)

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        bar_series.attachAxis(axis_x)
        bar_series.attachAxis(axis_y)
        chart.setTitle("Доходы и расходы по месяцам")

    def update_distribution_chart(self):
        chart = self.distribution_pie_chart_view.chart()
        if chart:
            chart.removeAllSeries()

        client = AppStorage.current_client
        if not client:
            return

        summary = self.stats_controller.get_transaction_type_summary(client.id)

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
        chart.addSeries(pie_series)
        chart.setTitle("Распределение транзакций по типам")

    def create_account(self):
        client = AppStorage.current_client
        if not client:
            return

        account_number = self.account_number_input.text().strip()
        account_type = self.account_type_combo.currentText()

        if not account_number or not account_type:
            self.user_controller.show_error("Заполните все поля")
            return

        success = self.user_controller.create_account(
            client.id, account_number, account_type
        )
        if success:
            print("[DEBUG] Счёт создан успешно")  # log
            self.account_number_input.clear()
            self.load_user_data()
        else:
            self.user_controller.show_error("Не удалось создать счёт")

    def deposit_balance(self):
        account_index = self.deposit_account_combo.currentIndex()
        account_id = self.deposit_account_combo.itemData(account_index)
        amount_text = self.deposit_amount_input.text().strip()

        if not amount_text:
            self.user_controller.show_error("Введите сумму")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.user_controller.show_error("Некорректная сумма")
            return

        success = self.user_controller.deposit_balance(account_id, amount)
        if success:
            self.deposit_amount_input.clear()
            self.load_user_data()
        else:
            self.user_controller.show_error("Ошибка пополнения")

    def make_transfer(self):
        from_index = self.transfer_from_combo.currentIndex()
        from_account_id = self.transfer_from_combo.itemData(from_index)
        to_account_number = self.to_account_input.text().strip()
        amount_text = self.transfer_amount_input.text().strip()

        if not all([to_account_number, amount_text]):
            self.user_controller.show_error("Заполните все поля")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.user_controller.show_error("Некорректная сумма")
            return

        to_account = self.user_controller.data_service.get_account_by_number(
            to_account_number
        )
        if not to_account:
            self.user_controller.show_error("Счёт получателя не найден")
            return

        success = self.user_controller.transfer_funds(
            from_account_id, to_account_number, amount, "Перевод пользователю"
        )

        if success:
            self.to_account_input.clear()
            self.transfer_amount_input.clear()
            self.load_user_data()
