import socket
import sys
import os 
import signal

class ClientSocket(object):
    
    def __init__(self,connection = None):
        self.connection = connection

    def connect(self,host,port):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((host, port))
            return True
        except Exception as e:
            print(e)
            return False

    def receive(self):
        if (self.connection):
            return self.connection.recv(1024).decode()
        else:
            return None

    def send(self,msg):
    	if self.connection:
        	self.connection.send(msg.encode())

    def disconnect(self):
        self.connection.close()