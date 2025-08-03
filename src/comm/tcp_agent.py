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
import json
from comm.enums.state_code import StateCode
import time

class TcpAgent():
    
    def __init__(self,
                 port:int = 5005) -> None:
        self.port = port
        self.read_buffer = Queue()
        self.connection = None
        
    def wait_connection(self) -> object:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ip = "0.0.0.0"
            s.bind((ip, self.port))
            s.listen(1)
            connection, (address, _) = s.accept()
            self.connection = connection
            return address

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
            payload_jsonstr = payload.decode("utf-8")
            payload_dict = json.loads(payload_jsonstr)
            return payload_dict["stat"], payload_dict["msg"]
    
    def send(self, 
             stat:StateCode,
             msg:object) -> None:
        if self.connection:
            payload_dict = {}
            payload_dict["stat"] = stat.value
            payload_dict["msg"] = msg
            payload_jsonstr = json.dumps(payload_dict)
            payload = payload_jsonstr.encode("utf-8")
            payload_length = len(payload)
            header = payload_length.to_bytes(4, 'big')
            self.connection.sendall(header + payload)
            

    def wait_state(self, 
                   target_state:StateCode, 
                   timeout = -1) -> object:
        time_start = time.time()
        while True:
            stat, msg = self.receive()
            if stat == target_state.value:  
                return msg
            if time.time() - time_start > timeout and timeout != -1 :
                return None
            time.sleep(0.01)
