from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from app.ui.controllers.auth_controller import AuthController


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.resize(400, 600)
        self.controller = AuthController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Имя")

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Фамилия")

        self.passport = QLineEdit()
        self.passport.setPlaceholderText("Номер паспорта")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Телефон")

        register_btn = QPushButton("Зарегистрироваться")
        register_btn.clicked.connect(self.handle_register)

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.back_to_login)

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Подтверждение:"))
        layout.addWidget(self.confirm_input)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.first_name)
        layout.addWidget(QLabel("Фамилия:"))
        layout.addWidget(self.last_name)
        layout.addWidget(QLabel("Паспорт:"))
        layout.addWidget(self.passport)
        layout.addWidget(QLabel("Телефон:"))
        layout.addWidget(self.phone)
        layout.addWidget(register_btn)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def handle_register(self):
        email = self.email_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        fname = self.first_name.text()
        lname = self.last_name.text()
        passport = self.passport.text()
        phone = self.phone.text()

        if not all([email, password, confirm, fname, lname, passport]):
            QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return
        if password != confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        auth_id = self.controller.register(email, password)
        if not auth_id:
            QMessageBox.warning(self, "Ошибка", "Этот email уже занят")
            return

        client_data = {
            "first_name": fname,
            "last_name": lname,
            "passport_number": passport,
            "phone_number": phone or None,
            "email": email,
        }

        if self.controller.create_client_for_user(auth_id, **client_data):
            QMessageBox.information(self, "Успех", "Вы зарегистрированы!")
            self.back_to_login()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать профиль клиента")

    def back_to_login(self):
        self.close()
        from app.ui.views.auth_window import AuthWindow
        self.auth_window = AuthWindow()
        self.auth_window.show()
