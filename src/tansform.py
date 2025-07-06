import numpy as np
from numpy import sin as s, cos as c
from dh_tables import config4_v3
from math import pi

def dh_transform(theta, d, a, alpha):
    return np.array([
        [c(theta), -s(theta)*c(alpha), s(theta)*s(alpha), a*c(theta)],
        [s(theta), c(theta)*c(alpha), -c(theta)*s(alpha), a*s(theta)],
        [0, s(alpha), c(alpha), d],
        [0, 0, 0, 1]
    ])

def foward_kinematics(dh_table):
    T = np.eye(4)
    for row in dh_table:
        Ti = dh_transform(*row)
        T = T @ Ti
    return T

if __name__ == "__main__":
    input = config4_v3.left(0, 0, pi)
    T = foward_kinematics(input)
    print(f"{T}")
    