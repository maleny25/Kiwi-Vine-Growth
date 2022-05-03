from openalea.plantgl.all import *
import numpy as np
import random
##########################################

# Define color of basic components
AMBIENT_BRANCH_CLR = Color3(101, 69, 33)
SPECULAR_BRANCH_CLR = Color3(101, 69, 33)
EMISSION_BRANCH_CLR = Color3(101, 69, 33)

# BRANCH_MATERIAL = Material(AMBIENT_BRANCH_CLR, 1, SPECULAR_BRANCH_CLR, EMISSION_BRANCH_CLR, 1, 0)
BRANCH_MATERIAL = ImageTexture("Bark.jpg")
LEAF_MATERIAL = Material(Color3(60,179,113), 1, Color3(0,0,0), Color3(0,0,0), 1, 0) #ImageTexture("./leaf_texture.png")

NUM_CANES = 18
TRUNK_HEIGHT = 10


scale = 0.3
leaf_base = Polyline2D.Circle(0.01,25)
leaf_curve = NurbsCurve2D(np.array([(0,0,1), (2,1,1), (1.25,2,1), (0.75,3,1),
                   (0,5,1),(0,5,1),(-0.75,3,1),(-1.25,2,1),(-2,1,1),(0,0,1)])*scale)
#leaf = Shape((Translated(-2,0,0, ExtrudedHull(leaf_curve, leaf_base))), LEAF_MATERIAL)

FRUIT_MATERIAL = ImageTexture("./kiwi_skin.jpg")
fruit = Shape(Sphere(0.25), FRUIT_MATERIAL)

##########################################
# user inputs
p_bb = 0.2 # probability that tree will remain dormant
p_sd = 0.7 # probability that tree will actively grow if not dormant
steps = 0


##########################################

# Helper functions

#x axis rotation matrix
rot_x = lambda x: np.array([[1, 0, 0], [0, np.cos(x), -1 * np.sin(x)], [0, np.sin(x), np.cos(x)]])
#y axis rotation matrix
rot_y = lambda x: np.array([[np.cos(x), 0, np.sin(x)], [0, 1, 0], [-1 * np.sin(x), 0, np.cos(x)]])
#z axis rotation matrix
rot_z = lambda x: np.array([[np.cos(x), -1 * np.sin(x), 0], [np.sin(x), np.cos(x), 0], [0, 0, 1]])
#for adding two tuples together
tuple_add = lambda a, b: tuple(map(sum, zip(a, b)))

# Helpter method to rotate the given object as specified along the x, y, and z axes
def rotate(shape, x_rot, y_rot, z_rot):
    shape = AxisRotated((1,0,0), x_rot, shape)
    shape = AxisRotated((0,1,0), y_rot, shape)
    shape = AxisRotated((0,0,1), z_rot, shape)
    return shape

# Randomly generates an angles
def rand_angle():
    return random.randrange(0, 3.14 * 2 * 1000000, 1)/1000000

# Generates a new leaf with a random orientation randomly located between loc1
# and (loc1+loc1_extension)
def gen_leaf(loc1, loc1_extension, leaf=True):

    offset = loc1_extension*np.random.random(1)
    loc = tuple_add(loc1, offset)
    if leaf:
        leaf = ExtrudedHull(leaf_curve, leaf_base)
        material = LEAF_MATERIAL
    else: # is fruit
        leaf = Sphere(0.25)
        material = FRUIT_MATERIAL
    leaf = rotate(leaf, rand_angle(), rand_angle(), rand_angle())
    leaf = Shape(Translated(loc[0], loc[1], loc[2], leaf), material)
    return leaf

##########################################

# Define geometry of basic components
#create trunk
trunk = Cylinder(0.2, TRUNK_HEIGHT)
trunk = Shape(trunk, BRANCH_MATERIAL)

#create both leaders
leader = Cylinder(0.15, TRUNK_HEIGHT)
leader = AxisRotated((0,1,0), pi/2, leader)
leader = Translated(0, 0, TRUNK_HEIGHT, leader)
leader = Shape(leader, BRANCH_MATERIAL)

leader2 = Cylinder(0.15, TRUNK_HEIGHT)
leader2 = AxisRotated((0,1,0), pi * 1.5, leader2)
leader2 = Translated(0, 0, TRUNK_HEIGHT, leader2)
leader2 = Shape(leader2, BRANCH_MATERIAL)

#create 10 canes
canes = [] #the list of cane objects
canes_pos = [] #a tuple of the starting position and vector normal of each cane
cane_leaves = []

for i in range(5):
    c = Cylinder(0.1, TRUNK_HEIGHT/2)
    c = AxisRotated((1,0,0), pi * 1.5, c)
    c = Translated(0, 0, TRUNK_HEIGHT, c)
    c = Translated(TRUNK_HEIGHT - (i * 4), 0, 0, c)
    c = Shape(c, BRANCH_MATERIAL)
    canes_pos.append((TRUNK_HEIGHT - (i * 4), pi * 1.5))
    canes.append(c)
    NUM_LEAVES = int(np.random.normal(7, 2))
    cane_leaves += [gen_leaf([TRUNK_HEIGHT - (i * 4), 0, TRUNK_HEIGHT], [0, TRUNK_HEIGHT/2, 0]) for n in range(NUM_LEAVES)]

