import numpy as np
from numpy import sin as s, cos as c
import kinematics.dh_tables as dh_tables
from math import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def _dh_transform(theta, d, a, alpha):
    return np.array([
        [c(theta), -s(theta)*c(alpha), s(theta)*s(alpha), a*c(theta)],
        [s(theta), c(theta)*c(alpha), -c(theta)*s(alpha), a*s(theta)],
        [0, s(alpha), c(alpha), d],
        [0, 0, 0, 1]
    ])

def _foward_kinematics(dh_table):
    T = np.eye(4)
    for row in dh_table:
        Ti = _dh_transform(*row)
        T = T @ Ti
    return T

def forward_kinematics(angles_rad, dh_table):
    angles_rad = angles_rad + [0] * (6 - len(angles_rad))
    angles_rad_left = angles_rad[:3]
    angles_rad_right = angles_rad[3:]
    T_left = _foward_kinematics(dh_table.left(*angles_rad_left))
    T_right = _foward_kinematics(dh_table.right(*angles_rad_right))
    return T_left, T_right
    