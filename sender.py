import socket
from tenacity import retry, wait_exponential

class Sender:
    def __init__(self,client_ip = None):
        # If ip not provided, network discover it 
        self.client_ip = '127.0.0.1' 
        self.port = 1977 

        self.retries=0
        self.connected=False
        self.socket = socket.socket()
    
    @retry(wait=wait_exponential(multiplier=1, min=1, max=10))
    def connect(self):
        self.retries+=1
        print(f'Trying to connect to client ... #{self.retries}')
        self.socket.connect((self.client_ip, self.port)) 
        self.connected=True

    def notify(self, message):
        if self.connected == True: 
            self.socket.send(message.encode())

    def __del__(self):
        client_socket.close()

