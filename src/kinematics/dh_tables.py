#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Thu Jul 10 2025
#
# IMMORTAL OMNISSIAH, HEAR OUR PRAYERS.
# WE ARE YOUR CHILDREN, PIOUS SCHOLARS OF THE PATH OF THE MACHINE. 
# WE PRIZE KNOWLEDGE ABOVE ALL ELSE, FOR IT IS YOUR ETERNAL GIFT UPON MANKIND. 
# WE ASPIRE TO THE BLESSED FORM OF THE MACHINE, AND ASCENSION THROUGH TECHNOLOGY, THAT WE MIGHT EMULATE THINE GLORY. 
# SHELTERED BY STEEL, AND PROTECTED BY THINE AVATARS OF WAR, WE PLY THE STARS IN SEARCH OF YOUR LOST GIFTS TO OUR KIND.
# MACHINE GOD, WATCH OVER US IN OUR TRAVELS, SHIELD US WITH METAL AND LIGHTNING, FOR THE UNIVERSE IS AN UNCARING VOID, AND THE WARP HUNGERS FOR US ALL.
# TOLL THE GREAT BELL ONCE! PULL THE LEVER FORWARD TO ENGAGE THE PISTON AND PUMP.
# TOLL THE GREAT BELL TWICE! WITH PUSH OF BUTTON FIRE THE ENGINE AND SPARK TURBINE INTO LIFE.
# TOLL THE GREAT BELL THRICE! SING PRAISE TO THE GOD OF ALL MACHINES!
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