for i in range(5):
    c = Cylinder(0.1, TRUNK_HEIGHT/2)
    c = AxisRotated((1,0,0), pi * .5, c)
    c = Translated(0, 0, TRUNK_HEIGHT, c)
    c = Translated(TRUNK_HEIGHT - int(TRUNK_HEIGHT/5) - (i * 4), 0, 0, c)
    c = Shape(c, BRANCH_MATERIAL)
    canes_pos.append((TRUNK_HEIGHT -int(TRUNK_HEIGHT/5)- (i * 4), pi * .5))
    canes.append(c)
    NUM_LEAVES = int(np.random.normal(7, 2))
    cane_leaves += [gen_leaf([TRUNK_HEIGHT - int(TRUNK_HEIGHT/5) - (i*4), 0, TRUNK_HEIGHT], [0, -TRUNK_HEIGHT/2, 0]) for n in range(NUM_LEAVES)]

#randomly generate nodes by randomly choosing a cane and then randomly choosing a position on the cane
import random
nodes = []
end = []
for i in range(NUM_CANES):
    n = random.randrange(0, TRUNK_HEIGHT, 1)
    loc = random.randrange(0, 5, 1)
    pos, angle = canes_pos[n]
    node = Cylinder(0.25, 0.25)
    if (angle < pi):
        loc *= -1
    node = Translated(pos, loc, TRUNK_HEIGHT, node)
    node = Shape(node, BRANCH_MATERIAL)
    nodes.append(node)
    end.append((pos, loc, TRUNK_HEIGHT))

# Create grass floor
points = [(-15,-15,0),
            (15,-15,0),
            (15,15,0),
            (-15,15,0)]
# A list of colors
colors = [Color4(0,150,0,155),
          Color4(0,150,0,155),
          Color4(0,150,0,155),
          Color4(0,150,0,155)]
# A list of directions for the normals
normals = [(0,0,1) for i in range(4)]
# A list of indices that set the indices for the quads
indices = [(0, 1, 2, 3)]
# Creation of the quadset
grass = QuadSet(points,indices,normals,indices,colors)
##########################################

# Add components to scene based on growing algorithm

# Initialize tree
DORMANT, GROW, ABORT = 0, 1, 2
scene_objects = [trunk, leader, leader2] + canes + nodes + [grass] + cane_leaves# start with just tree trunk

########### Growth folling Markov Model outlined in paper

#Markov Chain
#initialize list of shoots
shoots = []
def markov(p_bb = p_bb, p_sd = p_sd, scene_objects = scene_objects, shoots=shoots):
    #Initialize the state of each node
    states = []
    for i in range(NUM_CANES):
        states.append(DORMANT)

    #shoots = []
    for i in range(NUM_CANES):
        while states[i] != ABORT:
            if states[i] == DORMANT:
                if np.random.binomial(1000, p_bb, 1) > p_bb*1000:
                    states[i] = GROW
                # else remain dormant
            elif states[i] == GROW:
                shoot = Cylinder(0.05, 4)

                # randomly generate three angles
                x = rand_angle()
                y = rand_angle()
                z = rand_angle()
                # make shoot grow in a random direction
                shoot = rotate(shoot, x, y, z)
                # offset new shoot by the end of the last shoot it's growing off of
                shoot  = Translated(end[i][0], end[i][1], end[i][2], shoot)
                #add shoot to the list of shoots
                shoots.append(shoot)

                #compute the end of the new shoot by rotating a vector of length 4
                v = np.array([0, 0, 4])
                new_end = np.dot(rot_x(x), v)
                new_end = np.dot(rot_y(y), new_end)
                new_end = np.dot(rot_z(z), new_end)

                NUM_LEAVES = int(np.random.normal(7, 2))
                #leaves = [rotate(ExtrudedHull(leaf_curve, leaf_base), rand_angle(), rand_angle(), rand_angle()) for n in range(NUM_LEAVES)]
                #offsets = [tuple_add(end[i], new_end*np.random.random(1)) for n in range(NUM_LEAVES)]
                #leaves = [Shape(Translated(offsets[n][0], offsets[n][1], offsets[n][2], leaves[n]), LEAF_MATERIAL) for n in range(NUM_LEAVES)]
                leaves = [gen_leaf(end[i], new_end) for n in range(NUM_LEAVES)]
                NUM_FRUITS = int(np.random.normal(0.5, 2))
                fruits = [gen_leaf(end[i], new_end, leaf=False) for f in range(NUM_FRUITS)]

                # offset the new end position by the old end position
                end[i] = tuple_add(end[i], new_end)

                #change to user input
                if np.random.binomial(1000, 1 - p_sd, 1) > (1 - p_sd) *1000:
                    states[i] = ABORT

                # Add objects to scene
                scene_objects.append(leader)
                scene_objects += leaves
                scene_objects += fruits
            else:
                raise ValueError("Invalid state: " + cur_state)
        i += 1

markov()
scene_objects.pop(-1)
scene_objects += shoots

scene = Scene(scene_objects)

##########################################
# Display
Viewer.display(scene)
Viewer.frameGL.setBgColor(135, 206, 235)
Viewer.grids.setXYPlane(True)
Viewer.grids.setYZPlane(False)
Viewer.grids.setXZPlane(False)
# yield

# #scene_objects.append(leader2)
# scene_objects += shoots
# scene = Scene(scene_objects)

# ##########################################
# # Display
# Viewer.display(scene)
# Viewer.frameGL.setBgColor(135, 206, 235)
# Viewer.grids.setXYPlane(True)
# Viewer.grids.setYZPlane(False)
# Viewer.grids.setXZPlane(False)
# # Viewer.frameGL.saveImage("user/result.png")

#[(0,0,1),(1.5, 0.5, 1), (2,2,1), (1.5,3,1), (.5,3.5,1), (0,4,1), (-.5,3.5,1), (-1.5,3,1), (-2,2,1), (-1.5,.5,1),(0,0,1)]
