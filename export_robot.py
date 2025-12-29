from robot_visualization.robot import Robot
import numpy as np
import os

robot_asset_path = os.path.join(os.path.dirname(__file__), 'robot_assets/urdf/IRB1100_4_058.urdf')
Nq = 6

robot = Robot(urdf_file=robot_asset_path)

plotter = robot.plotter

np.random.seed(1)

q0 = np.random.rand(Nq)

robot.update(q=q0)

plotter.export_obj(os.path.join(os.path.dirname(__file__), 'out/robots/robot.obj'))

# start blender and import the exported obj file to visualize the robot