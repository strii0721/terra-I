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

from numpy import np
import scipy
import cv2
from utils.stereo_vision_utils import StereoVisionUtils

class SingleCamera():
    def __init__(self,) -> None:
        self.LOWER_BOUND_BLUE = np.array([100, 150, 50])
        self.UPPER_BOUND_BLUE = np.array([140, 255, 255])
        essential_parameters = scipy.io.loadmat("resources/essential_parameters_single.mat")
        self.focal_x, self.focal_y = essential_parameters["focal_length"]
        self.focal_z = self.focal_x
        self.principal_point_x, self.principal_point_y = essential_parameters["principal_point"]
        self.K = essential_parameters["K"]
        self.distortion = essential_parameters["distortion"]
        self.target_size = 50
        
    
    def calculate_3d_coordinate(self,
                                image):
        image_undistort = cv2.undistort(image, self.K, self.distortion)
        hsv = cv2.cvtColor(image_undistort, cv2.COLOR_BGR2HSV)
        h_channel = hsv[:, :, 0]
        s_channel = hsv[:, :, 1]
        v_channel = hsv[:, :, 2]
        mask = StereoVisionUtils.calculate_mask(hsv, 
                                                self.LOWER_BOUND_BLUE, 
                                                self.UPPER_BOUND_BLUE)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        circular_candidates = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 200:
                continue
            ellipse = cv2.fitEllipse(cnt) if len(cnt) >= 5 else None
            if ellipse:
                (x, y), (major, minor), angle = ellipse
                eccentricity = np.sqrt(1 - (minor / major) ** 2)
                if 0.0 < eccentricity < 0.75 and 10 < major < 800:
                    circular_candidates.append((x, y, major))
                    
        if circular_candidates:
            largest = max(circular_candidates, key=lambda x: x[2])
            x_pixel, y_pixel, ball_pixel_diameter = largest
            z = (self.target_size * self.focal_x) / ball_pixel_diameter
            x = ((x_pixel - self.principal_point_x) * z) / self.focal_x
            y = -((y_pixel - self.principal_point_y) * z) / self.focal_y
        return x, y, z