import socket
from tenacity import retry, wait_exponential
from libs.zeroconfig import ServiceDiscover


class Client:
    def __init__(self, args):
        self.setup()
        self.args = args

    async def start(self):
        args = self.args
        if args.server_ip is not None:
            self.server_ip = args.server_ip
            self.server_port = args.server_port
        else:
            zero = ServiceDiscover()
            self.server_ip, self.server_port = await zero.find()
        self.connect()

    def setup(self):
        self.retries = 0
        self.connected = False
        self.socket = socket.socket()
        self.socket.settimeout(1)

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10))
    def connect(self):
        self.retries += 1
        print(f"Trying to connect to server ... #{self.retries}")
        self.socket.connect((self.server_ip, self.server_port))
        self.connected = True
        print("Connected.")

    def notify_changes(self):
        if self.connected is True:
            try:
                data = self.socket.recv(1).decode()
                if not data:
                    self.conn_reset()
                return int(data)
            except socket.timeout:
                return
            except Exception as e:
                print(f"{e} - Error with connection: Reconnecting..")
                self.conn_reset()

    def conn_reset(self):
        self.connected = False
        self.socket.close()
        self.setup()
        self.connect()

    def __del__(self):
        self.socket.close()
