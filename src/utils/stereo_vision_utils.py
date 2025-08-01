#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Fri Aug 01 2025
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

import cv2
import numpy as np

class StereoVisionUtils():
    @staticmethod
    def calculate_mask(image:np.typing.NDArray, 
                       lower_bound:np.typing.NDArray,
                       upper_bound:np.typing.NDArray) -> np.typing.NDArray:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        return mask
    
    @staticmethod
    def calculate_center(image:np.typing.NDArray, 
                         lower_bound:np.typing.NDArray,
                         upper_bound:np.typing.NDArray) -> tuple|None:
        mask = StereoVisionUtils.calculate_mask(image, 
                                                lower_bound, 
                                                upper_bound)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            main_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(main_contour)
            if M['m00'] != 0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                return (x, y)
        return None