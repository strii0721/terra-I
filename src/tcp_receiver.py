import socket

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5005       # Keep consistent with MATLAB

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening on port {PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            try:
                angles = [float(a) for a in data.split(',')]
                print("Received angles:", angles)
                # TODO: Motor control function move_to_angles(angles)
            except:
                print("Invalid data:", data)
