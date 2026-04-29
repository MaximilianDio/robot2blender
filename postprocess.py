# Postprocessing: transform to pdf: e.g.

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

files = ["robot_0000_0000.svg", "robot_0001_0000.svg"]

for file in files:
    drawing = svg2rlg(f"out/renders/{file}")
    renderPDF.drawToFile(drawing, f"out/renders/{file.replace('.svg', '.pdf')}")
    # renderPM.drawToFile(drawing, f"out/renders/{file.replace('.svg', '.png')}", fmt="PNG")