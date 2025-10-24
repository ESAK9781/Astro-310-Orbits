'''
Just a nice place to put a bunch of formulas from / derived from the 
formula sheet that didn't fit anywhere else.
'''
import math
from MSII_useful_consts import MIU, R_EARTH, MAX_E_ITERATIONS

# convert hours to seconds
def h_to_sec(hours : float) -> float:
    return (hours * 60 * 60)

# convert km to meters
def km_to_m(km):
    return km * 1000

# take an imaging payload, use it to calculate the max height we can go to
def get_payload_max_height(payload, min_resolution_m):
    return ((payload["aperture"] * min_resolution_m) / (2.44 * 2.44 * payload["max_wl"])) / 1000


# checks that the adcs and camera will work together so we can capture what we aim at.
# derivation done / submitted on paper
def assess_camera_adcs_compatibility(payload, adcs):
    adcs_d_over_h = adcs["pointing accuracy"]
    cam_sw_over_h = (2 * payload["det_rad"]) / payload["fl"]

    return (adcs_d_over_h < cam_sw_over_h) # make sure the swath width is bigger than the pointing error


# takes a desired period (in seconds), converts it to a necessary semimajor axis
def period_to_axis(seconds : float):
    return (((seconds / (2 * math.pi)) ** 2) * MIU) ** (1/3) # derived from period formula

# directly from the formula sheet
# accepts height in meters
def get_payload_resolution(payload, height):
    return (2.44 * payload["max_wl"] * km_to_m(height)) / payload["aperture"]



# accepts a list of [deg N, deg E] pairs and gets the average latitude of them
def get_avg_latitude(points):
    total_lat = 0
    for point in points:
        total_lat += point[0]
    return total_lat / len(points)

# accepts a list of [deg N, deg E] pairs and gets the average longitude of them
def get_avg_longitude(points):
    total_lon = 0
    for point in points:
        total_lon += point[1]
    return total_lon / len(points)



# convert a desired h at apogee and a semimajor axis into an eccentricity
def apogee_h_to_e(semimajor_axis, apogee_h, check_e_vals=True):
    apogee_r = apogee_h + R_EARTH
    # use r_a = a(1+e) to solve for e
    e_solution = (apogee_r / semimajor_axis) - 1
    
    if (check_e_vals):
        assert(e_solution > 0) # make sure nothing funky is going on (i.e. invalid solutions)
        assert(e_solution < 1)
    else:
        e_solution = max(min(e_solution, 0.9999), 0.0001)
    
    return e_solution

# use orbit prediction techniques from class to compute the intial v we would need in order to 
# hit apogee at time=time_on_target
def calc_v_at_t0_to_hit_apogee_at_t(semimajor_axis, e, time_on_target):
    n = math.sqrt(MIU / math.pow(semimajor_axis, 3)) # calc n, direct from formula sheet
    tof = time_on_target # time of flight
    vf = math.radians(180) # hit apogee at t_final
    ef = math.acos((e + math.cos(vf)) / (1 + e * math.cos(vf))) # direct from formula sheet
    if (vf > math.pi): # double angle check
        ef = (math.pi * 2) - ef
    
    mf = ef - e * math.sin(ef)
    mi = mf - n * tof # derived from formula sheet
    while (mi < 0): # add back 2pi until mi becomes positive again (based on -2kpi from formula sheet)
        mi += 2 * math.pi 
    
    # E = M + e*sin(E), iterate. From the formula sheet
    ei = mi + e * math.sin(mi)
    for i in range(MAX_E_ITERATIONS):
        ei = mi + e * math.sin(ei) # iterate like we learned in class
    
    vi = math.acos((math.cos(ei) - e) / (1 - e * math.cos(ei)))
    
    # double angle check
    if (ei > math.pi):
        vi = (math.pi * 2) - ei
        
    return math.degrees(vi) # return the initial v in degrees


# use orbit prediction techniques from class to compute the intial v we would need in order to 
# hit perigee at time=time_on_target
def calc_v_at_t0_to_hit_perigee_at_t(semimajor_axis, e, time_on_target):
    n = math.sqrt(MIU / math.pow(semimajor_axis, 3)) # calc n, direct from formula sheet
    tof = time_on_target # time of flight
    vf = math.radians(0) # hit apogee at t_final
    ef = math.acos((e + math.cos(vf)) / (1 + e * math.cos(vf))) # direct from formula sheet
    if (vf > math.pi): # double angle check
        ef = (math.pi * 2) - ef
    
    mf = ef - e * math.sin(ef)
    mi = mf - n * tof # derived from formula sheet
    while (mi < 0): # add back 2pi until mi becomes positive again (based on -2kpi from formula sheet)
        mi += 2 * math.pi 
    
    # E = M + e*sin(E), iterate. From the formula sheet
    ei = mi + e * math.sin(mi)
    for i in range(MAX_E_ITERATIONS):
        ei = mi + e * math.sin(ei) # iterate like we learned in class
    
    vi = math.acos((math.cos(ei) - e) / (1 - e * math.cos(ei)))
    
    # double angle check
    if (ei > math.pi):
        vi = (math.pi * 2) - ei
        
    return math.degrees(vi) # return the initial v in degrees


# convert a desired h at perigee and a semimajor axis into an eccentricity
def perigee_h_to_e(semimajor_axis, perigee_h, check_e_vals=True):
    perigee_r = perigee_h + R_EARTH
    # use r_p = a(1-e) to solve for e
    e_solution = -((perigee_r / semimajor_axis) - 1)
    
    if (check_e_vals):
        assert(e_solution > 0) # make sure nothing funky is going on (i.e. invalid solutions)
        assert(e_solution < 1)
    else:
        e_solution = max(min(e_solution, 0.9999), 0.0001)
    
    return e_solution