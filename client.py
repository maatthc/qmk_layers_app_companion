import socket
import threading
from zeroconfig import Advertiser

NUM_CLIENTS = 1


class Client:
    def __init__(self, gui, port):
        host = "0.0.0.0"

        self.gui = gui
        self.socket = socket.socket()
        self.socket.bind((host, port))
        print(f"Binding to : {host}:{port}")
        self.socket.listen(NUM_CLIENTS)
        self.socket.settimeout(1)
        self.event = threading.Event()
        thread = threading.Thread(target=self.serve)
        thread.deamon = True
        thread.start()
        self.gui.set_thread_event(self.event)

        adv = Advertiser(port)
        adv.register()

    def serve(self):
        while not self.event.is_set():
            try:
                conn, address = self.socket.accept()
                conn.settimeout(1)
                print("Connection from: " + str(address))
                while not self.event.is_set():
                    try:
                        data = str(conn.recv(1024).decode())
                        if not data:
                            break
                        self.gui.on_function_key(int(data))
                    except socket.timeout:
                        continue
                    except Exception as e:
                        print(f"Error receiving data: {e}")
                        continue
                conn.close()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error with client {address}: {e}")

    def __del__(self):
        self.socket.close()
