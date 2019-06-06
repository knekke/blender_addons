# importOBJ_principledShader
A customized obj importer for Blender, that creates a Principled BSDF Material. We use it for importing from 3DCoat, but it should work for other applications as well.

A small example video:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/R0hI1Ki9xsI/0.jpg)](https://www.youtube.com/watch?v=R0hI1Ki9xsI)


# Match Transforms

##### What it does:

Adds some buttons to the Tools/Transform panel that allow you to match the selected objects (singular or plural) tansforms (all or location, rotation, scale) to the active object (last selected).

![][transforms]


# InstantMeshesRemesh

A simple addon that uses the commandline version of [Instant Meshes]  to integrate it into Blender. 

##### What it does:
  - Exports your object 
  - runs InstantMeshes with the specified settings / or opens the UI with your Mesh
  - imports the result and sets UVs and Materials
  - hides the original Object.  
  
**IMPORTANT:** when using the UI you have to save your mesh as **%TEMP%\out.obj** (or whatever your temp dir is in Linux/Mac)

##### Installation instructions:

1. Download the original Instant Meshes program (binaries or build yourself)
1. Download InstantMeshesRemesh.py from my github repo and put it into your addons folder
1. Activate it inside Blender and set the filepath to the Instant Meshes executable  
![][remesh_addon]  
1. Now you should have a Instant Meshes Remesh command in the object menu  
![][remesh_menu]


[transforms]: <https://raw.githubusercontent.com/knekke/blender_addons/master/readme_img/matchtranforms.png>
[remesh_py]: <https://raw.githubusercontent.com/knekke/blender_addons/master/InstantMeshesRemesh.py>
[remesh_addon]: <https://github.com/knekke/blender_addons/blob/master/readme_img/remesh_installation.png?raw=true>
[remesh_menu]: <https://github.com/knekke/blender_addons/blob/master/readme_img/remesh_menu.png?raw=true>
[Instant Meshes]: <https://github.com/wjakob/instant-meshes>
