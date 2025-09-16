import socket
from tenacity import retry, wait_exponential
from zeroconfig import ServiceDiscover


class Client:
    def __init__(self, gui, args):
        self.gui = gui
        self.setup()

        if args.server_ip is not None:
            self.server_ip = args.server_ip
            self.server_port = args.server_port
            return

        zero = ServiceDiscover()
        self.server_ip, self.server_port = zero.find()

    def setup(self):
        self.retries = 0
        self.connected = False
        self.socket = socket.socket()

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10))
    def connect(self):
        self.retries += 1
        print(f"Trying to connect to server ... #{self.retries}")
        self.socket.connect((self.server_ip, self.server_port))
        self.connected = True
        print("Connected.")
        self.receive_changes()

    def receive_changes(self):
        if self.connected is True:
            while True:
                try:
                    data = str(self.socket.recv(1024).decode())
                    if not data:
                        break
                    self.gui.updateLayer(int(data))
                except Exception as e:
                    print(f"{e} - Error with connection: Reconnecting..")
                    self.conn_reset()

    def conn_reset(self):
        self.socket.close()
        self.setup()
        self.connect()

    def __del__(self):
        self.socket.close()
