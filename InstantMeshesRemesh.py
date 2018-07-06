
bl_info = {
    "name": "Instant Meshes Remesh",
    "author": "knekke",
    "category": "Object",
}

import bpy
import os
import subprocess
import tempfile
import shutil


class InstantMeshesRemeshPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    filepath = bpy.props.StringProperty(
            name="Instant Meshes Executable",
            subtype='FILE_PATH',
            )

    def draw(self, context):
        layout = self.layout
        layout.label(text="""Please specify the path to 'Instant Meshes.exe'
            Get it from https://github.com/wjakob/instant-meshes""")
        layout.prop(self, "filepath")


class InstantMeshesRemeshBatch(bpy.types.Operator):
    """Remesh selected objects with last used settings"""
    bl_idname = "object.instant_meshes_remesh_batch"
    bl_label = "Instant Meshes Remesh BATCH"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = bpy.context.selected_objects
        for other_obj in bpy.data.objects:
                    other_obj.select = False
        for i in s:
            i.select = True
            bpy.context.scene.objects.active = i
            bpy.ops.object.instant_meshes_remesh()
            for slot, mat in enumerate(i.data.materials):
                bpy.data.objects[i.name+'_remesh'].data.materials[slot] = mat.copy() 
                bpy.data.objects[i.name+'_remesh'].data.materials[slot].diffuse_color = (0.3,1,0.3)
            i.select = False
            bpy.context.scene.objects.active = None
        return {'FINISHED'}

class InstantMeshesRemesh(bpy.types.Operator):
    """Remesh by using the Instant Meshes program"""
    bl_idname = "object.instant_meshes_remesh"
    bl_label = "Instant Meshes Remesh"
    bl_options = {'REGISTER', 'UNDO'}

    exported = False
    deterministic = bpy.props.BoolProperty(name="Deterministic (slower)", description="Prefer (slower) deterministic algorithms", default=False)
    dominant = bpy.props.BoolProperty(name="Dominant", description="Generate a tri/quad dominant mesh instead of a pure tri/quad mesh", default=False)
    intrinsic = bpy.props.BoolProperty(name="Intrinsic", description="Intrinsic mode (extrinsic is the default)", default=False)
    boundaries = bpy.props.BoolProperty(name="Boundaries", description="Align to boundaries (only applies when the mesh is not closed)", default=False)
    crease = bpy.props.IntProperty(name="Crease Degree", description="Dihedral angle threshold for creases", default=0, min=0, max=100)
    verts = bpy.props.IntProperty(name="Vertex Count", description="Desired vertex count of the output mesh", default=2000, min=200, max=50000)
    smooth = bpy.props.IntProperty(name="Smooth iterations", description="Number of smoothing & ray tracing reprojection steps (default: 2)", default=2, min=0, max=10)
    openUI = bpy.props.BoolProperty(name="Open in InstantMeshes", description="Opens the selected object in Instant Meshes and imports the result when you are done.", default=False)
    
    loc = None
    rot = None
    scl = None
    meshname = None
 
    def execute(self, context):
        exe = context.user_preferences.addons[__name__].preferences.filepath
        orig = os.path.join(tempfile.gettempdir(),'original.obj')
        output = os.path.join(tempfile.gettempdir(),'out.obj')

        if not self.exported:
            try:
                os.remove(orig)
            except:
                pass
            self.meshname = bpy.context.active_object.name
            mesh = bpy.context.active_object
            self.loc = mesh.matrix_world.to_translation()
            self.rot = mesh.matrix_world.to_euler('XYZ')
            self.scl = mesh.matrix_world.to_scale()
            bpy.ops.object.location_clear()
            bpy.ops.object.rotation_clear()
            bpy.ops.object.scale_clear()
            bpy.ops.export_scene.obj(filepath=orig,
                                        check_existing=False, 
                                        axis_forward='Y', axis_up='Z',
                                        use_selection=True, 
                                        use_mesh_modifiers=True, 
                                        use_mesh_modifiers_render=False,
                                        use_edges=True, 
                                        use_smooth_groups=False, 
                                        use_smooth_groups_bitflags=False, 
                                        use_normals=True, 
                                        use_uvs=True, 
                                        use_materials=False)
            self.exported = True
            mesh.location = self.loc
            mesh.rotation_euler = self.rot
            mesh.scale = self.scl

        mesh = bpy.data.objects[self.meshname]
        mesh.hide = False
        options = ['-c', str(self.crease), 
                '-v', str(self.verts),
                '-S', str(self.smooth),
                '-o', output]
        if self.deterministic:
            options.append('-d')
        if self.dominant:
            options.append('-D')
        if self.intrinsic:
            options.append('-i')
        if self.boundaries:
            options.append('-b')
            
        cmd = [exe] + options + [orig]
        if self.openUI:
            os.chdir(os.path.dirname(orig))
            shutil.copy2(orig, output)
            subprocess.run([exe, output])
            self.openUI = False
        else:
            subprocess.run(cmd)
        
        bpy.ops.import_scene.obj(filepath=output, 
                                use_smooth_groups=False,
                                use_image_search=False)
        imported_mesh = bpy.context.selected_objects[0]
        imported_mesh.location = self.loc
        imported_mesh.rotation_euler = self.rot
        imported_mesh.scale = self.scl
        print(mesh, mesh.name)
        imported_mesh.name = mesh.name + '_remesh'
        for i in mesh.data.materials:
            print('setting mat: ' +i.name)
            imported_mesh.data.materials.append(i)
        for edge in imported_mesh.data.edges:
            edge.use_edge_sharp = False
        for other_obj in bpy.data.objects:
            other_obj.select = False
        imported_mesh.select = True
        bpy.ops.object.shade_flat()
        mesh.select = True
        bpy.context.scene.objects.active = mesh
        bpy.ops.object.data_transfer(use_reverse_transfer=False, 
                                        use_freeze=False, data_type='UV', use_create=True, vert_mapping='NEAREST', 
                                        edge_mapping='NEAREST', loop_mapping='NEAREST_POLYNOR', poly_mapping='NEAREST', 
                                        use_auto_transform=False, use_object_transform=True, use_max_distance=False, 
                                        max_distance=1.0, ray_radius=0.0, islands_precision=0.1, layers_select_src='ACTIVE',
                                        layers_select_dst='ACTIVE', mix_mode='REPLACE', mix_factor=1.0)
        mesh.select = False
        mesh.hide = True
        mesh.hide_render = True
        imported_mesh.select = False
        os.remove(output)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(InstantMeshesRemeshBatch.bl_idname)
    self.layout.operator(InstantMeshesRemesh.bl_idname)

def register():
    bpy.utils.register_class(InstantMeshesRemesh)
    bpy.utils.register_class(InstantMeshesRemeshBatch)
    bpy.utils.register_class(InstantMeshesRemeshPrefs)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    try:
        os.remove(os.path.join(tempfile.gettempdir(),'original.obj'))
        os.remove(os.path.join(tempfile.gettempdir(),'out.obj'))
    except:
        pass

def unregister():
    bpy.utils.unregister_class(InstantMeshesRemesh)
    bpy.utils.unregister_class(InstantMeshesRemeshBatch)
    bpy.utils.unregister_class(InstantMeshesRemeshPrefs)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()