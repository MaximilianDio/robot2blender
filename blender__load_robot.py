# run the export_robot.py (easier than including dependencies for python)

import os
import bpy
from math import sin, cos, radians
from mathutils import Vector

set_camera = True
set_material = True
render_frame = True
load_robot = True
remove_robot = True

phi = 90
theta = 80  # polar angle from z-axis, adjust for different views
view_offset_x = 0.6  # adjust to center the robot in view if needed
view_offset_y = 0.0
view_offset_z = 1.2
ortho_scale = 1.4  # adjust for zoom level

base_colors = [(204/255, 227/255, 242/255, 1.0), (1.0, 0.8, 0.8, 1.0)]  # RGBA for the base color of the material
shade_colors = [(0, 120/255, 189/255, 1.0), (1.0, 0.2, 0.2, 1.0)]  # RGBA for the shaded color of the material


## !! Set the File Output in the compositor
working_dir = os.path.abspath("C:\\Users\\aq75owes\\Documents\\Paper\\atlas_avp\\02_figures\\problems\\dual_arm\\data\\avp")

#os.path.dirname(os.path.dirname(__file__))

out_name = f"img"



if set_camera:
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

obj_list = []
for ii, idx_list in enumerate([[0,3]]):
    frames = [
    [[f"Robot_avp_0_{i}.obj", f"Robot_avp_1_{i}.obj"]]  for i in range(idx_list[0], idx_list[1],1)
]   
    for i, frame in enumerate(frames):
        for j, obj_names in enumerate(frame):
            
            if set_material:
                # color settings
                mat_name = "singleLineHatch"
                mat = bpy.data.materials.get(mat_name)

                if mat is None:
                    raise RuntimeError(f"Base material '{mat_name}' not found")

                mat_name = f"{mat_name}_{i:02d}_{j:02d}"
                existing = bpy.data.materials.get(mat_name)
                mat = existing if existing else mat.copy()
                mat.name = mat_name

                mat.use_nodes = True
                node_tree = mat.node_tree

                # Find the Color Ramp node
                color_ramp_node = None
                for node in node_tree.nodes:
                    if node.type == 'VALTORGB':
                        color_ramp_node = node
                        break

                # if color_ramp_node:
                elements = color_ramp_node.color_ramp.elements
                n_frames = max(len(frames) - 1, 1)
                t = 0.2 + 0.8 * i / n_frames  # 0 → 20% color, 1 → 100% color
                def lerp_white(color):
                    return tuple(1.0 + t * (c - 1.0) if k < 3 else c for k, c in enumerate(color))
                # First stop (left) — RGBA
                elements[0].color = lerp_white(shade_colors[j])
                # Second stop (right) — RGBA
                elements[1].color = lerp_white(base_colors[j])

                # You can also adjust stop positions
                elements[0].position = 0.0
                elements[1].position = 0.3  # matches your current setup

                # Set Freestyle line color (contour)
                view_layer = bpy.context.view_layer

                for lineset in view_layer.freestyle_settings.linesets:
                    linestyle = lineset.linestyle
                    print(lineset.name, linestyle.color)  # RGB tuple
            
                    # To change the color:
                    linestyle.color = shade_colors[j][:3]  # use RGB from shade_colors
            
            ## import the objects for this frame

            if load_robot:
                for obj_name in obj_names:
                    file_path = os.path.join(working_dir, "robots", obj_name)
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
                    obj.data.materials.append(mat)
            
    if render_frame:
        ### render to file
        output_path = os.path.join(working_dir, 'renders', f"{out_name}")
        scene.render.filepath = output_path

        tree = bpy.context.scene.node_tree
        # Get all File Output nodes
        file_outputs = [n for n in tree.nodes if n.type == 'OUTPUT_FILE']
        for fo in file_outputs:
            print(f"File Output: {fo.name}, base_path: {fo.base_path}")
            for slot in fo.file_slots:
                print(f"  slot: {slot.path}")
                slot.path = f"{out_name}_{ii:02d}"


        bpy.ops.render.render(write_still = True)

    # remove the objects after rendering
    if load_robot and remove_robot:
        for obj in obj_list:
            bpy.data.objects.remove(obj, do_unlink=True)

# generate the export definition for the LaTeX overlay
if set_camera:
    latex_output_path = os.path.join(working_dir, 'renders', f'{out_name}_def.tex')
    with open(latex_output_path, 'w') as f:
        f.write(f"\\def\\xoffset{{{view_offset_x}}}\n")
        f.write(f"\\def\\yoffset{{{view_offset_y}}}\n")
        f.write(f"\\def\\zoffset{{{view_offset_z}}}\n")
        f.write(f"\\def\\viewphi{{{phi}}}\n")
        f.write(f"\\def\\viewtheta{{{theta}}}\n")
        f.write(f"\\def\\orthoScale{{{camera.data.ortho_scale}}}\n")