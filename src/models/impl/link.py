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

from models.part import Part
from models.enums.part_types import PartTypes
import numpy as np

class Link(Part):
    
    def __init__(self,
                 name:str,
                 endpoint_vector:np.typing.NDArray,
                 visibility:bool = True):
        self.name = name
        self.type = PartTypes.LINK
        self.endpoint_vector = endpoint_vector
        self.visibility = visibility
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, 
             value:str) -> None:
        self._name = value
    
    @property
    def type(self) -> PartTypes:
        return self._type
    
    @type.setter
    def type(self,
             value:PartTypes) -> None:
        self._type = value
    
    @property
    def visibility(self) -> bool:
        return self._visibility
    
    @visibility.setter
    def visibility(self, 
                   value:bool) -> None:
        self._visibility = value