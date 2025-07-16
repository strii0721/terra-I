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

from models.impl.robotic_arm import RoboticArm
from models.impl.link import Link
from models.impl.rotational_joint import RotationalJoint
import numpy as np
from visualizations.renderer import Renderer
from models.impl.ground import Ground
from math import pi
from kinematics.controllers.impl.simulation_controller import SimulationController

CONTROL_INTERVAL = 0.1
RENDER_INTERVAL = 0.1
L_INVERSE_KINEMATIC_ANALYSIS_BASIS = [
    "_rf-1",
    "_rf-2",
    "_rf-3",
    "l-link_3-0"
]
L_LISTEN_LIST = [
    "la-j1",
    "la-j2",
    "la-j3",
    "l-link_3-0"
]
GROUND = Ground()
LEFT_ARM = RoboticArm()\
    .construct(Link("l-link_0-0", np.array([0, 0, 110])))\
    .construct(RotationalJoint("la-j1", np.array([0, 1, 0]), initial_control_variable = 0))\
    .construct(Link("l-link_1-0", np.array([0, -85, 0])))\
    .construct(RotationalJoint("la-j2", np.array([0, 0, 1]), initial_control_variable = 0))\
    .construct(Link("l-link_2-2", np.array([85, 0, 0])))\
    .construct(RotationalJoint("la-j3", np.array([0, 0, 1]), initial_control_variable = 0))\
    .construct(Link("l-link_3-0", np.array([85, 0, 0])))
L_CONTROLLER = SimulationController(LEFT_ARM, control_interval = CONTROL_INTERVAL)\
    .initialize()\
    .bind_inverse_kinematic_analysis_basis(L_INVERSE_KINEMATIC_ANALYSIS_BASIS)
RENDERER = Renderer(render_interval = RENDER_INTERVAL)


