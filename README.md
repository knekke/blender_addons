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

##### Installation instructions:
Download the original Instant Meshes program (binaries or build yourself)
Download InstantMeshesRemesh.py from my github repo and put it into your addons folder
Activate it inside Blender and set the filepath to the Instant Meshes executable
![][remesh_addon]
Now you should have a Instant Meshes Remesh command in the object menu
![][remesh_menu]


[transforms]: <https://raw.githubusercontent.com/knekke/blender_addons/master/readme_img/matchtranforms.png>
[remesh_py]: <https://raw.githubusercontent.com/knekke/blender_addons/master/InstantMeshesRemesh.py>
[remesh_addon]: <https://github.com/knekke/blender_addons/blob/master/readme_img/remesh_installation.png?raw=true>
[remesh_menu]: <https://github.com/knekke/blender_addons/blob/master/readme_img/remesh_menu.png?raw=true>
[Instant Meshes]: <https://github.com/wjakob/instant-meshes>
