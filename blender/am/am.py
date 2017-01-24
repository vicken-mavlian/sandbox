from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import data

import filterwidget
import imgviewer
import logview
import blenderview
import importlib
importlib.reload(imgviewer)

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
        department = self.departments.currentText()
        

    def filterChanged(self, event):
        # TODO: Hack, the model may not be a proxy model. Probably requires refactoring
        text = self.filter_widget.filter_edit.text()
        syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.Wildcard)
        case_sensitivity = QtCore.Qt.CaseSensitive
        regExp = QtCore.QRegExp(text, case_sensitivity, syntax)

        proxymodel = self.assets_view.model()
        proxymodel.setFilterRegExp(regExp)
        self.assets_view.expandAll()


class AMAssetInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AMAssetInfo, self).__init__(parent)

        self.assets_browser = AssetsBrowser()
        self.assets_model = AssetsModel()
        self.assets_proxy_model = AssetsProxyModel()
        self.assets_proxy_model.setSourceModel(self.assets_model)

        self.assets_browser.assets_view.setModel(self.assets_proxy_model)
        self.assets_browser.assets_view.selectionModel().currentChanged.connect(self.current_asset_changed)

        self.log_browser = logview.LogBrowser()
        self.log_browser.log_view.selectionModel().currentChanged.connect(self.current_revision_changed)
        #logview.populate(self.log_browser.model)

        self.blender_browser = blenderview.BlenderBrowser()

        splitter = QtWidgets.QSplitter()

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter.addWidget(self.assets_browser)
        splitter.addWidget(self.log_browser)
        splitter.addWidget(self.blender_browser)

        layout.addWidget(splitter)

        self.setLayout(layout)

    def current_asset_changed(self, event):
        department = 'model'

        # TODO Hack, it may not be a proxy model
        asset_item = event.model().mapToSource(event)
        asset_model = event.model().sourceModel()

        asset_name = asset_model.itemFromIndex(asset_item).text()

        # clear the revision logs model by setting row count to 0
        log_model = self.log_browser.model
        log_model.setRowCount(0)

        for asset_revision in data.asset_revisions:
            correct_asset = asset_revision.asset.name == asset_name
            correct_department = asset_revision.department == 'model'
            if correct_asset and correct_department:
                for rev in asset_revision.revisions:
                    version = rev.version
                    date = rev.date
                    user = rev.user
                    comment = rev.comment
                    published = rev.publish

                    log_model.insertRow(0)
                    log_model.setData(log_model.index(0, log_model.VERSION), version)
                    log_model.setData(log_model.index(0, log_model.DATE), date)
                    log_model.setData(log_model.index(0, log_model.USER), user)
                    log_model.setData(log_model.index(0, log_model.COMMENT), comment)
                    log_model.setData(log_model.index(0, log_model.PUBLISHED), published)


    def current_revision_changed(self, event):
        print(event)

class AMMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AMMainWindow, self).__init__(parent)

        self.asset_info = AMAssetInfo()
        self.setCentralWidget(self.asset_info)

        self.setWindowTitle("Asset Management")


def populate_asset_model(model):
    data.regenerate()
    root = model.invisibleRootItem()

    for category in data.categories:
        item = QtGui.QStandardItem()
        item.setText(category)
        root.appendRow(item)

    for asset in data.assets:
        category = asset.category
        name = asset.name
        item = QtGui.QStandardItem()
        item.setText(name)

        # TODO Hack hack hack, getting first item in list. so bad.
        section_item = model.findItems(category)[0]
        section_item.appendRow(item)

if __name__ == "__main__":
    import sys

    if not QtWidgets.qApp.instance():
        app = QtWidgets.QApplication(sys.argv)
        asset_manager = AMMainWindow()

        asset_model = asset_manager.asset_info.assets_model
        populate_asset_model(asset_model)
        asset_manager.asset_info.assets_browser.assets_view.expandAll()

        asset_manager.show()
        sys.exit(app.exec_())

