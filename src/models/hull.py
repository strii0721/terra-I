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

from models.interfaces.assembly import Assembly
import pandas as pd
from enums.render_object_types import RenderObjectTypes

class Hull(Assembly):
    
    def __init__(self) -> None:
        self._parts = pd.DataFrame()
        
    
    @property
    def parts(self) -> pd.DataFrame:
        return self._parts
    
    def standard_input(self,
                       control_variable:list) -> None:
        pass
    
    def standard_output(self) -> list:
        return []
    
    def retrieve_render_list(self,
                             render_object_type:RenderObjectTypes) -> list:
        match render_object_type:
            case RenderObjectTypes.FACE:
                x1 = 0
                y1 = -(38.1+5)
                z1 = -(26.05-2)
                x2 = 360
                y2 = 220.3-(38.1+5)
                z2 = (2+23.95)
                faces_list = [
                    [(x1, y1, z1), (x1, y2, z1), (x2, y2, z1), (x2, y1, z1)],
                    [(x1, y1, z1), (x1, y1, z2), (x1, y2, z2), (x1, y2, z1)],
                    [(x1, y1, z1), (x1, y1, z2), (x2, y1 ,z2), (x2, y1, z1)],
                    [(x2, y1, z1), (x2, y1, z2), (x2, y2, z2), (x2, y2, z1)],
                    [(x2, y2, z1), (x2, y2, z2), (x1, y2, z2), (x1, y2, z1)]
                ]
                return faces_list
            case _:
                return []