#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Thu Jul 10 2025
#
# Copyright (c) 2025 S.I.C.
#

import numpy as np
from numpy import sin as s, cos as c
from math import sqrt
import scipy
from scipy.spatial.transform import Rotation as R
from utils.three_dim_calculation import ThreeDimCalculation

class KinematicUtils:

    def get_dh_transformation_matrix(theta:float,
                                     d:float,
                                     a:float,
                                     alpha:float) -> np.typing.NDArray:
        """Construct a transformation matrix that has undergone theta, d, a, and alpha transformations.
    
        Args:
            theta (float):  Rotation angle around the z-axis.
            d (float):      Translation distance along the z-axis.
            a (float):      Translation distance along the x-axis.
            alpha (float):  Rotation angle around the x-axis
    
        Returns:
            np.typing.NDArray: Transformation matrix for a single row in D-H table.
        """
        return np.array([
            [c(theta), -s(theta)*c(alpha), s(theta)*s(alpha), a*c(theta)],
            [s(theta), c(theta)*c(alpha), -c(theta)*s(alpha), a*s(theta)],
            [0, s(alpha), c(alpha), d],
            [0, 0, 0, 1]
        ], dtype = np.float64)
    
    def forward_kinematics(dh_table:list, 
                           names: list | None = None) -> dict:
        """Perform forward kinematic analysis to reference frames.
    
        Args:
            dh_table (list):   Target D-H table.
            names (list):                   Target joint number.
    
        Returns:
            dict: Position-orientation matrix of reference frames from base to tip.
        """
        
        T = np.eye(4)
        po_matrixs = {}
        for idx, row in enumerate(dh_table):
            Ti = KinematicUtils.get_dh_transformation_matrix(*row)
            T = T @ Ti
            if names is None: 
                name = str(idx)
            else:
                if idx == len(names):
                    name = "enf"
                else:
                    name = names[idx]
            po_matrixs[name] = T
        return po_matrixs
    
    def jacobian(po_matrixs_getter,
                 joint_inputs:list) -> np.typing.NDArray:
        """Construct a Jacobian matrix from D-H table.
    
        Args:
            dh_table (np.typing.NDArray):  Target D-H table.
    
        Returns:
            np.typing.NDArray: Jacobian matrix.
        """
        
        po_matrixs_dict = po_matrixs_getter(joint_inputs)
        po_matrixs = list(po_matrixs_dict.values())
        zs = []
        ps = []
        for po_matrix in po_matrixs:
            zs.append(po_matrix[0:3, 2])
            ps.append(po_matrix[0:3, 3])
        p_end = ps[-1]
        Jv = []
        Jw = []
        for i in range(len(po_matrixs)-1):
            Jv.append(np.cross(zs[i], p_end - ps[i]))
            Jw.append(zs[i])
        J = np.vstack([np.array(Jv).T, np.array(Jw).T])
        return J
    
    def _calculate_error(target_po_matrix,
                         current_po_matrix):
        """Calculating position-orientation error in the numerical solution process of inverse kinematics.
    
        Args:
            po_target (np.typing.NDArray):     Target position-orientation matirx.
            po_current (np.typing.NDArray):    Current position-orientation merix.
    
        Returns:
            np.typing.NDArray: Column vector of axial position-orientation error.
        """
        
        p_error = target_po_matrix[0:3,3] - current_po_matrix[0:3,3]
        r_matrix_target  = target_po_matrix[0:3, 0:3]
        r_matrix_current = current_po_matrix[0:3, 0:3]
        r_matrix_error   = r_matrix_target @ r_matrix_current.T
        log_R = scipy.linalg.logm(r_matrix_error)
        o_error = np.array([
            log_R[2,1],
            log_R[0,2],
            log_R[1,0]
        ])
        return np.append(p_error, o_error)
    
    def inverse_kinematics(po_matrixs_getter, 
                           target_po_matrix:np.typing.NDArray, 
                           current_joint_inputs:list, 
                           max_iteration:int = 10000, 
                           shreshold:float = 1e-3, 
                           learning_rate:float = 0.1):
        """Perform forward kinematic analysis.
    
        Args:
            po_matrixs_getter (function):   Config function of D-H table.
            po_target (np.typing.NDArray):  Target position-orientation matirx.
            angles_current (list):          Initial angles of each joints
            max_iters (int):                Maximum number of iterations.
            shreshold (float):              Threshold of error vector norm.
            learning_rate (float):          Learning rate.
    
        Returns:
            np.typing.NDArray: Column vector of axial position-orientation error.
        """
        
        for i in range(max_iteration):
            po_matrixs_dict = po_matrixs_getter(current_joint_inputs)
            current_po_matrix = list(po_matrixs_dict.values())[-1]
            po_error = KinematicUtils._calculate_error(target_po_matrix, current_po_matrix)
            print(f"[{i}] error norm = {np.linalg.norm(po_error):.6f}, current_joint_inputs = {current_joint_inputs}")
            if np.linalg.norm(po_error) < shreshold:
                return current_joint_inputs
            J = KinematicUtils.jacobian(po_matrixs_getter = po_matrixs_getter,
                                        joint_inputs = current_joint_inputs)
            delta_inputs = learning_rate * np.linalg.pinv(J) @ po_error
            current_joint_inputs = np.array(current_joint_inputs) + delta_inputs
            current_joint_inputs = current_joint_inputs.tolist()
        
        raise RuntimeError("Inverse Kinematic Analysis Failed...")
    
    def calculate_dh_parameters(endpoint_vector:np.typing.NDArray,
                                rotation_direction:np.typing.NDArray) -> tuple:
        """Perform standard D-H analysis with a relative joint coordinate and rotation direction. Generate standard D-H parameters: theta, d, a, alpha. Please refer to the documentation in the docs folder in the project root directory for the formula derivation.
    
        Args:
            endpoint_vector (np.typing.NDArray):       A vector pointing from the previous joint to the current joint, i.e. the coordinates of current joint relative to the previous reference frame.
            rotation_direction (np.typing.NDArray):    Vector of joint rotation direction.
    
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
        return (theta, d, a, alpha)
    
    def calculate_lam(endpoint_vector:np.typing.NDArray,
                      rotation_direction:np.typing.NDArray) -> float:
        """Calculate lam in the process of automatically confirming reference frame. lam is very important in the process of calibrating the current reference system position, and lam is needed to eliminate the influence of movement in the z-axis direction.
    
        Args:
            endpoint_vector (np.typing.NDArray):       A vector pointing from the previous joint to the current joint, i.e. the coordinates of current joint relative to the previous reference frame.
            rotation_direction (np.typing.NDArray):    Vector of joint rotation direction.
    
        Returns:
            float: The distance between the origin of the reference system on the next joint and the actual joint on the z-axis of that reference system (distinguishing between positive and negative).
        """
        x_p, y_p, z_p = endpoint_vector
        x_r, y_r, z_r = rotation_direction
        
        if x_r**2 + y_r**2 == 0:
            lam = -(x_p * x_r + y_p * y_r + z_p * z_r)/(x_r**2 + y_r**2 + z_r**2)
        else:
            lam = - (x_p * x_r + y_p * y_r)/(x_r**2 + y_r**2)
        return lam