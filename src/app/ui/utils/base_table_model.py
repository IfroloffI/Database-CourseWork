from PyQt6.QtCore import QAbstractTableModel, Qt


class BaseTableModel(QAbstractTableModel):
    def __init__(self, data: list, headers: list):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self._headers[section]
        return None
