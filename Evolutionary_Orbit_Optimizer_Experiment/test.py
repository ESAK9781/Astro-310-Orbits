from Scoring import score_orbit
from OrbitAsSolution import Satellite, Const_Solution
from Orbit import Orbit
from useful_consts import *
from CoolGeometry import shoot_astro_ray



# create our Milestone 1 solution

orb_1 = Orbit(
    a=42241.09773,
    e=0.8348021861,
    i=50.825,
    raan=340.5,
    w=245,
    v=180
)

orb_2 = Orbit(
    a=42241.09773,
    e=0.8348021861,
    i=50.825,
    raan=100.5,
    w=245,
    v=154.5099795
)

orb_3 = Orbit(
    a=42241.09773,
    e=0.8348021861,
    i=50.825,
    raan=220.5,
    w=245,
    v=205.4900205
)

constellation = Const_Solution()
constellation.sats[0].orb = orb_1
constellation.sats[1].orb = orb_2
constellation.sats[2].orb = orb_3
constellation.payload = PAYLOADS[0] # pick a good one for now


score_orbit(constellation, 1)

# FINALLY! GOT IT TO WORK AS EXPECTED!

