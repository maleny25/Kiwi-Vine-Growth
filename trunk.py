from openalea.plantgl.all import *

c = 0.1
qi = 5
Gmax = 10
dsdt = (c/(c + qi)) * Gmax

sink_size = 1

def trunk(sink_size = sink_size, dsdt = dsdt):
    cir = Polyline2D.Circle(1,50)

    prof1 = NurbsCurve([(0.0, 0.0, 0, 1),
                    (0, 0, 1, 1),
                    (0, 0, 2, 2),
                    (0, 0, 3, 2),
                    (0, 0.0, 10, 2)])
    scales1 = [(0.4 * sink_size, 0.4 * sink_size),
            (0.3, 0.3),
            (0.2, 0.2),
            (0.1, 0.1),
            (0.1, 0.1)]
    br1 = Extrusion(prof1, cir, scales1)
    col = Material(Color3(127,72,0))
    shb = [Shape(br1,col)]
    scene = Scene(shb)
    Viewer.display(scene)
    sink_size += dsdt
    yield