from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import data

import assetsview
import blenderview

class AMAssetInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AMAssetInfo, self).__init__(parent)

        self.assets_browser = assetsview.AssetsBrowser()
        self.assets_model = assetsview.AssetsModel()
        self.assets_proxy_model = assetsview.AssetsProxyModel()
        self.assets_proxy_model.setSourceModel(self.assets_model)

        self.assets_browser.view.setModel(self.assets_proxy_model)

        self.shots_browser = assetsview.AssetsBrowser()
        self.shots_model = assetsview.AssetsModel()
        self.shots_proxy_model = assetsview.AssetsProxyModel()
        self.shots_proxy_model.setSourceModel(self.shots_model)

        self.shots_browser.view.setModel(self.shots_proxy_model)

        self.shot_assets_tab = QtWidgets.QTabWidget()
        self.shot_assets_tab.addTab(self.assets_browser, "assets")
        self.shot_assets_tab.addTab(self.shots_browser, "shots")

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.shot_assets_tab)

        self.setLayout(layout)


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

        self.blender_browser.asset_summary.log_browser.log_view.selectionModel().currentChanged.connect(self.current_revision_changed)

        self.asset_info.assets_browser.view.selectionModel().currentChanged.connect(self.update_asset_logs)
        self.asset_info.assets_browser.departments.currentIndexChanged.connect(self.update_asset_logs)

        self.asset_info.shots_browser.view.selectionModel().currentChanged.connect(self.update_shot_logs)
        self.asset_info.shots_browser.departments.currentIndexChanged.connect(self.update_shot_logs)

    def update_shot_logs(self, event):
        department = self.asset_info.shots_browser.departments.currentText()

        # TODO Hack, it may not be a proxy model
        asset_model = self.asset_info.shots_browser.view.model().sourceModel()

        index = self.asset_info.shots_browser.view.selectionModel().currentIndex()
        index = self.asset_info.shots_browser.view.model().mapToSource(index)
        item = asset_model.itemFromIndex(index)
        if not item:
            return

        if not item.parent():
            return

        sequence_name = item.parent().text()
        shot_name = item.text()

        # clear the revision logs model by setting row count to 0
        log_model = self.blender_browser.asset_summary.log_browser.model
        log_model.setRowCount(0)

        for shot_revision in data.shot_revisions:
            correct_shot = (shot_revision.asset.name == shot_name) and \
                           (shot_revision.asset.section == sequence_name)
            correct_department = shot_revision.department == department
            if correct_shot and correct_department:
                for rev in shot_revision.revisions:
                    version = rev.version
                    date = rev.date
                    user = rev.user
                    comment = rev.comment
                    published = rev.publish
                    thumbnail = rev.thumbnail

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
        department = self.asset_info.assets_browser.departments.currentText()

        # TODO Hack, it may not be a proxy model
        asset_model = self.asset_info.assets_browser.view.model().sourceModel()

        index = self.asset_info.assets_browser.view.selectionModel().currentIndex()
        index = self.asset_info.assets_browser.view.model().mapToSource(index)
        item = asset_model.itemFromIndex(index)
        if not item:
            return

        asset_name = item.text()

        # clear the revision logs model by setting row count to 0
        log_model = self.blender_browser.asset_summary.log_browser.model

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
                    thumbnail = rev.thumbnail

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

    def current_revision_changed(self, event):
        tab_idx = self.asset_info.shot_assets_tab.currentIndex()
        tab_text = self.asset_info.shot_assets_tab.tabText(tab_idx)

        # TODO this if statement is hokey
        if tab_text == 'assets':
            revisions = data.asset_revisions
        else:
            revisions = data.shot_revisions

        # TODO assumes both tabs have same dept widget
        browser = self.asset_info.shot_assets_tab.currentWidget()
        view = browser.view
        department = browser.departments.currentText()

        index = view.selectionModel().currentIndex()
        index = view.model().mapToSource(index)
        # TODO it may not be a proxy model
        item = view.model().sourceModel().itemFromIndex(index)
        if not item:
            return
        asset_name = item.text()

        log_model = self.blender_browser.asset_summary.log_browser.model

        index = self.blender_browser.asset_summary.log_browser.log_view.selectionModel().currentIndex()
        index = self.blender_browser.asset_summary.log_browser.log_view.model().mapToSource(index)

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

        for asset_revision in revisions:
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

    for asset in data.assets:
        section = asset.section
        name = asset.name

        section_items = model.findItems(section)
        if section_items:
            section_item = section_items[0]
        else:
            section_item = QtGui.QStandardItem()
            section_item.setText(section)
            root.appendRow(section_item)

        item = QtGui.QStandardItem()
        item.setText(name)
        section_item.appendRow(item)


def populate_shots_model(model):
    model.setRowCount(0)

    root = model.invisibleRootItem()

    for shot in data.shots:
        section = shot.section
        name = shot.name

        section_items = model.findItems(section)
        if section_items:
            section_item = section_items[0]
        else:
            section_item = QtGui.QStandardItem()
            section_item.setText(section)
            root.appendRow(section_item)

        item = QtGui.QStandardItem()
        item.setText(name)
        section_item.appendRow(item)

if __name__ == "__main__":
    import sys
    data.regenerate()

    if not QtWidgets.qApp.instance():
        app = QtWidgets.QApplication(sys.argv)
        asset_manager = AMMainWindow()

        asset_model = asset_manager.main_widget.asset_info.assets_model
        populate_assets_model(asset_model)
        asset_manager.main_widget.asset_info.assets_browser.view.expandAll()

        shots_model = asset_manager.main_widget.asset_info.shots_model
        populate_shots_model(shots_model)
        asset_manager.main_widget.asset_info.shots_browser.view.expandAll()

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
asset_manager.main_widget.asset_info.assets_browser.view.expandAll()

shots_model = asset_manager.main_widget.asset_info.shots_model
populate_shots_model(shots_model)
asset_manager.main_widget.asset_info.shots_browser.view.expandAll()

asset_manager.show()

