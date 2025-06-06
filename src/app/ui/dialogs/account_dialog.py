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


class AccountDialog(QDialog):
    def __init__(self, parent=None, account=None):
        super().__init__(parent)
        self.setWindowTitle(
            "Добавить счет" if account is None else "Редактировать счет"
        )
        self.account = account
        layout = QVBoxLayout()
        form = QFormLayout()

        self.number_edit = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["checking", "savings", "credit"])
        self.balance_edit = QLineEdit()
        self.balance_edit.setValidator(QtGui.QDoubleValidator())
        self.currency_edit = QLineEdit()
        self.currency_edit.setText("RUB")
        self.active_check = QComboBox()
        self.active_check.addItems(["Активен", "Неактивен"])

        form.addRow("Номер счета*:", self.number_edit)
        form.addRow("Тип счета*:", self.type_combo)
        form.addRow("Баланс*:", self.balance_edit)
        form.addRow("Валюта*:", self.currency_edit)
        form.addRow("Статус:", self.active_check)

        if account:
            self.number_edit.setText(account.account_number)
            self.type_combo.setCurrentText(account.account_type)
            self.balance_edit.setText(f"{account.balance:.2f}")
            self.currency_edit.setText(account.currency)
            self.active_check.setCurrentIndex(0 if account.is_active else 1)

        buttons = QPushButton("Сохранить")
        buttons.clicked.connect(self._validate_and_accept)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def _validate_and_accept(self):
        try:
            balance = float(self.balance_edit.text())
            if balance < 0:
                raise ValueError("Баланс не может быть отрицательным")
            if not self.number_edit.text().strip():
                raise ValueError("Номер счета обязателен")
            if not self.currency_edit.text().strip():
                raise ValueError("Валюта обязательна")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def get_data(self):
        return {
            "account_number": self.number_edit.text().strip(),
            "account_type": self.type_combo.currentText(),
            "balance": float(self.balance_edit.text()),
            "currency": self.currency_edit.text().strip(),
            "is_active": self.active_check.currentIndex() == 0,
        }
