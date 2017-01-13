from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import os, sys

####### Filter #########
class FilterEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super(FilterEdit, self).__init__()
        self.setPlaceholderText("Filter")

class LogFilter(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LogFilter, self).__init__(parent=parent)
        self.publish_checkbox = QtWidgets.QCheckBox('published only')
        self.filter_edit = FilterEdit()

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.publish_checkbox)
        layout.addWidget(self.filter_edit)
        self.setLayout(layout)

##### End Filter ########

class LogView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(LogView, self).__init__(parent=parent)
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(self.NoEditTriggers)

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
        data = self.sourceModel().data(index)

        if self.publish_filter:
            if not data:
                index = model.index(sourceRow, model.COMMENT, sourceParent)
                data = model.data(index)

                return False

        return super(LogProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

class LogModel(QtGui.QStandardItemModel):
    DATE, USER, COMMENT, PUBLISHED = range(4)

class LogBrowser(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LogBrowser, self).__init__(parent)

        self.model = LogModel()
        self.model.setColumnCount(4)
        # XXX more columns: version, is_published
        self.model.setHorizontalHeaderLabels(["date", "user", "comment", "published"])

        self.proxymodel = LogProxyModel()#QtCore.QSortFilterProxyModel()
        self.proxymodel.setDynamicSortFilter(True)
        self.proxymodel.setSourceModel(self.model)
        self.proxymodel.setFilterKeyColumn(-1)

        self.log_filter = LogFilter()
        self.log_view = LogView()

        self.log_view.setModel(self.proxymodel)
        #self.log_view.setColumnHidden(self.model.PUBLISHED, True)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.log_filter)
        layout.addWidget(self.log_view)
        self.setLayout(layout)

        self.log_filter.publish_checkbox.toggled.connect(self.filterChanged)
        self.log_filter.filter_edit.textChanged.connect(self.filterChanged)

    def filterChanged(self, event):
        publish_only = self.log_filter.publish_checkbox.isChecked()
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
