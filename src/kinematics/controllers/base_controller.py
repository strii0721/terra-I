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

from abc import ABC, abstractmethod
from models.kinematic_computable_assembly import  KinematicComputableAssembly
from typing import Self

class BaseController(ABC):
    
    @property
    @abstractmethod
    def control_object(self) -> KinematicComputableAssembly:
        pass
    
    @control_object.setter
    @abstractmethod
    def control_object(self,
                       value:KinematicComputableAssembly):
        pass
    
    @property
    @abstractmethod
    def control_interval(self) -> float:
        pass
    
    @control_interval.setter
    @abstractmethod
    def control_interval(self,
                         value:float) -> None:
        pass
    
    @abstractmethod
    def initialize(self) -> Self:
        pass
    
    @abstractmethod
    def standard_input(self,
                       control_variable_list:list) -> None:
        pass
    
    @abstractmethod
    def delta_input(self,
                    delta_control_variable_list:list) -> None:
        pass
    
    @abstractmethod
    def standard_output(self) -> list:
        pass