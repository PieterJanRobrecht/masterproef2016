import socket
import threading
import time
from Queue import Queue
from threading import Thread
from message import Message


class Dock(object):
    def __init__(self):
        # Used for opening a socket on the host machine
        self.port = None
        self.host = None
        self.message_socket = None
        # Used for communicating with the broker
        self.broker_host = None
        self.broker_port = None
        # Used for transferring message from listening thread to handle_message thread
        # A message can be anything here since there is no content check
        self.message_queue = Queue()

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

        message_thread = Thread(target=self.handle_message, args=())
        message_thread.daemon = True
        message_thread.start()
        return thread

    def open_socket(self):
        """Open a socket on defined port and interface

            Opens a socket on interface and port defined in object creation
        """
        print("DOCK -- Opening port " + str(self.port) + " on interface " + self.host)
        # Queue a maximum connect requests
        max_connection_request = 1
        # print("Opening socket")
        self.message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_socket.bind((self.host, self.port))
        self.message_socket.listen(max_connection_request)
        # print("Ready for receiving data on port " + str(self.port) + " on interface " + self.host)

    def listen_for_data(self):
        """Listen for data on the defined socket

            Listen every x second for data on the socket
        """
        print("DOCK -- Listening to port " + str(self.port) + " on interface " + self.host)
        # timeout in sec
        timeout = 3
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            conn, address = self.message_socket.accept()
            print("DOCK -- Connected by \n\t\t" + str(address))
            conn.send("Ready")
            # Receive length
            data = conn.recv(1024)
            if data:
                file_size = int(data)
                conn.send("Received length")
                data = conn.recv(file_size)
                print("DOCK -- received data: \n\t\t" + data)
                self.message_queue.put(data)
            time.sleep(timeout)
        print("DOCK -- Closing listening thread")

    def handle_message(self):
        """Handling all messages in the message_queue

            All messages in the message_queue will be handled
            If there are no messages the thread will be stopped until a new message arrives
        """
        while True:
            data = self.message_queue.get()
            print("You should really do something with this " + data)

    def send_message(self, message):
        print("DOCK -- sending new message \n\t\t" + str(message))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.broker_host, self.broker_port))
        data = s.recv(1024)
        if str(data) == "Ready":
            s.send(str(len(message)))
            oke = s.recv(1024)
            if str(oke) == "Received length":
                s.send(str(message))
        s.close()

    def connect_to_broker(self, sub_dict):
        """Set parameters and subscribe with broker

            All necessary socket parameters are set
            A dictionary with subscription type is sent
        """
        self.broker_host = '10.2.0.57'
        self.broker_port = 12347
        self.subscribe_to_messages(sub_dict)

    def subscribe_to_messages(self, sub_dict):
        """"Create subscribe message and send it to the broker
        """
        subscribe_message = Message()
        subscribe_message.create_message(self.host, "subscribe", sub_dict)
        self.send_message(subscribe_message)
