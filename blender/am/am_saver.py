from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import os

import data
import blenderview


class LabeledLineEdit(QtWidgets.QWidget):
    def __init__(self, label="", parent=None):
        super(LabeledLineEdit, self).__init__(parent=parent)
        self.label = QtWidgets.QLabel(label)
        self.line_edit = QtWidgets.QLineEdit()

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)


class Header(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Header, self).__init__(parent=parent)

        self.save_revision = QtWidgets.QLabel()
        font = self.save_revision.font()
        font.setPointSize(20)
        self.save_revision.setFont(font)
        self.save_revision.setText('Save Revision')

        self.asset_information = QtWidgets.QLabel()
        font = self.asset_information.font()
        font.setPointSize(12)
        self.asset_information.setText('Character / Mei / Surfacing / v010')
        self.asset_information.setFont(font)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 10, 0, 10)

        layout.addWidget(self.asset_information)
        spacer = QtWidgets.QSpacerItem(200, QtWidgets.QSizePolicy.Fixed)
        layout.addSpacerItem(spacer)

        layout.setAlignment(self.asset_information, QtCore.Qt.AlignLeft)

        self.setLayout(layout)


class Save(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Save, self).__init__(parent=parent)

        self.save_button = QtWidgets.QPushButton('Save')
        self.save_and_publish_button = QtWidgets.QPushButton('Save and Publish')

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()
        layout.addWidget(self.save_button)
        layout.addWidget(self.save_and_publish_button)

        self.setLayout(layout)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent=parent)
        self.header = Header()
        self.version_summary = blenderview.VersionSummary()
        self.version_summary.log_browser.hide()
        self.thumbnail = blenderview.Thumbnail()
        self.comment_box = blenderview.CommentBox()
        self.save = Save()

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.header)
        layout.addWidget(self.version_summary)
        layout.addWidget(self.save)

        self.setLayout(layout)

        image_path = os.path.join(data.root_path, 'resources', 'click.png')
        image = QtGui.QImage(image_path)
        pixmap = QtGui.QPixmap(image)
        self.version_summary.thumbnail.setPixmap(pixmap)
        self.version_summary.thumbnail.clicked.connect(self.thumbnail_clicked)

    def thumbnail_clicked(self):
        def poop():
            info = {'wicked':'sweet',
                    'better':[0, 1, 2, 3, 4, 5]}
            broadcast(info)

        pos = QtGui.QCursor.pos()
        camera_menu = QtWidgets.QMenu("Cameras", parent=self)
        camera_menu.addAction("Camera.001", poop)
        camera_menu.addAction("Camera.002", poop)
        camera_menu.addAction("Camera.003", poop)

        menu = QtWidgets.QMenu(parent=self)
        menu.addAction("Current Camera", poop)
        menu.addMenu(camera_menu)
        menu.exec_(pos)


class AMMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AMMainWindow, self).__init__(parent=parent)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.setWindowTitle("Asset Management")

        self.setFixedSize(self.minimumSize())


callbacks = []


def add_callback(callback_item):
    callbacks.append(callback_item)

def broadcast(info):
    for callback_item in callbacks:
        callback_item(info)

if __name__ == "__main__":
    import sys
    data.regenerate()

    if not QtWidgets.qApp.instance():
        app = QtWidgets.QApplication(sys.argv)
        asset_manager = AMMainWindow()

        asset_manager.show()
        sys.exit(app.exec_())

import sys
import importlib
importlib.reload(data)
data.regenerate()

if not QtWidgets.qApp.instance():
    app = QtWidgets.QApplication(sys.argv)
asset_manager = AMMainWindow()

asset_manager.show()

