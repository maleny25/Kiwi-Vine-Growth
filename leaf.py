from openalea.plantgl.all import *
import numpy as np
LEAF_MATERIAL = Material(Color3(60,179,113), 1, Color3(0,0,0), Color3(0,0,0), 1, 0) #ImageTexture("./leaf_texture.png")

scale = 0.3
thickness = .1
leaf_base = NurbsCurve2D(np.array([(2, 1,1), (0, 1 + thickness, 1), (-2,1,1), (0, 1 - thickness, 1)])*scale)
leaf_curve = NurbsCurve2D(np.array([(0,0,1),(1.5, 0.5, 1), (2,2,1), (1.5,3,1), (.5,3.5,1), (0,4,1), (0,4,1), (-.5,3.5,1), (-1.5,3,1), (-2,2,1), (-1.5,.5,1),(0,0,1)])*scale)


leaf = Shape(Translated(-2,0,0, ExtrudedHull(leaf_curve, leaf_base)), LEAF_MATERIAL)

scene = Scene([leaf])
Viewer.display(scene)

Viewer.frameGL.setBgColor(135, 206, 235)
Viewer.grids.setXYPlane(True)
Viewer.grids.setYZPlane(False)
Viewer.grids.setXZPlane(False)