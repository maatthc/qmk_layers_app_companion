import socket
import threading

NUM_CLIENTS=1

class Client:
    def __init__(self,gui,port):
        host = '127.0.0.1'
        self.gui=gui

        self.socket = socket.socket()
        self.socket.bind((host, port))
        print(f'Binding to : {host}:{port}')
        self.socket.listen(NUM_CLIENTS)
        self.socket.settimeout(1)
        event=threading.Event()
        thread = threading.Thread(target=self.serve,args=(event,)) 
        thread.deamon = True
        thread.start()
        self.gui.set_thread_event(event)

    def serve(self, event):
        while not event.is_set():
            try:
                conn, address = self.socket.accept()
                conn.settimeout(1)
                print("Connection from: " + str(address))
                while not event.is_set():
                    try:
                        data = str(conn.recv(1024).decode())
                        if not data:
                            break
                        print("Data received: " + str(data))
                        self.gui.on_function_key(data) 
                    except:
                        continue
                conn.close()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error with client {address}: {e}")
        self.socket.close()
