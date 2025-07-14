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

from kinematics.controllers.base_controller import BaseController
from models.kinematic_computable_assembly import KinematicComputableAssembly
import os
from dk.logger.log4p import Log4P
from kinematics.utils.kinematic_utils import KinematicUtils
from models.enums.part_types import PartTypes
from typing import Self
import numpy as np
import time
from typing import Callable
from utils.spatial_utils import SpatialUtils
from math import pi

class SimulationController(BaseController):
    
    def __init__(self,
                 control_object:KinematicComputableAssembly,
                 control_interval:float = 0.1):
        self.control_object = control_object
        self.control_interval = control_interval
        
    @property
    def control_object(self) -> KinematicComputableAssembly:
        return self._control_object
    
    @control_object.setter
    def control_object(self,
                       value:KinematicComputableAssembly):
        self._control_object = value
    
    @property
    def control_interval(self) -> float:
        return self._control_interval
    
    @control_interval.setter
    def control_interval(self,
                         value:float) -> None:
        self._control_interval = value
    
    def initialize(self) -> Self:
        self.control_object.initialize()
        initial_control_variables = self.control_object.retrive_control_variable_list()
        self.standard_input(initial_control_variables)
        return self
    
    def standard_input(self,
                       control_variable_list:list) -> None:
        normalized_control_variable_list = SpatialUtils.normalize_angle_list(control_variable_list)
        pose_matrixs_dict = KinematicUtils.calculate_pose_matrix_dict(self.control_object,
                                                                      normalized_control_variable_list)
        self.control_object.update_control_variable(normalized_control_variable_list)
        self.control_object.update_pose_matrix(pose_matrixs_dict)
        
    def delta_input(self,
                    delta_control_variable_list:list) -> None:
        current_control_variable_list = self.standard_output()
        control_variable_list = [current + delta for current, delta in zip(current_control_variable_list, delta_control_variable_list)]
        self.standard_input(control_variable_list)
        
    def trajectory_input(self,
                         trajectory:list) -> None:
        for control_variable_list in trajectory:
            self.standard_input(control_variable_list)
            time.sleep(self.control_interval)        
        
    def target_input(self,
                     true_target_pose_matrix:np.typing.NDArray,
                     trajectory_generate_function:Callable,
                     mode:str = "full",
                     amap:bool = True,
                     enable_log:bool = False) -> None:
        retry_delay = 5
        retry_portion = 1
        logger = Log4P()
        true_mode = mode
        target_pose_matrix = true_target_pose_matrix
        reachable = False
        substitute_position = False
        retry_num = 0
        while not reachable or substitute_position:
            try:
                trajectory = trajectory_generate_function(self.control_object, 
                                                          target_pose_matrix, 
                                                          mode = mode,
                                                          enable_log = enable_log)
                if not self.validate_trajectory(trajectory):
                    raise Exception("Exceeding angle restrictions...")
                logger.info(f"Moving to target...")
                reachable = True
                self.trajectory_input(trajectory)
                logger.info(f"Movement completed....")
            except Exception as e:
                logger.info(f"{e}")
            finally:
                if not reachable:
                    if amap:
                        retry_num += 1
                        if retry_num == 1:
                            logger.info("Therefore, tring same position in positial mode...")
                            substitute_position = False
                        else:
                            logger.info("Therefore, tring a closer position instead in positial mode...")
                            substitute_position = True
                            retry_portion = 0.7
                        current_pose_matrix = list(KinematicUtils.calculate_pose_matrix_dict(
                            self.control_object,
                            self.standard_output()
                        ).values())[-1]
                        target_pose_matrix = KinematicUtils.generate_midway_pose_matrix(
                            current_pose_matrix, target_pose_matrix, retry_portion
                        )
                        new_position = KinematicUtils.calculate_position_from_pose_matrix(target_pose_matrix)
                        mode = "positional"
                        logger.info(f"Replacement position confirmed {new_position}, retry in ")
                        for i in range(retry_delay):
                            logger.info(f"{retry_delay - i} s")
                            time.sleep(1)
                    else:
                        logger.info("Therefore, retry in")
                        for i in range(retry_delay):
                            logger.info(f"{retry_delay - i} s")
                            time.sleep(1)
                            
                elif substitute_position:
                    logger.info(f"Replacement position is reachable, let's try the true position again...")
                    reachable = False
                    substitute_position = False
                    target_pose_matrix = true_target_pose_matrix
                    mode = true_mode
                    logger.info(f"Position confirmed, retry in ")
                    for i in range(retry_delay):
                        logger.info(f"{retry_delay - i} s")
                        time.sleep(1)

    def route_input(self,
                    target_pose_matrix_list:list,
                    trajectory_generate_function:Callable,
                    mode:str = "full",
                    amap:bool = True,
                    enable_log:bool = False) -> None:
        for tartget in target_pose_matrix_list:
            self.target_input(tartget,
                              trajectory_generate_function,
                              mode,
                              amap,
                              enable_log)
            
    def standard_output(self) -> list:
        control_variable_list = self.control_object.retrieve_control_variable_list()
        return control_variable_list
    
    def listen(self,
               listened_object_names:list) -> None:
        """Listen to pose information of a given object and print it in the terminal.
    
        Args:
            track_objects (list): Name list of objects that need to track.
    
        Returns:
            None.
        """
        
        logger = Log4P()
        
        objects = {
            name: (entity, po_matrix)
            for name, entity, po_matrix in zip(
                self.control_object.parts["index"],
                self.control_object.parts["entity"],
                self.control_object.parts["pose_matrix"])
        }
        
        objects = objects | {
            name: (entity, po_matrix)
            for name, entity, po_matrix in zip(
                self.control_object.reference_frames["index"],
                self.control_object.reference_frames["entity"],
                self.control_object.reference_frames["pose_matrix"])
        }
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.info(f"      ==   Kinematic Simulation System  ==")
        logger.info(f"")
        logger.info(f"Author: strii0721       SING PRAISE TO THE GOD OF ALL MACHINES!")
        logger.info(f"")
        logger.info(f"===========================================================")
        for name in listened_object_names:
            entity = objects[name][0]
            po_matix = objects[name][1]
            x, y, z = KinematicUtils.calculate_position_from_pose_matrix(po_matix)
            x_vector, y_vector, z_vector = KinematicUtils.calculate_orientation_from_pose_matrix(po_matix)
            logger.info(f"Name: {name}")
            logger.info(f"Position: x = {x:.6f}    y = {y:.6f}    z = {z:.6f}")
            logger.info(f"Orientation:")
            logger.info(f" - X-Axis: {np.round(x_vector, decimals=6)}")
            logger.info(f" - Y-Axis: {np.round(y_vector, decimals=6)}")
            logger.info(f" - Z-Axis: {np.round(z_vector, decimals=6)}")
            match entity.type:
                case PartTypes.ROTATIONAL_JOINT:
                    logger.info(f"Current Output: {entity.control_variable}")
                case _:
                    pass
            logger.info(f"------------------------------------------------")
        logger.info(f"===========================================================")
        
    def listen_daemon(self,
                      listened_object_names:list) -> None:
        """Listen to pose information of a given object and print it in the terminal.
    
        Args:
            track_objects (list): Name list of objects that need to track.
    
        Returns:
            None.
        """
        
        logger = Log4P()
        while True:
            objects = {
                name: (entity, po_matrix)
                for name, entity, po_matrix in zip(
                    self.control_object.parts["index"],
                    self.control_object.parts["entity"],
                    self.control_object.parts["pose_matrix"])
            }

            objects = objects | {
                name: (entity, po_matrix)
                for name, entity, po_matrix in zip(
                    self.control_object.reference_frames["index"],
                    self.control_object.reference_frames["entity"],
                    self.control_object.reference_frames["pose_matrix"])
            }
        
            os.system('cls' if os.name == 'nt' else 'clear')
            logger.info(f"      ==   Kinematic Simulation System  ==", True)
            logger.info(f"", True)
            logger.info(f"Author: strii0721       SING PRAISE TO THE GOD OF ALL MACHINES!", True)
            logger.info(f"", True)
            logger.info(f"===========================================================", True)
            for name in listened_object_names:
                entity = objects[name][0]
                pose_matix = objects[name][1]
                x, y, z = KinematicUtils.calculate_position_from_pose_matrix(pose_matix)
                x_vector, y_vector, z_vector = KinematicUtils.calculate_orientation_from_pose_matrix(pose_matix)
                logger.info(f"Name: {name}", True)
                logger.info(f"Position: x = {x:.6f}    y = {y:.6f}    z = {z:.6f}", True)
                logger.info(f"Orientation:", True)
                logger.info(f" - X-Axis: {np.round(x_vector, decimals=6)}", True)
                logger.info(f" - Y-Axis: {np.round(y_vector, decimals=6)}", True)
                logger.info(f" - Z-Axis: {np.round(z_vector, decimals=6)}", True)
                match entity.type:
                    case PartTypes.ROTATIONAL_JOINT:
                        logger.info(f"Current Output: {entity.control_variable}")
                    case _:
                        pass
                logger.info(f"------------------------------------------------", True)
            logger.info(f"===========================================================")
            time.sleep(self.control_interval)
        
    def bind_inverse_kinematic_analysis_basis(self,
                                 names: list) -> Self:
        """Specify reference systems or components to participate in inverse kinematics analysis. This function is recommended to be called after the entire robotic arm has been constructed (using Configuration.confirm_construct()).
    
        Args:
            names (np.typing.NDArray): The names of the reference system or component that needs to participate in the inverse kinematics analysis.
    
        Returns:
            None.
        """
        
        part_names = self.control_object.retrieve_part_index_list()
        reference_frame_names = self.control_object.retrieve_reference_frame_index_list()
        for name in names:
            if name not in part_names + reference_frame_names:
                raise Exception(f"Fail to locate a joint or reference frame named {name}")
            self.control_object.inverse_kinematic_analysis_basis.append(name)
            
        return self
    
    def validate_trajectory(self,
                            trajectory:list) -> bool:
        for control_variable_list in trajectory:
            valid_input = self.validate_input(control_variable_list)
            if not valid_input:
                return False
        return True
    
    def validate_input(self,
                       control_variable_list:list):
        return True