from openalea.plantgl.all import *
scene = Scene()
c = Cylinder(1, 10)
color = Material(Color3(255,0,0),0,Color3(0,0,0),Color3(0,0,0),1,0)
shape = Shape(c, color)
scene.add(shape)
Viewer.display(scene)

Viewer.frameGL.setBgColor(255,255,200)
Viewer.grids.setXYPlane(True)
Viewer.grids.setYZPlane(False)
Viewer.grids.setXZPlane(False)
Viewer.frameGL.saveImage("user/result.png")