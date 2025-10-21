
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
MIN_LIFETIME = 5 # minimum lifetime in years of the constellation
MIN_CROSSLINK = 14 # db
MONTHS_TO_ILC = 36 # months until we need to be able to launch
MISSION_OPS_COST = 8000000 # dollars per year

NUM_SATS = 3

POINTS_OF_INTEREST = [ # [deg N, deg E]
    [53, 33.45], # Pochep
    [53.25, 34.3], # Bryansk
    [48.7, 44.45], # Volgograd
    [48.35, 43.7] # Krepinskii
]



MIN_RESOLUTION = 4 # smallest feature we need to see in meters

# collected from BORG simulation
INTIAL_EARTH_POS = 18.6 # initial longitude in deg of i vector at t=0

############## Grading Parameters ##########

# a little more difficult to explain. The number of different timestamps the program will check
# a constellation for in order to ensure proper coverage
POSITIONAL_TESTING_RESOLUTION = 100

POSITIONAL_TESTING_TIME_FUDGE = 5*60 # a maximum 5 minute fudge factor that is added to the 
# testing times in order to prevent aliasing of any sort



################ Raymarching Algorithm Parameters ########################
MIN_MARCH_DIST = 0.1

################ Optimization Controls ####################################
MAX_E_ITERATIONS = 150 # max iterations when calculating E from M