import bpy

class RotationMemory:
    original_rotation = {}

class OBJECT_OT_CopyRotation(bpy.types.Operator):
    bl_idname = "object.copy_rotation"
    bl_label = "Copy Rotation"
    
    def execute(self, context):
        old_part = context.scene.old_part
        new_part = context.scene.new_part
        
        if old_part and new_part:
            RotationMemory.original_rotation[new_part.name] = new_part.rotation_euler.copy()
            
            new_part.rotation_euler = old_part.rotation_euler
            self.report({'INFO'}, f"Rotation copied from {old_part.name} to {new_part.name}")
        else:
            self.report({'ERROR'}, "Please select both Old Part and New Part")
        
        return {'FINISHED'}

class OBJECT_OT_UndoRotation(bpy.types.Operator):
    bl_idname = "object.undo_rotation"
    bl_label = "Undo Rotation"
    
    def execute(self, context):
        new_part = context.scene.new_part
        
        if new_part and new_part.name in RotationMemory.original_rotation:
            new_part.rotation_euler = RotationMemory.original_rotation[new_part.name]
            self.report({'INFO'}, f"Rotation restored for {new_part.name}")
        else:
            self.report({'ERROR'}, "No rotation to undo or New Part not selected")
        
        return {'FINISHED'}

class OBJECT_PT_CopyRotationPanel(bpy.types.Panel):
    bl_label = "Copy Rotation Tool"
    bl_idname = "OBJECT_PT_copy_rotation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        
        layout.prop(context.scene, "old_part", text="Old Part")
        layout.prop(context.scene, "new_part", text="New Part")
        
        layout.operator("object.copy_rotation", text="Swap Rotation")
        
        layout.operator("object.undo_rotation", text="Undo Rotation")

def register_properties():
    bpy.types.Scene.old_part = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.new_part = bpy.props.PointerProperty(type=bpy.types.Object)

def unregister_properties():
    del bpy.types.Scene.old_part
    del bpy.types.Scene.new_part

def register():
    bpy.utils.register_class(OBJECT_OT_CopyRotation)
    bpy.utils.register_class(OBJECT_OT_UndoRotation)
    bpy.utils.register_class(OBJECT_PT_CopyRotationPanel)
    register_properties()

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CopyRotation)
    bpy.utils.unregister_class(OBJECT_OT_UndoRotation)
    bpy.utils.unregister_class(OBJECT_PT_CopyRotationPanel)
    unregister_properties()

if __name__ == "__main__":
    register()
