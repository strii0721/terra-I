from math import pi
import numpy as np

class Configuration:
    @staticmethod
    def _judge(angles, position):
        pass
    def left(angles):
        pass
    def right(angles):
        pass

class Config4V3(Configuration):
    @staticmethod
    def _judge(angles, position):
        if position == "left":
            return angles[0], angles[1], angles[2]
        elif position == "right":
            if len(angles) == 3:
                return angles[0], angles[1], angles[2]
            elif len(angles) == 6:
                return angles[3], angles[4], angles[5]

    def left(angles):
        la_j1, la_j2, la_j3 = Config4V3._judge(angles, "left")
        return np.array([
            # [theta,   d,  a,  alpha]
            [0, 0, 5.1, -pi/2],
            [la_j1, 5.3, 30.891, pi/2],
            [la_j2, 0, 269.91, -pi/2],
            [la_j3, 22.8, 250, 0]
        ])
        
    def right(angles):
        ra_j1, ra_j2, ra_j3 = Config4V3._judge(angles, "left")
        return np.array([
            # [theta,   d,  a,  alpha]
            [0, 0, 354.9, pi/2],
            [ra_j1, -128.8, 30.891, pi/2],
            [ra_j2, 0, 269.91, -pi/2],
            [ra_j3, 22.8, 250, 0]
        ])