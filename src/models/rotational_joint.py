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

from models.interfaces.joint import Joint
from enums.part_types import PartTypes
import numpy as np

class RotationalJoint(Joint):
    
    def __init__(self,
                 name:str,
                 rotation_direction:np.typing.NDArray,
                 initial_control_variable:float = 0,
                 visibility:bool = True):
        self._name = name
        self._type = PartTypes.ROTATIONAL_JOINT
        self.rotation_direction = rotation_direction
        self._control_variable = initial_control_variable
        self._visibility = visibility
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def type(self) -> PartTypes:
        return self._type
    
    @property
    def visibility(self) -> bool:
        return self._visibility
    
    @property
    def control_variable(self) -> float:
        return self._control_variable
    
    @control_variable.setter
    def control_variable(self,
                         control_variable:float):
        self._control_variable = control_variable