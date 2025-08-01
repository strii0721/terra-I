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
from dk.logger.log4p import Log4P
from cv.dual_camera import DualCamera
import scipy.io

logger = Log4P()
dual_camera = DualCamera()
image_left_path = "resources/stereo_calibration/ball/left/1754055534.8428326-left.bmp"
image_right_path = "resources/stereo_calibration/ball/right/1754055534.8428326-right.bmp"
image_left = cv2.imread(image_left_path)
image_right = cv2.imread(image_right_path)

image_marked_left = image_left.copy()
image_marked_right = image_right.copy()
center_left = DualCamera.calculate_center(image = image_left, 
                                          lower_bound = dual_camera.LOWER_BOUND_BLUE, 
                                          upper_bound = dual_camera.UPPER_BOUND_BLUE)
center_right = DualCamera.calculate_center(image = image_right, 
                                           lower_bound = dual_camera.LOWER_BOUND_BLUE, 
                                           upper_bound = dual_camera.UPPER_BOUND_BLUE)
cv2.circle(image_marked_left, 
           center_left, 
           radius = 5, 
           color = (0, 0, 255), 
           thickness = -1)
cv2.circle(image_marked_right, 
           center_right, 
           radius = 5, 
           color = (0, 0, 255), 
           thickness = -1)
cv2.imshow("Left", image_marked_left)
cv2.imshow("Right", image_marked_right)

x, y, z = dual_camera.calculate_3d_coordinate(image_left,
                                              image_right)
logger.info(f"x = {x * 1000} mm")
logger.info(f"y = {y * 1000} mm")
logger.info(f"z = {z * 1000} mm")

cv2.waitKey(0)