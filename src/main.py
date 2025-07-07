import kinematics.dh_tables as dh_tables
import kinematics.calculation as kcal
from math import pi

angles_init = [0, 0, -pi]
angles = [0, 0, -3*pi/2]

po_target = kcal.forward_kinematics(dh_tables.Config4V3.left(angles))

angles_target = kcal.inverse_kinematics(dh_tables.Config4V3.left,
                                        po_target,
                                        angles_init)

print(f"{angles_target}")