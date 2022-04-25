from openalea.plantgl.all import *
import numpy as np
##########################################

# Define color of basic components
AMBIENT_BRANCH_CLR = Color3(101, 69, 33)
SPECULAR_BRANCH_CLR = Color3(101, 69, 33)
EMISSION_BRANCH_CLR = Color3(101, 69, 33)

BRANCH_MATERIAL = Material(AMBIENT_BRANCH_CLR, 1, SPECULAR_BRANCH_CLR, EMISSION_BRANCH_CLR, 1, 0)
LEAF_MATERIAL = Material(Color3(60,179,113), 0, Color3(0,0,0), Color3(0,0,0), 1, 0)
##########################################

# Define geometry of basic components
trunk = Cylinder(3, 10)
trunk = Shape(trunk, BRANCH_MATERIAL)

leader = Cylinder(2, 5)
leader = AxisRotated((0,1,0), pi/2., leader)
leader = Translated(0, 0, 5, leader)
leader = Shape(leader, BRANCH_MATERIAL)

shape = Cylinder(1, 5)
cane = Shape(shape, BRANCH_MATERIAL)

shape = Sphere(1)
leaf = Shape(shape, LEAF_MATERIAL)

##########################################

# Add components to scene based on growing algorithm

# Initialize tree
DORMANT, GROW, ABORT = 0, 1, 2
p_bb = 0.2 # probability that tree will remain dormant
p_sd = 0.7 # probability that tree will actively grow if not dormant
steps = 0
cur_state = DORMANT
scene_objects = [trunk] # start with just tree trunk

# Growth folling Markov Model outlined in paper
while cur_state != ABORT:
    if cur_state == DORMANT:
        if np.random.binomial(1000, p_bb, 1) > p_bb*1000:
            cur_state = GROW
        # else remain dormant
    elif cur_state == GROW:
        if np.random.binomial(1000, p_bb, 1) > p_bb*1000:
            cur_state = ABORT
        # TODO: add objects to scene
        scene_objects.append(leader)
    else:
        raise ValueError("Invalid state: " + cur_state)
#scene_objects.append(leader2)
scene = Scene(scene_objects)

##########################################
# Display
Viewer.display(scene)
Viewer.frameGL.setBgColor(135, 206, 235)
Viewer.grids.setXYPlane(True)
Viewer.grids.setYZPlane(False)
Viewer.grids.setXZPlane(False)
# Viewer.frameGL.saveImage("user/result.png")
