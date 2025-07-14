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

import saves.statics.default as CFG
from threading import Thread
from enums.render_object_types import RenderObjectTypes

from utils.kinematic_utils import KinematicUtils
from math import pi

'''
This runtime is using "Linear Joint Interpolation"
This simulation demonstrates the initialisation process of the robotic arm.
'''

# Variable Area #########################################################
POSITION_TEST = KinematicUtils.generate_pose_matrix_from_position(CFG.TARGET.coordinate)
LEFT_STOP_0 = KinematicUtils.calculate_pose_matrix_dict(CFG.LEFT_ARM, [0, 0, -pi])["l-link_3-0"]
LEFT_STOP_1 = KinematicUtils.calculate_pose_matrix_dict(CFG.LEFT_ARM, [-pi/2, 0, -pi])["l-link_3-0"]
LEFT_STOP_2 = KinematicUtils.calculate_pose_matrix_dict(CFG.LEFT_ARM, [-pi/2, 0, -pi/2])["l-link_3-0"]
LEFT_STOP_3 = KinematicUtils.calculate_pose_matrix_dict(CFG.LEFT_ARM, [-pi/2, 0, 0])["l-link_3-0"]
LEFT_ACTION_1 = KinematicUtils.calculate_pose_matrix_dict(CFG.LEFT_ARM, [-pi/2, 0, pi/2])["l-link_3-0"]
l_target_pose_matrix_list = [
    # LEFT_STOP_0,
    LEFT_STOP_1, 
    LEFT_STOP_2, 
    LEFT_STOP_3, 
    # LEFT_ACTION_1,
    POSITION_TEST
]
RIGHT_STOP_0 = KinematicUtils.calculate_pose_matrix_dict(CFG.RIGHT_ARM, [pi, 0, pi])["r-link_3-0"]
RIGHT_STOP_1 = KinematicUtils.calculate_pose_matrix_dict(CFG.RIGHT_ARM, [pi/2, 0, pi])["r-link_3-0"]
RIGHT_STOP_2 = KinematicUtils.calculate_pose_matrix_dict(CFG.RIGHT_ARM, [pi/2, 0, 3*pi/2])["r-link_3-0"]
RIGHT_STOP_3 = KinematicUtils.calculate_pose_matrix_dict(CFG.RIGHT_ARM, [pi/2, 0, 4*pi/2])["r-link_3-0"]
RIGHT_ACTION_1 = KinematicUtils.calculate_pose_matrix_dict(CFG.RIGHT_ARM, [pi/2, 0, 5*pi/2])["r-link_3-0"]
r_target_pose_matrix_list = [
    # RIGHT_STOP_0, 
    RIGHT_STOP_0, 
    RIGHT_STOP_1, 
    RIGHT_STOP_2, 
    RIGHT_STOP_3, 
    # RIGHT_ACTION_1,
    POSITION_TEST
]

#########################################################################

  
# Exports ###############################################################
THREAD_LIST = [
    # Thread(target = CFG.L_CONTROLLER.listen_daemon, args = (CFG.L_LISTEN_LIST,)),
    # Thread(target = CFG.R_CONTROLLER.listen_daemon, args = (CFG.R_LISTEN_LIST,)),
    Thread(target = CFG.L_CONTROLLER.route_input, args = (l_target_pose_matrix_list,
                                                           KinematicUtils.tp_linear_joint_interpolation,
                                                           "full",
                                                           True,
                                                           True)),
    Thread(target = CFG.R_CONTROLLER.route_input, args = (r_target_pose_matrix_list,
                                                           KinematicUtils.tp_linear_joint_interpolation,
                                                           "full",
                                                           True,
                                                           False))
]
def FRAME():
    CFG.RENDERER.clean_points()
    CFG.RENDERER.clean_lines()
    CFG.RENDERER.clean_faces()
    
    CFG.RENDERER.add_faces(CFG.HULL.retrieve_render_list(RenderObjectTypes.FACE))
    CFG.RENDERER.add_points(CFG.TARGET.retrieve_render_list(RenderObjectTypes.POINT))
    CFG.RENDERER.add_lines(CFG.LEFT_ARM.retrieve_render_list(RenderObjectTypes.LINE))
    CFG.RENDERER.add_lines(CFG.RIGHT_ARM.retrieve_render_list(RenderObjectTypes.LINE))
    
    CFG.RENDERER.render()
########################################################################