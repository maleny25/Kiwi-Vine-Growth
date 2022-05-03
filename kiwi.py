from openalea.plantgl.all import *
import numpy as np
LEAF_MATERIAL = Material(Color3(60,179,113), 1, Color3(0,0,0), Color3(0,0,0), 1, 0) #ImageTexture("./leaf_texture.png")

#adjust to create different sized kiwis
scale = 1

leaf_base = Polyline2D.Circle(scale * 1,50)
leaf_curve = NurbsCurve2D(scale * np.array([(0,0,1),(0.85,.15,1), (1.25, 1, 1), (1.5,2,1), (1.25,3,1), (0.85,3.85,1), (0,4,1), (0,4,1), (-.85,3.85,1), (-1.25,3,1), (-1.5,2,1), (-1.25,1,1),(-.85,.15,1),(0,0,1)])*scale)
leaf = Shape(Translated(-2,0,0, ExtrudedHull(leaf_curve, leaf_base)), LEAF_MATERIAL)

scene = Scene([leaf])
Viewer.display(scene)

Viewer.frameGL.setBgColor(162,165,104)
Viewer.grids.setXYPlane(True)
Viewer.grids.setYZPlane(False)
Viewer.grids.setXZPlane(False)