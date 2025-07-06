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

# def damped_pinv(J, damping=0.01):
#     JT = J.T
#     return JT @ np.linalg.inv(J @ JT + (damping ** 2) * np.eye(J.shape[0]))

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

    for i in range(1, 4):
        Jv.append(np.cross(zs[i], p_end - ps[i]))
        Jw.append(zs[i])

    J = np.vstack([np.array(Jv).T, np.array(Jw).T])
    return J

def damped_pinv(J, damping=0.01):
    JT = J.T
    return JT @ np.linalg.inv(J @ JT + (damping ** 2) * np.eye(J.shape[0]))

def inverse_kinematics(dh_table_config, po_target, angles_init, 
                       max_iters=10000, tol=1e-3, learning_rate=0.01):
    angles_current = np.array(angles_init)
    for i in range(max_iters):
        dh_table = dh_table_config(angles_current)
        po_current = forward_kinematics(dh_table)
        error = po_target[0:3,3] - po_current[0:3,3]
        print(f"[{i}] error norm = {np.linalg.norm(error):.6f}, angle = {angles_current}")
        if np.linalg.norm(error) < tol:
            return angles_current
        J = jacobian(dh_table)
        Jv = J[0:3, :]
        # delta_angles = learning_rate * np.linalg.pinv(Jv) @ error
        delta_angles = learning_rate * damped_pinv(Jv, damping=0.1) @ error
        # Jv_pinv = damped_pinv(Jv)
        # d_angles = learning_rate * Jv_pinv @ error[0:3,3]
        angles_current += delta_angles
    
    raise RuntimeError("Inverse Kinematic Analysis Failed...")
