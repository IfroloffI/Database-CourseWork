from app.ui.controllers.base_controller import BaseController
from app.core.database.models import Client
from typing import Optional
from app.ui.utils.base_table_model import BaseTableModel


class ClientController(BaseController):
    def load_clients(self, table_view):
        clients = self.data_service.get_all_clients()
        data = []
        for client in clients:
            data.append(
                [
                    client.id,
                    client.last_name,
                    client.first_name,
                    client.passport_number,
                    client.phone_number or "",
                    client.email or "",
                    client.created_at.strftime("%Y-%m-%d %H:%M"),
                    client.updated_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )
        headers = [
            "ID",
            "Фамилия",
            "Имя",
            "Паспорт",
            "Телефон",
            "Email",
            "Создан",
            "Обновлен",
        ]
        table_view.setModel(BaseTableModel(data, headers))

    def select_client(self, client_id: int) -> Optional[Client]:
        return self.data_service.get_client_by_id(client_id)

    def add_client(self, **data) -> bool:
        try:
            success = self.data_service.add_client(**data)
            if success:
                self.data_updated.emit()
            return success
        except Exception as e:
            self.show_error(f"Ошибка при добавлении клиента: {str(e)}")
            return False

    def update_client(self, client_id: int, **data) -> bool:
        success = self.data_service.update_client(client_id, **data)
        if success:
            self.data_updated.emit()
        return success

    def delete_client(self, client_id: int) -> bool:
        success = self.data_service.delete_client(client_id)
        if success:
            self.data_updated.emit()
        return success

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        return self.data_service.get_client_by_id(client_id)
