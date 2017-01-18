# <pep8 compliant>
import bpy
from bpy.types import Header, Panel, Menu

from collections import namedtuple
import sys, os, importlib

module_path = os.path.join('c:/', 'Users', 'vicken.mavlian', 'Documents', 'GitHub', 'asset-management')
if module_path not in sys.path:
    sys.path.append(module_path)
import data
importlib.reload(data)
data.regenerate()

bl_info = {
    "name": "Tangent Asset Browser",
    "author": "Vicken Mavlian",
    "version": (1, 0),
    "blender": (2, 77, 0),
    "location": "FILE BROWSER > Tools",
    "description": "Asset Browsing",
    "warning": "",
    "wiki_url": "",
    "category": ""}


root_path = os.path.join('C:/', 'Users', 'vicken.mavlian', 'Documents', 'GitHub', 'asset-management', 'resources')

preview_collections = {}

def clear_list(uilist):
    while len(uilist):
        uilist.remove(0)

def update_asset_list(category):
    clear_list(bpy.context.scene.am_prop_group)

    for asset in data.assets:
        if asset.category == category:
            item = bpy.context.scene.am_prop_group.add()
            item.asset_name = asset.name
            item.id = len(bpy.context.scene.am_prop_group)

def update_revision_list(asset, department):
    clear_list(bpy.context.scene.am_rev_prop)

    for asset_revision in data.asset_revisions:
        correct_asset = (asset_revision.asset.name == asset)
        correct_department = (asset_revision.department == department)
        if correct_asset and correct_department:
            for rev in asset_revision.revisions:
                item = bpy.context.scene.am_rev_prop.add()
                item.version = rev.version
                item.date = rev.date
                item.user = rev.user
                item.comment = rev.comment
                item.publish = rev.publish
                item.id = len(bpy.types.Scene.am_prop_group)
            break

#def update_thumbnails(asset, department):
def update_thumbnails():
    pass

def enum_assets(self, context):
    items = []

    if context is None:
        return items

    wm = context.window_manager

    pcoll = preview_collections['assets']
    img_paths = []
    files = os.listdir(root_path)
    for i, asset in enumerate(data.assets):

        thumbnail_path = os.path.join(root_path, asset.thumbnail)
        if not os.path.isfile(thumbnail_path):
            continue

        if thumbnail_path in pcoll.keys():
            thumb = pcoll.get(thumbnail_path)
        else:
            thumb = pcoll.load(thumbnail_path, thumbnail_path, 'IMAGE')
        items.append((asset.name, asset.name, "", thumb.icon_id, i))

    pcoll.asset_previews = items
    return pcoll.asset_previews


def category_changed(self, context):
    scene = context.scene

    update_asset_list(scene.category)

    self.am_index = -1
    self.am_rev_index = -1

    clear_list(bpy.context.scene.am_rev_prop)


def department_changed(self, context):
    scene = context.scene

    asset_index = self.am_index
    asset = self.am_prop_group[asset_index].asset_name

    department = context.scene.department

    update_revision_list(asset, department)

    self.am_rev_index = -1

def asset_index_changed(self, context):
    scene = context.scene
    index = self.am_index
    asset = self.am_prop_group[index].asset_name
    department = scene.department
    update_revision_list(asset, department)

    self.am_rev_index = -1

def revision_index_changed(self, context):
    index = self.am_rev_index

    update_thumbnails()

class AssetManagementAppend(bpy.types.Operator):
    bl_idname = "asset_management.append"
    bl_label = "append asset"
    bl_description = "append selected asset into the current scene"

    def execute(self, context):
        print('append')
        return {'FINISHED'}


class AssetManagementLink(bpy.types.Operator):
    bl_idname = "asset_management.link"
    bl_label = "link asset"
    bl_description = "link selected asset into the current scene"

    def execute(self, context):
        print('link')
        return {'FINISHED'}





class AssetManagementAssetProp(bpy.types.PropertyGroup):
    asset_name = bpy.props.StringProperty(name="asset_name")
    id = bpy.props.IntProperty()

