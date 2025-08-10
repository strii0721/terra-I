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

from models.assembly import Assembly
import pandas as pd
from simulation.enums.render_object_types import RenderObjectTypes

class Ground(Assembly):
    
    def __init__(self) -> None:
        self.parts = pd.DataFrame()
        
    @property
    def parts(self) -> pd.DataFrame:
        return self._parts
    
    @parts.setter
    def parts(self,
              value:pd.DataFrame) -> None:
        self._parts = value
        
    def retrieve_render_list(self,
                             render_object_type:RenderObjectTypes) -> list:
        match render_object_type:
            case RenderObjectTypes.FACE:
                x1 = -20
                y1 = -20
                z1 = 0
                x2 = 20
                y2 = 20
                z2 = 0
                faces_list = [
                    [(x1, y1, z1), (x1, y2, z1), (x2, y2, z2), (x2, y1, z1)],
                ]
                return faces_list
            case _:
                return []