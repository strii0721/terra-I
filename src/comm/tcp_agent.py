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
import json
from comm.enums.state_code import StateCode

class TcpAgent():
    
    def __init__(self,
                 port:int = 5005) -> None:
        self.port = port
        self.read_buffer = Queue()
        self.connection = None
        
    def wait_connection(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            logger = Log4P()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", self.port))
            s.listen(1)
            logger.info(f"Waiting for connection on port {self.port}...")
            connection, addr = s.accept()
            self.connection = connection
            logger.info(f"Connected by {addr}, start listening...")

    def receive(self) -> tuple:
        if self.connection:
            header = self.connection.recv(4)
            length = int.from_bytes(header, 'big')
            payload = b''
            while len(payload) < length:
                packet = self.connection.recv(length - len(payload))
                if not packet:
                    raise ConnectionError("Connection terminated.")
                payload += packet
            payload = payload.decode()
            payload_dict = json.loads(payload)
            return payload_dict["stat"], payload_dict["msg"]
    
    def send(self, 
             stat:StateCode,
             msg:object) -> None:
        if self.connection:
            payload_dict = {}
            payload_dict["stat"] = stat
            payload_dict["msg"] = msg
            payload = json.dumps(payload_dict)
            payload = payload.encode()
            length = len(payload)
            header = length.to_bytes(4, 'big')
            self.connection.sendall(header + payload)
            

    def wait_state(self, 
                   target_state:StateCode) -> object:
        stat, msg = self.receive()
        if stat == target_state:
            return msg
