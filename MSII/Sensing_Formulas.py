

def get_payload_max_height(payload, min_resolution_m):
    return ((payload["aperture"] * min_resolution_m) / (2.44 * 2.44 * payload["max_wl"])) / 1000


# checks that the adcs and camera will work together so we can capture what we aim at.
# derivation done / submitted on paper
def assess_camera_adcs_compatibility(payload, adcs):
    adcs_d_over_h = adcs["pointing accuracy"]
    cam_sw_over_h = (2 * payload["det_rad"]) / payload["fl"]

    return (adcs_d_over_h < cam_sw_over_h) # make sure the swath width is bigger than the pointing error
