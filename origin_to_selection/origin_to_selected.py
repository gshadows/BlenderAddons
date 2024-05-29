import bpy

bl_info = {
    "name": "Origin to Selection",
    "description": "Adds new menu item to quick move object origin to the current selection (vertices) mid-point",
    "author": "G-Shadow",
    "category": "Object",
    "location": "Shift + S > Origin to Selection",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "warning": "",
    "doc_url": "https://github.com/gshadows/BlenderAddons",
    "wiki_url": "https://github.com/gshadows/BlenderAddons", # Compatibility with pre-3.0 versions.
    "tracker_url": "https://github.com/gshadows/BlenderAddons/issues"
}

class OriginToSelection(bpy.types.Operator):
    """Set the object's origin to the selection"""
    bl_idname = "object.origin_to_selection"
    bl_label = "Origin to Selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' or context.mode == 'EDIT') and context.area.type == 'VIEW_3D'

    def execute(self, context):
        # Save state
        old_cursor = bpy.context.scene.cursor.location
        old_mode = bpy.context.object.mode

        # Origin to Selected
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Restore state
        bpy.context.scene.cursor.location = old_cursor
        bpy.ops.object.mode_set(mode=old_mode)

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OriginToSelection.bl_idname, text=OriginToSelection.bl_label, icon='CURSOR')

def register():
    bpy.utils.register_class(OriginToSelection)
    bpy.types.VIEW3D_MT_snap_pie.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OriginToSelection)
    bpy.types.VIEW3D_MT_snap_pie.remove(menu_func)

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
