from PyQt5 import QtWidgets


class FilterEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super(FilterEdit, self).__init__()
        self.setPlaceholderText("Filter")


class FilterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FilterWidget, self).__init__(parent=parent)
        self.filter_edit = FilterEdit()

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.filter_edit)
        self.setLayout(layout)
