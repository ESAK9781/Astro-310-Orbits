
########### Physical / Mathematical Constants ##########
MIU = 398600.5 # km^3 s^-2
R_EARTH = 6378.137 # km
DAY_AS_SECONDS = 24 * 60 * 60 # s
EARTH_ROTATION_PER_SEC = 360 / DAY_AS_SECONDS # deg/sec
MIN_DRAGLESS_ALTITUDE = 600 # how many km to stay above Earth to avoid drag perturbations
GEOSYNCHRONOUS_SEMIMAJOR_AXIS = 42241.09773 # a necessary to have ~24 hour period


########### Project Specifications ###################
TOTAL_DEV_BUDGET = 225000000 # $
MISSION_OP_COST = 8000000 # $
COST_BUFFER_MARGIN = 1.1 # factor to multiply estimated costs by for margin

MIN_CROSSLINK = 14 # db

NUM_SATS = 3

POINTS_OF_INTEREST = [ # [deg N, deg E]
    [53, 33.45], # Pochep
    [53.25, 34.3], # Bryansk
    [48.7, 44.45], # Volgograd
    [48.35, 43.7] # Krepinskii
]

PAYLOADS = [
    { # Astra Hi-Res Imager
        "name": "Astra Hi-Res Imager",
        "min_wl": 0.00000038, # m
        "max_wl": 0.00000075, # m
        "det_rad": 0.15, # m
        "fl": 4, # m
        "aperture": 1.2, # m
        "hor_pix": 30000, # pixels
        "vert_pix": 500, # pixels
        "bit_pix": 12, # bits/pixel
        "length": 2, # m
        "width": 1.5, # m
        "height": 3, # m
        "tot_mass": 200, # kg
        "tot_pow": 225, # W
        "cost": 31000000, # $
        "delivery": 12 # months
    }, { # SpaceCam 42
        "name": "SpaceCam 42",
        "min_wl": 0.00000045, # m
        "max_wl": 0.00000075, # m
        "det_rad": 0.06, # m
        "fl": 1, # m
        "aperture": 1.1, # m
        "hor_pix": 13000, # pixels
        "vert_pix": 800, # pixels
        "bit_pix": 16, # bits/pixel
        "length": 1.5, # m
        "width": 1, # m
        "height": 2, # m
        "tot_mass": 125, # kg
        "tot_pow": 185, # W
        "cost": 22000000, # $
        "delivery": 10 # months
    }, { # Dragonfly Imager
        "name": "Dragonfly Imager",
        "min_wl": 0.00000035, # m
        "max_wl": 0.00000080, # m
        "det_rad": 0.12, # m
        "fl": 2.5, # m
        "aperture": 0.9, # m
        "hor_pix": 35000, # pixels
        "vert_pix": 500, # pixels
        "bit_pix": 12, # bits/pixel
        "length": 1, # m
        "width": 1, # m
        "height": 2, # m
        "tot_mass": 100, # kg
        "tot_pow": 190, # W
        "cost": 18000000, # $
        "delivery": 10 # months
    }, { # Tiny Cam
        "name": "Tiny Cam",
        "min_wl": 0.00000050, # m
        "max_wl": 0.00000070, # m
        "det_rad": 0.04, # m
        "fl": 1, # m
        "aperture": 0.6, # m
        "hor_pix": 35000, # pixels
        "vert_pix": 1000, # pixels
        "bit_pix": 10, # bits/pixel
        "length": 0.6, # m
        "width": 0.6, # m
        "height": 0.6, # m
        "tot_mass": 25, # kg
        "tot_pow": 75, # W
        "cost": 5000000, # $
        "delivery": 3 # months
    }
]

MIN_RESOLUTION = 4 # smallest feature we need to see

# collected from BORG simulation
INTIAL_EARTH_POS = 18.6 # initial longitude in deg of i vector at t=0

############## Learning Parameters ##########

ANGLE_FUDGE_FACTOR = 90 # degree standard deviation for picking new angular parameters 
# with gaussian distribution at full learn rate

SEMIMAJOR_AXIS_FUDGE_FACTOR = R_EARTH # standard deviation for picking new semimajor axis with
# gaussian distribution at full learn rate

ECCENTRICITY_FUDGE_FACTOR = 0.5 # standard deviation for picking new semimajor axis with gaussian
# distribution at full learn rate


# a little more difficult to explain. The number of different timestamps the program will check
# a constellation for in order to ensure proper coverage
POSITIONAL_TESTING_RESOLUTION = 100

POSITIONAL_TESTING_TIME_FUDGE = 5*60 # a maximum 5 minute fudge factor that is added to the 
# testing times in order to prevent aliasing of any sort



################ Raymarching Algorithm Parameters ########################
MIN_MARCH_DIST = 0.1

################ Optimization Controls ####################################
MAX_E_ITERATIONS = 150 # max iterations when calculating E from M