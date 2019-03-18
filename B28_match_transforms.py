bl_info = {
    "name": "Match Transforms",
    "author": "knekke",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Tools/Transform Panel",
    "description": "Matches the transforms of selected objects to the active object",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }


import bpy


class MatchTransformsOperator(bpy.types.Operator):
    "Match Transforms - selected to active Objects"
    bl_idname = "object.match_transform"
    bl_label = "Match Transform"
    location = bpy.props.BoolProperty()
    rotation = bpy.props.BoolProperty()
    scale = bpy.props.BoolProperty()

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


def add_button(self, context):
    layout = self.layout
    col = layout.column()
    col.label(text="Match selected to active")

    row = col.row(align=True)
    row.alignment = 'EXPAND'
    row2 = col.row(align=True)
    row2.alignment = 'EXPAND'

    butt = layout.operator("object.match_transform", text="All", text_ctxt="All")
    butt.location = True
    butt.rotation = True
    butt.scale = True

    buttl = layout.operator("object.match_transform", text="Loc")
    buttl.location = True
    buttl.rotation = False
    buttl.scale = False

    buttr = layout.operator("object.match_transform", text="Rot")
    buttr.location = False
    buttr.rotation = True
    buttr.scale = False

    butts = layout.operator("object.match_transform", text="Scl")
    butts.location = False
    butts.rotation = False
    butts.scale = True


def register():
    bpy.utils.register_class(MatchTransformsOperator)
    bpy.types.VIEW3D_PT_tools_active.append(add_button)


def unregister():
    bpy.utils.unregister_class(MatchTransformsOperator)
    bpy.types.VIEW3D_PT_tools_active.remove(add_button)


if __name__ == "__main__":
    register()
