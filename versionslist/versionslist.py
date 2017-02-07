from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

import sys


class VersionsDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        #painter.setBrush(QtGui.QBrush(QtCore.Qt.red))

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        painter.drawText(option.rect.x(), option.rect.y(), "wcied")


class VersionsList(QtWidgets.QTreeView):
    def __init__(self):
       super(VersionsList, self).__init__()

class VersionItem(QtWidgets.QTreeWidgetItem):
    def __init__(self):
        super(VersionItem, self).__init__()
        self.setText(0, 'ok')
        self.setText(1, 'ok')
        self.setText(2, 'ok')

    def sizeHint(self, p_int):
        return QtCore.QSize(300,300)

class Item(QtWidgets.QWidget):
    def __init__(self):
        super(Item, self).__init__()
        l = QtWidgets.QLabel('wicked')
        b = QtWidgets.QPushButton('button')

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(l)
        layout.addWidget(b)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        #option.palette.highlight()
        #QtGui.QPalette.highlight()

        if self.hasFocus():
            pen = QtGui.QPen()
            pen.setWidth(5)
            pen.setColor(QtGui.QPalette().color(QtGui.QPalette.Mid))
            painter.setPen(pen)

            #brush = QtGui.QBrush()

            #painter.setBrush(QtGui.QPalette().light())

            painter.drawRect(event.rect())
            #painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QPalette().light()))
        painter.end()

    def mousePressEvent(self, event):
        self.setFocus()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.model = QtGui.QStandardItemModel()
        root = self.model.invisibleRootItem()
        root.appendRow(QtGui.QStandardItem('item 1'))
        root.appendRow(QtGui.QStandardItem('item 2'))
        root.appendRow(QtGui.QStandardItem('item 3'))

        self.versions_list = VersionsList()
        self.versions_list.setModel(self.model)
        self.versions_list.setItemDelegate(VersionsDelegate())

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        #layout.addWidget(self.versions_list)
        #widget = QtWidgets.QTreeWidget()
        #widget.addTopLevelItem(VersionItem())
        #layout.addWidget(widget)
        layout.addWidget(Item())
        layout.addWidget(Item())
        layout.addWidget(Item())
        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

