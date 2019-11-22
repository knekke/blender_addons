 
bl_info = {
    "name": "Match Transforms",
    "author": "knekke",
    "version": (1, 0),
    "blender": (2, 81, 0),
    "location": "View3D > UI > Item > Match Tools",
    "description": "Match LRS",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }

import bpy


class MatchTransformsOperator(bpy.types.Operator):
    "Match Transforms - selected to active Objects"
    bl_idname = "object.match_transform"
    bl_label = "Match Transform"
    bl_options = {'REGISTER', 'UNDO'}
    location : bpy.props.BoolProperty()
    rotation : bpy.props.BoolProperty()
    scale : bpy.props.BoolProperty()

    def execute(self, context):
        target = bpy.context.object
        loc = target.matrix_world.to_translation()
        rot = target.matrix_world.to_euler('XYZ')
        scl = target.matrix_world.to_scale()
        for i in bpy.context.selected_objects:
            if not i == target:
                if self.location:
                    i.location = loc
                if self.rotation:
                    i.rotation_euler = rot
                if self.scale:
                    i.scale = scl
        #target.select_set(state=False)
        #bpy.context.view_layer.objects.active = target #bpy.context.selected_objects[-1]
        return {'FINISHED'}

# -----------------

class MatchToolPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_idname = "MATCH001_PT_objs"
    bl_label = "Match Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        box = layout.box()
        row = box.row()
        row.label(text="Match Object Transforms:", icon = "LOOP_FORWARDS")
        row = box.row()

        matchall = row.operator("object.match_transform", text="ALL", text_ctxt="ALL")
        matchall.location = True
        matchall.rotation = True
        matchall.scale = True

        sub = box.row()
        sub.scale_x = 1.0
        loc = sub.operator("object.match_transform", text="LOC", text_ctxt="LOC")
        loc.location = True
        loc.rotation = False
        loc.scale = False
       
        rot = sub.operator("object.match_transform", text="ROT", text_ctxt="ROT")
        rot.location = False
        rot.rotation = True
        rot.scale = False
       
        scl = sub.operator("object.match_transform", text="SCL", text_ctxt="SCL")
        scl.location = False
        scl.rotation = False
        scl.scale = True
       
#------------------

def register():
    bpy.utils.register_class(MatchToolPanel)
    bpy.utils.register_class(MatchTransformsOperator)



def unregister():
    bpy.utils.unregister_class(MatchToolPanel)
    bpy.utils.unregister_class(MatchTransformsOperator)


if __name__ == "__main__":
    register()
