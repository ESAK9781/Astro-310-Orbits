##############################
# MSIII_Orbit.py
# Author: Elijah Sakamoto
# Documentation: None
##############################


import math

from MSIII_useful_consts import *


# fix angles over 360 or under 0 to their counterpart on that range
def loop_angle(theta, radians=False):
    if (radians):
        while (theta > 2 * math.pi):
            theta -= 2 * math.pi
        while (theta < 0):
            theta += 2 * math.pi
        return theta
    else:
        while (theta > 360):
            theta -= 360
        while (theta < 0):
            theta += 360
        return theta

class MSIII_Orbit:
    def __init__(self, other_orbit):
        self.i = other_orbit.i
        self.a = other_orbit.a
        self.e = other_orbit.e
        self.raan = other_orbit.raan
        self.v = other_orbit.v
        self.w = other_orbit.w
        self.n = other_orbit.n
        self.period = other_orbit.period

    def __init__(self, a, e, i, raan, w, v):
        self.a = a
        self.e = max(min(e, 1), 0) # restrict e to between 0 and 1

        self.raan = loop_angle(raan)
        self.i = loop_angle(i)
        self.v = loop_angle(v)
        self.w = loop_angle(w)

        # the best way of dealing with special orbits, as it turns out,
        # is to pretend they don't exist.
        if (i == 0): # is it equatorial? Not anymore!
            self.i = 0.00000001
        if (e == 0): # is it circular? Not anymore!
            self.e = 0.00000001


        # calculate n for orbit predictions
        self.n = math.sqrt(MIU / math.pow(self.a, 3)) # from formula sheet
        self.period = (2 * math.pi) / self.n # from formula sheet
        
    def recomp_meta_vars(self):
        if (self.a <= 0): # patch negative semimajor axis bug
            self.a = 0.00000001
        
        self.e = max(min(self.e, 1), 0) # restrict e to between 0 and 1

        self.raan = loop_angle(self.raan)
        self.i = loop_angle(self.i)
        self.v = loop_angle(self.v)
        self.w = loop_angle(self.w)

        # the best way of dealing with special orbits, as it turns out,
        # is to pretend they don't exist.
        if (self.i == 0): # is it equatorial? Not anymore!
            self.i = 0.00000001
        if (self.e == 0): # is it circular? Not anymore!
            self.e = 0.00000001


        # calculate n for orbit predictions
        self.n = math.sqrt(MIU / math.pow(self.a, 3)) # from formula sheet
        self.period = (2 * math.pi) / self.n # from formula sheet
        
        if (math.floor(self.period) == 0): # patch zero period bug
            self.period = 1
        

    def to_string(self):
        out = "ORBIT: \n"
        out += "\ta    : " + str(self.a) + "\n"
        out += "\te    : " + str(self.e) + "\n"
        out += "\ti    : " + str(self.i) + "\n"
        out += "\traan : " + str(self.raan) + "\n"
        out += "\tw    : " + str(self.w) + "\n"
        out += "\tv    : " + str(self.v) + "\n"
        return out.strip()

    # accepts v in radians
    def get_position_at_v(self, v):
        r = (self.a * (1 - math.pow(self.e, 2))) / (1 + self.e * math.cos(v)) # from formula sheet
        x = r * math.cos(v) # x position on orbital plane
        y = r * math.sin(v) # y position on orbital plane

        sinw = math.sin(math.radians(self.w))
        cosw = math.cos(math.radians(self.w))

        sini = math.sin(math.radians(self.i))
        cosi = math.cos(math.radians(self.i))

        sino = math.sin(math.radians(self.raan))
        coso = math.cos(math.radians(self.raan))

        '''
        What we do here is a bit complicated. We have 2D coordinates on the orbital plane in the 
        form <x,y,0>. We want these in ijk coordinates, so we have to do some transformations.
        
        First, we rotate about the z axis by w. Then, we rotate about the x axis by i to 
        factor in inclination. Finally, we rotate about the z axis by raan. These transformations
        were conceptually figured out using the whiz wheel.

        We multiply all of these transformation matrices together using a computing tool like
        Wolfram Alpha. This yields a giant matrix which represents the entire transformation.
        However, since our z is initially zero, the entire rightmost column of the matrix will
        end up having no impact on our final vector. Thus, we do not even waste the time to compute
        it.

        Calculations and notes for this process may be included. I learned about rotation matrices
        from my Linear Algebra course and sourced the initial Rx and Rz rotation matrices from a 
        reference image on Wikipedia.
        '''

        # RwRiRo = [
        #     [
        #         (coso * cosw) - (cosi * sino * sinw),
        #         (cosi * sino * cosw) + (coso * sinw),
        #         (sini * sino)
        #     ], [
        #         (-sino * cosw) - (cosi * coso * sinw),
        #         (cosi * coso * cosw) - (sino * sinw),
        #         (sini * coso)
        #     ]
        # ]

        # ok, things werent working. Figured out w and o were swapped somehow. Now it works.
        # Why? God knows.
        RwRiRo = [ 
            [
                (cosw * coso) - (cosi * sinw * sino),
                (cosi * sinw * coso) + (cosw * sino),
                (sini * sinw)
            ], [
                (-sinw * coso) - (cosi * cosw * sino),
                (cosi * cosw * coso) - (sinw * sino),
                (sini * cosw)
            ]
        ]

        # multiply <x,y,0> by RwRiRo to get real ijk positions
        pos = [
            (x * RwRiRo[0][0]) + (y * RwRiRo[1][0]), # i
            (x * RwRiRo[0][1]) + (y * RwRiRo[1][1]), # j
            (x * RwRiRo[0][2]) + (y * RwRiRo[1][2])  # k
        ]

        return pos

        
    def get_v_at_time(self, time):
        time = math.floor(time) % math.floor(self.period)

        vi = math.radians(self.v)
        cos_vi = math.cos(vi) # to save an expensive cosine computation
        ei = math.acos((self.e + cos_vi) / (1 + self.e * cos_vi)) # from formula sheet
        if (vi > math.pi): # half-plane check
            ei = (2 * math.pi) - ei

        mi = ei - self.e * math.sin(ei) # from formula sheet

        mf = mi + self.n * time # from formula sheet
        mf = loop_angle(mf, radians=True) # adjust for full passes

        ef = mf - self.e * math.sin(mf) # procedure from class to find new ef
        delta = 1

        loop_escape_counter = MAX_E_ITERATIONS
        while (delta > 0.001):
            new_ef = mf - self.e * math.sin(ef)
            delta = abs(new_ef - ef)
            ef = new_ef

            loop_escape_counter -= 1
            if (loop_escape_counter < 0):
                break
        
        cos_ef = math.cos(ef) # to save an expensive cosine computation
        vf = math.acos((cos_ef - self.e) / (1 - self.e * cos_ef)) # from formula sheet
        if (ef > math.pi): # half-plane check
            vf = (2 * math.pi) - vf
        
        return math.degrees(vf)
    
    # returns a position vector based on the time in seconds, uses whole numbers
    def get_position_at_time(self, time):
        v_time = math.radians(self.get_v_at_time(time))
        return self.get_position_at_v(v_time) # convert v to a position vector
        



