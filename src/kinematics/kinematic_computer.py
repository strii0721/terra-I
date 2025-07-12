#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Sat Jul 12 2025
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
from enums.part_types import PartTypes
from utils.kinematic_utils import KinematicUtils
from numpy import sin as s, cos as c
from dk.logger.log4p import Log4P
from models.robotic_arm import RoboticArm

class KinematicComputer:
    
    def calculate_compensation_transformation_matrix(self,
                                                     control_object:RoboticArm,
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
    
    def calculate_dh_table(self,
                           control_object:RoboticArm,
                           control_variables:list) -> list:
        """Generate standard D-H table from given inputs. It should be noted that the generated D-H table is the parameters of each reference frame rather than each joint.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            None.
        """
        
        if len(control_variables) != control_object.retrive_control_variables_num():
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
    
    def calculate_pose_matrixs(self,
                               control_object:RoboticArm,
                               control_variables:list) -> dict:
        """Perform forward kinematic analysis and return position-orientation matrixs of each joints and reference frame.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            dict: Position-orientation matrix of each joints and reference frame.
        """
        
        if len(control_variables) != control_object.retrive_control_variables_num():
            raise Exception("The number of input signals does not match the number of joints...")
        dh_table = self.calculate_dh_table(control_object,
                                           control_variables)
        compensate_transformation_matrixs_dict = self.calculate_compensation_transformation_matrix(control_object,
                                                                                                   control_variables)
        names = control_object.retrieve_reference_frame_indexs()
        reference_frame_pose_matrixs = self.cascade_forward_kinematics(dh_table = dh_table,
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
    
    def cascade_forward_kinematics(self,
                                   dh_table:list, 
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
    
    def inverse_kinematics(self,
                           control_object:RoboticArm,
                           target_pose_matrix:np.typing.NDArray, 
                           current_control_variables:list, 
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
        logger = Log4P()
        for i in range(max_iteration):
            pose_matrixs_dict = self.calculate_pose_matrixs(control_object,
                                                            current_control_variables)
            current_pose_matrix = list(pose_matrixs_dict.values())[-1]
            po_error = KinematicUtils.calculate_pose_error(target_pose_matrix, current_pose_matrix)
            logger.info(f"[{i}] error norm = {np.linalg.norm(po_error):.6f}, current_control_variables = {current_control_variables}")
            if np.linalg.norm(po_error) < shreshold:
                return current_control_variables
            basis_names = control_object.inverse_kinematic_analysis_basis
            basis_pose_matrixs = []
            for name in basis_names:
                basis_pose_matrixs.append(pose_matrixs_dict[name])
            J = KinematicUtils.calculate_jacobian_matrix(basis_pose_matrixs)
            delta_control_variables = learning_rate * np.linalg.pinv(J) @ po_error
            new_control_variables = np.array(current_control_variables) + delta_control_variables
            current_control_variables = new_control_variables.tolist()
        raise RuntimeError("Inverse Kinematic Analysis Failed...")