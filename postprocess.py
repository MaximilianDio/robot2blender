# Postprocessing: transform to pdf: e.g.

import os
from pathlib import Path
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

render_dir = Path("out/renders")

files = [f for f in os.listdir(render_dir) if f.endswith(".svg")]

for file in files:
    drawing = svg2rlg(f"out/renders/{file}")
    renderPDF.drawToFile(drawing, f"out/renders/{file.replace('.svg', '.pdf')}")
    # renderPM.drawToFile(drawing, f"out/renders/{file.replace('.svg', '.png')}", fmt="PNG")