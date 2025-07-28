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

from core.controllers.base_controller import BaseController
from models.kinematic_computable_assembly import KinematicComputableAssembly
import os
from dk.logger.log4p import Log4P
from core.utils.kinematic_utils import KinematicUtils
from models.enums.part_types import PartTypes
from typing import Self
import numpy as np
import time
from typing import Callable
from utils.spatial_utils import SpatialUtils
from core.utils.dynamics_utils import DynamicUtils
from math import pi

class SimulationController(BaseController):
    
    def __init__(self,
                 control_object:KinematicComputableAssembly,
                 control_interval:float = 0.1,
                 gravity_impact_factor:float = 0):
        """Construction method.

        Args:
            control_object (KinematicComputableAssembly): Entity of controlled robotic arm.
            control_interval (float, optional): Control interval, in seconds. Defaults to 0.1.
            gravity_impact_factor (float, optional): A percentage value used to adjust the effect of gravity on joint torque output. Defaults to 0.
        """        
        self.control_object = control_object
        self.control_interval = control_interval
        self.rotational_joint_torque_limit_dict = {}
        self.gravity_impact_factor = gravity_impact_factor
        self.input_history = []
        
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
        """Initialize robotic arm. Invoke initialization function in robotic arm entity first.

        Returns:
            Self: For chained calls.
        """
        self.control_object.initialize()
        initial_control_variables = self.control_object.retrive_control_variable_list()
        self.standard_input(initial_control_variables)
        self.rotational_joint_torque_limit_dict = self.control_object.retrieve_rotational_joint_torque_limit_dict()
        return self
    
    def standard_input(self,
                       control_variable_list:list) -> None:
        """Read a list of control variable list and control joints to target value.

        Args:
            control_variable_list (list): Control variable list.
        """  
        normalized_control_variable_list = SpatialUtils.normalize_angle_list(control_variable_list)
        pose_matrixs_dict = KinematicUtils.calculate_pose_matrix_dict(self.control_object,
                                                                      normalized_control_variable_list)
        self.control_object.update_control_variable(normalized_control_variable_list)
        self.control_object.update_pose_matrix(pose_matrixs_dict)
        if len(self.input_history) < 3:
            self.input_history.append(control_variable_list)
        else:
            for i in range(2):
                self.input_history[i] = self.input_history[i+1]
            self.input_history[2] = control_variable_list
        
    def delta_input(self,
                    delta_control_variable_list:list) -> None:
        """Control joints with a list of delta control variable.

        Args:
            delta_control_variable_list (list): A list of delta control variable.
        """        
        current_control_variable_list = self.standard_output()
        control_variable_list = [current + delta for current, delta in zip(current_control_variable_list, delta_control_variable_list)]
        self.standard_input(control_variable_list)
        
    def trajectory_input(self,
                         trajectory:list) -> None:
        """Control robotic arm to move along a specific trajectory. Trajectory is a sequence of control variable list.

        Args:
            trajectory (list): A sequence of control variable list.
        """      
        self.input_history = []
        for control_variable_list in trajectory:
            self.standard_input(control_variable_list)
            time.sleep(self.control_interval)        
        
    def target_input(self,
                     true_target_pose_matrix:np.typing.NDArray,
                     trajectory_generate_function:Callable,
                     mode:str = "full",
                     amap:bool = True,
                     enable_log:bool = False) -> None:
        """Control robotic arm moving toward a target, trajectory generated automatically.

        Args:
            true_target_pose_matrix (np.typing.NDArray): Complete target pose matrix.
            trajectory_generate_function (Callable): The function that generates trajectory.
            mode (str, optional): If true target pose matrix is not reachable, shall change to positional mode. Defaults to "full".
            amap (bool, optional): If position is not reachable, shall robotic arm try to reach target position as much as possible. Defaults to True.
            enable_log (bool, optional): Toggle log. Defaults to False.
        """        
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
                trajectory = self.fulfill_trajectory(trajectory)
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
        """Control robotic arm moving along a sequence of target.

        Args:
            target_pose_matrix_list (list): A list of target pose matrix.
            trajectory_generate_function (Callable): The function that generates trajectory.
            mode (str, optional): If true target pose matrix is not reachable, shall change to positional mode. Defaults to "full".
            amap (bool, optional): If position is not reachable, shall robotic arm try to reach target position as much as possible. Defaults to True.
            enable_log (bool, optional): Toggle log. Defaults to False.
        """        
        for tartget in target_pose_matrix_list:
            self.target_input(tartget,
                              trajectory_generate_function,
                              mode,
                              amap,
                              enable_log)
            
    def standard_output(self) -> list:
        """Get current control variable list of each joints.

        Returns:
            list: A list of current control variables for each joints.
        """             
        control_variable_list = self.control_object.retrieve_control_variable_list()
        return control_variable_list
    
    def angular_accelleration_output(self) -> dict:
        """Get current angular accelleration list of each joints.

        Returns:
            dict: A list of current angular accelleration list of each joints.
        """        
        control_variable_history = self.input_history
        angular_accelleration_dict = {}
        alpha_list = DynamicUtils.calculate_angular_acceleration_list(self.control_interval,
                                                                      control_variable_history[0],
                                                                      control_variable_history[1],
                                                                      control_variable_history[2])
        rotational_joint_list = self.control_object.retrieve_parts_entity_in_type([PartTypes.ROTATIONAL_JOINT])
        for index, rotational_joint in enumerate(rotational_joint_list):
            angular_accelleration_dict[rotational_joint.index] = alpha_list[index]
        return angular_accelleration_dict
        
    def torque_output(self) -> dict:
        """Get current torque output list of each joints.

        Returns:
            dict: A list of current torque output list of each joints.
        """      
        control_variable_history = self.input_history
        torque_dict = {}
        alpha_dict = self.angular_accelleration_output()
        inertia_dict = DynamicUtils.calculate_inertia_dict(self.control_object,
                                                           control_variable_history[-2])
        gravity_torque_dict = DynamicUtils.calculate_gravity_torque_dict(self._control_object,
                                                                         control_variable_history[-2])
        for _, joint_index in enumerate(gravity_torque_dict):
            torque_dict[joint_index] = inertia_dict[joint_index] * alpha_dict[joint_index] + gravity_torque_dict[joint_index]
        return torque_dict
    
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
        rotational_joint_acceleration_dict = {}
        rotational_joint_torque_dict = {}
        if len(self.input_history) == 3:
            rotational_joint_acceleration_dict = self.angular_accelleration_output()
            rotational_joint_torque_dict = self.torque_output()
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.info(f"      ==   Kinematic Simulation System  ==")
        logger.info(f"")
        logger.info(f"Author: strii0721       SING PRAISE TO THE GOD OF ALL MACHINES!")
        logger.info(f"")
        logger.info(f"===========================================================")
        for index in listened_object_names:
            entity = objects[index][0]
            po_matix = objects[index][1]
            x, y, z = KinematicUtils.calculate_position_from_pose_matrix(po_matix)
            x_vector, y_vector, z_vector = KinematicUtils.calculate_orientation_from_pose_matrix(po_matix)
            logger.info(f"Name: {index}")
            logger.info(f"Position: x = {x:.6f}    y = {y:.6f}    z = {z:.6f}")
            logger.info(f"Orientation:")
            logger.info(f" - X-Axis: {np.round(x_vector, decimals=6)}")
            logger.info(f" - Y-Axis: {np.round(y_vector, decimals=6)}")
            logger.info(f" - Z-Axis: {np.round(z_vector, decimals=6)}")
            match entity.type:
                case PartTypes.ROTATIONAL_JOINT:
                    logger.info(f"Current Output: {entity.control_variable}")
                    if len(rotational_joint_torque_dict) != 0:
                        logger.info(f"Anuglar Acceleration at Last Frame: {rotational_joint_acceleration_dict[index]}")
                        logger.info(f"Torque Output at Last Frame: {rotational_joint_torque_dict[index]}")
                case _:
                    pass
            logger.info(f"------------------------------------------------")
        logger.info(f"===========================================================")
        
    def listen_daemon(self,
                      listened_object_names:list) -> None:
        """Listen to pose information of a given object and print it in the terminal.
    
        Args:
            listened_object_names (list): Name list of objects that need to track.
    
        Returns:
            None.
        """
        
        logger = Log4P()
        while True:
            self.listen(listened_object_names)
            time.sleep(self.control_interval)
        
    def bind_inverse_kinematic_analysis_basis(self, 
                                              names: list) -> Self:
        """Specify reference systems or components to participate in inverse kinematics analysis. This function is recommended to be called after the entire robotic arm has been constructed (using Configuration.confirm_construct()).
    
        Args:
            names (np.typing.NDArray): The names of the reference system or component that needs to participate in the inverse kinematics analysis.
    
        Returns:
            Self: For chained calls
        """
        
        part_names = self.control_object.retrieve_part_index_list()
        reference_frame_names = self.control_object.retrieve_reference_frame_index_list()
        for name in names:
            if name not in part_names + reference_frame_names:
                raise Exception(f"Fail to locate a joint or reference frame named {name}")
            self.control_object.inverse_kinematic_analysis_basis.append(name)
            
        return self
    
    def check_trajectory(self, 
                         trajectory:list) -> list:
        """Check input trajectory if every input satisfy torque output limit of each joints.

        Args:
            trajectory (list): Trajectory to be checked.

        Returns:
            list: A valid trajectory.
        """        
        invalid_control_loop_index_list = []
        rotation_torque_dict = {}
        torque_dict = {}
        for control_loop_index, control_variable_list in enumerate(trajectory):
            if control_loop_index >= 1 and control_loop_index <= len(trajectory) -2:
                inertia_dict = DynamicUtils.calculate_inertia_dict(self.control_object,
                                                                   control_variable_list)
                angular_acceleration_list = DynamicUtils.calculate_angular_acceleration_list(self.control_interval,
                                                                                             trajectory[control_loop_index-1],
                                                                                             trajectory[control_loop_index],
                                                                                             trajectory[control_loop_index+1])
                for index,  joint_index in enumerate(inertia_dict.keys()):
                    rotation_torque_dict[joint_index] = inertia_dict[joint_index] * angular_acceleration_list[index]
                gravity_torque_dict = DynamicUtils.calculate_gravity_torque_dict(self.control_object,
                                                                                 control_variable_list,
                                                                                 impact_factor = self.gravity_impact_factor)
                for joint_index in rotation_torque_dict:
                    torque_dict[joint_index] = rotation_torque_dict[joint_index] + gravity_torque_dict[joint_index]
                for joint_index, torque in torque_dict.items():
                    if torque > self.rotational_joint_torque_limit_dict[joint_index]:
                        invalid_control_loop_index_list.append((control_loop_index, gravity_torque_dict, inertia_dict))
        return invalid_control_loop_index_list
    
    def fulfill_trajectory(self, 
                           trajectory:list) -> list:
        """Insert intermediate values at appropriate positions in the invalid trajectory.

        Args:
            trajectory (list): Invalid trajectory

        Returns:
            list: A valid trajectory based on input trajectory
        """        
        invalid_loop_list = self.check_trajectory(trajectory)
        
        while len(invalid_loop_list) != 0:
            offset = 0
            for invalid_loop in invalid_loop_list:
                invalid_loop_index = invalid_loop[0] + offset
                gravity_torque_list = list(invalid_loop[1].values())
                inertia_list = list(invalid_loop[2].values())
                torque_limit_list = list(self.rotational_joint_torque_limit_dict.values())
                alpha_limit_list = ((np.array(torque_limit_list) - np.array(gravity_torque_list)) / np.array(inertia_list))
                previous_control_variable_list = np.array(trajectory[invalid_loop_index - 1])
                current_control_variable_list = np.array(trajectory[invalid_loop_index])
                
                delta_control_variable_list = np.abs(current_control_variable_list - previous_control_variable_list) / pi * 180
                delta_control_variable_list_max = 0.5 * alpha_limit_list * self.control_interval**2
                
                step_num_list = delta_control_variable_list / delta_control_variable_list_max
                
                step_num = int(np.max(np.ceil(step_num_list)))
                if step_num <= 1:
                    step_num = 2
                
                insert_list = [(previous_control_variable_list + (current_control_variable_list - previous_control_variable_list) * (k / step_num)).tolist() for k in range(1, step_num)]
                for inserted_control_variable_list in reversed(insert_list):
                    trajectory.insert(invalid_loop_index, inserted_control_variable_list)
                    
                offset += step_num - 1

            invalid_loop_list = self.check_trajectory(trajectory)
        return trajectory