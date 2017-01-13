import bpy

class MyList(bpy.types.IDPropertyGroup):
        pass

bpy.types.Scene.CollectionProperty(
        attr= 'my_list',
        type=  MyList,
        name= "My List",
        description= ""
)
bpy.types.Scene.IntProperty(
        attr= 'my_list_index',
        name= "My List Index",
        default= -1,
        min= -1,
        max= 100
)

class MyListItem(bpy.types.IDPropertyGroup):
        pass

MyList.PointerProperty(
        attr= 'my_item',
        type=  MyListItem,
        name= "MyListItem",
        description= ""
)

MyListItem.BoolProperty(
        attr= 'enable',
        name= "Enable",
        description= "",
        default= True
)

class MY_LIST_OT_add(bpy.types.Operator):
        bl_idname      = 'my_list.add'
        bl_label       = "Add list item"
        bl_description = "Add list item"

        def invoke(self, context, event):
                sce= context.scene

                my_list= sce.my_list

                my_list.add()
                my_list[-1].name= "ItemName"

                return{'FINISHED'}


class MY_LIST_OT_del(bpy.types.Operator):
        bl_idname      = 'my_list.remove'
        bl_label       = "Remove list item"
        bl_description = "Remove list item"

        def invoke(self, context, event):
                sce= context.scene

                my_list= sce.my_list

                if sce.my_list_index >= 0:
                   my_list.remove(sce.my_list_index)
                   sce.my_list_index-= 1

                return{'FINISHED'}


'''
 GUI
'''
class MyButtonsPanel():
        bl_space_type  = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context     = 'render'

class MyPanel(MyButtonsPanel, bpy.types.Panel):
        bl_label = "My Panel"

        def draw(self, context):
                layout= self.layout

                sce= context.scene

                split= layout.split()
                row= split.row()
                row.template_list(sce, 'my_list', sce, 'my_list_index', rows= 3)
                col= row.column(align=True)
                col.operator('my_list.add', text="", icon="ZOOMIN")
                col.operator('my_list.remove', text="", icon="ZOOMOUT")

                if sce.my_list_index >= 0 and len(sce.my_list) > 0:
                        list_item= sce.my_list[sce.my_list_index]

                        layout.separator()

                        layout.prop(list_item.my_item, 'enable')