class AssetManagementRevisionProp(bpy.types.PropertyGroup):
    version = bpy.props.StringProperty(name="version")
    date = bpy.props.StringProperty(name="date")
    user = bpy.props.StringProperty(name="user")
    comment = bpy.props.StringProperty(name="comment")
    publish = bpy.props.StringProperty(name="publish")
    id = bpy.props.IntProperty()


class AssetManagementAssetItems(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(item.asset_name)


class AssetManagementRevisionItems(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pcoll = preview_collections['revision']
        if item.publish == 'True':
            icon = pcoll['publish']
        else:
            icon = pcoll['wip']

        row = layout.row(align=True)
        row.label(item.version, icon_value=icon.icon_id)
        row.label(item.date)
        row.label(item.user)
        row.label(item.comment)

class ASSETMANAGEMENT_asset_browser(Panel):
    bl_space_type = 'VIEW_3D' #FILE_BROWSER
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks" # "Asset Browsing"
    bl_label = "Asset Browser"

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        scene = context.scene

        wm = context.window_manager

        row = layout.row(align=True)
        row.prop(scene, 'category')

        row = layout.row(align=True)
        pcoll = preview_collections['revision']
        row.template_list("AssetManagementAssetItems", "", scene, "am_prop_group",
                          scene, "am_index", item_dyntip_propname="path", rows=1, maxrows=10)

        row = layout.row()
        row.prop(scene, "department", expand=True)

        column = layout.column(align=True)

        column.template_icon_view(wm, "asset_previews")
        column.template_list("AssetManagementRevisionItems", "", scene, "am_rev_prop",
                          scene, "am_rev_index", item_dyntip_propname="path", rows=1, maxrows=10)

        row = layout.column()

        row.prop(scene, 'am_comments')

        row = layout.row(align=True)
        row.operator(AssetManagementAppend.bl_idname, "append")
        row.operator(AssetManagementLink.bl_idname, "link")


def register():
    bpy.utils.register_module(__name__)


    pcoll = bpy.utils.previews.new()
    pcoll.asset_previews = ()
    preview_collections['assets'] = pcoll


    pcoll = bpy.utils.previews.new()
    pcoll.asset_previews = []

    thumbnail_path = os.path.join(root_path, 'rev_publish.png')
    thumb = pcoll.load('publish', thumbnail_path, 'IMAGE')
    pcoll.asset_previews.append(('publish', 'publish', "", thumb.icon_id, 0))

    thumbnail_path = os.path.join(root_path, 'rev_wip.png')
    thumb = pcoll.load('wip', thumbnail_path, 'IMAGE')
    pcoll.asset_previews.append(('wip', 'wip', "", thumb.icon_id, 1))

    preview_collections['revision'] = pcoll

    bpy.types.WindowManager.asset_previews = bpy.props.EnumProperty(items=enum_assets)
    bpy.types.Scene.am_comments = bpy.props.StringProperty(name="comments")

    bpy.types.Scene.am_prop_group = bpy.props.CollectionProperty(type=AssetManagementAssetProp)
    bpy.types.Scene.am_index = bpy.props.IntProperty(update=asset_index_changed)


    bpy.types.Scene.am_rev_prop = bpy.props.CollectionProperty(type=AssetManagementRevisionProp)
    bpy.types.Scene.am_rev_index = bpy.props.IntProperty(update=revision_index_changed)

    bpy.types.Scene.category = bpy.props.EnumProperty(items=((c, c.capitalize(), '', i) for i,c in enumerate(data.categories)),
                                                    name="Category",
                                                    description="Category selection",
                                                    update=category_changed)

    bpy.types.Scene.department = bpy.props.EnumProperty(items=((d, d.capitalize(), '', i) for i,d in enumerate(data.departments)),
                                                    name="Department",
                                                    description="Department selection",
                                                    update=department_changed)


    bpy.context.scene.category = data.categories[0]
    bpy.context.scene.department = data.departments[0]

    clear_list(bpy.context.scene.am_prop_group)
    clear_list(bpy.context.scene.am_rev_prop)

def unregister():
    pass



if __name__ == "__main__":  # only for live edit.
    register()
