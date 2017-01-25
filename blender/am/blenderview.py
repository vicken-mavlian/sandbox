from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import filterwidget

import data

import os

class BlenderView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(BlenderView, self).__init__(parent=parent)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(self.NoEditTriggers)
        self.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
        self.setHeaderHidden(True)

class BlenderProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(BlenderProxyModel, self).__init__()
        self.publish_filter = False

    def filterAcceptsRow(self, sourceRow, sourceParent):

        model = self.sourceModel()

        # if there's no parent, that means it's a data "category" item. so accept the row
        index = model.index(sourceRow, 0, sourceParent)
        item = model.itemFromIndex(index)
        if not item.parent():
            return True

        return super(BlenderProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)


class BlenderModel(QtGui.QStandardItemModel):
    DATABLOCKS = range(1)


class AssetSummary(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AssetSummary, self).__init__(parent)

        self.thumbnail = QtWidgets.QLabel()
        self.thumbnail.setScaledContents(True)
        self.thumbnail.setFixedSize(QtCore.QSize(128, 128))

        self.comment_box = QtWidgets.QTextEdit()
        self.comment_box.setReadOnly(True)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.thumbnail)
        layout.addWidget(self.comment_box)
        self.setLayout(layout)

class BlenderFile(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BlenderFile, self).__init__(parent)
        self.blender_filter = filterwidget.FilterWidget()
        self.blender_view = BlenderView()

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.blender_filter)
        layout.addWidget(self.blender_view)
        self.setLayout(layout)

class BlenderBrowser(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BlenderBrowser, self).__init__(parent)
        self.asset_summary = AssetSummary()
        self.blender_file = BlenderFile()

        self.model = BlenderModel()
        self.model.setColumnCount(1)
        self.model.setHorizontalHeaderLabels(['Datablock'])

        self.proxymodel = BlenderProxyModel()
        self.proxymodel.setDynamicSortFilter(True)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.setFilterKeyColumn(-1)
        self.proxymodel.setSourceModel(self.model)

        self.blender_file.blender_view.setModel(self.proxymodel)

        splitter = QtWidgets.QSplitter()
        splitter.setOrientation(QtCore.Qt.Vertical)
        splitter.addWidget(self.asset_summary)
        splitter.addWidget(self.blender_file)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.blender_file.blender_filter.filter_edit.textChanged.connect(self.filterChanged)

        self.setRevision("", "")

    def setRevision(self, comment, thumbnail):
        if thumbnail:
            image_path = os.path.join(data.root_path, 'resources', thumbnail)
        else:
            image_path = os.path.join(data.root_path, 'resources', 'empty.png')

        image = QtGui.QImage(image_path)
        pixmap = QtGui.QPixmap(image)

        self.asset_summary.thumbnail.setPixmap(pixmap)
        self.asset_summary.comment_box.setText(comment)

    def filterChanged(self, event):
        text = self.blender_file.blender_filter.filter_edit.text()
        syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.Wildcard)
        case_sensitivity = QtCore.Qt.CaseSensitive
        regExp = QtCore.QRegExp(text, case_sensitivity, syntax)

        self.proxymodel.setFilterRegExp(regExp)

        self.blender_file.blender_view.expandAll()