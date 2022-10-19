"""Some definitions of constant quantities throughout the code"""
# The bands are all in lowercase such that they can be handled more consistently.
ALL_GALEX_BANDS = ('fuv', 'nuv')
ALL_SWEEP_BANDS = ('g', 'r', 'z', 'w1', 'w2', 'w3', 'w4')
ALL_VHS_BANDS = ('y', 'j', 'h', 'ks')

ALL_BANDS = ALL_GALEX_BANDS + ALL_SWEEP_BANDS + ALL_VHS_BANDS

# The magnitude corrections to convert from the vega to the AB system,
# which is important for the VHS bands:

VEGA_AB_DICT = {"y": 0.60, "j": 0.92, "h": 1.37, "ks": 1.83}
