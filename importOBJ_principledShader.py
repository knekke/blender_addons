
import bpy
import os

bl_info = {
    "name": "Obj Import with principled Shader",
    "author": "knekke",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "File > Import-Export",
    "description": "Obj Import with principled Shader",
    "category": "Import-Export"}

def create_materials(matname, textures, objname):
    # Test if material exists
    # If it does not exist, create it:
    mat = (bpy.data.materials.get(matname) or 
           bpy.data.materials.new(matname))

    # Enable 'Use nodes':
    mat.use_nodes = True
    tree = mat.node_tree
    nodes = tree.nodes

    for node in nodes:

        if not node.name == 'Material Output':
            nodes.remove(node)
        else:
            outnode = node
    # Add a diffuse shader and set its location:   
    s_princ = nodes.new('ShaderNodeBsdfPrincipled')
    s_princ.location = (0,300)
    tree.links.new(s_princ.outputs['BSDF'], outnode.inputs['Surface'])
    
    if 'BaseColor' in textures:
        texC = bpy.data.images.load(textures['BaseColor'], check_existing=True)
        texCol = nodes.new("ShaderNodeTexImage")
        texCol.location = (-300,400)
        texCol.name = 'BaseColor' 
        texCol.label = 'BaseColor' 
        texCol.image = texC
        tree.links.new(texCol.outputs['Color'], s_princ.inputs['Base Color'])

    if 'Metalness' in textures:
        texS = bpy.data.images.load(textures['Metalness'], check_existing=True)
        texMet = nodes.new("ShaderNodeTexImage")
        texMet.color_space = 'NONE'
        texMet.location = (-500,150)
        texMet.name = 'Metalness' 
        texMet.label = 'Metalness' 
        texMet.image = texS
        tree.links.new(texMet.outputs['Color'], s_princ.inputs['Metallic'])

    if 'Roughness' in textures:
        texG = bpy.data.images.load(textures['Roughness'], check_existing=True)
        texGloss = nodes.new("ShaderNodeTexImage")
        texGloss.color_space = 'NONE'
        texGloss.location = (-300,0)
        texGloss.name = 'Roughness' 
        texGloss.label = 'Roughness' 
        texGloss.image = texG
        tree.links.new(texGloss.outputs['Color'], s_princ.inputs['Roughness'])
        
    if 'Normal' in textures:
        nmapnode = nodes.new("ShaderNodeNormalMap")
        nmapnode.location = (-300,-300)
        nmapnode.inputs[0].default_value = 1
        texN = bpy.data.images.load(textures['Normal'], check_existing=True)
        texNmap = nodes.new("ShaderNodeTexImage")
        texNmap.color_space = 'NONE'
        texN.use_alpha = False
        texNmap.location = (-500,-300)
        texNmap.name = 'Normal' 
        texNmap.label = 'Normal' 
        texNmap.image = texN
        tree.links.new(nmapnode.outputs['Normal'], s_princ.inputs['Normal'])
        tree.links.new(texNmap.outputs['Color'], nmapnode.inputs['Color'])

    if 'EmissiveColor' in textures:
        texE = bpy.data.images.load(textures['EmissiveColor'], check_existing=True)
        texEmit = nodes.new("ShaderNodeTexImage")
        texEmit.location = (-600,0)
        texEmit.name = 'EmissiveColor' 
        texEmit.label = 'EmissiveColor' 
        texEmit.image = texE
        #tree.links.new(texGloss.outputs['Color'], s_princ.inputs['Emission'])
    try:
        #print(matname)
        ob = bpy.data.objects[matname]
        ob.data.materials[0] = mat
    except:
        pass

def readObj(objfile):
    #objfile = 'H:/01_Projects/Thomas_Projects/3dcoat/Flink_Dose/Export02/Dose02.obj'
    dirname = os.path.dirname(objfile)
    with open(objfile,'r') as f:
        objlines = f.read().splitlines()

    objs = {}
    objname = ''
    for line in objlines:
        if line:
            split_line = line.strip().split(' ', 1)
            if len(split_line) < 2:
                continue

            prefix, value = split_line[0], split_line[1]
            if prefix == 'g':
                objname = value
                objs[objname] = {'name' : value}
            # For files without an 'o' statement
            elif prefix == 'usemtl':
                objs[objname]['matname'] = value
    
    with open(objfile.replace('.obj', '.mtl'), 'r') as f:
        mtllines = f.read().splitlines()

    materials = {}
    matname = ''
    for line in mtllines:
        if line:
            split_line = line.strip().split(' ', 1)
            if len(split_line) < 2:
                continue

            prefix, data = split_line[0], split_line[1]
            if 'newmtl' in prefix:
                matname = data
                materials[matname] = {}
            elif prefix == 'map_Kd':
                materials[matname]['BaseColor'] = dirname + '\\' + data
            elif prefix == 'map_Ks':
                materials[matname]['Roughness'] = dirname + '\\' + data
            elif prefix == 'bump':
                materials[matname]['Displacement'] = dirname + '\\' + split_line[-1].split('\\')[-1]
                try:
                    materials[matname]['displ_value'] = split_line[-1].split(' ')[-2]
                except:
                    materials[matname]['displ_value'] = 0
            elif prefix == 'map_bump':
                materials[matname]['Normal'] = dirname + '\\' + data
    print(dirname)
    for matname in materials.keys():
        for i in os.listdir(dirname):
            for n in [matname, os.path.basename(objfile).split('.')[0]]:
                print(n+'_metalness  --->  ' + i.lower())
                if (n+'_ao').lower() in i.lower():
                    materials[matname]['ao'] = dirname + '\\' + i
                if (n+'_emissivecolor').lower() in i.lower():
                    materials[matname]['EmissiveColor'] = dirname + '\\' + i
                if (n+'_metalness').lower() in i.lower():
                    materials[matname]['Metalness'] = dirname + '\\' + i
                if (n+'_opacity').lower() in i.lower():
                    materials[matname]['Opacity'] = dirname + '\\' + i
    return objs, materials

 
def load_obj(obj, objects, materials, objname):

        
    for obj in objects.keys():
        matname = objects[obj]['matname']
        create_materials(matname, materials[matname], objname)

class ObjImportPrinc(bpy.types.Operator):
    """Test exporter which just writes hello world"""
    bl_idname = "import_scene.obj_princ"
    bl_label = "Selecet OBJ file"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")


    def execute(self, context):
        location = os.path.dirname(self.filepath)
        objfiles = {}
        for file in os.listdir(location):
            ext = file.split('.')[-1]            
            if ext == 'obj':
                name = file.split('.')[0]
                objfiles[name] = os.path.join(location, file)

        for objname in objfiles.keys():
            obj = objfiles[objname]
            bpy.ops.import_scene.obj(filepath=obj, 
                                axis_forward='Y', axis_up='Z', filter_glob="*.obj;*.mtl", 
                                use_edges=True, use_smooth_groups=True, use_split_objects=True, 
                                use_split_groups=True, use_groups_as_vgroups=False, use_image_search=False, 
                                split_mode='ON', global_clamp_size=0.0)
            objects, materials = readObj(obj) 
            load_obj(obj, objects, materials, objname)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'} 

def menu_func_import(self, context):
    self.layout.operator(ObjImportPrinc.bl_idname, text="Obj with principled shader")

def register():
    bpy.utils.register_class(ObjImportPrinc)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
    
def unregister():
    bpy.utils.unregister_class(ObjImportPrinc)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__": 
    register()