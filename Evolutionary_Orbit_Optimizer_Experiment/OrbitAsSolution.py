from Optimizer import OptimizeableSolution
from Orbit import Orbit
import random
from useful_consts import *


class Satellite:
    def __init__(self):
        # design a random orbit based on acceptable ranges for each COE
        self.orb = Orbit(
            a=random.uniform(R_EARTH + 600, 5 * R_EARTH),
            e=random.uniform(0, 1),
            i=random.uniform(0, 180),
            raan=random.uniform(0, 360),
            w=random.uniform(0, 360),
            v=0 # true anomaly always starts at 0
        )
        
        self.orb.recomp_meta_vars()

    def get_copy(self):
        out = Satellite()
        out.orb.a = self.orb.a
        out.orb.e = self.orb.e
        out.orb.i = self.orb.i
        out.orb.raan = self.orb.raan
        out.orb.w = self.orb.w
        out.orb.v = self.orb.v
        out.orb.recomp_meta_vars()
        return out

    
    def get_fudged(self, fudge_factor):
        out = Satellite()
        out.orb.a = random.gauss(self.orb.a, fudge_factor * SEMIMAJOR_AXIS_FUDGE_FACTOR)
        out.orb.e = max(min(random.gauss(self.orb.e, fudge_factor * ECCENTRICITY_FUDGE_FACTOR), 0.9999), 0.0001) # pin it between 0 and 1, while keeping elliptical
        out.orb.raan = random.gauss(self.orb.raan, fudge_factor * ANGLE_FUDGE_FACTOR)
        out.orb.w = random.gauss(self.orb.w, fudge_factor * ANGLE_FUDGE_FACTOR)
        out.orb.v = 0 # keep initial v at 0 for simplicity

        # 0.5 bc only 0-180
        out.orb.i = random.gauss(self.orb.i, fudge_factor * ANGLE_FUDGE_FACTOR * 0.5) 
        
        out.orb.recomp_meta_vars()
        return out
    
    # makes a child satellite that is the exact average of both its parents
    def make_child(self, other_satellite):
        out = Satellite()
        out.orb.a = (self.orb.a + other_satellite.orb.a) / 2
        out.orb.e = (self.orb.e + other_satellite.orb.e) / 2
        out.orb.i = (self.orb.i + other_satellite.orb.i) / 2
        out.orb.raan = (self.orb.raan + other_satellite.orb.raan) / 2
        out.orb.w = (self.orb.w + other_satellite.orb.w) / 2
        out.orb.v = (self.orb.v + other_satellite.orb.v) / 2
        
        out.orb.recomp_meta_vars()
        return out

# an extension of the OptimizeableSolution class to represent an entire constellation
class Const_Solution(OptimizeableSolution):
    def __init__(self):
        self.sats = []
        for i in range(NUM_SATS):
            self.sats.append(Satellite())

        self.payload = random.choice(PAYLOADS)
    
    def getRandomSolution(self):
        return Const_Solution()
    
    def fudgeSelf(self, fudge_factor):
        for sat in self.sats: # mutate each of the satellites
            sat = sat.get_fudged(fudge_factor)
        
        if (random.uniform(0, 1) < fudge_factor): # with a fudge_factor % chance, mutate the payload
            self.payload = random.choice(PAYLOADS)
    
    # create a new solution that is the old sulution randomly fudged a bit
    def fudgeSolution(self, fudge_factor):
        out = Const_Solution()
        out.sats = [] # clear the satellites
        for sat in self.sats: # mutate each of the satellites
            out.sats.append(sat.get_fudged(fudge_factor))

        if (random.uniform(0, 1) < fudge_factor): # possibly mutate the payload
            out.payload = random.choice(PAYLOADS)

        return out
    
    # create new solutions based on two parents
    def makeBabies(self, other_parent, fudge_factor, count, include_parents=True):
        out = []
        if (include_parents):
            out.append(self)
            out.append(other_parent)
        
        # a child that is the exact midpoint between the two solutions
        average_child = Const_Solution()
        for i in range(NUM_SATS): # average all the satellite orbit COEs for avg child
            average_child.sats[i] = self.sats[i].make_child(other_parent.sats[i])
        # pick one of the parents' payloads randomly as the starting point for the first child
        average_child.payload = random.choice([self.payload, other_parent.payload])

        while (len(out) < count):
            out.append(average_child.fudgeSolution(fudge_factor))

        return out
    

    def _to_string(self):
        out = ""
        out += "CONSTELLATION\n"
        out += "Payload: " + self.payload["name"] + "\n"
        out += "############## ORBITS ##############\n"
        for sat in self.sats:
            out += sat.orb._to_string() + "\n"
        
        return out

