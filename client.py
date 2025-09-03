import socket
import threading

NUM_CLIENTS=1

class Client:
    def __init__(self,gui):
        host = '127.0.0.1'
        port = 1977
        self.gui=gui

        self.socket = socket.socket()
        self.socket.bind((host, port))
        print(f'Binding to : {host}:{port}')
        self.socket.listen(NUM_CLIENTS)
        thread = threading.Thread(target=self.serve) 
        thread.start()
        # Close thread at GUI end

    def serve(self):
        while True:
            conn, address = self.socket.accept()
            print("Connection from: " + str(address))
            while True:
                data = str(conn.recv(1024).decode())
                if not data:
                    break
                print("Data received: " + str(data))
                self.gui.on_function_key(data) 
            conn.close()
