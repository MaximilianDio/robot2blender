# run the export_robot.py (easier than including dependencies for python)

import os
import bpy
from math import sin, cos, radians
from mathutils import Vector

robots = [["path_01/Robot_0.obj", "path_01/Robot_1.obj"]]
out_name = f"renders/robot"

phi = 135
theta = 60  # polar angle from z-axis, adjust for different views
view_offset_x = 0.2  # adjust to center the robot in view if needed
view_offset_y = 0.0
view_offset_z = 0.5
ortho_scale = 1.2  # adjust for zoom level

# compute camera position in spherical coordinates
r = 2.0
view_x = r * sin(radians(theta)) * cos(radians(phi - 90))
view_y = r * sin(radians(theta)) * sin(radians(phi - 90))
view_z = r * cos(radians(theta)) 

view_offset = Vector((view_offset_x, view_offset_y, view_offset_z))  # adjust to center the robot in view if needed
view_location = Vector((view_x, view_y, view_z)) + view_offset
# set camera position and orientation
camera = bpy.data.objects['Camera']
camera.location = view_location
camera.rotation_euler = (radians(theta), 0, radians(phi))  # point towards the origin
camera.data.type = 'ORTHO'
camera.data.ortho_scale = ortho_scale  # adjust for zoom level

working_dir = os.path.dirname(os.path.dirname(__file__))

for i, obj_names in enumerate(robots):
    
    obj_list = []
    for obj_name in obj_names:
        file_path = os.path.join(working_dir, 'out', 'robots', obj_name)
        print(file_path)

        bpy.ops.import_scene.obj(filepath=file_path)
        # set pose of the imported object
        context = bpy.context
        scene = context.scene
        obj = scene.objects[-1]
        obj_list.append(obj)

        obj.rotation_euler = (0, 0, 0)

        # Apply smooth shading to all faces
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth()

        # Enable auto smooth at 10 degrees
        obj.data.use_auto_smooth = True
        obj.data.auto_smooth_angle = radians(5)

        # Remove all existing materials
        obj.data.materials.clear()

        # Apply singleLineHatch material
        mat_name = "singleLineHatch"
        mat = bpy.data.materials.get(mat_name)

        if mat is None:
            mat = bpy.data.materials.new(name=mat_name)

        obj.data.materials.append(mat)

    ### render to file
    output_path = os.path.join(working_dir, 'out', f"{out_name}_{i:04d}_")
    scene.render.filepath = output_path
    bpy.ops.render.render(write_still = True)

    # remove the objects after rendering
    for obj in obj_list:
        bpy.data.objects.remove(obj, do_unlink=True)

# generate the export definition for the LaTeX overlay
latex_output_path = os.path.join(working_dir, 'out', f'{out_name}_def.tex')
with open(latex_output_path, 'w') as f:
    f.write(f"\\def\\xoffset{{{view_offset_x}}}\n")
    f.write(f"\\def\\yoffset{{{view_offset_y}}}\n")
    f.write(f"\\def\\zoffset{{{view_offset_z}}}\n")
    f.write(f"\\def\\viewphi{{{phi}}}\n")
    f.write(f"\\def\\viewtheta{{{theta}}}\n")
    f.write(f"\\def\\orthoScale{{{camera.data.ortho_scale}}}\n")