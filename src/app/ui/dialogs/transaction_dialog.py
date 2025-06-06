from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QComboBox,
)
from PyQt6 import QtGui
from PyQt6.QtWidgets import QMessageBox


class TransactionDialog(QDialog):
    def __init__(self, parent=None, transaction=None, accounts=None):
        super().__init__(parent)
        self.setWindowTitle(
            "Добавить транзакцию" if transaction is None else "Редактировать транзакцию"
        )
        self.transaction = transaction
        self.accounts = accounts or []
        layout = QVBoxLayout()
        form = QFormLayout()

        self.from_account_combo = QComboBox()
        self.to_account_combo = QComboBox()
        self.amount_edit = QLineEdit()
        self.amount_edit.setValidator(QtGui.QDoubleValidator(0, 999999999, 2))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["transfer", "deposit", "withdrawal"])
        self.description_edit = QLineEdit()

        self._populate_accounts()

        form.addRow("Отправитель:", self.from_account_combo)
        form.addRow("Получатель*:", self.to_account_combo)
        form.addRow("Сумма*:", self.amount_edit)
        form.addRow("Тип операции*:", self.type_combo)
        form.addRow("Описание:", self.description_edit)

        if transaction:
            if transaction.from_account_id:
                idx = next(
                    (
                        i
                        for i, acc in enumerate(self.accounts)
                        if acc.id == transaction.from_account_id
                    ),
                    0,
                )
                self.from_account_combo.setCurrentIndex(idx)
            idx = next(
                (
                    i
                    for i, acc in enumerate(self.accounts)
                    if acc.id == transaction.to_account_id
                ),
                0,
            )
            self.to_account_combo.setCurrentIndex(idx)
            self.amount_edit.setText(f"{transaction.amount:.2f}")
            self.type_combo.setCurrentText(transaction.transaction_type)
            self.description_edit.setText(transaction.description or "")

        buttons = QPushButton("Сохранить")
        buttons.clicked.connect(self._validate_and_accept)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def _populate_accounts(self):
        self.from_account_combo.addItem("Внесение средств", None)
        self.to_account_combo.addItem("Выберите счет", None)
        for acc in self.accounts:
            self.from_account_combo.addItem(
                f"{acc.account_number} ({acc.account_type})", acc.id
            )
            self.to_account_combo.addItem(
                f"{acc.account_number} ({acc.account_type})", acc.id
            )

    def _validate_and_accept(self):
        try:
            amount = float(self.amount_edit.text())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
            to_account = self.to_account_combo.currentData()
            if not to_account:
                raise ValueError("Получатель обязателен")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def get_data(self):
        return {
            "from_account_id": self.from_account_combo.currentData(),
            "to_account_id": self.to_account_combo.currentData(),
            "amount": float(self.amount_edit.text()),
            "transaction_type": self.type_combo.currentText(),
            "description": self.description_edit.text().strip() or None,
        }
