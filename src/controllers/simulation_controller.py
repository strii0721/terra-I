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

from controllers.interfaces.base_controller import BaseController
from models.robotic_arm import RoboticArm
import os
from dk.logger.log4p import Log4P
from utils.kinematic_utils import KinematicUtils
from enums.part_types import PartTypes
from kinematics.kinematic_computer import KinematicComputer
from typing import Self

class SimulationController(BaseController):
    
    def __init__(self,
                 control_object:RoboticArm):
        self._control_object = control_object
    
    @property
    def control_object(self) -> RoboticArm:
        return self._control_object
    
    def initialize(self) -> Self:
        self.control_object.initialize()
        initial_control_variables = self.control_object.retrive_control_variable_list()
        self.standard_input(initial_control_variables)
        return self
    
    def standard_input(self,
                       control_variable_list:list) -> None:
        kinematic_computer = KinematicComputer()
        pose_matrixs_dict = kinematic_computer.calculate_pose_matrixs(self.control_object,
                                                                      control_variable_list)
        self.control_object.update_control_variable(control_variable_list)
        self.control_object.update_pose_matrix(pose_matrixs_dict)
        
    def delta_input(self,
                    delta_control_variable_list:list) -> None:
        current_control_variable_list = self.standard_output()
        control_variable_list = [current + delta for current, delta in zip(current_control_variable_list, delta_control_variable_list)]
        self.standard_input(control_variable_list)
        
    
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
            x, y, z = KinematicUtils.calculate_position_from_po_matrix(po_matix)
            x_vector, y_vector, z_vector = KinematicUtils.calculate_orientation_from_po_matrix(po_matix)
            logger.info(f"Name: {name}")
            logger.info(f"Position: x = {x}    y = {y}    z = {z}")
            logger.info(f"Orientation:")
            logger.info(f" - X-Axis: {x_vector}")
            logger.info(f" - Y-Axis: {y_vector}")
            logger.info(f" - Z-Axis: {z_vector}")
            match entity.type:
                case PartTypes.ROTATIONAL_JOINT:
                    logger.info(f"Current Output: {entity.control_variable}")
                case _:
                    pass
            logger.info(f"------------------------------------------------")
        logger.info(f"===========================================================")
        
    def enable_inverse_kinematic(self,
                                 names: list) -> None:
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