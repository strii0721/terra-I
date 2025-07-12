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

from saves.default import Default
from threading import Thread
from utils.kinematic_utils import KinematicUtils
from math import pi
from enums.render_object_types import RenderObjectTypes

c = Default()

# Variable Area
target_control_variable_list = [-pi/2, 0, 0]
target_pose_matrix = KinematicUtils.calculate_pose_matrix_dict(c.left_arm,
                                                               target_control_variable_list)["link_3-0"]
trajectory = KinematicUtils.average_trajactory_plan(c.left_arm,
                                                    target_pose_matrix)

#  Thread Area
thread_controller = Thread(target = c.controller.trajectory_input, args=(trajectory,))

thread_controller.start()

# Rendering Area
while True:
    c.controller.listen(c.LISTEN_LIST)
    c.renderer.clean_lines()
    c.renderer.clean_faces()
    c.renderer.add_lines(c.left_arm.retrieve_render_list(RenderObjectTypes.LINE))
    c.renderer.add_faces(c.hull.retrieve_render_list(RenderObjectTypes.FACE))
    c.renderer.render()