from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import filterwidget

import os, sys

class LogView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(LogView, self).__init__(parent=parent)
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(self.NoEditTriggers)
        self.header().setSortIndicator(0, QtCore.Qt.AscendingOrder)
        #self.setUniformRowHeights(True)

class LogProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(LogProxyModel, self).__init__()
        self.publish_filter = False

    def setPublishFilter(self, state):
        self.publish_filter = state
        self.invalidateFilter()

    def publishFilter(self):
        return self.publish_filter

    def filterAcceptsRow(self, sourceRow, sourceParent):
        model = self.sourceModel()

        index = model.index(sourceRow, model.PUBLISHED, sourceParent)
        data = self.sourceModel().data(index) == 'True'

        if self.publish_filter:
            if not data:
                index = model.index(sourceRow, model.COMMENT, sourceParent)
                data = model.data(index)

                return False

        return super(LogProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

class LogModel(QtGui.QStandardItemModel):
    VERSION, DATE, USER, COMMENT, PUBLISHED, THUMBNAIL = range(6)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        # handle SizeHintRole so that multiline items don't expand the row height
        if role == QtCore.Qt.SizeHintRole:
            # TODO hardcoded height to 20. Should figure out system default for min size.
            return QtCore.QSize(0, 20)
        return super(LogModel, self).data(index, role)


class LogBrowser(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LogBrowser, self).__init__(parent)

        self.model = LogModel()
        self.model.setColumnCount(4)
        # XXX more columns: version, is_published
        self.model.setHorizontalHeaderLabels(["version", "date", "user", "comment", "published", "thumbnail"])

        self.proxymodel = LogProxyModel()#QtCore.QSortFilterProxyModel()
        self.proxymodel.setDynamicSortFilter(True)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.setFilterKeyColumn(-1)

        self.publish_checkbox = QtWidgets.QCheckBox('published only')
        self.log_filter = filterwidget.FilterWidget()
        self.log_view = LogView()

        self.log_view.setModel(self.proxymodel)
        self.log_view.setColumnHidden(self.model.PUBLISHED, True)
        self.log_view.setColumnHidden(self.model.THUMBNAIL, True)

        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(self.log_filter)
        filter_layout.addWidget(self.publish_checkbox)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(filter_layout)
        layout.addWidget(self.log_view)
        self.setLayout(layout)

        self.publish_checkbox.toggled.connect(self.filterChanged)
        self.log_filter.filter_edit.textChanged.connect(self.filterChanged)

    def filterChanged(self, event):
        publish_only = self.publish_checkbox.isChecked()

        text = self.log_filter.filter_edit.text()
        syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.Wildcard)
        case_sensitivity = QtCore.Qt.CaseSensitive
        regExp = QtCore.QRegExp(text, case_sensitivity, syntax)

        self.proxymodel.setFilterRegExp(regExp)
        self.proxymodel.setPublishFilter(publish_only)

class LogViewer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(LogViewer, self).__init__(parent)
        self.log_browser = LogBrowser()

        model = self.log_browser.model
        populate(model)

        self.setCentralWidget(self.log_browser)

        self.setWindowTitle("Log Viewer")

def populate(model):
    logs = [
            ('vicken.mavlian', '2017-08-10 12:00PM', 'published asset to be wicked', True),
            ('cristian.kovacs', '2017-07-02 12:00PM', 'published asset to be less wicked', True),
            ('cristian.kovacs', '2017-09-01 12:00PM', 'published asset to be bad', False),
            ('vicken.mavlian', '2017-03-20 12:00PM', 'made wicked again', False),
            ('vicken.mavlian', '2017-12-12 12:00PM', 'made even better', True),
            ]

    for user, date, comment, published in logs:
        model.insertRow(0)
        model.setData(model.index(0, model.DATE), date)
        model.setData(model.index(0, model.USER), user)
        model.setData(model.index(0, model.COMMENT), comment)
        model.setData(model.index(0, model.PUBLISHED), published)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    logviewer = LogViewer()
    logviewer.show()
    logviewer.resize(800,200)



    sys.exit(app.exec_())
