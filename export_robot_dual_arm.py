from robot_visualization.robot import Robot
import numpy as np
import os
import pyvista as pv

# ── Robot configurations ───────────────────────────────────────────────────────
# Add or remove entries to control how many robots appear in the scene.
robots_config = [
    {
        "urdf": os.path.join(os.path.dirname(__file__), "robot_assets/urdf/iiwa7_lbr1.urdf"),
        "q0": np.zeros(7),
        "color": "lightgray",
        "label": "Robot A",
        "base_position": np.array([-0.3682, 0.0,  -0.7048]),
    },
        {
        "urdf": os.path.join(os.path.dirname(__file__), "robot_assets/urdf/iiwa7_lbr2.urdf"),
        "q0": np.zeros(7),
        "color": "lightgray",
        "label": "Robot B",
        "base_position": np.array([-0.3682, 0.0,  -0.7048]),
    },
]

# Joint limits for iiwa7 (radians)
JOINT_LIMITS = [
    (-2.967, 2.967),
    (-2.094, 2.094),
    (-2.967, 2.967),
    (-2.094, 2.094),
    (-2.967, 2.967),
    (-2.094, 2.094),
    (-3.054, 3.054),
]

# ── Build scene ────────────────────────────────────────────────────────────────
plotter = pv.Plotter()

robots = []
qs = []

for cfg in robots_config:
    q = cfg["q0"].copy()
    qs.append(q)

    robot = Robot(
        urdf_file=cfg["urdf"],
        plotter=plotter,
        color=cfg["color"],
        p0=cfg["base_position"],
    )
    robot.update(q=q)
    robots.append(robot)

# ── Slider panels ──────────────────────────────────────────────────────────────
# Each robot gets a vertical column of sliders. Columns are laid out left-to-right.
n_robots = len(robots_config)
panel_w = min(0.22, 0.95 / n_robots - 0.02)  # shrink panels if many robots
panel_gap = 0.02
n_joints = len(JOINT_LIMITS)

for ri, (robot, q, cfg) in enumerate(zip(robots, qs, robots_config)):
    x0 = panel_gap + ri * (panel_w + panel_gap)
    x1 = x0 + panel_w

    # Column header label
    plotter.add_text(
        cfg["label"],
        position=(x0, 0.94),
        viewport=True,
        font_size=9,
        color=cfg["color"],
    )

    def make_callback(r, qi, i):
        def callback(value):
            qi[i] = value
            r.update(q=qi)
        return callback

    for ji, (lower, upper) in enumerate(JOINT_LIMITS):
        posy = 0.88 - ji * 0.12
        plotter.add_slider_widget(
            callback=make_callback(robot, q, ji),
            rng=[lower, upper],
            value=float(q[ji]),
            title=f"J{ji + 1}",
            pointa=(x0, posy),
            pointb=(x1, posy),
            style="modern",
            fmt="%.2f",
        )

    # Export button — pixel coordinates; space 150 px per robot
    btn_x = 10 + ri * 150

    def make_export(r, label):
        def export_callback(flag):
            safe_label = label.replace(" ", "_")
            out_path = os.path.join(
                os.path.dirname(__file__), f"out/robots/{safe_label}.obj"
            )
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            plotter.export_obj(out_path)
            print(f"Exported {label} → {out_path}")
        return export_callback

    plotter.add_checkbox_button_widget(
        callback=make_export(robot, cfg["label"]),
        value=False,
        position=(btn_x, 10),
        size=35,
        color_on="green",
        color_off="green",
    )
    plotter.add_text(
        f"Export {cfg['label']}",
        position=(btn_x + 40, 18),
        font_size=8,
        color="white",
    )

plotter.show()
