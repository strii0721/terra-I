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
from threading import Thread

class TcpAgent():
    
    def __init__(self,
                 ip:str = "0.0.0.0",
                 port:int = 5005) -> None:
        self.ip = ip
        self.port = port
        self.read_buffer = Queue()
        self.connection = None
        
    def wait(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            logger = Log4P()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.ip, self.port))
            s.listen(1)
            logger.info(f"Waiting for connection on port {self.port}...")
            connection, addr = s.accept()
            self.connection = connection
            logger.info(f"Connected by {addr}, start listening...")
            tcp_service = Thread(target = self.listen)
            tcp_service.daemon = True
            tcp_service.start()

    def listen(self) -> None:
        if self.connection:
            while True:
                data = self.connection.recv(1024).strip()
                try:
                    if not data:
                        break
                    # control_variable_list = [float(a) for a in data.split(',')]
                    self.read_buffer.put(data)
                except:
                    logger.info("Invalid data:", data)

    def read(self) -> object:
        data = self.read_buffer.get()
        return data
    
    def send(self, 
             message: object) -> None:
        if self.connection:
            try:
                logger = Log4P()
                self.connection.sendall(message.encode())
                logger.info(f"Send data: {str(message)}")
            except Exception as e:
                print("Send failed:", e)
