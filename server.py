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

connectedclients = {}

def client(conn, addr):
    connected = True

    while connected:
        data_length = conn.recv(HEADER).decode(FORMAT)
        if data_length:
            data_length = int(data_length)
            data = conn.recv(data_length).decode(FORMAT)
            if data == DISCONNECT_MSG:
                print(f'[CLIENT] : {addr} : DISCONNECTED')
                for i in list(connectedclients):
                    if connectedclients[i] == conn:
                        del connectedclients[i]
                connected = False
            elif "%%%%%" in data:
                print(f"[CLIENT] : -CONNECTION- : Address : {addr} : Username: {data[5:]}")
                connectedclients[data[5:]] = conn
            elif data == "*****PING":
                conn.send("*****PONG".encode(FORMAT))
            else:
                print(f"[CLIENT] : -DATA- : Address : {addr}" + " { Data : " + data + " }")
                for i in connectedclients:
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
        print(connectedclients)
        thread = threading.Thread(target = client, args=(conn, addr)) #create a thread on cpu to run client() simultaneously
        thread.start()
        print("[SERVER] : -ACTIVE CONNECTIONS- : " + str(threading.activeCount()-1))

print("[SERVER]: Starting up server...")
start()