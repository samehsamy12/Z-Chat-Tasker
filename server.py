import socket
import json

HOST = '127.0.0.1'
PORT = 65432
tasks_list = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Z-Chat Server is active on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            if not data: continue
            
            request = json.loads(data.decode('utf-8'))
            
            if request['action'] == 'add':
                tasks_list.append(request['task'])
                print(f"New Task added: {request['task']}")
                conn.sendall(b"Server: Task Saved.")
                
            elif request['action'] == 'get_all':
                conn.sendall(json.dumps(tasks_list).encode('utf-8'))