from math import pi
import numpy as np

class config4_v3:

    def left(la_j1, la_j2, la_j3):
        return np.array([
            # [theta,   d,  a,  alpha]
            [0, 0, 5.1, -pi/2],
            [la_j1, 5.3, 30.891, pi/2],
            [la_j2, 0, 269.91, -pi/2],
            [la_j3, 22.8, 250, 0]
        ])
        
    def right(ra_j1, ra_j2, ra_j3):
        return np.array([
            # [theta,   d,  a,  alpha]
            [0, 0, 354.9, pi/2],
            [ra_j1, -128.8, 30.891, pi/2],
            [ra_j2, 0, 269.91, -pi/2],
            [ra_j3, 22.8, 250, 0]
        ])