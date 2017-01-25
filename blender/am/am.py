from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import data

import filterwidget

import assetsview
import shotsview
import logview
import blenderview


class AMAssetInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AMAssetInfo, self).__init__(parent)

        self.assets_browser = assetsview.AssetsBrowser()
        self.assets_model = assetsview.AssetsModel()
        self.assets_proxy_model = assetsview.AssetsProxyModel()
        self.assets_proxy_model.setSourceModel(self.assets_model)

        self.assets_browser.assets_view.setModel(self.assets_proxy_model)
        self.assets_browser.assets_view.selectionModel().currentChanged.connect(self.update_asset_logs)
        self.assets_browser.departments.currentIndexChanged.connect(self.update_asset_logs)

        self.shots_browser = shotsview.ShotsBrowser()
        self.shots_model = shotsview.ShotsModel()
        self.shots_proxy_model = shotsview.ShotsProxyModel()
        self.shots_proxy_model.setSourceModel(self.shots_model)

        self.shots_browser.shots_view.setModel(self.shots_proxy_model)
        self.shots_browser.shots_view.selectionModel().currentChanged.connect(self.update_shot_logs)
        self.shots_browser.departments.currentIndexChanged.connect(self.update_shot_logs)

        self.shot_assets_tab = QtWidgets.QTabWidget()
        self.shot_assets_tab.addTab(self.assets_browser, "assets")
        self.shot_assets_tab.addTab(self.shots_browser, "shots")

        self.log_browser = logview.LogBrowser()
        splitter = QtWidgets.QSplitter()
        splitter.setOrientation(QtCore.Qt.Vertical)
        splitter.addWidget(self.shot_assets_tab)
        splitter.addWidget(self.log_browser)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)

        self.setLayout(layout)

    def update_shot_logs(self, event):
        department = self.shots_browser.departments.currentText()

        # TODO Hack, it may not be a proxy model
        asset_model = self.shots_browser.shots_view.model().sourceModel()

        index = self.shots_browser.shots_view.selectionModel().currentIndex()
        index = self.shots_browser.shots_view.model().mapToSource(index)
        item = asset_model.itemFromIndex(index)
        if not item:
            return

        sequence_name = item.parent().text()
        shot_name = item.text()

        # clear the revision logs model by setting row count to 0
        log_model = self.log_browser.model
        log_model.setRowCount(0)

        for sequence in data.shots:
            if sequence.name == sequence_name:
                for shot in sequence.shots:
                    if shot.name == shot_name:
                        for rev in shot.revisions:
                            version = rev.version
                            date = rev.date
                            user = rev.user
                            comment = rev.comment
                            published = rev.publish
                            thumbnail= rev.thumbnail

                            import os
                            if published == 'True':
                                icon_path = os.path.join(data.root_path, 'resources', 'rev_publish.png')
                            else:
                                icon_path = os.path.join(data.root_path, 'resources', 'rev_wip.png')
                            icon = QtGui.QIcon(icon_path)

                            log_model.insertRow(0)
                            log_model.setData(log_model.index(0, log_model.VERSION), version)
                            log_model.setData(log_model.index(0, log_model.VERSION), icon, role=QtCore.Qt.DecorationRole)
                            log_model.setData(log_model.index(0, log_model.DATE), date)
                            log_model.setData(log_model.index(0, log_model.USER), user)
                            log_model.setData(log_model.index(0, log_model.COMMENT), comment)
                            log_model.setData(log_model.index(0, log_model.PUBLISHED), published)
                            log_model.setData(log_model.index(0, log_model.THUMBNAIL), thumbnail)

    def update_asset_logs(self, event):
        department = self.assets_browser.departments.currentText()

        # TODO Hack, it may not be a proxy model
        asset_model = self.assets_browser.assets_view.model().sourceModel()

        index = self.assets_browser.assets_view.selectionModel().currentIndex()
        index = self.assets_browser.assets_view.model().mapToSource(index)
        item = asset_model.itemFromIndex(index)
        if not item:
            return

        asset_name = item.text()

        # clear the revision logs model by setting row count to 0
        log_model = self.log_browser.model
        log_model.setRowCount(0)

        for asset_revision in data.asset_revisions:
            correct_asset = asset_revision.asset.name == asset_name
            correct_department = asset_revision.department == department
            if correct_asset and correct_department:
                for rev in asset_revision.revisions:
                    version = rev.version
                    date = rev.date
                    user = rev.user
                    comment = rev.comment
                    published = rev.publish
                    thumbnail= rev.thumbnail

                    import os
                    if published == 'True':
                        icon_path = os.path.join(data.root_path, 'resources', 'rev_publish.png')
                    else:
                        icon_path = os.path.join(data.root_path, 'resources', 'rev_wip.png')
                    icon = QtGui.QIcon(icon_path)

                    log_model.insertRow(0)
                    log_model.setData(log_model.index(0, log_model.VERSION), version)
                    log_model.setData(log_model.index(0, log_model.VERSION), icon, role=QtCore.Qt.DecorationRole)
                    log_model.setData(log_model.index(0, log_model.DATE), date)
                    log_model.setData(log_model.index(0, log_model.USER), user)
                    log_model.setData(log_model.index(0, log_model.COMMENT), comment)
                    log_model.setData(log_model.index(0, log_model.PUBLISHED), published)
                    log_model.setData(log_model.index(0, log_model.THUMBNAIL), thumbnail)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.asset_info = AMAssetInfo()
        self.blender_browser = blenderview.BlenderBrowser()

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self.asset_info)
        splitter.addWidget(self.blender_browser)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)

        self.setLayout(layout)

        self.asset_info.log_browser.log_view.selectionModel().currentChanged.connect(self.current_revision_changed)

    def current_revision_changed(self, event):
        department = self.asset_info.assets_browser.departments.currentText()

        # TODO Hack, it may not be a proxy model
        asset_model = self.asset_info.assets_browser.assets_view.model().sourceModel()

        index = self.asset_info.assets_browser.assets_view.selectionModel().currentIndex()
        index = self.asset_info.assets_browser.assets_view.model().mapToSource(index)
        asset_name = asset_model.itemFromIndex(index).text()

        log_model = self.asset_info.log_browser.log_view.model().sourceModel()

        index = self.asset_info.log_browser.log_view.selectionModel().currentIndex()
        index = self.asset_info.log_browser.log_view.model().mapToSource(index)

        comment = ""
        thumbnail = ""
        version = -1
        row = index.row()
        if row != -1:
            version = log_model.data(log_model.index(row, log_model.VERSION))
            comment = log_model.data(log_model.index(row, log_model.COMMENT))
            thumbnail = log_model.data(log_model.index(row, log_model.THUMBNAIL))

        self.blender_browser.setRevision(comment, thumbnail)

        # TODO all this below should be moved to BlenderBrowser class

        model = self.blender_browser.model
        model.setRowCount(0)

        for asset_revision in data.asset_revisions:
            correct_asset = asset_revision.asset.name == asset_name
            correct_department = asset_revision.department == department
            if correct_asset and correct_department:
                for rev in asset_revision.revisions:
                    if rev.version == version:
                        for datablock in rev.blend.datablocks:
                            model.insertRow(0)
                            model.setData(model.index(0, 0), datablock.name)
                            item = model.item(0,0)

                            for data_object in datablock.datas:
                                data_item = QtGui.QStandardItem()
                                data_item.setText(data_object.name)
                                item.appendRow(data_item)

        self.blender_browser.blender_file.blender_view.expandAll()

class AMMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AMMainWindow, self).__init__(parent)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.setWindowTitle("Asset Management")


def populate_assets_model(model):
    model.setRowCount(0)

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

def populate_shots_model(model):
    model.setRowCount(0)

    root = model.invisibleRootItem()

    for sequence in data.shots:
        seq_item = QtGui.QStandardItem()
        seq_item.setText(sequence.name)
        root.appendRow(seq_item)

        for shot in sequence.shots:
            shot_item = QtGui.QStandardItem()
            shot_item.setText(shot.name)

            seq_item.appendRow(shot_item)

if __name__ == "__main__":
    import sys
    data.regenerate()

    if not QtWidgets.qApp.instance():
        app = QtWidgets.QApplication(sys.argv)
        asset_manager = AMMainWindow()

        asset_model = asset_manager.main_widget.asset_info.assets_model
        populate_assets_model(asset_model)
        asset_manager.main_widget.asset_info.assets_browser.assets_view.expandAll()

        shots_model = asset_manager.main_widget.asset_info.shots_model
        populate_shots_model(shots_model)
        asset_manager.main_widget.asset_info.shots_browser.shots_view.expandAll()


        asset_manager.show()
        sys.exit(app.exec_())


import sys
import importlib
importlib.reload(data)
data.regenerate()

if not QtWidgets.qApp.instance():
    app = QtWidgets.QApplication(sys.argv)
asset_manager = AMMainWindow()

asset_model = asset_manager.main_widget.asset_info.assets_model
populate_assets_model(asset_model)
asset_manager.main_widget.asset_info.assets_browser.assets_view.expandAll()

asset_manager.show()

