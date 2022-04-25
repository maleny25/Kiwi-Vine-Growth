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
trunk = Cylinder(0.5, 10)
trunk = Shape(trunk, BRANCH_MATERIAL)


leader = Cylinder(0.5, 10)
leader = AxisRotated((0,1,0), pi/2, leader)
leader = Translated(0, 0, 10, leader)
leader = Shape(leader, BRANCH_MATERIAL)

leader2 = Cylinder(0.5, 10)
leader2 = AxisRotated((0,1,0), pi * 1.5, leader2)
leader2 = Translated(0, 0, 10, leader2)
leader2 = Shape(leader2, BRANCH_MATERIAL)

canes = []
canes_pos = []

for i in range(5):
    c = Cylinder(0.5, 5)
    c = AxisRotated((1,0,0), pi * 1.5, c)
    c = Translated(0, 0, 10, c)
    c = Translated(10 - (i * 4), 0, 0, c)
    c = Shape(c, BRANCH_MATERIAL)
    canes_pos.append((10 - (i * 4), pi * 1.5))
    canes.append(c)

for i in range(5):
    c = Cylinder(0.5, 5)
    c = AxisRotated((1,0,0), pi * .5, c)
    c = Translated(0, 0, 10, c)
    c = Translated(8 - (i * 4), 0, 0, c)
    c = Shape(c, BRANCH_MATERIAL)
    canes_pos.append((8 - (i * 4), pi * .5))
    canes.append(c)


#randomly generate nodes
import random
nodes = []
end = []
for i in range(18):
    n = random.randrange(0, 10, 1)
    loc = random.randrange(0, 5, 1)
    pos, angle = canes_pos[n]

    

    node = Cylinder(0.25, 0.25)

    #node = AxisRotated((x/10, y/10, z/10), angle, node)
    
    if (angle < pi):
        loc *= -1
    node = Translated(pos, loc, 10, node)
    node = Shape(node, BRANCH_MATERIAL)
    nodes.append(node)
    end.append((pos, loc, 10))

shape = Sphere(1)
leaf = Shape(shape, LEAF_MATERIAL)

##########################################

# Add components to scene based on growing algorithm

# Initialize tree
DORMANT, GROW, ABORT = 0, 1, 2
p_bb = 0.2 # probability that tree will remain dormant
p_sd = 0.7 # probability that tree will actively grow if not dormant
steps = 0
scene_objects = [trunk, leader, leader2] + canes + nodes# start with just tree trunk



# Growth folling Markov Model outlined in paper
num_aborted = 0
states = []
for i in range(18):
    states.append(DORMANT)

extend = []
while num_aborted < 18:
    for i in range(18):
        if states[i] == ABORT:
            continue
        elif states[i] == DORMANT:
            if np.random.binomial(1000, p_bb, 1) > p_bb*1000:
                states[i] = GROW
            # else remain dormant
        elif states[i] == GROW:
            x = random.randrange(0, 3.14 * 2 * 1000000, 1)/1000000
            y = random.randrange(0, 3.14 * 2 * 1000000, 1)/1000000
            z = random.randrange(0, 3.14 * 2 * 1000000, 1)/1000000
      
            node = Cylinder(0.25, 4)
            node = AxisRotated((1,0,0), x, node)
            node = AxisRotated((0,1,0), y, node)
            node = AxisRotated((0,0,1), z, node)
            node  = Translated(end[i][0], end[i][1], end[i][2], node)
            extend.append(node)
            print(1, end[i])
            tuple_add = lambda a, b: tuple(map(sum, zip(a, b))) 
            new_end = (4 * x/(2 * pi), 4 * y/(2 * pi), 4 * z/(2 * pi))
            end[i] = tuple_add(end[i], new_end)
            print(2, end[i])
            if np.random.binomial(1000, p_bb, 1) > p_bb*1000:
                states[i] = ABORT
                num_aborted += 1

            # TODO: add objects to scene
            scene_objects.append(leader)
        else:
            raise ValueError("Invalid state: " + cur_state)
#scene_objects.append(leader2)
scene_objects += extend
scene = Scene(scene_objects)

##########################################
# Display
Viewer.display(scene)
Viewer.frameGL.setBgColor(135, 206, 235)
Viewer.grids.setXYPlane(True)
Viewer.grids.setYZPlane(False)
Viewer.grids.setXZPlane(False)
# Viewer.frameGL.saveImage("user/result.png")
