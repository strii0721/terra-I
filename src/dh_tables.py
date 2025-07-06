from math import pi
import numpy as np

class config4_v3:

    la_j1 = 0
    la_j2 = 0
    la_j3 = pi

    ra_j1 = pi/2
    ra_j2 = 0
    ra_j3 = pi

    def left(la_j1, la_j2, la_j3):
        return np.array([
            # [theta,   d,  a,  alpha]
            [la_j1, 0, 5.1, -pi/2],
            [la_j2, 5.3, 30.891, pi/2],
            [la_j3, 0, 269.91, -pi/2],
            [0, 0, 250, 0]
        ])
        
    def right(ra_j1, ra_j2, ra_j3):
        return np.array([
            # [theta,   d,  a,  alpha]
            [ra_j1, 0, 354.9, pi/2],
            [ra_j2, -128.8, 30.891, pi/2],
            [ra_j3, 0, 269.91, -pi/2],
            [0, 0, 250, 0]
        ])