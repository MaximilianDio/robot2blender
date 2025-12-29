# Render a line SVG of a robot obtained from an .obj 

The repository is designed to generate png and svg files similar to

<img src="https://github.com/MaximilianDio/robot2blender/blob/main/out/robot.png" width="400">
<img src="https://github.com/MaximilianDio/robot2blender/blob/main/out/robot0000.svg" width="400">


Use the `render_robot.blend` Blender file

## The following is automated by running the script in the render_robot.blend file.

- Define the output directory of the renderer in scene/Output 
- Import an .obj (obtained by using the appropriate Python code `export_robot.py`)
- set camera Settings (pose/ aspect ratio, etc.)
- Press F12 to render the Image
