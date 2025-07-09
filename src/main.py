import kinematics.dh_tables as dh_tables
from utils.kinematic_utils import KinematicUtils
from utils.three_dim_calculation import ThreeDimCalculation

import numpy as np

# angles_init = [0, 0, pi]
# angles = [0, 0, -pi/2]

# po_target = kcal.forward_kinematics(dh_tables.Config4V3.left(angles))

# angles_target = kcal.inverse_kinematics(dh_tables.Config4V3.left,
#                                         po_target,
#                                         angles_init)

# print(f"{angles_target}")
# logger = Log4P()
# logger.info("test")

# joint = Joint([5,5,5])

# print(joint.axis_direction)

endpoint_vector = np.array([0, 0, 0])
direction_vector = ThreeDimCalculation.convert_to_unit_vector(np.array([0, 1, 1]))

theta, d, a, alpha = KinematicUtils.calculate_dh_parameters(endpoint_vector, 
                                              direction_vector)
print(f"theta={theta}, d={d}, a={a}, alpha={alpha}")