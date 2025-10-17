'''

This is where the magic happens! We don't actually need to figure out what the perfect orbit looks
like, we just need to figure out how to detect one. If something is important to us about an 
orbit, we can just write a way to measure that and factor it into the scoring function!

Behold, the beauty of Machine Learning!

'''

from Orbit import Orbit
from OrbitAsSolution import Const_Solution, Satellite
from useful_consts import *
from CoolGeometry import shoot_astro_ray, rot_x, rot_y, rot_z
import math
import random

# scores the coverage of the constellation of the target points from 0 to 1 (highest coverage) by far the most computationally intensive
def coverage_metric(con : Const_Solution):
    system_period = DAY_AS_SECONDS # the time it should take the whole system to return to 
    # the same state (all sats + earth in the same place)
    for sat in con.sats: # multiply by period of each satellite
        sat : Satellite # type annotation, ignore
        system_period *= sat.orb.period

    time_interval = system_period / POSITIONAL_TESTING_RESOLUTION # time interval to check by

    total_points_checked = 0 # track the amount of points we check
    total_points_seen = 0 # track how many times we see them when we check


    target_points_t0 = [] # to store the position of the target points at t=0 in ijk coords
    for i in range(len(POINTS_OF_INTEREST)):
        poi = [R_EARTH * 1.25, 0, 0] # initialize the point of interest to R_Earth, 0, 0
        poi = rot_y(poi, math.radians(-POINTS_OF_INTEREST[i][0]))
        poi = rot_z(poi, math.radians(POINTS_OF_INTEREST[i][1] - INTIAL_EARTH_POS))
        target_points_t0.append(poi)

    for i in range(POSITIONAL_TESTING_RESOLUTION):
        t = (time_interval * i) + random.uniform(-POSITIONAL_TESTING_TIME_FUDGE, 
                                                 POSITIONAL_TESTING_TIME_FUDGE)
        
        poi_t = [] # track the positions of the points of interest at time t
        delta_angle = math.radians(EARTH_ROTATION_PER_SEC * (t % DAY_AS_SECONDS)) # we just assume it rotates once a day
        for p in target_points_t0:
            poi_t.append(rot_z(p, delta_angle)) # rotate it however much the Earth has turned

        sat_pos_t = [] # track the positions of all the satellites at time t
        for sat in con.sats:
            sat_pos_t.append(sat.orb.get_position_at_time(t))


        # calculate the sensor range for this constellation, dev by 1000 to get km
        sens_rang = (con.payload["aperture"] * MIN_RESOLUTION) / (2.44 * con.payload["min_wl"]) / 1000

        for p in poi_t:
            total_points_checked += 1 # we are checking another point
            for sp in sat_pos_t:
                ray_dist = shoot_astro_ray(sp, p)
                # if we see it (i.e. != 0) and can sense it (i.e. not out of range)
                if (0 < ray_dist < sens_rang): 
                    total_points_seen += 1
                    break # the point is covered, no need for another check
    
    return total_points_seen / total_points_checked # return the average percentage of the time we see each point
        
# returns 1 if meets budget, 0 if does not
def check_cost_requirement(con : Const_Solution):
    tot_cost = 0
    tot_cost += 3 * con.payload["cost"]
    # factor in other costs...


    tot_cost *= COST_BUFFER_MARGIN
    if (tot_cost > TOTAL_DEV_BUDGET):
        return 0
    return 1


# return 1 if it doesn't crash, 0 if it probably will
def check_doesnt_crash_requirement(con : Const_Solution):
    for sat in con.sats:
        orb : Orbit = sat.orb
        r_perigee = orb.a * (1 - orb.e)
        if (r_perigee < R_EARTH + MIN_DRAGLESS_ALTITUDE): # check if it goes too low at perigee
            return 0
    return 1 # if all of the satellites stay high enough

# incentivize eccentric orbits because they have more coverage (usually)
def eccentricity_incentive_metric(con : Const_Solution):
    tot_e = 0
    for sat in con.sats:
        orb : Orbit = sat.orb
        tot_e += orb.e
    
    return tot_e / len(con.sats) # return the average eccentricity

# score how geosynchronous something is based off semimajor axis
# useful because decreases phase shifting and unsynchronized orbits
def geosync_incentive_metric(con : Const_Solution):
    tot_error = 0
    for sat in con.sats:
        orb : Orbit = sat.orb
        tot_error += abs(GEOSYNCHRONOUS_SEMIMAJOR_AXIS - orb.a)
    avg_error = tot_error / len(con.sats)
    
    return math.exp(-0.00001 * avg_error) # gradually go from 1 at avg_error = 0, all the way to 0 at higher error


def self_sync_metric(con : Const_Solution):
    tot_diff = 0
    for i in range(len(con.sats)):
        for j in range(len(con.sats)):
            if (i == j):
                continue
            tot_diff += abs(con.sats[i].orb.a - con.sats[j].orb.a)
    avg_diff = tot_diff / 3
    return math.exp(-0.00001 * avg_diff)



# returns the total composite score of the constellation
def score_constellation(con : Const_Solution, verbosity=0):
    
    scoring_method = { # represented as object to easily add new metric + requirements
        "requirements": [ # requirements have to be 1, or the whole score becomes 0
            ("cost", check_cost_requirement), # name, method
            ("no crash", check_doesnt_crash_requirement)
        ],
        "metrics": [ # metrics score performance and are weighted by importance
            ("coverage", coverage_metric, 100), # name, method, weight
            ("e incentive", eccentricity_incentive_metric, 10),
            ("geo sync", geosync_incentive_metric, 10),
            ("self sync", self_sync_metric, 20)
        ]
    }



    if (verbosity > 0):
        print("Solution Score: ")
        

    requirement_composite = 1
    metric_composite = 0

    if (verbosity > 0):
        print("\tRequirement Scores:")
    for layer in scoring_method["requirements"]:
        layer_score = layer[1](con)
        if (verbosity > 0):
            print("\t\t" + layer[0] + " : " + str(layer_score))
        requirement_composite *= layer_score # multiply together so one failed requirement can zero out the score

    if (verbosity > 0):
        print("\tRequirement Composite : " + str(requirement_composite))
        print("\tMetric Scores:")

    total_metric_weights = 0
    for met in scoring_method["metrics"]:
        total_metric_weights += met[2]
    metric_normalization_factor = 1 / total_metric_weights

    for met in scoring_method["metrics"]:
        metric_score = met[1](con)
        if (verbosity > 0):
            print("\t\t" + met[0] + " : " + str(metric_score))
        metric_composite += metric_score * met[2] * metric_normalization_factor # factor in the relative weights

    composite_score = requirement_composite * metric_composite
    if (verbosity > 0):
        print("\tMetric Composite : " + str(metric_composite))
        print("Overall Score: " + str(composite_score))
    
    return composite_score