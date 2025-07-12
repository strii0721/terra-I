#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Fri Jul 11 2025
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

import numpy as np
from math import sqrt

class SpatialUtils:
    
    @staticmethod
    def normalize_vector(vector:np.typing.NDArray) -> np.typing.NDArray:
        """Return a unit vector align with a given vector.
    
        Args:
            vector (np.typing.NDArray): Given vector.
    
        Returns:
            np.typing.NDArray: A unit vector align with a given vector.
        """
        
        magnitude = sqrt(sum(v**2 for v in vector))
        unit_vector = vector / magnitude
        return unit_vector
    
    @staticmethod
    def calculate_rotation_angle(vector_start:np.typing.NDArray,
                                 vector_end:np.typing.NDArray, 
                                 normal:np.typing.NDArray) -> float:
        """Calculate the angle between two spatial vectors, given the positive direction of the angle. The result is in rad.
    
        Args:
            vector_start (np.typing.NDArray):   Start vector.
            vector_end (np.typing.NDArray):     End vector.
            normal (np.typing.NDArray):         Positive direction of rotation.
    
        Returns:
            float: Angle of rotation from start vector to end vector, positive direction of rotation is vector normal.
        """
        if np.linalg.norm(vector_start) < 1e-8 or np.linalg.norm(vector_end) < 1e-8: 
            return 0.0
        else:
            vector_start = SpatialUtils.normalize_vector(vector_start)
            vector_end = SpatialUtils.normalize_vector(vector_end)
            cross_product = np.cross(vector_start, vector_end)
            dot_product = np.dot(vector_start, vector_end)
            if np.linalg.norm(normal) < 1e-8:
                normal = np.array([1, 0, 0])
            normal = SpatialUtils.normalize_vector(normal)
            sign = np.sign(np.dot(cross_product, normal))
            angle_rad = np.arctan2(np.linalg.norm(cross_product) * sign, dot_product)
            return angle_rad