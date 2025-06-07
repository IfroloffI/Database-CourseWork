from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from app.ui.controllers.auth_controller import AuthController
from app.ui.views.main_window import MainWindow
from app.ui.views.user_window import UserWindow
import os

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.resize(400, 400)
        self.controller = AuthController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        image_label = QLabel()
        pixmap = QPixmap("app/static/icons/logo.png")
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(360, 360, Qt.AspectRatioMode.KeepAspectRatio))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(image_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Email / Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.handle_login)

        register_btn = QPushButton("Зарегистрироваться")
        register_btn.clicked.connect(self.open_registration)

        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def handle_login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        role = self.controller.authenticate(login, password)

        if role == "admin":
            self.close()
            self.admin_window = MainWindow()
            self.admin_window.show()
        elif role == "user":
            self.close()
            self.user_window = UserWindow()
            self.user_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_registration(self):
        self.close()
        from app.ui.views.registration_window import RegistrationWindow
        self.registration_window = RegistrationWindow()
        self.registration_window.show()
