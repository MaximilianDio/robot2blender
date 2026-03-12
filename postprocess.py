# Postprocessing: transform to pdf: e.g.

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

drawing = svg2rlg("out/robot0000.svg")
renderPDF.drawToFile(drawing, "out/robot.pdf")
# renderPM.drawToFile(drawing, "out/robot.png", fmt="PNG")