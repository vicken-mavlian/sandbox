from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import data

import filterwidget

class ShotsModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(ShotsModel, self).__init__()

    def repopulate(self):
        self.beginResetModel()
        self.clear()

        root = self.invisibleRootItem()
        for obj in []:
            item = QtGui.QStandardItem(obj.name)
            root.appendRow(item)

        self.endResetModel()

    def dataChanged(self, top_left, bottom_right, roles=[]):
        return super(ShotsModel, self).__init__()


class ShotsView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(ShotsView, self).__init__(parent)
        self.setHeaderHidden(True)
        self.setEditTriggers(self.NoEditTriggers)
        self.setAlternatingRowColors(True)


class ShotsProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(ShotsProxyModel, self).__init__()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        model = self.sourceModel()

        # if there's no parent, that means it's a "category" item, not an asset. so accept the row
        index = model.index(sourceRow, 0, sourceParent)
        item = model.itemFromIndex(index)
        if not item.parent():
            return True

        return super(ShotsProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

class ShotsBrowser(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ShotsBrowser, self).__init__(parent)

        self.departments = QtWidgets.QComboBox()
        self.departments.addItems(data.departments)

        self.filter_widget = filterwidget.FilterWidget()
        self.view = ShotsView()

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.departments)
        layout.addWidget(self.filter_widget)
        layout.addWidget(self.view)

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

        proxymodel = self.view.model()
        proxymodel.setFilterRegExp(regExp)
        self.view.expandAll()
