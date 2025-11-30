##############################
# MSIII_Constraints.py
# Author: Elijah Sakamoto
# Documentation: None
##############################


from MSIII_useful_consts import *
from pretty_outputs import indent_section

'''
Some useful wrapper classes for test outputs, just to make sure
'''

class MSIII_Budget_Summary:
    def __init__(self, total_expected_cost, total_certain_cost):
        self.cost = total_expected_cost
        self.cost_with_margin = total_expected_cost * COST_BUFFER_MARGIN
        self.budget = TOTAL_DEV_BUDGET
        self.meets_budget = (self.cost < self.budget)
        self.meets_budget_with_margin = (self.cost_with_margin < self.budget)
        self.total_certain_cost = total_certain_cost
        self.remaining_cash = (self.budget / COST_BUFFER_MARGIN) - self.total_certain_cost
        
    def to_string(self, constellation_name=""): # just formats everything nice and pretty
        output_string = ""
        output_string += f"Constellation {constellation_name} Budgeting:\n"
        output_string += f"\tMargin Meets Budget:  {self.meets_budget_with_margin}\n"
        output_string += f"\tCertain Cost:        ${self.total_certain_cost}\n"
        output_string += f"\tEst. Cost:           ${self.cost}\n"
        output_string += f"\tCost With Margin:    ${self.cost_with_margin}\n"
        output_string += f"\tBudget:              ${self.budget}\n"
        output_string += f"\tMeets Budget:         {self.meets_budget}\n"
        output_string += f"\tUnallocated Money:   ${self.remaining_cash}\n"
        return output_string
    


class MSIII_Coverage_Summary:
    def __init__(self, adcs_cam_compatible, points_in_los_range,
                 points_in_los, points_in_range, points_checked, closest_approach):
        self.adcs_cam_compatible = adcs_cam_compatible
        self.points_in_los_range = points_in_los_range
        self.points_in_los = points_in_los
        self.points_in_range = points_in_range
        self.points_checked = points_checked
        self.closest_approach = closest_approach
        self.percent_coverage = points_in_los_range / points_checked # percentage of points we saw
        if (not adcs_cam_compatible):
            self.percent_coverage = 0 # yeah, we probably cant actually see anything
    
    def to_string(self, constellation_name=""): # just formats everything nice and pretty
        output_string = ""
        output_string += f"Constellation {constellation_name} Point Coverage:\n"
        output_string += f"\tCan Point Within SW:     {self.adcs_cam_compatible}\n"
        output_string += f"\t% Coverage:              {self.percent_coverage}%\n"
        output_string += f"\tPoints Sampled:          {self.points_checked}\n"
        output_string += f"\tPoints in range and LOS: {self.points_in_los_range}\n"
        output_string += f"\tPoints in range:         {self.points_in_range}\n"
        output_string += f"\tPoints in LOS:           {self.points_in_los}\n"
        output_string += f"\tClosest Approach:        {self.closest_approach} km\n"
        return output_string
    
class MSIII_Visitation_Summary:
    def __init__(self, average_visitations : float):
        self.average_visitations = average_visitations
    
    def to_string(self, constellation_name=""):
        output_string = ""
        output_string += f"Constellation {constellation_name} Visitation Summary:\n"
        output_string += f"\tAverage visitations per day: {self.average_visitations}\n"
        return output_string


class MSIII_Orbit_Viability_Summary:
    def __init__(self, orbit_test_results):
        self.orbit_test_results = orbit_test_results
        self.viable_overall = True
        for test in orbit_test_results: # only viable overall if all orbits are viable
            self.viable_overall = self.viable_overall and (not test["is_catastrophic"])
    
    def to_string(self, constellation_name=""):
        viability_lable = "VIABLE"
        if (not self.viable_overall):
            viability_lable = "CATASTROPHIC"

        output_string = ""
        output_string += f"Constellation {constellation_name} Orbit Viability: {viability_lable}\n"
        for i in range(len(self.orbit_test_results)):
            orbit_summary_block = ""
            orbit_summary_block += f"ORBIT {i + 1}\n"
            
            this_test = self.orbit_test_results[i]
            orbit_summary_block += f"\tCATASTROPHIC?      {this_test["is_catastrophic"]}\n"
            orbit_summary_block += f"\tDRAGLESS?          {this_test["avoids_drag"]}\n"
            orbit_summary_block += f"\tCRASHLESS?         {this_test["no_crash"]}\n"
            orbit_summary_block += f"\tMax Altitude:      {this_test["max_alt"]} km\n"
            orbit_summary_block += f"\tMin Altitude:      {this_test["min_alt"]} km\n"
            orbit_summary_block += f"\tIs Geosynchronous: {this_test["geosynchronous"]}\n"

            output_string += indent_section(orbit_summary_block, 1)
        
        return output_string

