#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Thu Jul 10 2025
#
# IMMORTAL OMNISSIAH, HEAR OUR PRAYERS.
# WE ARE YOUR CHILDREN, PIOUS SCHOLARS OF THE PATH OF THE MACHINE. 
# WE PRIZE KNOWLEDGE ABOVE ALL ELSE, FOR IT IS YOUR ETERNAL GIFT UPON MANKIND. 
# WE ASPIRE TO THE BLESSED FORM OF THE MACHINE, AND ASCENSION THROUGH TECHNOLOGY, THAT WE MIGHT EMULATE THINE GLORY. 
# SHELTERED BY STEEL, AND PROTECTED BY THINE AVATARS OF WAR, WE PLY THE STARS IN SEARCH OF YOUR LOST GIFTS TO OUR KIND.
# MACHINE GOD, WATCH OVER US IN OUR TRAVELS, SHIELD US WITH METAL AND LIGHTNING, FOR THE UNIVERSE IS AN UNCARING VOID, AND THE WARP HUNGERS FOR US ALL.
# TOLL THE GREAT BELL ONCE! PULL THE LEVER FORWARD TO ENGAGE THE PISTON AND PUMP.
# TOLL THE GREAT BELL TWICE! WITH PUSH OF BUTTON FIRE THE ENGINE AND SPARK TURBINE INTO LIFE.
# TOLL THE GREAT BELL THRICE! SING PRAISE TO THE GOD OF ALL MACHINES!
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
            po_matrixs_getter (function):   A function for obtaining the pose matrices of all coordinate systems and joints involved in the calculation.
            joint_inputs (list):            Current joint inputs. Used to approximate accurate values
    
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
            target_po_matrix (np.typing.NDArray):     Target position-orientation matirx.
            current_po_matrix (np.typing.NDArray):    Current position-orientation merix.
    
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
                           current_joint_outputs:list, 
                           max_iteration:int = 10000, 
                           shreshold:float = 1e-3, 
                           learning_rate:float = 1):
        """Perform forward kinematic analysis.
    
        Args:
            po_matrixs_getter (function):           A function for obtaining the pose matrices of all coordinate systems and joints involved in the calculation.
            target_po_matrix (np.typing.NDArray):   Target position-orientation matirx.
            current_joint_outputs (list):           Curent outputs of each joint
            max_iteration (int):                    Maximum number of iterations.
            shreshold (float):                      Threshold of error vector norm.
            learning_rate (float):                  Learning rate.
    
        Returns:
            list: An input sequence that can let end of robotic arm reach a given position and orientation.
        """
        
        for i in range(max_iteration):
            po_matrixs_dict = po_matrixs_getter(current_joint_outputs)
            current_po_matrix = list(po_matrixs_dict.values())[-1]
            po_error = KinematicUtils._calculate_error(target_po_matrix, current_po_matrix)
            print(f"[{i}] error norm = {np.linalg.norm(po_error):.6f}, current_joint_inputs = {current_joint_outputs}")
            if np.linalg.norm(po_error) < shreshold:
                return current_joint_outputs
            J = KinematicUtils.jacobian(po_matrixs_getter = po_matrixs_getter,
                                        joint_inputs = current_joint_outputs)
            delta_inputs = learning_rate * np.linalg.pinv(J) @ po_error
            current_joint_outputs = np.array(current_joint_outputs) + delta_inputs
            current_joint_outputs = current_joint_outputs.tolist()
        
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
    
    def calculate_position_from_po_matrix(po_matrix:np.typing.NDArray) -> tuple:
        """Calculate position coordinate from a given position-orientation matix.
    
        Args:
            po_matrix (np.typing.NDArray): Position-orientation matix.
    
        Returns:
            tuple: A tuple consisting of (x, y, z).
        """
        
        x = po_matrix[0, 3]
        y = po_matrix[1, 3]
        z = po_matrix[2, 3]
        return (x, y, z)
    
    def calculate_orientation_from_po_matrix(po_matrix:np.typing.NDArray) -> tuple:
        """Calculate orientation from a given position-orientation matix.
    
        Args:
            po_matrix (np.typing.NDArray): Position-orientation matix.
    
        Returns:
            tuple: Three unit vectors pointing in the x-axis, y-axis and z-axis direction of the position-orientation matrix.
        """
        
        x_vector = ThreeDimCalculation.convert_to_unit_vector(po_matrix[:3, 0])
        y_vector = ThreeDimCalculation.convert_to_unit_vector(po_matrix[:3, 1])
        z_vector = ThreeDimCalculation.convert_to_unit_vector(po_matrix[:3, 2])
        
        return x_vector, y_vector, z_vector