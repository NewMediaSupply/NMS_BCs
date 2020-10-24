import bpy 
import importlib
import os
from bpy.types import WindowManager, PropertyGroup
from bpy.props import EnumProperty


bl_info = {
    "name": "NMS_BCs",
    "author": "New Media Supply",
    "version": (1, 0, 0),
    "blender": (2, 90, 0),
    "location": "View3D > N-Panel",
    "description": "Custom shapes for Boxcutter",
    "warning": "Work in Progress",
    "category": "3D View"
}

# UI
class NMSBC_PT_customshapes(bpy.types.Panel):
    bl_label = "Custom Shapes lib"
    bl_idname = "NMSBC_PT_customshapes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NMS_BCs'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        row = layout.row()
        
        # This tells Blender to draw the my_previews window manager object
        # (Which is our preview)
        row.template_icon_view(wm, "nmsbcs_preview_thumbs", scale=6.0, scale_popup=6.0)
        
        # Just a way to access which one is selected
        # row = layout.row()
        # row.label(text="You selected: " + bpy.context.scene.my_thumbnails)

classes =( 
    NMSBC_PT_customshapes,
)

preview_collection = {}

def get_preview_thumbs_enum(self, context):
    enum_items = []

    if context is None:
        return enum_items

    pcoll = preview_collection['shapes']
    target_dir = pcoll.my_previews_dir

    image_paths = [img for img in os.listdir(target_dir) if img.endswith('.png')]
    for i, name in enumerate(image_paths):
        filepath = os.path.join(target_dir, name)
        icon = pcoll.get(name)
        if not icon:
            thumb = pcoll.load(name, filepath, 'IMAGE')
        else:
            thumb = pcoll[name]
        enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.my_previews = enum_items
    return pcoll.my_previews
    
def load_shape(self, context):
    """ Run preset load and replacement """
    shape_preset = os.path.join(preview_collection['shapes'].my_previews_dir, self.nmsbcs_preview_thumbs.replace('.png', '.blend'))
    # print(shape_preset)
    # print(os.path.dirname(__file__))
    # print(bpy.data.window_managers["WinMan"].nmsbcs_preview_thumbs)
    path = shape_preset + ("\\Object\\")
    object_name = bpy.data.window_managers["WinMan"].nmsbcs_preview_thumbs
    object_namestripped = object_name.replace(".png", "")
    bpy.ops.wm.append(filename=object_namestripped, directory=path)
    context.scene.bc.shape = bpy.data.objects[object_namestripped]
    # print(path)
    # print(object_name.replace(".png", ""))


    



def register():
    from bpy.types import Scene
    from bpy.props import StringProperty, EnumProperty
    from bpy.utils import register_class
    
    for cls in classes:
        register_class(cls)

    import bpy.utils.previews
    # Presets preview collection setup
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = os.path.join(
        os.path.dirname(__file__), 'NMS', 'shapes'
    )
    pcoll.my_previews = ()

    preview_collection["shapes"] = pcoll

    WindowManager.nmsbcs_preview_thumbs = EnumProperty(
        items=get_preview_thumbs_enum,
        update=load_shape,
    )
    
def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    for pcoll in preview_collection.values():
        bpy.utils.previews.remove(pcoll)
    preview_collection.clear()
    


if __name__ == "__main__":
    register()
