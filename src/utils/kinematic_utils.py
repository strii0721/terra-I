import numpy as np
from numpy import sin as s, cos as c
from math import sqrt
import scipy
from utils.three_dim_calculation import ThreeDimCalculation

class KinematicUtils:

    def _dh_transform(theta, 
                      d, 
                      a, 
                      alpha):
        """Construct a transformation matrix that has undergone theta, d, a, and alpha transformations.
    
        Args:
            theta (float):  Rotation angle around the z-axis.
            d (float):      Translation distance along the z-axis.
            a (float):      Translation distance along the x-axis.
            alpha (float):  Rotation angle around the x-axis
    
        Returns:
            np.array(list): Transformation matrix for a single row in D-H table.
        """
        return np.array([
            [c(theta), -s(theta)*c(alpha), s(theta)*s(alpha), a*c(theta)],
            [s(theta), c(theta)*c(alpha), -c(theta)*s(alpha), a*s(theta)],
            [0, s(alpha), c(alpha), d],
            [0, 0, 0, 1]
        ], dtype = np.float64)
    
    def forward_kinematics(dh_table, 
                           joint_no = None):
        """Perform forward kinematic analysis.
    
        Args:
            dh_table (np.array(list)):  Target D-H table.
            joint_no (int):            Target joint number.
    
        Returns:
            np.array(list): position-orientation matrix of target joint.
        """
        
        if joint_no is None: joint_no = len(dh_table)
        T = np.eye(4)
        for idx, row in enumerate(dh_table):
            Ti = KinematicUtils._dh_transform(*row)
            T = T @ Ti
            if idx + 1 == joint_no: return T
        return T
    
    # def damped_pinv(J, damping=0.01):
    #     JT = J.T
    #     return JT @ np.linalg.inv(J @ JT + (damping ** 2) * np.eye(J.shape[0]))
    
    def jacobian(dh_table):
        """Construct a Jacobian matrix from D-H table.
    
        Args:
            dh_table (np.array(list)):  Target D-H table.
    
        Returns:
            np.array(list): Jacobian matrix.
        """
        
        joints_num = dh_table.shape[0]
        Ts = [np.eye(4)]
        # for row in dh_table:
        #     Ti= _dh_transform(*row)
        #     Ts.append(Ts[-1] @ Ti)
        for idx in range(joints_num):
            Ts.append(KinematicUtils.forward_kinematics(dh_table = dh_table, 
                                         joint_no = idx + 1))
        zs = []
        ps = []
        for T in Ts:
            zs.append(T[0:3, 2])
            ps.append(T[0:3, 3])
        p_end = ps[-1]
        Jv = []
        Jw = []
        for i in range(1, joints_num):
            Jv.append(np.cross(zs[i], p_end - ps[i]))
            Jw.append(zs[i])
        J = np.vstack([np.array(Jv).T, np.array(Jw).T])
        return J
    
    def _calculate_error(po_target, 
                   po_current):
        """Calculating position-orientation error in the numerical solution process of inverse kinematics.
    
        Args:
            po_target (np.array(list)):     Target position-orientation matirx.
            po_current (np.array(list)):    Current position-orientation merix.
    
        Returns:
            np.array(list): Column vector of axial position-orientation error.
        """
        p_error = po_target[0:3,3] - po_current[0:3,3]
        r_matrix_target  = po_target[0:3, 0:3]
        r_matrix_current = po_current[0:3, 0:3]
        r_matrix_error   = r_matrix_target @ r_matrix_current.T
        log_R = scipy.linalg.logm(r_matrix_error)
        o_error = np.array([
            log_R[2,1],
            log_R[0,2],
            log_R[1,0]
        ])
        # return np.vstack((p_error, o_error))
        return np.append(p_error, o_error)
    
    def inverse_kinematics(dh_table_config, 
                           po_target, 
                           angles_init, 
                           max_iters = 10000, 
                           shreshold = 1e-3, 
                           learning_rate = 0.01):
        """Perform forward kinematic analysis.
    
        Args:
            dh_table_config (function):     Config function of D-H table.
            po_target (np.array(list)):     Target position-orientation matirx.
            angles_init (list):             Initial angles of each joints
            max_iters (int):                Maximum number of iterations.
            shreshold (float):              Threshold of error vector norm.
            learning_rate (float):          Learning rate.
    
        Returns:
            np.array(list): Column vector of axial position-orientation error.
        """
        
        angles_current = np.array(angles_init, dtype=np.float64)
        for i in range(max_iters):
            dh_table = dh_table_config(angles_current)
            po_current = KinematicUtils.forward_kinematics(dh_table)
            po_error = KinematicUtils._calculate_error(po_target, po_current)
            # p_error, o_error = cal_error(po_target, po_current)
            # po_error = np.vstack((p_error, o_error))
            print(f"[{i}] error norm = {np.linalg.norm(po_error):.6f}, angle = {angles_current}")
            if np.linalg.norm(po_error) < shreshold:
                return angles_current
            J = KinematicUtils.jacobian(dh_table)
            # Jv = J[0:3, :]
            # delta_angles = learning_rate * damped_pinv(Jv, damping=0.1) @ error
            delta_angles = learning_rate * np.linalg.pinv(J) @ po_error
            angles_current += delta_angles
        
        raise RuntimeError("Inverse Kinematic Analysis Failed...")
    
    def calculate_dh_parameters(endpoint_vector,
                                rotation_direction):
        """Perform standard D-H analysis with a relative joint coordinate and rotation direction. Generate standard D-H parameters: theta, d, a, alpha.
    
        Args:
            endpoint_vector (np.array(list)):       A vector pointing from the previous joint to the current joint, i.e. the coordinates of current joint relative to the previous reference frame.
            rotation_direction (np.array(list)):    Vector of joint rotation direction。
    
        Returns:
            tuple: Standard D-H parameters: theta, d, a, alpha.
        """
        
        x_p, y_p, z_p = endpoint_vector
        x_r, y_r, z_r = rotation_direction
        
        if x_r**2 + y_r**2 == 0:
            d = 0
            lam = -(x_p * x_r + y_p * y_r + z_p * z_r)/(x_r**2 + y_r**2 + z_r**2)
        else:
            d = z_p - z_r * (x_p * x_r + y_p * y_r)/(x_r**2 + y_r**2)
            lam = - (x_p * x_r + y_p * y_r)/(x_r**2 + y_r**2)
            
        a = sqrt((x_p + lam * x_r)**2 + (y_p + lam * y_r)**2 + (z_p + lam * z_r - d)**2)
        oo = np.array([x_p + lam * x_r, y_p + lam * y_r, z_p + lam * z_r - d])
        x = np.array([1, 0, 0])
        z = np.array([0, 0, 1])
        theta = ThreeDimCalculation.calculate_rotation_angle_rad(x, oo, z)
        alpha = ThreeDimCalculation.calculate_rotation_angle_rad(z, rotation_direction, oo)
        return theta, d, a, alpha