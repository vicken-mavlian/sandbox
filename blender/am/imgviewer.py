from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import os, sys

class FilterEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super(FilterEdit, self).__init__()
        self.setPlaceholderText("Filter")

class ImageView(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent=parent)
        self.setViewMode(self.IconMode)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Minimum))
        self.setUniformItemSizes(True)
        self.setMovement(self.Snap)
        self.setSelectionMode(self.NoSelection)
        self.setEditTriggers(self.NoEditTriggers)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def sizeHint(self):
        import math

        item_height = self.sizeHintForRow(0)
        item_width = self.sizeHintForColumn(0)

        if not item_width:
            return QtCore.QSize()

        item_count = self.model().rowCount()

        area_width = self.childrenRect().width()
        items_per_row = (area_width-1)//item_width

        rows = item_count
        if self.viewMode() == self.IconMode:
            rows = math.ceil(item_count/items_per_row)
        height = (rows * item_height)+(self.size().height()-self.childrenRect().height())

        size = QtCore.QSize()
        size.setHeight(height)

        return size

    def resizeEvent(self, event):
        super(ImageView, self).resizeEvent(event)
        self.updateGeometry()

    def filterItems(self, filter_text):
        self.model().setFilterRegExp(filter_text)

class ImageBrowser(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageBrowser, self).__init__(parent)

        self.filter_edit = FilterEdit()

        self.image_list = ImageView()
        self.image_list.setIconSize(QtCore.QSize(100,100))

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.filter_edit)
        layout.addWidget(self.image_list)
        self.setLayout(layout)
        self.setMinimumSize(QtCore.QSize(0, 0))

        self.model = QtGui.QStandardItemModel()
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.image_list.setModel(self.proxy_model)

        resource_path = os.path.join(os.path.dirname(__file__), 'resources')
        for img in os.listdir(resource_path):
            if img.endswith('.png'):
                image_path = os.path.join(resource_path, img)
                icon = QtGui.QIcon(image_path)
                item = QtGui.QStandardItem(icon, img)
                self.model.appendRow(item)

        self.filter_edit.textChanged.connect(self.image_list.filterItems)
        self.image_list.clicked.connect(self.itemClicked)

    def itemClicked(self, event):
        print(self, "item clicked", event)


class ImageViewer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)

        self.image_browser = ImageBrowser()
        self.setCentralWidget(self.image_browser)

        self.setWindowTitle("Image Viewer")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    imgviewer = ImageViewer()
    imgviewer.show()
    imgviewer.resize(800,200)
    sys.exit(app.exec_())
