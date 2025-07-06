import numpy as np
from numpy import sin as s, cos as c

def _dh_transform(theta, d, a, alpha):
    return np.array([
        [c(theta), -s(theta)*c(alpha), s(theta)*s(alpha), a*c(theta)],
        [s(theta), c(theta)*c(alpha), -c(theta)*s(alpha), a*s(theta)],
        [0, s(alpha), c(alpha), d],
        [0, 0, 0, 1]
    ])

def forward_kinematics(dh_table):
    T = np.eye(4)
    for row in dh_table:
        Ti = _dh_transform(*row)
        T = T @ Ti
    return T

def jacobian(dh_table):
    Ts = [np.eye(4)]
    for row in dh_table:
        Ti= _dh_transform(*row)
        Ts.append(Ts[-1] @ Ti)
    zs = []
    ps = []
    for T in Ts:
        zs.append(T[0:3, 2])
        ps.append(T[0:3, 3])
    
    p_end = ps[-1]
    Jv = []
    Jw = []

    for i in range(3):
        Jv.append(np.cross(zs[i], p_end - ps[i]))
        Jw.append(zs[i])

    J = np.vstack([np.array(Jv).T, np.array(Jw).T])
    return J

