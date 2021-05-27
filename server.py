import socket
import threading
import time

#local tcp variables
port = 3000
ip = socket.gethostbyname(socket.gethostname())
address = (ip, port)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "/disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)

connectedclients = []

def client(conn, addr):
    print(f"[CLIENT] : -CONNECTION- : Address : {addr}" )

    connected = True

    while connected:
        data_length = conn.recv(HEADER).decode(FORMAT)
        if data_length:
            data_length = int(data_length)
            data = conn.recv(data_length).decode(FORMAT)
            if data == DISCONNECT_MSG:
                print(f'[CLIENT] : {addr} : DISCONNECTED')
                del connectedclients[connectedclients.index(conn)]
                connected = False
            print(f"[CLIENT] : -DATA- : Address : {addr}" + " { Data : " + data + " }")
            for i in range(0, len(connectedclients)):
                connectedclients[i].send(data.encode(FORMAT))

    conn.close()
    return

def start():
    time.sleep(1)
    print("[SERVER]: Server running with code 0")
    server.listen()
    time.sleep(0.5)
    print("[SERVER]: Server listening on " + ip + ":" + str(port))

    while True:
        conn, addr = server.accept()
        connectedclients.append(conn)
        print(connectedclients)
        thread = threading.Thread(target = client, args=(conn, addr)) #create a thread on cpu to run client() simultaneously
        thread.start()
        print("[SERVER] : -ACTIVE CONNECTIONS- : " + str(threading.activeCount()-1))

print("[SERVER]: Starting up server...")
start()