import socket
import time
import mysql.connector
import pymysql as pymysql

from dock import Dock
from threading import Thread


class ReleaseDock(Dock):
    def __init__(self, host, port, database_user, database_password, database_host, database_name):
        super(ReleaseDock, self).__init__()
        self.host = host
        self.port = port
        self.database_user = database_user
        self.database_password = database_password
        self.database_host = database_host
        self.database_name = database_name
        self.cursor = None
        self.cnx = None
        print("New ReleaseDock made")
        # print(self.data_socket)

    def start_service(self):
        # open socket
        self.open_socket()
        # connect to database
        self.connect_to_database()
        # subscribe to event handler
        # start listening for data
        thread = Thread(target=self.listen_for_data, args=())
        thread.daemon = True
        thread.start()
        return thread

    def open_socket(self):
        print("Starting ReleaseDock service")
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.bind((self.host, self.port))
        # Queue a maximum of 1 connect requests
        self.data_socket.listen(1)
        print("ReleaseDock ready for receiving data on port " + str(self.port) + " on interface " + self.host)
        # print(self.data_socket)

    def listen_for_data(self):
        print("ReleaseDock listening for data on port " + str(self.data_socket.getsockname()[1]))
        while True:
            conn, address = self.data_socket.accept()
            print('Connected by', address)
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            time.sleep(3)
        conn.close()

    def connect_to_database(self):
        print("Connecting to database")
        self.cnx = mysql.connector.connect(user=self.database_user, password=self.database_password,
                                           host=self.database_host,
                                           database=self.database_name)
        self.cursor = self.cnx.cursor(dictionary=True)
        print("Connected to database")

    def check_database_connection(self):
        sq = "SELECT NOW()"
        try:
            self.cursor.execute(sq)
        except pymysql.Error as e:
            if e.errno == 2006:
                print("Something went wrong with the database connection... Reconnecting")
                return self.connect_to_database()
            else:
                print ("No connection with database.")
                return False
