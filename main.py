from openalea.plantgl.all import *
import numpy as np
##########################################

# Define color of basic components
AMBIENT_BRANCH_CLR = Color3(101, 69, 33)
SPECULAR_BRANCH_CLR = Color3(101, 69, 33)
EMISSION_BRANCH_CLR = Color3(101, 69, 33)

BRANCH_MATERIAL = Material(AMBIENT_BRANCH_CLR, 1, SPECULAR_BRANCH_CLR, EMISSION_BRANCH_CLR, 1, 0)
LEAF_MATERIAL = Material(Color3(60,179,113), 1, Color3(0,0,0), Color3(0,0,0), 1, 0) #ImageTexture("./leaf_texture.png")

##########################################
#user inputs

##########################################

#Lambda functions

#x axis rotation matrix
rot_x = lambda x: np.array([[1, 0, 0], [0, np.cos(x), -1 * np.sin(x)], [0, np.sin(x), np.cos(x)]])
#y axis rotation matrix
rot_y = lambda x: np.array([[np.cos(x), 0, np.sin(x)], [0, 1, 0], [-1 * np.sin(x), 0, np.cos(x)]])
#z axis rotation matrix
rot_z = lambda x: np.array([[np.cos(x), -1 * np.sin(x), 0], [np.sin(x), np.cos(x), 0], [0, 0, 1]])
#for adding two tuples together
tuple_add = lambda a, b: tuple(map(sum, zip(a, b))) 

##########################################

# Define geometry of basic components
#create trunk
trunk = Cylinder(0.2, 10)
trunk = Shape(trunk, BRANCH_MATERIAL)

#create both leaders
leader = Cylinder(0.15, 10)
leader = AxisRotated((0,1,0), pi/2, leader)
leader = Translated(0, 0, 10, leader)
leader = Shape(leader, BRANCH_MATERIAL)

leader2 = Cylinder(0.15, 10)
leader2 = AxisRotated((0,1,0), pi * 1.5, leader2)
leader2 = Translated(0, 0, 10, leader2)
leader2 = Shape(leader2, BRANCH_MATERIAL)

#create 10 canes
canes = [] #the list of cane objects
canes_pos = [] #a tuple of the starting position and vector normal of each cane

for i in range(5):
    c = Cylinder(0.1, 5)
    c = AxisRotated((1,0,0), pi * 1.5, c)
    c = Translated(0, 0, 10, c)
    c = Translated(10 - (i * 4), 0, 0, c)
    c = Shape(c, BRANCH_MATERIAL)
    canes_pos.append((10 - (i * 4), pi * 1.5))
    canes.append(c)

for i in range(5):
    c = Cylinder(0.1, 5)
    c = AxisRotated((1,0,0), pi * .5, c)
    c = Translated(0, 0, 10, c)
    c = Translated(8 - (i * 4), 0, 0, c)
    c = Shape(c, BRANCH_MATERIAL)
    canes_pos.append((8 - (i * 4), pi * .5))
    canes.append(c)

#randomly generate nodes by randomly choosing a cane and then randomly choosing a position on the cane
import random
nodes = []
end = []
for i in range(18):
    n = random.randrange(0, 10, 1)
    loc = random.randrange(0, 5, 1)
    pos, angle = canes_pos[n]
    node = Cylinder(0.25, 0.25) 
    if (angle < pi):
        loc *= -1
    node = Translated(pos, loc, 10, node)
    node = Shape(node, BRANCH_MATERIAL)
    nodes.append(node)
    end.append((pos, loc, 10))

scale = 0.3
leaf_base = Polyline2D.Circle(0.01,25)
leaf_curve = NurbsCurve2D(np.array([(0,0,1), (2,1,1), (1.25,2,1), (0.75,3,1),
                   (0,5,1),(0,5,1),(-0.75,3,1),(-1.25,2,1),(-2,1,1),(0,0,1)])*scale)
leaf = Shape(Translated(-2,0,0, ExtrudedHull(leaf_curve, leaf_base)), LEAF_MATERIAL)

##########################################

# Add components to scene based on growing algorithm

# Initialize tree
DORMANT, GROW, ABORT = 0, 1, 2
p_bb = 0.2 # probability that tree will remain dormant
p_sd = 0.7 # probability that tree will actively grow if not dormant
steps = 0
scene_objects = [trunk, leader, leader2] + canes + nodes# start with just tree trunk



########### Growth folling Markov Model outlined in paper

#Initialize the state of each node
num_aborted = 0
states = []
for i in range(18):
    states.append(DORMANT)

#Markov Chain
#initialize list of shoots
shoots = []
while num_aborted < 18:
    for i in range(18):
        if states[i] == ABORT:
            continue
        elif states[i] == DORMANT:
            if np.random.binomial(1000, p_bb, 1) > p_bb*1000:
                states[i] = GROW
            # else remain dormant
        elif states[i] == GROW:
            #randomly generate three angles
            x = random.randrange(0, 3.14 * 2 * 1000000, 1)/1000000
            y = random.randrange(0, 3.14 * 2 * 1000000, 1)/1000000
            z = random.randrange(0, 3.14 * 2 * 1000000, 1)/1000000
            #create a shoot
            shoot = Cylinder(0.05, 4)

            #make shoot grow in a random direction
            #rotate shoot's x axis by randomly generated x angle
            shoot = AxisRotated((1,0,0), x, shoot)
            #rotate shoot's y axis by randomly generated y angle
            shoot = AxisRotated((0,1,0), y, shoot)
            #rotate shoot's z axis by randomly generated z angle
            shoot = AxisRotated((0,0,1), z, shoot)

            #offset new shoot by the end of the last shoot it's growing off of
            shoot  = Translated(end[i][0], end[i][1], end[i][2], shoot)
            #add shoot to the list of shoots
            shoots.append(shoot)

            #compute the end of the new shoot by rotating a vector of length 4
            v = np.array([0, 0, 4])
            new_end = np.dot(rot_x(x), v)
            new_end = np.dot(rot_y(y), new_end)
            new_end = np.dot(rot_z(z), new_end)

            #offset the new end position by the old end position
            end[i] = tuple_add(end[i], new_end)
            
            
            if np.random.binomial(1000, p_bb, 1) > p_bb*1000:
                states[i] = ABORT
                num_aborted += 1

            # TODO: add objects to scene
            scene_objects.append(leader)
        else:
            raise ValueError("Invalid state: " + cur_state)
#scene_objects.append(leader2)
scene_objects += shoots
scene = Scene(scene_objects)

##########################################
# Display
Viewer.display(scene)
Viewer.frameGL.setBgColor(135, 206, 235)
Viewer.grids.setXYPlane(True)
Viewer.grids.setYZPlane(False)
Viewer.grids.setXZPlane(False)
# Viewer.frameGL.saveImage("user/result.png")
