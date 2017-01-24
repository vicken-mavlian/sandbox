class Dummy(object):
    pass

try:
    import bpy
except ImportError:
    bpy = Dummy()

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


