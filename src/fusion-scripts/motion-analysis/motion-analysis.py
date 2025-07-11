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


import traceback
import adsk.core
import csv
import time

# System Settings
_APP = adsk.core.Application.get()
_UI  = _APP.userInterface
_PRODUCT = _APP.activeProduct


# User Settings
FOOTPRINT_NAME = "fusion-motion-analysis"
# CSV_PATH = "C:\\Users\\lynchpin\\repository\\terra-I\\resources\\joint_angles_20250630_233108.csv"
CSV_PATH = "C:\\Users\\lynchpin\\repository\\terra-I\\resources\\init.csv"
FPS = 60
DESIGN = _PRODUCT # Derived Classes: "CAM", "Design", "Drawing"


control_interval = 1/FPS
ROOT = DESIGN.rootComponent
with open(CSV_PATH, 'r') as f:
    reader = csv.reader(f)
    sequence = [row for row in reader]

# Main method
def run(_context: str):

    try:
        _UI.messageBox(f'"{FOOTPRINT_NAME} in progress...')
        
        ############  Defining and binding joints  ############
        for joint in ROOT.allJoints:
            if joint.name == "la-j1" : la_j1 = joint
            if joint.name == "la-j2" : la_j2 = joint
            if joint.name == "la-j3" : la_j3 = joint
            if joint.name == "ra-j1" : ra_j1 = joint
            if joint.name == "ra-j2" : ra_j2 = joint
            if joint.name == "ra-j3" : ra_j3 = joint

        joints = [la_j1, la_j2, la_j3, ra_j1, ra_j2, ra_j3]     # Confirm binding
        
        ####################  Rendering  ######################
        for row in sequence:
            for idx, angle_rad in enumerate(row):
                joints[idx].jointMotion.rotationValue = float(angle_rad)
            _APP.activeViewport.refresh()
            time.sleep(control_interval)
            
    except Exception as e:
        _UI.messageBox(f"Error occured:\n{traceback.format_exc()}")
        _UI.messageBox(f"Error message:\n{str(e)}")
