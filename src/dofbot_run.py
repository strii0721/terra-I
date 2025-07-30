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

from core.controllers.impl.dofbot_controller import DofbotController
from threading import Thread
from core.comm.tcp_agent import TcpClient
import time
from dk.logger.log4p import Log4P
from math import pi

def main():
    logger = Log4P()
    dofbot_controller = DofbotController(initial_control_variable_list = [pi/2, 1*pi/2, pi/2, pi/2, pi/2, pi/2])
    dofbot_controller.initialize()
    # dofbot_controller.standard_input([pi/2, pi/2 + pi/180, pi/2, pi/2, pi/2, pi/2])
    time.sleep(1)
    logger.info(f"Robotic arm initialized...")
    tcp_client = TcpClient()
    
    tcp_service = Thread(target = tcp_client.listen)
    tcp_service.daemon = True
    tcp_service.start()
    while True:
        control_variable_list = tcp_client.read()
        logger.info(f"Current input: {control_variable_list}")
        dofbot_controller.standard_input(control_variable_list)
try:
    main()
except KeyboardInterrupt:
  print("Program terminated! ")