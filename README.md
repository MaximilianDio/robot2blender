To render an SVG of the robot, use the `render_robot` Blender file. 

- Define the output directory of the renderer in scene/Output 
- Import an .obj (obtained by using the appropriate python code `export_robot.py`)
- set camera Settings (pose/ aspect ratio, etc.)
- Press F12 to render the Image

## run script in Blender

```python
import os
import bpy
from math import radians
from mathutils import Vector

obj_name = "demo.obj"
out_name = "robot"

working_dir = os.path.dirname(os.path.dirname(__file__))

file_path = os.path.join(working_dir, 'robots', obj_name)
print(file_path)

bpy.ops.import_scene.obj(filepath=file_path)

# set pose of the imported object
context = bpy.context
scene = context.scene
obj = scene.objects[-1]
obj.rotation_euler = (0,0,0)

# render to file
output_path = os.path.join(working_dir, 'out', out_name)
scene.render.filepath = output_path
bpy.ops.render.render(write_still = True)

# remove the object after 
bpy.data.objects.remove(obj, do_unlink=True)
```

