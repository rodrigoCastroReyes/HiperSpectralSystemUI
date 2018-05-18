import socket

class ServerSocketWrapper(object):

    def __init__(self,addr,port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_addr = addr
        self.port = port

    def listen(self):
        self.socket.bind((self.ip_addr,self.port))
        self.socket.listen(1)
        self.finish = True

    def accept(self):
        return self.socket.accept()

    def receive(self,client):
        return client.recv(1024).decode()

    def send(self,client,msg):
        return client.send(msg.encode())
