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

from abc import abstractmethod
from models.assembly import Assembly
import pandas as pd

class KinematicComputableAssembly(Assembly):
    
    @property
    @abstractmethod
    def reference_frames(self) -> pd.DataFrame:
        pass
    
    @reference_frames.setter
    @abstractmethod
    def reference_frames(self,
                         value:pd.DataFrame) -> None:
        pass
    
    @property
    @abstractmethod
    def inverse_kinematic_analysis_basis(self) -> list:
        pass
    
    @inverse_kinematic_analysis_basis.setter
    @abstractmethod
    def inverse_kinematic_analysis_basis(self,
                                         value: list) -> None:
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        pass
    
    @abstractmethod
    def retrive_joint_num(self) -> int:
        pass
    
    @abstractmethod
    def retrieve_reference_frame_index_list(self) -> list:
        pass
    
    @abstractmethod
    def retrieve_control_variable_list(self) -> list:
        pass
    
    @abstractmethod
    def retrive_control_variable_list(self) -> list:
        pass
    
    @abstractmethod
    def retrieve_part_index_list(self) -> list:
        pass
    
    @abstractmethod
    def update_control_variable(self,
                                control_variables:list) -> None:
        pass
    
    @abstractmethod
    def update_pose_matrix(self,
                           pose_matrixs:dict) -> None:
        pass