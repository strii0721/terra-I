#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Sat Jul 12 2025
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
from utils.kinematic_utils import KinematicUtils
import time
from dk.logger.log4p import Log4P
import saves.statics.default as CFG

target_control_variable_list = [pi/2, 0, pi]
target_pose_matrix = KinematicUtils.calculate_pose_matrix_dict(CFG.RIGHT_ARM,
                                                               target_control_variable_list)["r-link_3-0"]
start = time.time()
calculated_result = KinematicUtils.inverse_kinematics(CFG.RIGHT_ARM,
                                                      target_pose_matrix,
                                                      learning_rate = 0.2,
                                                      shreshold = 1e-6,
                                                      enable_log = True)
end = time.time()
logger = Log4P()
logger.info(f"Calculation time: {end-start:.6f} sec")
logger.info(f"Target control variables: {calculated_result}")