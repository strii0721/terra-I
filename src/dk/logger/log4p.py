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

from datetime import datetime
from dk.logger.enums.log_levels import LogLevels as LL
import os

class Log4P:
    def __init__(self,
                 log_file_path = "logs/log4p.log") -> None:
        
        self.log_file_path = log_file_path
        self.cache = ""
        
    
    def _log(self, 
             level:LL, 
             message:str,
             hold) -> None:
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        log_string = ""
        log_string += f"[{timestamp}] "
        log_string += f"[{level.value}] "
        log_string += f"{message}"
        if hold:
            self.cache += log_string + "\n"
        else:
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            self.cache += log_string
            print(self.cache)
            with open(self.log_file_path, "a") as f:
                f.write(self.cache)
                f.write("\n")
            self.cache = ""
    
    def info(self, 
             message:str,
             hold = False) -> None:
        self._log(LL.INFO,
                  message,
                  hold)
        
