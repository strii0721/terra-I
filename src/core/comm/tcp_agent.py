#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Tue Jul 29 2025
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

import socket
from queue import Queue
from dk.logger.log4p import Log4P

class TcpClient():
    
    def __init__(self,
                 host:str = "0.0.0.0",
                 port:int = 5005) -> None:
        self.host = host
        self.port = port
        self.read_buffer = Queue()
        self.connection = None

    def listen(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            logger = Log4P()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(1)
            logger.info(f"Listening on port {self.port}...")
            connection, addr = s.accept()
            self.connection = connection
            with connection:
                logger.info(f"Connected by {addr}")
                while True:
                    data = connection.recv(1024).decode().strip()
                    try:
                        if not data:
                            break
                        control_variable_list = [float(a) for a in data.split(',')]
                        self.read_buffer.put(control_variable_list)
                    except:
                        logger.info("Invalid data:", data)

    def read(self) -> list:
        control_variable_list = self.read_buffer.get()
        return control_variable_list
    
    def send(self, 
             message: str) -> None:
        if self.connection:
            try:
                self.connection.sendall((message + "\n").encode())
            except Exception as e:
                print("Send failed:", e)
