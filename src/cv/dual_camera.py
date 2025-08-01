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
import scipy.io
from dk.logger.log4p import Log4P
from utils.stereo_vision_utils import StereoVisionUtils

class DualCamera():
    def __init__(self,) -> None:
        self.LOWER_BOUND_BLUE = np.array([100, 150, 50])
        self.UPPER_BOUND_BLUE = np.array([140, 255, 255])
        essential_parameters = scipy.io.loadmat("resources/essential_parameters_dual.mat")
        self.intrinsic_matrix_left = essential_parameters["intrinsic_matrix_left"]
        self.intrinsic_matrix_right = essential_parameters["intrinsic_matrix_right"]
        self.distortion_left = essential_parameters["distortion_left"]
        self.distortion_right = essential_parameters["distortion_right"]
        self.rotation_matrix = essential_parameters["rotation_matrix"]
        self.translation = essential_parameters["translation"].flatten() / 1000
        self.image_size = essential_parameters["image_size"][0][::-1]
        self.R1, self.R2, self.P1, self.P2, self.Q, _, _ = cv2.stereoRectify(self.intrinsic_matrix_left, 
                                                                             self.distortion_left, 
                                                                             self.intrinsic_matrix_right, 
                                                                             self.distortion_right, 
                                                                             self.image_size, 
                                                                             self.rotation_matrix, 
                                                                             self.translation, 
                                                                             alpha = 100)
        self.map_x_left, self.map_y_left = cv2.initUndistortRectifyMap(self.intrinsic_matrix_left, 
                                                                       self.distortion_left, 
                                                                       self.R1, 
                                                                       self.P1, 
                                                                       self.image_size, 
                                                                       cv2.CV_16SC2)
        self.map_x_right, self.map_y_right = cv2.initUndistortRectifyMap(self.intrinsic_matrix_right, 
                                                                         self.distortion_right, 
                                                                         self.R2, 
                                                                         self.P2, 
                                                                         self.image_size, 
                                                                         cv2.CV_16SC2)

        self.block_size = 3
        self.image_channel_num = 3
        self.stereo = cv2.StereoSGBM_create(minDisparity=1,
                                            numDisparities=64,
                                            blockSize = self.block_size,
                                            P1 = 8 * self.image_channel_num * self.block_size ** 2,
                                            P2 = 32 * self.image_channel_num * self.block_size ** 2,
                                            disp12MaxDiff = 1,
                                            uniquenessRatio = 10,
                                            speckleWindowSize = 100,
                                            speckleRange = 32, 
                                            mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)
    def calculate_3d_coordinate(self, 
                                image_left:np.typing.NDArray, 
                                image_right:np.typing.NDArray) -> tuple:
        image_left_rectified = cv2.remap(image_left.copy(), self.map_x_left, self.map_y_left, cv2.INTER_LINEAR)
        image_right_rectified = cv2.remap(image_right.copy(), self.map_x_right, self.map_y_right, cv2.INTER_LINEAR)
        center_right = StereoVisionUtils.calculate_center(image = image_right_rectified, 
                                                          lower_bound = self.LOWER_BOUND_BLUE, 
                                                          upper_bound = self.UPPER_BOUND_BLUE)
        print(f"center: {center_right}")
        gray_left = cv2.cvtColor(image_left_rectified, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(image_right_rectified, cv2.COLOR_BGR2GRAY)
        disparity = self.stereo.compute(gray_left, 
                                        gray_right).astype(np.float32) / 16
        print(f"disparity = {disparity}")
        points_3D = cv2.reprojectImageTo3D(disparity, self.Q, handleMissingValues = True)     
        cv2.circle(image_right_rectified, 
                   center_right, 
                   radius = 5, 
                   color = (0, 0, 255), 
                   thickness = -1)
        cv2.imshow("Left Rectified", image_left_rectified)
        cv2.imshow("Right Rectified", image_right_rectified)
        print(f"Q = {self.Q}")
        
        x, y, z = points_3D[center_right[1], center_right[0]]
        print(f"{points_3D.shape}")
        return x, y, z
        
    