class MSIII_Volume_Summary:
    def __init__(self, payload, structure):
        
        # create copies of both dimensions
        payload_dimensions = [payload["length"], payload["width"], payload["height"]]
        struct_dimensions = structure["internal volume"].copy()

        # sort each of the dimension lists (because they can be rotated in any direction)
        payload_dimensions.sort()
        struct_dimensions.sort()

        # check that each dimension fits
        payload_fits = True # assume it does, until proven otherwise
        for i in range(len(payload_dimensions)):
            if (payload_dimensions[i] > struct_dimensions[i]):
                payload_fits = False
                break # we have seen enough, it does not fit
        
        self.payload_fits = payload_fits
        self.used_volume = payload_dimensions[0] * payload_dimensions[1] * payload_dimensions[2]
        self.total_volume = struct_dimensions[0] * struct_dimensions[1] * struct_dimensions[2]
        self.remaining_volume = self.total_volume - self.used_volume

    def to_string(self, constellation_name=""):
        output_string = ""
        output_string += f"Constellation {constellation_name} Volume Summary:\n"
        output_string += f"\tPayload Fits:     {self.payload_fits}\n"
        output_string += f"\tAvailable Volume: {self.total_volume} m^3\n"
        output_string += f"\tUsed Volume:      {self.used_volume} m^3\n"
        output_string += f"\tRemaining Volume: {self.remaining_volume} m^3\n"

        return output_string

class MSIII_Concise_Constellation_Summary:
    def __init__(self, orbit : MSIII_Orbit_Viability_Summary, budget : MSIII_Budget_Summary,
                 volume : MSIII_Volume_Summary):
        self.meets_budget = budget.meets_budget_with_margin
        self.is_viable = orbit.viable_overall
        self.in_volume = volume.payload_fits
        self.passes_inspection = self.meets_budget and self.is_viable and self.in_volume
    
    def to_string(self, constellation_name=""):
        output_string = ""
        output_string += f"Constellation {constellation_name} Concise Summary:\n"
        output_string += f"\tPasses:       {self.passes_inspection}\n"
        output_string += f"\tIn Budget:    {self.meets_budget}\n"
        output_string += f"\tViable Orbit: {self.is_viable}\n"
        output_string += f"\tVolume Fits:  {self.in_volume}\n"


        return output_string
    
class MSIII_Comprehensive_Constellation_Summary:
    def __init__(self, orbit : MSIII_Orbit_Viability_Summary, budget: MSIII_Budget_Summary,
                 cover : MSIII_Coverage_Summary, volume : MSIII_Volume_Summary,
                 visitation : MSIII_Visitation_Summary):
        self.orbit = orbit
        self.budget = budget
        self.cover = cover
        self.volume = volume
        self.concise = MSIII_Concise_Constellation_Summary(self.orbit, self.budget, self.volume)
        self.visitation = visitation

    def to_string(self, constellation_name=""):
        output_string = ""
        output_string += f"Constellation {constellation_name} Comprehensive Summary: \n"
        output_string += indent_section(self.concise.to_string(constellation_name), 1)
        output_string += indent_section(self.orbit.to_string(constellation_name), 1)
        output_string += indent_section(self.budget.to_string(constellation_name), 1)
        output_string += indent_section(self.volume.to_string(constellation_name), 1)
        output_string += indent_section(self.visitation.to_string(constellation_name), 1)
        output_string += indent_section(self.cover.to_string(constellation_name), 1)

        return output_string