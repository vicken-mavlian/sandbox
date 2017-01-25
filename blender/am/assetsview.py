from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import data

import filterwidget

class AssetsModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(AssetsModel, self).__init__()

    def repopulate(self):
        self.beginResetModel()
        self.clear()

        root = self.invisibleRootItem()
        for obj in []:
            item = QtGui.QStandardItem(obj.name)
            root.appendRow(item)

        self.endResetModel()

    def dataChanged(self, top_left, bottom_right, roles=[]):
        return super(AssetsModel, self).__init__()


class AssetsView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(AssetsView, self).__init__(parent)
        self.setHeaderHidden(True)
        self.setEditTriggers(self.NoEditTriggers)
        self.setAlternatingRowColors(True)


class AssetsProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(AssetsProxyModel, self).__init__()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        model = self.sourceModel()

        # if there's no parent, that means it's a "category" item, not an asset. so accept the row
        index = model.index(sourceRow, 0, sourceParent)
        item = model.itemFromIndex(index)
        if not item.parent():
            return True

        return super(AssetsProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

class AssetsBrowser(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AssetsBrowser, self).__init__(parent)

        self.departments = QtWidgets.QComboBox()
        self.departments.addItems(data.departments)

        self.filter_widget = filterwidget.FilterWidget()
        self.assets_view = AssetsView()

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.departments)
        layout.addWidget(self.filter_widget)
        layout.addWidget(self.assets_view)

        self.setLayout(layout)

        self.filter_widget.filter_edit.textChanged.connect(self.filterChanged)
        self.departments.currentIndexChanged.connect(self.departmentChanged)

    def departmentChanged(self, event):
        pass

    def filterChanged(self, event):
        # TODO: Hack, the model may not be a proxy model. Probably requires refactoring
        text = self.filter_widget.filter_edit.text()
        syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.Wildcard)
        case_sensitivity = QtCore.Qt.CaseSensitive
        regExp = QtCore.QRegExp(text, case_sensitivity, syntax)

        proxymodel = self.assets_view.model()
        proxymodel.setFilterRegExp(regExp)
        self.assets_view.expandAll()
