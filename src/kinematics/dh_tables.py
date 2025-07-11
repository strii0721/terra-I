#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Thu Jul 10 2025
#
# Copyright (c) 2025 S.I.C.
#


from math import pi
import numpy as np

class Configuration:
    @staticmethod
    def _judge(angles, 
               position):
        """Match input angle list.

        Args:
            angles (list):      Angles input.
            position (string):  Determine "left" or "right" arm

        Returns:
            tuple: Angles input of a specific arm.
        """
        pass
    
    def left(angles):
        """Construct a D-H table from input angles.

        Args:
            angles (np.array(list)):  Input angles.

        Returns:
            np.array(list): D-H table of a specific arm.
        """
        pass
    
    def right(angles):
        """Construct a D-H table from input angles.

        Args:
            angles (np.array(list)):  Input angles.

        Returns:
            np.array(list): D-H table of a specific arm.
        """
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
        ], dtype = np.float64)
        
    def right(angles):
        ra_j1, ra_j2, ra_j3 = Config4V3._judge(angles, "right")
        return np.array([
            # [theta,   d,  a,  alpha]
            [0, 0, 354.9, pi/2],
            [ra_j1, -128.8, 30.891, pi/2],
            [ra_j2, 0, 269.91, -pi/2],
            [ra_j3, 22.8, 250, 0]
        ], dtype = np.float64)