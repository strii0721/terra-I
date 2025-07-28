#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Mon Jul 28 2025
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

import time
from Arm_Lib import Arm_Device
from typing import Self
from math import pi
import csv

class DofbotController():
    
    def __init__(self,
                 control_interval:float = 0.5,
                 initial_control_variable_list:list = [pi/2, pi/2, pi/2, pi/2, pi/2, pi/2]) -> None:
        self.control_object =  Arm_Device()
        self.control_interval = control_interval
        self.initial_control_variable_list = initial_control_variable_list
    
    def initialize(self) -> Self:
        self.standard_input(self.initial_control_variable_list)
        return self
    
    def standard_input(self,
                       control_variable_list:list) -> None:
        self.control_object.Arm_serial_servo_write6(180 * control_variable_list[0] / pi,
                                                    180 * control_variable_list[1] / pi,
                                                    180 * control_variable_list[2] / pi,
                                                    180 * control_variable_list[3] / pi,
                                                    180 * control_variable_list[4] / pi,
                                                    180 * control_variable_list[5] / pi,
                                                    int(self.control_interval/1000))
        
    def trajectory_input(self,
                         trajectory:list) -> None:
        for control_variable_list in trajectory:
            self.standard_input(control_variable_list)
            time.sleep(self.control_interval)  
    
    def csv_input(self,
                  csv_file_path:str) -> None:
        trajectory = []
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                trajectory.append(row)
        self.trajectory_input(trajectory)
    
    def standard_output(self) -> list:
        control_variable_list = []
        for index in range(6):
            angle_degree = self.control_object.Arm_serial_servo_read(index+1)
            if angle_degree is not None: 
                angle_radian = pi * angle_degree / 180
            else: 
                angle_radian = None
            control_variable_list.append(angle_radian)
            
        return control_variable_list
        