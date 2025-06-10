from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QDialogButtonBox,
    QDialog,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from app.ui.controllers.auth_controller import AuthController
from app.ui.views.admin_window import AdminWindow
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
            image_label.setPixmap(
                pixmap.scaled(360, 360, Qt.AspectRatioMode.KeepAspectRatio)
            )
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
            new_version = self.show_admin_panel_choice_dialog()

            if new_version == True:
                self.close()
                self.admin_window = AdminWindow()
                self.admin_window.show()
            elif new_version == False:
                self.close()
                self.main_window = MainWindow()
                self.main_window.show()
            elif new_version == None:
                self.show()
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

    def show_admin_panel_choice_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор версии админ-панели")
        dialog.setMinimumSize(600, 300)
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 30)

        label = QLabel(
            "Какой версией панели администратора необходимо воспользоваться?\n\n"
            "В новой версии временно недоступны операции изменения и удаления,\n"
            "но добавлены улучшенная фильтрация, поиск и аналитика."
        )
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 14px;")
        layout.addWidget(label)

        button_layout = QVBoxLayout()
        button_layout.addStretch()

        button_box = QDialogButtonBox()
        new_button = button_box.addButton(
            "Новая версия", QDialogButtonBox.ButtonRole.AcceptRole
        )
        old_button = button_box.addButton(
            "Старая версия", QDialogButtonBox.ButtonRole.RejectRole
        )

        new_button.setFixedHeight(40)
        old_button.setFixedHeight(40)

        new_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 14px;
                border-radius: 6px;
                padding: 10px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """
        )
        old_button.setStyleSheet(
            """
            QPushButton {
                background-color: #E0E0E0;
                color: black;
                font-size: 14px;
                border-radius: 6px;
                padding: 10px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #CCCCCC;
            }
        """
        )

        button_layout.addWidget(new_button)
        button_layout.addWidget(old_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            return True
        elif result == QDialog.DialogCode.Rejected:
            return False
        else:
            return None
