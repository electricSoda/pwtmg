import socket

class client:
    def __init__(self, port, ip, address, HEADER, FORMAT, DISCONNECT_MSG, client):
        self.port = port
        self.ip = ip
        self.address = address
        self.HEADER = HEADER
        self.FORMAT = FORMAT
        self.DISCONECT_MSG = DISCONNECT_MSG
        self.client = client

    def sendmsg(self, data):
        message = data.encode(self.FORMAT)
        data_length = len(message)
        send_length = str(data_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def receive(self):
        return self.client.recv(4194304).decode(self.FORMAT)
