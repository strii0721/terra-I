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
This runtime is using "average trajactory plan"
'''

# Variable Area #########################################################
# target_pose_matrix_list = []
# target_control_variable_lists = [
#     [-pi/2, 0, -pi],
#     [-pi/2, pi/4, -pi],
#     [-pi/2, pi/4, 1e-1],
# ]
# for target_control_variable_list in target_control_variable_lists:
#     target_pose_matrix_list.append(KinematicUtils.calculate_pose_matrix_dict(CFG.LEFT_ARM,
#                                                                              target_control_variable_list)["link_3-0"])
#########################################################################
  
# Exports ###############################################################
THREAD_LIST = [
    Thread(target = CFG.L_CONTROLLER.listen_daemon, args = (CFG.L_LISTEN_LIST,)),   
    # Thread(target = CFG.R_CONTROLLER.listen_daemon, args = (CFG.R_LISTEN_LIST,)),
    # Thread(target = CFG.CONTROLLER_L.target_input, args = (target_pose_matrix_list,
    #                                                        KinematicUtils.average_trajactory_plan))
]
def FRAME():
    CFG.RENDERER.clean_lines()
    CFG.RENDERER.clean_faces()
    CFG.RENDERER.add_faces(CFG.HULL.retrieve_render_list(RenderObjectTypes.FACE))
    CFG.RENDERER.add_lines(CFG.LEFT_ARM.retrieve_render_list(RenderObjectTypes.LINE))
    CFG.RENDERER.add_lines(CFG.RIGHT_ARM.retrieve_render_list(RenderObjectTypes.LINE))
    CFG.RENDERER.render()
########################################################################