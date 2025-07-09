from structure.assembly import Assembly
from structure.components.link import Link
from structure.components.rotation_joint import RotationJoint
from kinematics.dh_tables import Config4V3
from utils.kinematic_utils import KinematicUtils

import numpy as np

left_arm = Assembly()
left_arm.construct("link_0-0", 
                   Link(np.array([1, 0, 0]), 5.1))\
        .construct("link_0-1", 
                   Link(np.array([0, 1, 0]), 5.3))\
        .construct("la-j1", 
                   RotationJoint(np.array([0, 1, 0])))\
        .construct("link_1-0", 
                   Link(np.array([1, 0, 0]), 30.891))\
        .construct("link_1-1", 
                   Link(np.array([0, 0, 1]), 19.45))\
        .construct("la-j2", 
                   RotationJoint(np.array([0, 0, 1])))\
        .construct("link_2-0", 
                   Link(np.array([0, 0, -1]), 19.45))\
        .construct("link_2-1", 
                   Link(np.array([1, 0, 0]), 269.91))\
        .construct("link_2-2", 
                   Link(np.array([0, 1, 0]), 22.8))\
        .construct("la-j3", 
                   RotationJoint(np.array([0, 1, 0])))\
        .construct("link_3-0", 
                   Link(np.array([1, 0, 0]), 250))

inputs = [0, 0, 0]
po_matrix = left_arm.get_po_matrixs(inputs)
fullscale_po_matrix = left_arm.get_fullscale_po_matrixs(inputs)
origin_po_matrixs = KinematicUtils.forward_kinematics(Config4V3.left(inputs))

print(f"{po_matrix}")
print(f"=======================================")
print(f"{fullscale_po_matrix}")
print(f"=======================================")
print(f"{origin_po_matrixs}")
