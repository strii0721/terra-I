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


from math import sqrt
import numpy as np

class ThreeDimCalculation:
    
    def convert_to_unit_vector(vector:np.typing.NDArray) -> np.typing.NDArray:
        """Return a unit vector align with a given vector.
    
        Args:
            vector (np.typing.NDArray): Given vector.
    
        Returns:
            np.typing.NDArray: A unit vector align with a given vector.
        """
        
        magnitude = sqrt(sum(v**2 for v in vector))
        unit_vector = vector / magnitude
        return unit_vector
    
    def calculate_rotation_angle_rad(start_vector:np.typing.NDArray, 
                                     end_vector:np.typing.NDArray, 
                                     normal:np.typing.NDArray):
        """Calculate the angle between two spatial vectors, given the positive direction of the angle.
    
        Args:
            start_vector (np.typing.NDArray):   Start vector.
            end_vector (np.typing.NDArray):     End vector.
            normal (np.typing.NDArray):         Positive direction of rotation.
    
        Returns:
            float: Angle of rotation from start vector to end vector, positive direction of rotation is vector normal.
        """
        if np.linalg.norm(start_vector) < 1e-8 or np.linalg.norm(end_vector) < 1e-8: 
            return 0.0
        else:
            start_vector = ThreeDimCalculation.convert_to_unit_vector(start_vector)
            end_vector = ThreeDimCalculation.convert_to_unit_vector(end_vector)
            cross_product = np.cross(start_vector, end_vector)
            dot_product = np.dot(start_vector, end_vector)
            if np.linalg.norm(normal) < 1e-8:
                normal = np.array([1, 0, 0])
            normal = ThreeDimCalculation.convert_to_unit_vector(normal)
            sign = np.sign(np.dot(cross_product, normal))
            angle_rad = np.arctan2(np.linalg.norm(cross_product) * sign, dot_product)
            return angle_rad