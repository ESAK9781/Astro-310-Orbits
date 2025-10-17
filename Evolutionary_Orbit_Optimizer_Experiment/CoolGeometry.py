import math
from useful_consts import *


class Sphere:
    def __init__(self, pos, r):
        self.pos = pos
        self.r = r
    

    # get the distance from this sphere to a point
    def dist(self, point):
        return math.dist(point, self.pos) - self.r

class Geometric_Universe:
    def __init__(self):
        self.obstacles = []

    def add_obstacle(self, obs): # add an obstacle to the universe
        self.obstacles.append(obs)

    def get_dist(self, point): # get dist from point to closest obstacle in universe
        if (len(self.obstacles) == 0):
            print("ERROR: CALCULATING DISTANCES IN EMPTY UNIVERSE")
            return 1000
        out = self.obstacles[0].dist(point)
        for i in range(1, len(self.obstacles)):
            out = min(out, self.obstacles[i].dist(point))

        return out

# move a point along a vector for a specific distance
def move_point_along_vector(point, vector, distance):
    return [
        point[0] + (distance * vector[0]),
        point[1] + (distance * vector[1]),
        point[2] + (distance * vector[2])
    ]

"""

Shoot a ray from position a (vector, km) to position b (vector, km). Returns either the distance
travelled (if there is no obstruction), or -1 if the path is obstructed by the Earth

Uses the raymarching algorithm, look it up for a conceptual understanding of how it works. I am 
implementing it from prior experience and understanding, so no documentation is necessary.

"""

def shoot_astro_ray(pos_a, pos_b):
    # set up the universe with the one relevant obstacle
    univ = Geometric_Universe()
    earth = Sphere((0,0,0), R_EARTH)
    univ.add_obstacle(earth)

    total_dist = math.dist(pos_a, pos_b)
    move_vect = [ # create the normal vector pointing from a to b
        (pos_b[0] - pos_a[0]) / total_dist,
        (pos_b[1] - pos_a[1]) / total_dist,
        (pos_b[2] - pos_a[2]) / total_dist
    ]

    move_pnt = (pos_a[0], pos_a[1], pos_a[2]) # create a copy of point a which we will 
    total_dist_moved = 0
    # move around the world

    last_move_dist = MIN_MARCH_DIST + 1
    while (last_move_dist > MIN_MARCH_DIST): # march as far as we can without colliding into something
        next_move_dist = min(univ.get_dist(move_pnt), math.dist(move_pnt, pos_b))
        
        move_pnt = move_point_along_vector(move_pnt, move_vect, next_move_dist)
        last_move_dist = next_move_dist
        total_dist_moved += last_move_dist
        if (total_dist_moved > total_dist): # should never happen, but just in case we passed it
            break
    

    if (math.dist(move_pnt, pos_b) < MIN_MARCH_DIST): # if it got real close to B
        return total_dist
    return -1 # otherwise it must have hit Earth



# rotate a point about the z axis by theta degrees
def rot_z(point, theta):
    sint = math.sin(math.radians(theta))
    cost = math.cos(math.radians(theta))

    rot_mat = [ # basic z axis rotation matrix
        [
            cost, sint, 0
        ], [
            -sint, cost, 0
        ], [
            0, 0, 1
        ]
    ]

    out = [ # multiply the point by the matrix
        (point[0] * rot_mat[0][0]) + (point[1] * rot_mat[1][0]) + (point[2] * rot_mat[2][0]),
        (point[0] * rot_mat[0][1]) + (point[1] * rot_mat[1][1]) + (point[2] * rot_mat[2][1]),
        (point[0] * rot_mat[0][2]) + (point[1] * rot_mat[1][2]) + (point[2] * rot_mat[2][2])        
    ]

    return out # return the new rotated point

# rotate a point about the x axis by theta degrees
def rot_x(point, theta):
    sint = math.sin(math.radians(theta))
    cost = math.cos(math.radians(theta))

    rot_mat = [ # basic x axis rotation matrix
        [
            1, 0, 0
        ], [
            0, cost, sint
        ], [
            0, -sint, cost
        ]
    ]

    out = [ # multiply the point by the matrix
        (point[0] * rot_mat[0][0]) + (point[1] * rot_mat[1][0]) + (point[2] * rot_mat[2][0]),
        (point[0] * rot_mat[0][1]) + (point[1] * rot_mat[1][1]) + (point[2] * rot_mat[2][1]),
        (point[0] * rot_mat[0][2]) + (point[1] * rot_mat[1][2]) + (point[2] * rot_mat[2][2])        
    ]

    return out # return the new rotated point


# rotate a point about the y axis by theta degrees
def rot_y(point, theta):
    sint = math.sin(math.radians(theta))
    cost = math.cos(math.radians(theta))

    rot_mat = [ # basic y axis rotation matrix
        [
            cost, 0, -sint
        ], [
            0, 1, 0
        ], [
            sint, 0, cost
        ]
    ]

    out = [ # multiply the point by the matrix
        (point[0] * rot_mat[0][0]) + (point[1] * rot_mat[1][0]) + (point[2] * rot_mat[2][0]),
        (point[0] * rot_mat[0][1]) + (point[1] * rot_mat[1][1]) + (point[2] * rot_mat[2][1]),
        (point[0] * rot_mat[0][2]) + (point[1] * rot_mat[1][2]) + (point[2] * rot_mat[2][2])        
    ]

    return out # return the new rotated point