##############################
# MSIII_Constellation.py
# Author: Elijah Sakamoto
# Documentation: None
##############################


from MSIII_Orbit import MSIII_Orbit
from MSIII_useful_consts import *
from MSIII_Components import *
from CoolGeometry import rot_x, rot_y, rot_z, shoot_astro_ray
from MSIII_Constraints import MSIII_Budget_Summary, MSIII_Coverage_Summary, MSIII_Orbit_Viability_Summary
from MSIII_Constraints import MSIII_Comprehensive_Constellation_Summary, MSIII_Concise_Constellation_Summary
from MSIII_Constraints import MSIII_Volume_Summary, MSIII_Visitation_Summary
from Formula_Sheet import assess_camera_adcs_compatibility, get_payload_max_height
from pretty_outputs import indent_section
import math
import random

class MSIII_Satellite:
    def __init__(self, sat_obj=None):
        if sat_obj == None:
            print("Using default satellite constructor, make sure to add orbits.")
            self.orbit = None
            return
        
        self.orbit = MSIII_Orbit(
            a=sat_obj["a"],
            e=sat_obj["e"],
            i=sat_obj["i"],
            raan=sat_obj["raan"],
            w=sat_obj["w"],
            v=sat_obj["v"]
        )

class MSIII_Constellation:
    def __init__(self):
        print("Using default constructor. Kinda sus.")
        self.sats = []
        for i in range(NUM_SATS):
            self.sats.append(MSIII_Satellite())
            
        self.payload = PAYLOADS[0]
        self.structure = STRUCTURES[0]
        self.adcs = ADCS[0]

    def __init__(self, constellation_dict):
        self.payload = constellation_dict["payload"]
        self.structure = constellation_dict["structure"]
        self.adcs = constellation_dict["adcs"]

        self.sats = []
        for sat in constellation_dict["sats"]: # initialize all the satellites
            self.sats.append(MSIII_Satellite(sat))
            
            
    def assess_budget(self) -> MSIII_Budget_Summary: # create an object representing adherence to the budget
        total_estimated_cost = 0
        total_certain_cost = 0
        
        for sat in self.sats: # factor in the costs of the satellites
            total_estimated_cost += self.payload["cost"]
            total_estimated_cost += self.adcs["cost"]
            total_estimated_cost += self.structure["cost"]

            total_certain_cost += self.payload["cost"]
            total_certain_cost += self.adcs["cost"]
            total_certain_cost += self.structure["cost"]
            

            # factor in typical costs for components we are not yet factoring in
            total_estimated_cost += AVERAGE_ANTENNA_COST 
            total_estimated_cost += AVERAGE_ELECTRICAL_COST
            total_estimated_cost += AVERAGE_PROPULSION_COST

        return MSIII_Budget_Summary(total_estimated_cost, total_certain_cost)
    
    def assess_coverage(self) -> MSIII_Coverage_Summary:
        # if we cannot point at the things we want to, we cannot consistently see anything
        cam_adcs_compatibility = assess_camera_adcs_compatibility(self.payload, self.adcs)

        system_period = DAY_AS_SECONDS # the time it should take the whole system to return to 
        # the system period is just 24 hours now because we are assuming geosynchronous orbits
        # this collapses the solution space and simplifies computations because they are all in 
        # sync

        time_interval = system_period / POSITIONAL_TESTING_RESOLUTION # time interval to check by

        total_points_checked = 0 # track the amount of points we check
        total_points_in_los_and_range = 0 # track how many times we see them when we check
        total_points_in_los = 0 # track how many times they are in los
        total_points_in_range = 0 # track how many times they are in range
        closest_approach = float("inf") # set the closest approach to infinity

        vision_range = get_payload_max_height(self.payload, MIN_RESOLUTION)



        target_points_t0 = [] # to store the position of the target points at t=0 in ijk coords
        for i in range(len(POINTS_OF_INTEREST)):
            point_of_interest = [R_EARTH + 5, 0, 0] # initialize the point of interest to R_Earth, 0, 0
            
            # rotate it around to get it in the right spot
            point_of_interest = rot_y(point_of_interest, -POINTS_OF_INTEREST[i][0]) 
            point_of_interest = rot_z(point_of_interest, POINTS_OF_INTEREST[i][1] - INTIAL_EARTH_POS)
            target_points_t0.append(point_of_interest)

        for i in range(POSITIONAL_TESTING_RESOLUTION):
            # we add random noise to the timestamps to check to prevent aliasing
            t = (time_interval * i) + random.uniform(-POSITIONAL_TESTING_TIME_FUDGE, 
                                                    POSITIONAL_TESTING_TIME_FUDGE)
            
            target_points_t = [] # track the positions of the points of interest at time t
            delta_angle = EARTH_ROTATION_PER_SEC * (t % DAY_AS_SECONDS) # we just assume it rotates once a day
            # this is not necessarily true, but it is a nice simplification
            
            for point in target_points_t0:
                target_points_t.append(rot_z(point, delta_angle)) # rotate it however much the Earth has turned

            sat_pos_t = [] # track the positions of all the satellites at time t
            for sat in self.sats:
                sat : MSIII_Satellite # type annotation, ignore
                sat_pos_t.append(sat.orbit.get_position_at_time(t))


            # now that we have computed their positions, we can ==============================
            # actually check whether we can see the points at this timestamp =================

            for point in target_points_t: # loop over all the target points
                total_points_checked += 1 # update our first counter
                can_see = False
                in_los = False
                in_range = False
                for sat in sat_pos_t:
                    los_dist = shoot_astro_ray(sat, point)
                    # check that we have los (los_dist != -1) and that it is in range
                    can_see = can_see or ((los_dist != -1) and (los_dist < vision_range))
                    in_los = in_los or (los_dist != -1)
                    in_range = in_range or (math.dist(sat, point) < vision_range)
                    closest_approach = min(closest_approach, math.dist(sat, point))

                if (can_see):
                    total_points_in_los_and_range += 1 # update our seen counter
                if (in_los):
                    total_points_in_los += 1 # update our los counter
                if (in_range):
                    total_points_in_range += 1 # update our range counter

        return MSIII_Coverage_Summary(cam_adcs_compatibility, total_points_in_los_and_range, 
                                     total_points_in_los, total_points_in_range, 
                                     total_points_checked, closest_approach)
        
    def assess_visitation(self) -> MSIII_Coverage_Summary:
        # if we cannot point at the things we want to, we cannot consistently see anything
        cam_adcs_compatibility = assess_camera_adcs_compatibility(self.payload, self.adcs)

        system_period = DAY_AS_SECONDS # the time it should take the whole system to return to 
        # the system period is just 24 hours now because we are assuming geosynchronous orbits
        # this collapses the solution space and simplifies computations because they are all in 
        # sync

        time_interval = system_period / POSITIONAL_TESTING_RESOLUTION # time interval to check by

        total_visits = 0
        sight_tracker = []
        for point in POINTS_OF_INTEREST:
            sight_tracker.append(False)

        vision_range = get_payload_max_height(self.payload, MIN_RESOLUTION)



        target_points_t0 = [] # to store the position of the target points at t=0 in ijk coords
        for i in range(len(POINTS_OF_INTEREST)):
            point_of_interest = [R_EARTH + 5, 0, 0] # initialize the point of interest to R_Earth, 0, 0
            
            # rotate it around to get it in the right spot
            point_of_interest = rot_y(point_of_interest, -POINTS_OF_INTEREST[i][0]) 
            point_of_interest = rot_z(point_of_interest, POINTS_OF_INTEREST[i][1] - INTIAL_EARTH_POS)
            target_points_t0.append(point_of_interest)

        for i in range(POSITIONAL_TESTING_RESOLUTION):
            # we add random noise to the timestamps to check to prevent aliasing
            t = (time_interval * i) + random.uniform(-POSITIONAL_TESTING_TIME_FUDGE, 
                                                    POSITIONAL_TESTING_TIME_FUDGE)
            
            target_points_t = [] # track the positions of the points of interest at time t
            delta_angle = EARTH_ROTATION_PER_SEC * (t % DAY_AS_SECONDS) # we just assume it rotates once a day
            # this is not necessarily true, but it is a nice simplification
            
            for point in target_points_t0:
                target_points_t.append(rot_z(point, delta_angle)) # rotate it however much the Earth has turned

            sat_pos_t = [] # track the positions of all the satellites at time t
            for sat in self.sats:
                sat : MSIII_Satellite # type annotation, ignore
                sat_pos_t.append(sat.orbit.get_position_at_time(t))


            # now that we have computed their positions, we can ==============================
            # actually check whether we can see the points at this timestamp =================

            point_index = -1 # keep track of which point we are on
            for point in target_points_t: # loop over all the target points
                point_index += 1 # increment upool
                can_see = False
                in_los = False
                in_range = False
                for sat in sat_pos_t:
                    los_dist = shoot_astro_ray(sat, point)
                    # check that we have los (los_dist != -1) and that it is in range
                    can_see = can_see or ((los_dist != -1) and (los_dist < vision_range))
                    in_los = in_los or (los_dist != -1)
                    in_range = in_range or (math.dist(sat, point) < vision_range)

                # whenevery our vision status changes for this point
                if (can_see != sight_tracker[point_index]): 
                    if (can_see):
                        # we entered another vision window!
                        total_visits += 1
                    sight_tracker[point_index] = can_see # update our tracker

        return MSIII_Visitation_Summary(float(total_visits) / float(len(POINTS_OF_INTEREST)))

    
    # check if there is anything goofy with our orbits that would make them unviable
    def assess_orbit_viability(self): 
        orbit_tests = [] # to keep track of each orbit's viability (there are 3 of them)

        for sat in self.sats:
            sat : MSIII_Satellite # type annotation, ignore
            this_test = {}
            this_orbit = sat.orbit

            # these are from formula sheet
            this_test["min_alt"] = (this_orbit.a * (1 - this_orbit.e)) - R_EARTH 
            this_test["max_alt"] = (this_orbit.a * (1 + this_orbit.e)) - R_EARTH

            this_test["no_crash"] = (this_test["min_alt"] > 0) # doesn't just hit the earth

            # can assume no drag
            this_test["avoids_drag"] = (this_test["min_alt"] > MIN_DRAGLESS_ALTITUDE)

            # an orbit is catastrophic if it degrades too much or crashes into Earth
            this_test["is_catastrophic"] = not (this_test["no_crash"] and this_test["avoids_drag"])

            # being almost geosynchronous is a perk we like, because it makes computations
            # easier and approximations more accurate (less timestamps to simulate because 
            # the combined period is shorter)
            this_test["geosynchronous"] = abs(this_orbit.period - DAY_AS_SECONDS) < 10

            orbit_tests.append(this_test)

        return MSIII_Orbit_Viability_Summary(orbit_tests) # put it in a nice organized report

    def assess_volume(self):
        return MSIII_Volume_Summary(self.payload, self.structure)

    def get_concise_summary(self):
        orbit_summary = self.assess_orbit_viability()
        budget_summary = self.assess_budget()
        volume_summary = self.assess_volume()
        return MSIII_Concise_Constellation_Summary(orbit_summary, budget_summary, volume_summary)
    
    def get_comprehensive_summary(self):
        orbit_summary = self.assess_orbit_viability()
        budget_summary = self.assess_budget()
        cover_summary = self.assess_coverage()
        volume_summary = self.assess_volume()
        visitation_summary = self.assess_visitation()

        return MSIII_Comprehensive_Constellation_Summary(orbit_summary,
                                                        budget_summary,
                                                        cover_summary, 
                                                        volume_summary,
                                                        visitation_summary)
    

    def to_string(self, const_name=""):
        output_str = ""
        output_str += f"Constellation {const_name}:\n"
        output_str += f"\tPayload:   {self.payload["name"]}\n"
        output_str += f"\tStructure: {self.structure["name"]}\n"
        output_str += f"\tADCS:      {self.adcs["name"]}\n"

        for sat in self.sats:
            output_str += indent_section(sat.orbit.to_string(), 1)

        return output_str

    def simulate(self, delta_t): # advance the whole constellation by delta_t seconds
        for sat in self.sats:
            sat.orbit.simulate(delta_t)
