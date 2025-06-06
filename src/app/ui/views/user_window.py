from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton


class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пользователь")
        self.resize(1000, 800)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Вы вошли как пользователь")
        layout.addWidget(label)

        # Пример кнопки выхода
        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.close)
        layout.addWidget(logout_btn)

        self.setLayout(layout)
