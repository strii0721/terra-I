#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Wed Jul 16 2025
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
from utils.spatial_utils import SpatialUtils
from models.kinematic_computable_assembly import KinematicComputableAssembly
from kinematics.utils.kinematic_utils import KinematicUtils
from models.enums.part_types import PartTypes
from typing import cast
from models.part import Part
from models.impl.link import Link
from models.impl.rotational_joint import RotationalJoint
from math import pi

class DynamicUtils():
    
    @staticmethod
    def calculate_angular_velocity_list(control_interval:float, 
                                        control_variable_list_0:list, 
                                        control_variable_list_1:list) -> list:
        """Calculate angular velocity of all rotational joints given a set of control varliable list (2 control loops)

        Args:
            control_interval (float):           Control interval
            control_variable_list_0 (list):     1st control_variable_list
            control_variable_list_1 (list):     2st control_variable_list
            
        Returns:
            list: a list of angular velocity of each rotational joint
        """
        
        angular_velocity_list = (np.array(control_variable_list_1) - np.array(control_variable_list_0)) / control_interval
        
        return angular_velocity_list.tolist()
    
    @staticmethod
    def calculate_angular_acceleration_list(control_interval:float, 
                                            control_variable_list_0:list, 
                                            control_variable_list_1:list, 
                                            control_variable_list_2:list) -> list:
        """Calculate angular acceleration of all rotational joints given a set of control varliable list (3 control loops)

        Args:
            control_interval (float): Control interval
            control_variable_list_0 (list): 1st control_variable_list
            control_variable_list_1 (list): 2st control_variable_list
            control_variable_list_2 (list): 2nd control_variable_list

        Returns:
            list: a list of angular acceleration of each rotational joint
        """        
        
        angular_velocity_list_0 = DynamicUtils.calculate_angular_velocity_list(control_interval,
                                                                          control_variable_list_0,
                                                                          control_variable_list_1)
        angular_velocity_list_1 = DynamicUtils.calculate_angular_velocity_list(control_interval,
                                                                          control_variable_list_1,
                                                                          control_variable_list_2)
        angular_acceleration_list = (np.array(angular_velocity_list_1) - np.array(angular_velocity_list_0) / control_interval)
        angular_acceleration_list = angular_acceleration_list / pi * 180
        
        return angular_acceleration_list.tolist()
    
    @staticmethod
    def calculate_link_inertia(joint_coordinate:tuple, 
                               rotation_direction:np.typing.NDArray,
                               link_coordinate_start:tuple,
                               link_coordinate_end:tuple,
                               link_rho:float,
                               link_sectional_area:float) -> float:
        """Calculate Inertia of a link spinning around a rotational joint. The moment of inertia of any thin rod rotating around any axis in space can be calculated using analytical geometry. The formula can be found in numerous references.

        Args:
            rotation_direction (np.typing.NDArray): A vector pointing to the rotation direction.
            link_coordinate_start (tuple): 3d coordinate of the startpoint of link.
            link_coordinate_end (tuple): 3d coordinate of the endpoint of link.
            link_rho (float): Rho of link material.
            link_area (float): Cross-sectional area of link.

        Returns:
            float: Inertia of the link on rotational joint.
        """
        
        joint_vector = np.array(joint_coordinate)
        link_start_vector = np.array(link_coordinate_start) - joint_vector
        link_end_vector = np.array(link_coordinate_end) - joint_vector
        rotation_direction_unit_vector = SpatialUtils.normalize_vector(rotation_direction)
        link_centre_vector = (link_start_vector + link_end_vector) / 2
        link_vector = link_end_vector - link_start_vector
        link_unit_vector = SpatialUtils.normalize_vector(link_vector)
        l = np.linalg.norm(link_vector)
        m = link_sectional_area * l * link_rho  
        d_vector = np.dot(rotation_direction_unit_vector, link_centre_vector) * rotation_direction_unit_vector - link_centre_vector
        d = np.linalg.norm(d_vector)
        inertia = (1 / 12) * m * l**2 * ( 1 - np.dot(link_unit_vector, rotation_direction_unit_vector)**2) + m * d**2
        return float(inertia)
        
        
    
    @staticmethod
    def calculate_particle_inertia(joint_coordinate:tuple,
                                   rotation_direction:np.typing.NDArray, 
                                   particle_coordinate:tuple, 
                                   mass:float) -> float:
        """Calculate Inertia of a particle spinning around a rotational joint. 

        Args:
            joint_coordinate (tuple): 3d coordinate of the rotational joint.
            rotation_direction (np.typing.NDArray): A vector pointing to the rotation direction.
            particle_coordinate (tuple): 3d coordinate of the particle.
            mass (float): mass of the particle.

        Returns:
            float: Inertia of the particle on rotational joint.
        """        
        
        joint_vector = np.array(joint_coordinate)
        particle_vector = np.array(particle_coordinate) - joint_vector
        rotation_direction_unit_vector = SpatialUtils.normalize_vector(rotation_direction)
        d_vector = np.dot(rotation_direction_unit_vector, particle_vector) * rotation_direction_unit_vector - particle_vector
        d = np.linalg.norm(d_vector)
        inertia = mass * d**2
        return float(inertia)
    
    @staticmethod
    def calculate_link_gravity_torque(joint_coordinate:tuple, 
                                      rotation_direction:np.typing.NDArray,
                                      link_coordinate_start:tuple,
                                      link_coordinate_end:tuple,
                                      link_rho:float,
                                      link_sectional_area:float,
                                      impact_factor:float = 0) -> float:
        
        gravity_vector = np.array([0, 0, -1])
        g = 9.8
        joint_vector = np.array(joint_coordinate)
        rotation_direction_unit_vector = SpatialUtils.normalize_vector(rotation_direction)
        link_vector_start = np.array(link_coordinate_start)
        link_vector_end = np.array(link_coordinate_end)
        link_vector_centre = (link_vector_end - link_vector_start) / 2
        l = np.linalg.norm(link_vector_end - link_vector_start)
        mass = l * link_sectional_area * link_rho
        r = link_vector_centre - joint_vector
        F = mass * gravity_vector * g
        torque_vector = np.cross(r, F)
        torque = np.dot(torque_vector, rotation_direction_unit_vector)
        return torque * impact_factor
        
    @staticmethod
    def calculate_particle_gravity_torque(joint_coordinate:tuple, 
                                          rotation_direction:np.typing.NDArray,
                                          particle_coordinate:tuple,
                                          mass:float,
                                          impact_factor:float = 0) -> float:
        
        gravity_vector = np.array([0, 0, -1])
        g = 9.8
        joint_vector = np.array(joint_coordinate)
        particle_vector = np.array(particle_coordinate)
        rotation_direction_unit_vector = SpatialUtils.normalize_vector(rotation_direction)
        r = particle_vector - joint_vector
        F = mass * gravity_vector * g
        torque_vector = np.cross(r, F)
        torque = np.dot(torque_vector, rotation_direction_unit_vector)
        return torque * impact_factor
    
    @staticmethod
    def calculate_inertia_list(control_object:KinematicComputableAssembly,
                               control_variable_list:list) -> list:
        """Calcule inertia on each rotational joint with given input control variable list.

        Args:
            control_object (KinematicComputableAssembly): Analysis target.
            control_variable_list (list): Input control variable list.

        Returns:
            list: Inertia list on each joint.
        """        
        
        inertia_list = []
        pose_matrix_dict = KinematicUtils.calculate_pose_matrix_dict(control_object, 
                                                                     control_variable_list)
        part_index_list = control_object.retrieve_part_index_list()
        part_index_list_enum = enumerate(part_index_list)
        for index, part_index in part_index_list_enum:
            part = control_object.parts.loc[control_object.parts["index"] == part_index, ["entity"]].iloc[0, 0]
            part = cast(Part, part)
            if part.type == PartTypes.ROTATIONAL_JOINT:
                if index != len(part_index_list) - 1:
                    part_index_list_subsequent = part_index_list[index + 1:]
                    inertia = 0
                    joint_coordinate = KinematicUtils.calculate_position_from_pose_matrix(pose_matrix_dict[part_index])
                    rotation_direction = KinematicUtils.calculate_orientation_from_pose_matrix(pose_matrix_dict[part_index])[-1]
                    coordinate_last = coordinate_current = joint_coordinate
                    for part_index_subsequent in part_index_list_subsequent:
                        part_subsequent = control_object.parts.loc[control_object.parts["index"] == part_index_subsequent, ["entity"]].iloc[0, 0]
                        part_subsequent = cast(Part, part_subsequent)
                        pose_matrix = pose_matrix_dict[part_index_subsequent]
                        coordinate_current = KinematicUtils.calculate_position_from_pose_matrix(pose_matrix)
                        match part_subsequent.type:
                            case PartTypes.LINK:
                                part_subsequent = cast(Link, part_subsequent)
                                
                                inertia += DynamicUtils.calculate_link_inertia(joint_coordinate, 
                                                                               rotation_direction,
                                                                               coordinate_last, 
                                                                               coordinate_current,
                                                                               part_subsequent.rho,
                                                                               part_subsequent.sectional_area)
                                coordinate_last = coordinate_current
                            case PartTypes.ROTATIONAL_JOINT:
                                part_subsequent = cast(RotationalJoint, part_subsequent)
                                inertia += DynamicUtils.calculate_particle_inertia(joint_coordinate, 
                                                                                   rotation_direction,
                                                                                   coordinate_current,
                                                                                   part_subsequent.mass)
                                coordinate_last = coordinate_current
                    inertia_list.append(inertia)
        return inertia_list
    
    @staticmethod
    def calculate_gravity_torque_list(control_object:KinematicComputableAssembly, 
                                      control_variable_list:list,
                                      impact_factor:float = 0) -> list:
        """Calcule gravity torque on each rotational joint with given input control variable list.

        Args:
            control_object (KinematicComputableAssembly): Analysis target.
            control_variable_list (list): Input control variable list.

        Returns:
            list: Gravity torque list on each joint.
        """        
        
        gravity_torque_list = []
        pose_matrix_dict = KinematicUtils.calculate_pose_matrix_dict(control_object, 
                                                                     control_variable_list)
        part_index_list = control_object.retrieve_part_index_list()
        part_index_list_enum = enumerate(part_index_list)
        for index, part_index in part_index_list_enum:
            part = control_object.parts.loc[control_object.parts["index"] == part_index, ["entity"]].iloc[0, 0]
            part = cast(Part, part)
            if part.type == PartTypes.ROTATIONAL_JOINT:
                if index != len(part_index_list) - 1:
                    part_index_list_subsequent = part_index_list[index + 1:]
                    gravity_torque = 0
                    joint_coordinate = KinematicUtils.calculate_position_from_pose_matrix(pose_matrix_dict[part_index])
                    rotation_direction = KinematicUtils.calculate_orientation_from_pose_matrix(pose_matrix_dict[part_index])[-1]
                    coordinate_last = coordinate_current = joint_coordinate
                    for part_index_subsequent in part_index_list_subsequent:
                        part_subsequent = control_object.parts.loc[control_object.parts["index"] == part_index_subsequent, ["entity"]].iloc[0, 0]
                        part_subsequent = cast(Part, part_subsequent)
                        pose_matrix = pose_matrix_dict[part_index_subsequent]
                        coordinate_current = KinematicUtils.calculate_position_from_pose_matrix(pose_matrix)
                        match part_subsequent.type:
                            case PartTypes.LINK:
                                part_subsequent = cast(Link, part_subsequent)
                                
                                gravity_torque += DynamicUtils.calculate_link_gravity_torque(joint_coordinate, 
                                                                                             rotation_direction,
                                                                                             coordinate_last, 
                                                                                             coordinate_current,
                                                                                             part_subsequent.rho,
                                                                                             part_subsequent.sectional_area,
                                                                                             impact_factor = impact_factor)
                                coordinate_last = coordinate_current
                            case PartTypes.ROTATIONAL_JOINT:
                                part_subsequent = cast(RotationalJoint, part_subsequent)
                                gravity_torque += DynamicUtils.calculate_particle_gravity_torque(joint_coordinate, 
                                                                                                 rotation_direction,
                                                                                                 coordinate_current,
                                                                                                 part_subsequent.mass,
                                                                                                 impact_factor = impact_factor)
                                coordinate_last = coordinate_current
                    gravity_torque_list.append(gravity_torque)
        return gravity_torque_list