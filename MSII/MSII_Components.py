
PAYLOADS = [ # from table 2
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

STRUCTURES = [ # from table 4
    { # option 1
        "name": "Option I",
        "internal volume": [1, 1, 1.5], # dimensions in meters
        "external side length": 2, # cube side length in meters
        "spring constant": 3*(10**7), # Newtons / meter
        "mass": 135, # kg
        "cost": 80000, # $
        "delivery": 5 # months
    }, { # option 2
        "name": "Option II",
        "internal volume": [1.5, 1.5, 2.5], # dimensions in meters
        "external side length": 3, # cube side length in meters
        "spring constant": 3.6*(10**7), # Newtons / meter
        "mass": 175, # kg
        "cost": 100000, # $
        "delivery": 5 # months
    }, { # option 3
        "name": "Option III",
        "internal volume": [2, 2, 3], # dimensions in meters
        "external side length": 3.5, # cube side length in meters
        "spring constant": 3.4*(10**7), # Newtons / meter
        "mass": 215, # kg
        "cost": 125000, # $
        "delivery": 5 # months
    }
]

ADCS = [ # from table 5
    { # option 1
        "name": "Option I",
        "pointing accuracy": 0.095, # deg
        "power": 25, # W
        "mass": 20, # kg
        "cost": 250000, # $
        "delivery": 4 # months
    }, { # option 2
        "name": "Option II",
        "pointing accuracy": 0.035, # deg
        "power": 40, # W
        "mass": 28, # kg
        "cost": 375000, # $
        "delivery": 6 # months
    }, { # option 3
        "name": "Option III",
        "pointing accuracy": 0.015, # deg
        "power": 30, # W
        "mass": 33, # kg
        "cost": 625000, # $
        "delivery": 8 # months
    }
]

GROUND_STATION_ANNUAL_COST = 3000000 # yearly cost to operate the ground station
AVERAGE_ANTENNA_COST = (450000 + 300000 + 375000) / 3 # average cost for an antenna
AVERAGE_PROPULSION_COST = (200000 + 450000 + 600000) / 3 # average cost for an propulsion system
AVERAGE_ELECTRICAL_COST = (350000 + 550000 + 900000) / 3 # average cost for an electrical system
