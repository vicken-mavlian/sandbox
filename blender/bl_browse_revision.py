# <pep8 compliant>
import bpy
from bpy.types import Header, Panel, Menu

from collections import namedtuple
import os

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

Asset = namedtuple('Asset', 'name thumbnail')
assets = []
for a in ['cone', 'cube', 'cylinder', 'icosphere', 'sphere', 'suzanne', 'torus']:
    asset = Asset(name=a, thumbnail=a+'.png')
    assets.append(asset)


Revision = namedtuple('Revision', 'version date user comment publish')
revisions = {}
revisions['cone'] = [
    Revision(version='1', date='2016-10-10', user='vicken.mavlian', comment='initial', publish='False'),
    Revision(version='2', date='2016-10-10', user='vicken.mavlian', comment='made better', publish='False'),
    Revision(version='3', date='2016-10-10', user='vicken.mavlian', comment='approved', publish='True'),
    Revision(version='4', date='2016-10-10', user='vicken.mavlian', comment='small fix', publish='False')
]


for a in ['cone', 'cube', 'cylinder', 'icosphere', 'sphere', 'suzanne', 'torus']:
    asset = Asset(name=a, thumbnail=a+'.png')
    assets.append(asset)


root_path = os.path.join('C:/', 'Users', 'vicken.mavlian', 'Documents', 'GitHub', 'asset-management', 'resources')

preview_collections = {}


category = []
for i, c in enumerate(['set', 'character', 'prop', 'material']):
    category.append((c.upper(), c.capitalize(), '', i))

dpts = []
for i, d in enumerate(['model', 'surface', 'hair', 'rig']):
    dpts.append((d.upper(), d.capitalize(), '', i))


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


def enum_assets(self, context):
    items = []

    if context is None:
        return items

    wm = context.window_manager

    pcoll = preview_collections['assets']
    img_paths = []
    files = os.listdir(root_path)
    for i, asset in enumerate(assets):

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

def asset_index_changed(self, context):
    index = self.am_index
    asset = self.am_prop_group[index]

#   XXX In case if we were interacting with a FILE_BROWSE space
#    path = os.path.join('t:\\', 'Projects', '0051_7723', 'rnd')
#    bpy.ops.file.select_bookmark(dir=path)


def revision_index_changed(self, context):
    index = self.am_rev_index

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
    # data = Scene
    # item = AssetManagementPropGroup
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(item.asset_name)

        #split.prop(item, "obj_name", text="", emboss=False, translate=False, icon='OBJECT_DATA')
        #split.prop(item, "ps_name", text="", emboss=False, translate=False, icon='PARTICLE_DATA')
        #split.prop(item, "use_cache", emboss=True, translate=False)


class AssetManagementRevisionItems(bpy.types.UIList):
    # data = Scene
    # item = AssetManagementPropGroup

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

        #split.prop(item, "obj_name", text="", emboss=False, translate=False, icon='OBJECT_DATA')
        #split.prop(item, "ps_name", text="", emboss=False, translate=False, icon='PARTICLE_DATA')
        #split.prop(item, "use_cache", emboss=True, translate=False)


class ASSETMANAGEMENT_asset_browser(Panel):
    bl_space_type = 'VIEW_3D' #FILE_BROWSER
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks" # "Asset Browsing"
    bl_label = "Asset Browser"

    def draw(self, context):
        #print(dir(bpy.context.space_data))
        layout = self.layout
        space = context.space_data
        scene = context.scene

        wm = context.window_manager

        row = layout.row(align=True)
        row.prop(scene, 'category')

        row = layout.row(align=True)
        pcoll = preview_collections['revision']
        #row.label(icon_value=pcoll['wip'].icon_id)
        row.template_icon_view(wm, "asset_previews")
        row.template_list("AssetManagementAssetItems", "", scene, "am_prop_group",
                          scene, "am_index", item_dyntip_propname="path", rows=1, maxrows=10)

        row = layout.row()
        row.prop(scene, "depts", expand=True)

        row = layout.row()
        row.template_list("AssetManagementRevisionItems", "", scene, "am_rev_prop",
                          scene, "am_rev_index", item_dyntip_propname="path", rows=1, maxrows=10)

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
    pcoll.asset_previews.append(('publish', 'publish', "", thumb.icon_id, i))

    thumbnail_path = os.path.join(root_path, 'rev_wip.png')
    thumb = pcoll.load('wip', thumbnail_path, 'IMAGE')
    pcoll.asset_previews.append(('wip', 'wip', "", thumb.icon_id, i))

    preview_collections['revision'] = pcoll

    bpy.types.WindowManager.asset_previews = bpy.props.EnumProperty(items=enum_assets)



    bpy.types.Scene.am_prop_group = bpy.props.CollectionProperty(type=AssetManagementAssetProp)
    bpy.types.Scene.am_index = bpy.props.IntProperty(update=asset_index_changed)


    bpy.types.Scene.am_rev_prop = bpy.props.CollectionProperty(type=AssetManagementRevisionProp)
    bpy.types.Scene.am_rev_index = bpy.props.IntProperty(update=revision_index_changed)


    bpy.types.Scene.category = bpy.props.EnumProperty(items=category,
                                                    name="Category",
                                                    description="Category selection")

    bpy.types.Scene.depts = bpy.props.EnumProperty(items=dpts,
                                                    name="Department",
                                                    description="Department selection")

    while len(bpy.context.scene.am_prop_group):
        bpy.context.scene.am_prop_group.remove(0)

    for a in assets:
        item = bpy.context.scene.am_prop_group.add()
        item.asset_name = a.name
        item.id = len(bpy.types.Scene.am_prop_group)


    while len(bpy.context.scene.am_rev_prop):
        bpy.context.scene.am_rev_prop.remove(0)

    for rev in revisions['cone']:
        item = bpy.context.scene.am_rev_prop.add()
        item.version = rev.version
        item.date = rev.date
        item.user = rev.user
        item.comment = rev.comment
        item.publish = rev.publish
        item.id = len(bpy.types.Scene.am_prop_group)



if __name__ == "__main__":  # only for live edit.
    register()
