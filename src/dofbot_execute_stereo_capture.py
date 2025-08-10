#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Mon Jul 28 2025
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

from threading import Thread
import time
from dk.logger.log4p import Log4P
from math import pi
import cv2
import os
from controllers.impl.dofbot_controller import DofbotController


def main():
    logger = Log4P()
    dofbot_controller = DofbotController()
    time.sleep(2)
    logger.info(f"Starting...")
    for index in range(20):
        image_left = dofbot_controller.image_output(camera_index = 0)
        image_right = dofbot_controller.image_output(camera_index = 2)
        timestamp = time.time()
        save_dir_base = "output/calibration"
        save_dir_left = f"{save_dir_base}/left"
        save_dir_right = f"{save_dir_base}/right"
        os.makedirs(save_dir_left, exist_ok =True)
        os.makedirs(save_dir_right, exist_ok = True)
        save_path_left = f"{save_dir_left}/{timestamp}-left.bmp"
        save_path_right = f"{save_dir_right}/{timestamp}-right.bmp"
        dofbot_controller.save_image(image_left, save_path_left)
        dofbot_controller.save_image(image_right, save_path_right)
        logger.info(f"Stereo image saved. Index: {index + 1}")
        cv2.imshow("Left Image", image_left)
        cv2.imshow("Right Image", image_right)
        cv2.waitKey(2000)
try:
    main()
except KeyboardInterrupt:
  print("Program terminated! ")