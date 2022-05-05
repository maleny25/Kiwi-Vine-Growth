from openalea.plantgl.all import *
import numpy as np
FRUIT_MATERIAL = ImageTexture("./kiwi_skin.jpg")

#adjust to create different sized kiwis
scale = 0.5

fruit_base = Polyline2D.Circle(scale * 1,50)
fruit_curve = NurbsCurve2D(scale * np.array([(0,0,1),(0.85,.15,1), (1.25, 1, 1), (1.5,2,1), (1.25,3,1), (0.85,3.85,1), (0,4,1), (0,4,1), (-.85,3.85,1), (-1.25,3,1), (-1.5,2,1), (-1.25,1,1),(-.85,.15,1),(0,0,1)])*scale)
fruit = Shape(Translated(-2,0,0, ExtrudedHull(fruit_curve, fruit_base)), FRUIT_MATERIAL)

scene = Scene([fruit])
Viewer.display(scene)

Viewer.frameGL.setBgColor(135, 206, 235)
Viewer.grids.setXYPlane(True)
Viewer.grids.setYZPlane(False)
Viewer.grids.setXZPlane(False)
