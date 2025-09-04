import socket
from tenacity import retry, wait_exponential

class Sender:
    def __init__(self,client_ip = None):
        # If ip not provided, network discover it 
        self.client_ip = '127.0.0.1' 
        self.port = 1977 
        self.setup()

    def setup(self):
        self.retries=0
        self.connected=False
        self.socket = socket.socket()
    
    @retry(wait=wait_exponential(multiplier=1, min=1, max=10))
    def connect(self):
        self.retries+=1
        print(f'Trying to connect to client ... #{self.retries}')
        self.socket.connect((self.client_ip, self.port)) 
        self.connected=True
        print('Connected.')

    def notify(self, message):
        if self.connected == True: 
            try:
                self.socket.send(message.encode())
            except :
                print('Broken connection: Reconnecting..')
                self.conn_reset()

    def conn_reset(self):
        self.socket.close()
        self.setup()
        self.connect()

    def __del__(self):
        self.socket.close()

