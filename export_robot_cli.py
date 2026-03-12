from robot_visualization.robot import Robot
import numpy as np
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Export robot to OBJ')
    parser.add_argument('--robot', default='GoFa5', help='Robot name (URDF filename without extension)')
    parser.add_argument('--q0', type=float, nargs='+', default=[-np.pi/4, -0.5, 0.5, 0.0, np.pi/2, np.pi],
                        help='Initial joint configuration as space-separated floats')
    args = parser.parse_args()

    robot_asset_path = os.path.join(os.path.dirname(__file__), f'robot_assets/urdf/{args.robot}.urdf')

    robot = Robot(urdf_file=robot_asset_path)

    plotter = robot.plotter

    np.random.seed(1)

    q0 = np.array(args.q0)  # initial joint configuration

    robot.update(q=q0)

    # robot.plot_ee_frame(q0)

    plotter.export_obj(os.path.join(os.path.dirname(__file__), 'out/robots/Robot_A.obj'))
    plotter.show()


if __name__ == '__main__':
    main()

# start blender and import the exported obj file to visualize the robot