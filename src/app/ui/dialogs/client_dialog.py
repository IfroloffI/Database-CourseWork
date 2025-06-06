from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout


class ClientDialog(QDialog):
    def __init__(self, parent=None, client=None):
        super().__init__(parent)
        self.setWindowTitle(
            "Добавить клиента" if client is None else "Редактировать клиента"
        )
        self.client = client
        layout = QVBoxLayout()
        form = QFormLayout()

        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.passport_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()

        form.addRow("Имя:", self.first_name_edit)
        form.addRow("Фамилия:", self.last_name_edit)
        form.addRow("Паспорт:", self.passport_edit)
        form.addRow("Телефон:", self.phone_edit)
        form.addRow("Email:", self.email_edit)

        if client:
            self.first_name_edit.setText(client.first_name)
            self.last_name_edit.setText(client.last_name)
            self.passport_edit.setText(client.passport_number)
            self.phone_edit.setText(client.phone_number or "")
            self.email_edit.setText(client.email or "")

        buttons = QPushButton("Сохранить")
        buttons.clicked.connect(self.accept)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_data(self):
        return {
            "first_name": self.first_name_edit.text(),
            "last_name": self.last_name_edit.text(),
            "passport_number": self.passport_edit.text(),
            "phone_number": self.phone_edit.text() or None,
            "email": self.email_edit.text() or None,
        }
