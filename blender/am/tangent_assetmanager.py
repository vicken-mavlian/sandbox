bl_info = {
    "name": "Asset Management",
    "description": "Interface for artist Asset Management",
    "author": "Vicken Mavlian",
    "version": (1,0),
    "blender": (2, 7, 8),
    "category": "File",
    "location": "File > Open Asset Management Interface",
    }

import bpy, os, sys, subprocess

import bpy
class ExMenu(bpy.types.Menu):
    bl_label = "Studio"

    def draw(self, context):
        layout = self.layout
        layout.operator(AssetManagerOpertator.bl_idname, text="open Asset Manager")


class AssetManagerOpertator(bpy.types.Operator):
    bl_idname = "ops.asset_manager_interface"
    bl_label = "open Asset Manager UI"

    def execute(self, context):
        import sys
        import importlib

        location = 'C:/Users/vicken.mavlian/Documents/GitHub/asset-management'
        if location not in sys.path:
            sys.path.append(location)
        import am
        importlib.reload(am)
        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_editor_menus.append("ExMenu")

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file.remove( "ExMenu" )

if __name__ == "__main__":  # only for live edit.
    bpy.utils.register_module(__name__)
