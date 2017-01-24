from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import filterwidget

class BlenderView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(BlenderView, self).__init__(parent=parent)
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(self.NoEditTriggers)

class BlenderProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(BlenderProxyModel, self).__init__()
        self.publish_filter = False

    def filterAcceptsRow(self, sourceRow, sourceParent):
        model = self.sourceModel()

        index = model.index(sourceRow, model.PUBLISHED, sourceParent)
        data = self.sourceModel().data(index)

        if False:
            if not data:
                index = model.index(sourceRow, model.COMMENT, sourceParent)
                data = model.data(index)

                return False

        return super(BlenderProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)


class BlenderModel(QtGui.QStandardItemModel):
    pass

class BlenderBrowser(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BlenderBrowser, self).__init__(parent)

        self.model = BlenderModel()
        #self.model.setColumnCount(4)
        # XXX more columns: version, is_published
        #self.model.setHorizontalHeaderLabels(["date", "user", "comment", "published"])

        self.proxymodel = BlenderProxyModel()#QtCore.QSortFilterProxyModel()
        self.proxymodel.setDynamicSortFilter(True)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.setFilterKeyColumn(-1)

        self.publish_checkbox = QtWidgets.QCheckBox('published only')
        self.blender_filter = filterwidget.FilterWidget()
        self.blender_view = BlenderView()

        self.blender_view.setModel(self.proxymodel)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.blender_filter)
        layout.addWidget(self.blender_view)
        self.setLayout(layout)

        self.blender_filter.filter_edit.textChanged.connect(self.filterChanged)

    def filterChanged(self, event):
        text = self.log_filter.filter_edit.text()
        syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.Wildcard)
        case_sensitivity = QtCore.Qt.CaseSensitive
        regExp = QtCore.QRegExp(text, case_sensitivity, syntax)

        self.proxymodel.setFilterRegExp(regExp)