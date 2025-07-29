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
import time
import cv2
from math import pi
from core.comm.tcp_client import TcpClient

def main():
    dofbot_controller = DofbotController(control_interval = 1)
    # dofbot_controller.initialize()
    # for i in range(45):
    #     delta_rad = pi/180
    #     control_variable_list = dofbot_controller.standard_output()
    #     new_control_variable_list = [rad + delta_rad for rad in control_variable_list]
    #     dofbot_controller.standard_input(new_control_variable_list)
    # while True:
    #     image = dofbot_controller.image_output()
    #     timestamp = time.time()
    #     name = f"{timestamp}-calibration.bmp"
    #     dir = f"./output/calibration"
    #     path = f"{dir}/{name}"
    #     if image is not None: 
    #         dofbot_controller.save_image(image, path)
    #         cv2.imshow('Image Window', image)
    #         cv2.waitKey(500)
    tcp_client = TcpClient()
    tcp_service = Thread(target = tcp_client.listen, 
                         args = ())
    tcp_service.start()
    while True:
        control_variable_list = tcp_client.read()
        dofbot_controller.standard_input(control_variable_list)
        
try:
    main()
except KeyboardInterrupt:
  print("Program terminated! ")