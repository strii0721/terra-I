import socket
from queue import Queue

class TcpClient():
    
    def __init__(self,
                 host:str = "0.0.0.0",
                 port:int = 5005) -> None:
        self.host = host
        self.port = port
        self.buffer = Queue()

    def listen(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)
            print(f"Listening on port {self.port}...")
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break
                    try:
                        contro_variable_list = [float(a) for a in data.split(',')]
                        self.buffer.put(contro_variable_list)
                    except:
                        print("Invalid data:", data)

    def read(self) -> list:
        control_variable_list = self.buffer.get()
        return control_variable_list