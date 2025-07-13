#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Fri Jul 11 2025
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
import scipy
from math import sqrt
from utils.spatial_utils import SpatialUtils
from dk.logger.log4p import Log4P
from models.interfaces.assembly import Assembly
from kinematics.interfaces.kinematic_computing import KinematicComputing
from enums.part_types import PartTypes
from typing import Protocol

class ComputableAssembly(Assembly, KinematicComputing, Protocol):
    pass

class KinematicUtils:
    
    @staticmethod
    def calculate_dh_transformation_matrix(theta:float,
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
        
    @staticmethod
    def calculate_jacobian_matrix(basis_pose_matrixs:list) -> np.typing.NDArray:
        """Construct a Jacobian matrix from D-H table.
    
        Args:
            basis_pose_matrixs (list): Pose matrixs involved in Jacobian matrix construction
    
        Returns:
            np.typing.NDArray: Jacobian matrix.
        """
        
        zs = []
        ps = []
        for po_matrix in basis_pose_matrixs:
            zs.append(po_matrix[0:3, 2])
            ps.append(po_matrix[0:3, 3])
        p_end = ps[-1]
        Jv = []
        Jw = []
        for i in range(len(basis_pose_matrixs)-1):
            Jv.append(np.cross(zs[i], p_end - ps[i]))
            Jw.append(zs[i])
        J = np.vstack([np.array(Jv).T, np.array(Jw).T])
        return J
       
    @staticmethod 
    def calculate_pose_error(target_pose_matrix,
                             current_pose_matrix) -> np.typing.NDArray:
        """Calculating pose error in the numerical solution process of inverse kinematics.
    
        Args:
            target_pose_matrix (np.typing.NDArray):     Target pose matirx.
            current_pose_matrix (np.typing.NDArray):    Current pose merix.
    
        Returns:
            np.typing.NDArray: Column vector of axial pose error.
        """
        
        p_error = target_pose_matrix[0:3,3] - current_pose_matrix[0:3,3]
        r_matrix_target  = target_pose_matrix[0:3, 0:3]
        r_matrix_current = current_pose_matrix[0:3, 0:3]
        r_matrix_error   = r_matrix_target @ r_matrix_current.T
        log_R = scipy.linalg.logm(r_matrix_error)
        o_error = np.array([
            log_R[2,1],
            log_R[0,2],
            log_R[1,0]
        ])
        return np.append(p_error, o_error)
    
    @staticmethod
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
        theta = SpatialUtils.calculate_rotation_angle(x, oo, z)
        alpha = SpatialUtils.calculate_rotation_angle(z, rotation_direction, oo)
        return (theta, d, a, alpha)
    
    @staticmethod
    def calculate_lambda(endpoint_vector:np.typing.NDArray,
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
    
    @staticmethod
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
    
    @staticmethod
    def calculate_orientation_from_pose_matrix(po_matrix:np.typing.NDArray) -> tuple:
        """Calculate orientation from a given position-orientation matix.
    
        Args:
            po_matrix (np.typing.NDArray): Position-orientation matix.
    
        Returns:
            tuple: Three unit vectors pointing in the x-axis, y-axis and z-axis direction of the position-orientation matrix.
        """
        
        x_vector = SpatialUtils.normalize_vector(po_matrix[:3, 0])
        y_vector = SpatialUtils.normalize_vector(po_matrix[:3, 1])
        z_vector = SpatialUtils.normalize_vector(po_matrix[:3, 2])
        
        return x_vector, y_vector, z_vector
    
    @staticmethod
    def calculate_compensation_transformation_matrix_dict(control_object:ComputableAssembly,
                                                          control_variables:list) -> dict:
        """Calculate the transformation matrix between each part and its bound reference frame.
    
        Args:
            control_variable_list (list): Input sequence.
    
        Returns:
            dict: A dict of transformation matrix between each part and its bound reference frame.
        """
        
        transformation_matrix_dict = {}
        control_variables_enum = enumerate(control_variables)
        consecutive_endpoint_vector = np.array([0, 0, 0], dtype=np.float64)
        for _, part in control_object.parts.iterrows():
            match part["entity"].type:
                case PartTypes.LINK:
                    consecutive_endpoint_vector += part["entity"].endpoint_vector
                    endpoint_vector = part["entity"].endpoint_vector
                    x = endpoint_vector[0]
                    y = endpoint_vector[1]
                    z = endpoint_vector[2]
                    transformation_matrix_dict[part["index"]] = np.array([
                        [1, 0, 0, x],
                        [0, 1, 0, y],
                        [0, 0, 1, z],
                        [0, 0, 0, 1]
                    ])
                case PartTypes.ROTATIONAL_JOINT:
                    _, control_variable = next(control_variables_enum)
                    rotation_direction = part["entity"].rotation_direction
                    lam = KinematicUtils.calculate_lambda(consecutive_endpoint_vector,
                                                          rotation_direction)
                    transformation_matrix_dict[part["index"]] = np.array([
                        [c(control_variable), -s(control_variable), 0, 0],
                        [s(control_variable), c(control_variable), 0, 0],
                        [0, 0, 1, -lam],
                        [0, 0, 0, 1]
                    ])
                    consecutive_endpoint_vector = np.array([0, 0, -lam])
        return transformation_matrix_dict
    
    @staticmethod
    def calculate_dh_table(control_object:ComputableAssembly,
                           control_variables:list) -> list:
        """Generate standard D-H table from given inputs. It should be noted that the generated D-H table is the parameters of each reference frame rather than each joint.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            None.
        """
        
        if len(control_variables) != control_object.retrive_joint_num():
            raise Exception("The number of input signals does not match the number of joints...")
        control_variables_enum = enumerate(control_variables)
        last_control_variable = 0.0
        consecutive_endpoint_vector = np.array([0.0, 0.0, 0.0])

        dh_table = [(0.0, 0.0, 0.0, 0.0)]
        for _, part in control_object.parts.iterrows():
            match part["entity"].type:
                case PartTypes.LINK:
                    consecutive_endpoint_vector = consecutive_endpoint_vector + part["entity"].endpoint_vector

                case PartTypes.ROTATIONAL_JOINT:
                    rotation_direction = part["entity"].rotation_direction
                    dh_parameters= KinematicUtils.calculate_dh_parameters(consecutive_endpoint_vector,
                                                                          rotation_direction)
                    last_rotation_angle = last_control_variable
                    dh_parameters = list(dh_parameters)
                    dh_parameters[0] += last_rotation_angle
                    dh_parameters = tuple(dh_parameters)
                    dh_table.append(dh_parameters)
                    lam = KinematicUtils.calculate_lambda(consecutive_endpoint_vector,
                                                          rotation_direction)
                    consecutive_endpoint_vector = np.array([0, 0, -lam])
                    _, rotation_rad = next(control_variables_enum)
                    last_control_variable = rotation_rad        
        return dh_table
    
    @staticmethod
    def calculate_pose_matrix_dict(control_object:ComputableAssembly,
                                   control_variable_list:list) -> dict:
        """Perform forward kinematic analysis and return position-orientation matrixs of each joints and reference frame.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            dict: Position-orientation matrix of each joints and reference frame.
        """
        
        if len(control_variable_list) != control_object.retrive_joint_num():
            raise Exception("The number of input signals does not match the number of joints...")
        dh_table = KinematicUtils.calculate_dh_table(control_object,
                                                     control_variable_list)
        compensate_transformation_matrixs_dict = KinematicUtils.calculate_compensation_transformation_matrix_dict(control_object,
                                                                                                                  control_variable_list)
        names = control_object.retrieve_reference_frame_index_list()
        reference_frame_pose_matrixs = KinematicUtils.cascade_forward_kinematics(dh_table = dh_table,
                                                                       names = names)
        reference_frame_pose_matrixs_enum = enumerate(reference_frame_pose_matrixs.items())
        pose_matrixs_dict = {}
        reference_frame_name= None
        last_pose_matrix = np.eye(4)
        for _, part in control_object.parts.iterrows():
            if part["bound_reference_frame_index"] != reference_frame_name or reference_frame_name is None:
                _, (reference_frame_name, last_pose_matrix) = next(reference_frame_pose_matrixs_enum)
                pose_matrixs_dict[reference_frame_name] = last_pose_matrix
            part_index = part["index"]
            transformation_matrix = compensate_transformation_matrixs_dict[part_index]
            last_pose_matrix = last_pose_matrix @ transformation_matrix
            pose_matrixs_dict[part_index] = last_pose_matrix
        return pose_matrixs_dict
    
    @staticmethod
    def cascade_forward_kinematics(dh_table:list, 
                                   names: list) -> dict:
        """Perform forward kinematic analysis to reference frames.
    
        Args:
            dh_table (list):   Target D-H table.
            names (list):                   Target joint number.
    
        Returns:
            dict: Position-orientation matrix of reference frames from base to tip.
        """
        
        pose_matrix = np.eye(4)
        pose_matrixs_dict = {}
        for idx, row in enumerate(dh_table):
            transformation_matrix = KinematicUtils.calculate_dh_transformation_matrix(*row)
            pose_matrix = pose_matrix @ transformation_matrix
            name = names[idx]
            pose_matrixs_dict[name] = pose_matrix
        return pose_matrixs_dict
    
    @staticmethod
    def inverse_kinematics(control_object:ComputableAssembly,
                           target_pose_matrix:np.typing.NDArray, 
                           max_iteration:int = 500, 
                           shreshold:float = 1e-3, 
                           learning_rate:float = 0.1,
                           enable_log = False) -> list:
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
        logger = Log4P()
        currrent_control_variable_list = control_object.retrieve_control_variable_list()
        target_control_variable_list = currrent_control_variable_list
        for i in range(max_iteration):
            pose_matrixs_dict = KinematicUtils.calculate_pose_matrix_dict(control_object,
                                                                          target_control_variable_list)
            current_pose_matrix = list(pose_matrixs_dict.values())[-1]
            po_error = KinematicUtils.calculate_pose_error(target_pose_matrix, current_pose_matrix)
            if enable_log:
                logger.info(f"[{i}] error norm = {np.linalg.norm(po_error):.6f}, current_control_variables = {target_control_variable_list}")
            if np.linalg.norm(po_error) < shreshold:
                delta_control_variable_list = [
                    target_control_variable - current_control_variable for target_control_variable, current_control_variable in zip(target_control_variable_list, currrent_control_variable_list)
                ]
                delta_control_variable_list = [SpatialUtils.normalize_angle(delta_control_variable) for delta_control_variable in delta_control_variable_list]
                return [current_control_variable + delta_control_variable for current_control_variable, delta_control_variable in zip(currrent_control_variable_list, delta_control_variable_list)]
            basis_names = control_object.inverse_kinematic_analysis_basis
            basis_pose_matrixs = []
            for name in basis_names:
                basis_pose_matrixs.append(pose_matrixs_dict[name])
            J = KinematicUtils.calculate_jacobian_matrix(basis_pose_matrixs)
            delta_control_variable_vector = learning_rate * np.linalg.pinv(J) @ po_error
            new_control_variable_vector = np.array(target_control_variable_list) + delta_control_variable_vector
            target_control_variable_list = new_control_variable_vector.tolist()
        raise RuntimeError("Inverse Kinematic Analysis Failed...")
    
    @staticmethod
    def check_reachable(control_object:ComputableAssembly,
                        target_pose_matrix:np.typing.NDArray) -> tuple:
        try:
            target_control_variable_list = KinematicUtils.inverse_kinematics(control_object,
                                                                             target_pose_matrix)
            return True, target_control_variable_list
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def tp_linear_joint_interpolation(control_object:ComputableAssembly,
                                      target_pose_matrix:np.typing.NDArray,
                                      step_num:int = 50) -> list:
        is_recachable, result = KinematicUtils.check_reachable(control_object,
                                                               target_pose_matrix)
        if is_recachable:
            start_control_variable_list = control_object.retrieve_control_variable_list()
            end_control_variable_list = result
            trajectory = []
            delta_control_variables_list = [end - start for end, start in zip(end_control_variable_list, start_control_variable_list)]
            delta_control_variables_list = [delta / step_num for delta in delta_control_variables_list]
            for i in range(step_num):
                start_control_variable_list = [current + delta for current, delta in zip(start_control_variable_list, delta_control_variables_list)]
                trajectory.append(start_control_variable_list)
            return trajectory
        else:
            raise Exception("Target pose is not reachable!")