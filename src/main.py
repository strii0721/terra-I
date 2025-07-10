from model.configuration import Configuration
from model.components.link import Link
from model.components.rotation_joint import RotationJoint
from kinematics.dh_tables import Config4V3
from utils.kinematic_utils import KinematicUtils
from math import pi

import numpy as np

left_arm = Configuration()
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
left_arm.enable_inverse_kinematic([
    "la-j2",
    "la-j3",
    "link_3-0"
])

inputs = [0, 0, -pi/6]
new_po_matrixs = left_arm.get_po_matrixs(inputs)
ori_po_matrixs = KinematicUtils.forward_kinematics(Config4V3.left(inputs))

for name, po_matrix in new_po_matrixs.items():
    print(f"{name}")
    print(f"{po_matrix}\n")
print(f"==========================")
for name, po_matrix in ori_po_matrixs.items():
    print(f"{name}")
    print(f"{po_matrix}\n")