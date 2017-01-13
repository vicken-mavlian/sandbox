from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import imgviewer
import logview

import bpy

class AMAssetCategory(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AMAssetCategory, self).__init__(parent)

        button_group = QtWidgets.QButtonGroup()

        btn1 = QtWidgets.QPushButton('charactes')
        btn2 = QtWidgets.QPushButton('sets')
        btn3 = QtWidgets.QPushButton('props')
        btn4 = QtWidgets.QPushButton('materials')

        btn1.setCheckable(True)
        btn2.setCheckable(True)
        btn3.setCheckable(True)
        btn4.setCheckable(True)

        button_group.setExclusive(True)
        button_group.addButton(btn1)
        button_group.addButton(btn2)
        button_group.addButton(btn3)
        button_group.addButton(btn4)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)
        self.setLayout(layout)

        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

class SceneObjectsModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(SceneObjectsModel, self).__init__()
        self.repopulate()

    def repopulate(self):
        self.beginResetModel()
        self.clear()

        root = self.invisibleRootItem()
        for obj in bpy.data.objects:
            item = QtGui.QStandardItem(obj.name)
            root.appendRow(item)

        self.endResetModel()

    def add_object(self, obj):
        root = self.invisibleRootItem()
        item = QtGui.QStandardItem(obj.name)
        root.appendRow(item)

    def remove_object(self, obj):
        root = self.invisibleRootItem()
        for item in self.findItems(obj.name):
            root.removeRow(item.row())

    def dataChanged(self, top_left, bottom_right, roles=[]):
        return super(SceneObjectsModel, self).__init__()

class ObjectList(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(ObjectList, self).__init__(parent)

    def selectionChanged(self, selected, deselected):
        objs = bpy.data.objects.keys()

        for obj in objs:
            bpy.data.objects[obj].select = False

        for index in selected.indexes():
            obj = index.data()
            if obj not in objs:
                continue
            bpy.data.objects[obj].select = True

class AssetsModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(AssetsModel, self).__init__()

    def repopulate(self):
        self.beginResetModel()
        self.clear()

        root = self.invisibleRootItem()
        for obj in bpy.data.objects:
            item = QtGui.QStandardItem(obj.name)
            root.appendRow(item)

        self.endResetModel()

    def dataChanged(self, top_left, bottom_right, roles=[]):
        return super(AssetsModel, self).__init__()

class AssetList(QtWidgets.QListView):
    def __init__(self, parent=None):
        super(AssetList, self).__init__(parent)

class AMLoadOptions(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AMLoadOptions, self).__init__(parent)

        button_group = QtWidgets.QButtonGroup()
        link_button = QtWidgets.QPushButton('link')
        append_button = QtWidgets.QPushButton('append')

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(link_button)
        layout.addWidget(append_button)
        self.setLayout(layout)

class AMAssetInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AMAssetInfo, self).__init__(parent)

        self.asset_category = AMAssetCategory()

        self.object_model = SceneObjectsModel()
        self.object_list = ObjectList()
        self.object_list.setModel(self.object_model)
        self.asset_browser = imgviewer.ImageBrowser()
        self.asset_browser.image_list.clicked.connect(self.item_clicked)

        self.log_browser = logview.LogBrowser()
        logview.populate(self.log_browser.model)

        self.load_options = AMLoadOptions()

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.asset_category)
        left_layout.addWidget(self.asset_browser)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setSpacing(0)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.log_browser)
        right_layout.addWidget(self.load_options)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

#        layout.addWidget(self.asset_category)
#        layout.addWidget(self.asset_browser)
#        layout.addWidget(self.log_browser)
#        #layout.addWidget(self.object_list)
#        layout.addWidget(self.load_options)

        self.setLayout(layout)

    def item_clicked(self, event):
        print("selected item: ", event)


class AMMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AMMainWindow, self).__init__(parent)

        self.asset_info = AMAssetInfo()
        self.setCentralWidget(self.asset_info)

        self.setWindowTitle("Asset Management")

import sys

if not QtWidgets.qApp.instance():
    app = QtWidgets.QApplication(sys.argv)
asset_manager = AMMainWindow()
asset_manager.show()

objs = set(bpy.context.scene.objects)
def update_ui(scene):
    global objs
    curr_objs = set(scene.objects)
    deleted_objs = objs - curr_objs
    added_objs = curr_objs - objs

    model = asset_manager.asset_info.object_model
    for deleted in deleted_objs:
        model.remove_object(deleted)

    for added in added_objs:
        model.add_object(added)

    objs = curr_objs

while len(bpy.app.handlers.scene_update_post):
    bpy.app.handlers.scene_update_post.pop(0)

bpy.app.handlers.scene_update_post.append(update_ui)


'''
#
# launcher from blender
#
import sys
import importlib

location = 'C:/Users/vicken.mavlian/Documents/GitHub/asset-management'
if location not in sys.path:
    sys.path.append(location)
import am
importlib.reload(am)
'''
