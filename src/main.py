#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Fri Jul 11 2025
#
# Copyright (c) 2025 S.I.C.
#


from model.robotic_arm import RoboticArm
from model.components.link import Link
from model.components.rotation_joint import RotationJoint
from math import pi
from services.renderer import Renderer
from model.payload import Payload

import numpy as np

left_arm = RoboticArm()
left_arm.construct("link_0-0", 
                   Link(np.array([5.1, 0, 0])))\
        .construct("link_0-1", 
                   Link(np.array([0, 5.3, 0])))\
        .construct("la-j1", 
                   RotationJoint(np.array([0, 1, 0])))\
        .construct("link_1-0", 
                   Link(np.array([30.891, 0, 0])))\
        .construct("link_1-1", 
                   Link(np.array([0, -19.45, 0])))\
        .construct("la-j2", 
                   RotationJoint(np.array([0, -1, 0])))\
        .construct("link_2-0", 
                   Link(np.array([0, 0, -19.45])))\
        .construct("link_2-1", 
                   Link(np.array([269.91, 0, 0])))\
        .construct("link_2-2", 
                   Link(np.array([0, 22.8, 0])))\
        .construct("la-j3", 
                   RotationJoint(np.array([0, 1, 0])))\
        .construct("link_3-0", 
                   Link(np.array([250, 0, 0])))\
        .confirm_construct()
        
left_arm.enabled_inverse_kinematic([
    "_rf-1",
    "_rf-2",
    "_rf-3",
    "link_3-0"
])

renderer = Renderer()
payload = Payload()

for suffix in range(1000):
    renderer.clean_lines()
    renderer.clean_faces()
    inputs = [0, pi/1000 * suffix, -pi/1000 * suffix]
    left_arm.control(inputs)
    
    renderer.add_lines(left_arm.get_render_list())
    renderer.add_faces(payload.get_render_list())
    renderer.render()
    