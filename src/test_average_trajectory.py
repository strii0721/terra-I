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

from models.robotic_arm import RoboticArm
from models.link import Link
from models.rotational_joint import RotationalJoint
import numpy as np
from visualization.renderer import Renderer
from models.hull import Hull
from math import pi
from controllers.simulation_controller import SimulationController
from utils.kinematic_utils import KinematicUtils
from threading import Thread
import time
from enums.render_object_types import RenderObjectTypes


CONTROL_INTERVAL = 0.1
RENDER_INTERVAL = 0.1

left_arm = RoboticArm()
left_arm.construct(Link("link_0-0", np.array([5.1, 0, 0])))\
    .construct(Link("link_0-1", np.array([0, 5.3, 0])))\
    .construct(RotationalJoint("la-j1", np.array([0, 1, 0])))\
    .construct(Link("link_1-0", np.array([30.891, 0, 0])))\
    .construct(Link("link_1-1", np.array([0, -19.45, 0])))\
    .construct(RotationalJoint("la-j2", np.array([0, -1, 0])))\
    .construct(Link("link_2-0", np.array([0, 0, -19.45])))\
    .construct(Link("link_2-1", np.array([269.91, 0, 0])))\
    .construct(Link("link_2-2", np.array([0, 22.8, 0])))\
    .construct(RotationalJoint("la-j3", np.array([0, 1, 0]), initial_control_variable = -pi))\
    .construct(Link("link_3-0", np.array([250, 0, 0])))
hull = Hull()
controller = SimulationController(left_arm).initialize()
inverse_kinematic_analysis_basis = ["_rf-1",
                                    "_rf-2",
                                    "_rf-3",
                                    "link_3-0"]

controller.bind_inverse_kinematic_analysis_basis(inverse_kinematic_analysis_basis)
target_control_variable_list = [-pi/2, 0, 0]
target_pose_matrix = KinematicUtils.calculate_pose_matrix_dict(left_arm,
                                                               target_control_variable_list)["link_3-0"]


trajectory = KinematicUtils.tp_linear_joint_interpolation(left_arm,
                                                    target_pose_matrix)
listem_to = ["la-j1",
             "la-j2",
             "la-j3",
             "link_3-0"]
renderer = Renderer()
thread_controller = Thread(target = controller.trajectory_input, args=(trajectory,))

thread_controller.start()

while True:
    controller.listen(listem_to)
    
    renderer.clean_lines()
    renderer.clean_faces()
    
    renderer.add_lines(left_arm.retrieve_render_list(RenderObjectTypes.LINE))
    renderer.add_faces(hull.retrieve_render_list(RenderObjectTypes.FACE))
    renderer.render()
    
    
