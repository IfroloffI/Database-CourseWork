from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from app.core.services.data_service import DataService


class BaseController(QObject):
    data_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.data_service = DataService()

    def show_error(self, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText(message)
        msg.setWindowTitle("Ошибка")
        msg.exec()
