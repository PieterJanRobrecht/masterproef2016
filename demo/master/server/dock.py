import socket
import time
from threading import Thread


class Dock(object):
    def __init__(self):
        self.port = None
        self.host = None
        self.data_socket = None

    def start_service(self):
        """Start all the necessary services for a Dock

            First open a socket
            Second start listening for data in a separate thread
            Return listening thread
        """
        self.open_socket()
        thread = Thread(target=self.listen_for_data, args=())
        thread.daemon = True
        thread.start()
        return thread

    def open_socket(self):
        """Open a socket on defined port and interface

            Opens a socket on interface and port defined in object creation
        """
        print("DOCK -- Opening port " + str(self.port) + " on interface " + self.host)
        # Queue a maximum connect requests
        max_connection_request = 1
        # print("Opening socket")
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.bind((self.host, self.port))
        self.data_socket.listen(max_connection_request)
        # print("Ready for receiving data on port " + str(self.port) + " on interface " + self.host)

    def listen_for_data(self):
        """Listen for data on the defined socket

            Listen every x second for data on the socket
        """
        print("DOCK -- Listening to port " + str(self.port) + " on interface " + self.host)
        # timeout in sec
        timeout = 3
        # print("Dock listening for data on port " + str(self.data_socket.getsockname()[1]))
        while True:
            conn, address = self.data_socket.accept()
            print('Connected by', address)
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            time.sleep(timeout)
        conn.close()
