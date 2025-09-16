import socket
import threading
from zeroconfig import Advertiser
from listener import ListenerInterface

NUM_CLIENTS = 1


class Server(ListenerInterface):
    def __init__(self, args):
        host = "0.0.0.0"
        self.clients = {}

        self.socket = socket.socket()
        self.socket.bind((host, args.port))
        print(f"Binding to : {host}:{args.port}")
        self.socket.listen(NUM_CLIENTS)
        self.socket.settimeout(1)
        self.event = threading.Event()
        thread = threading.Thread(target=self.serve)
        thread.deamon = True
        thread.start()

        adv = Advertiser(args.port)
        adv.register()

    def updateLayer(self, message):
        if self.connected is True:
            try:
                self.socket.send(str(message).encode())
            except Exception as e:
                print(f"{e} - Broken connection: Reconnecting..")
                self.conn_reset()

    def serve(self):
        while True:
            try:
                conn, address = self.socket.accept()
                print("Connection from: " + str(address))
                self.clients[conn] = address
            except Exception as e:
                print(f"Error with client: {e}")

    def __del__(self):
        self.socket.close()
